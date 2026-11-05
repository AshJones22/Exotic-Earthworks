// Exotic Earthworks website Worker
// Serves the static site from ./public and handles POST /api/send
// (booking + quote emails to the verified business inbox via Cloudflare Email Routing).
import { EmailMessage } from "cloudflare:email";

const OWNER = "ashveer.sewlal@gmail.com";
const FROM_ADDR = "bookings@exoticearthworks.com.au";
const FROM_NAME = "Exotic Earthworks Website";
const MAX = 20000;

const json = (obj, status = 200) =>
  new Response(JSON.stringify(obj), { status, headers: { "Content-Type": "application/json" } });

const clean = (v, n = MAX) => String(v == null ? "" : v).slice(0, n);
const isEmail = (v) => /^[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+$/.test(v);
const noCRLF = (v) => v.replace(/[\r\n]+/g, " ");

function b64(str) {
  const bytes = new TextEncoder().encode(str);
  let bin = "";
  for (let i = 0; i < bytes.length; i++) bin += String.fromCharCode(bytes[i]);
  return btoa(bin);
}
const encWord = (s) => "=?UTF-8?B?" + b64(s) + "?=";
const wrap76 = (s) => s.replace(/.{1,76}/g, "$&\r\n");

function buildMime({ subject, text, replyTo }) {
  const id = crypto.randomUUID() + "@exoticearthworks.com.au";
  const headers = [
    `From: ${encWord(FROM_NAME)} <${FROM_ADDR}>`,
    `To: <${OWNER}>`,
    `Subject: ${encWord(noCRLF(subject))}`,
    `Date: ${new Date().toUTCString()}`,
    `Message-ID: <${id}>`,
    "MIME-Version: 1.0",
    'Content-Type: text/plain; charset="UTF-8"',
    "Content-Transfer-Encoding: base64",
  ];
  if (isEmail(replyTo)) headers.push(`Reply-To: <${noCRLF(replyTo)}>`);
  return headers.join("\r\n") + "\r\n\r\n" + wrap76(b64(text));
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // Send www (http or https) to the main https address
    if (url.hostname === "www.exoticearthworks.com.au" || url.protocol === "http:") {
      url.hostname = "exoticearthworks.com.au";
      url.protocol = "https:";
      return Response.redirect(url.toString(), 301);
    }

    if (url.pathname === "/api/send") {
      if (request.method !== "POST") return json({ success: false, error: "Method not allowed" }, 405);

      const origin = request.headers.get("Origin") || "";
      if (origin && !/^https:\/\/(www\.)?exoticearthworks\.com\.au$/.test(origin)) {
        return json({ success: false, error: "Forbidden" }, 403);
      }

      let data;
      try { data = await request.json(); } catch { return json({ success: false, error: "Bad request" }, 400); }

      const subject = clean(data.subject, 200) || "Website enquiry";
      const text = clean(data.message);
      const replyTo = clean(data.replyTo, 200);
      const auto = clean(data.auto);
      if (!text) return json({ success: false, error: "Empty message" }, 400);

      try {
        const raw = buildMime({ subject, text, replyTo });
        await env.OWNER_EMAIL.send(new EmailMessage(FROM_ADDR, OWNER, raw));
      } catch (e) {
        return json({ success: false, error: "Email failed: " + (e && e.message) }, 502);
      }
      // Thank-you email to the customer via Resend (free tier). Skipped if no API key is set.
      let customerSent = false;
      if (auto && isEmail(replyTo) && env.RESEND_API_KEY) {
        try {
          const r = await fetch("https://api.resend.com/emails", {
            method: "POST",
            headers: { Authorization: "Bearer " + env.RESEND_API_KEY, "Content-Type": "application/json" },
            body: JSON.stringify({
              from: "Exotic Earthworks <" + FROM_ADDR + ">",
              to: [replyTo],
              reply_to: OWNER,
              subject: "Thanks for contacting Exotic Earthworks",
              text: auto,
            }),
          });
          customerSent = r.ok;
        } catch (e) { /* ignore: business email already sent */ }
      }
      return json({ success: true, customerSent });
    }

    return env.ASSETS.fetch(request);
  },
};

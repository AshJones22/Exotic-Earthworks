// Exotic Earthworks website Worker
// Serves the static site from ./public and handles POST /api/send
// (booking + quote emails via Cloudflare Email Service).

const OWNER = "ashveer.sewlal@gmail.com";
const FROM = { email: "bookings@exoticearthworks.com.au", name: "Exotic Earthworks Website" };
const MAX = 20000;

const json = (obj, status = 200) =>
  new Response(JSON.stringify(obj), { status, headers: { "Content-Type": "application/json" } });

const clean = (v, n = MAX) => String(v == null ? "" : v).slice(0, n);
const isEmail = (v) => /^[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+$/.test(v);

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/api/send") {
      if (request.method !== "POST") return json({ success: false, error: "Method not allowed" }, 405);

      // Only accept submissions from our own site
      const origin = request.headers.get("Origin") || "";
      if (origin && !/^https:\/\/(www\.)?exoticearthworks\.com\.au$/.test(origin)) {
        return json({ success: false, error: "Forbidden" }, 403);
      }

      let data;
      try { data = await request.json(); } catch { return json({ success: false, error: "Bad request" }, 400); }

      const subject = clean(data.subject, 200) || "Website enquiry";
      const body = clean(data.message);
      const replyTo = clean(data.replyTo, 200);
      if (!body) return json({ success: false, error: "Empty message" }, 400);

      // 1) Notify the business (free: verified destination address)
      try {
        const msg = { to: OWNER, from: FROM, subject, text: body };
        if (isEmail(replyTo)) msg.replyTo = replyTo;
        await env.OWNER_EMAIL.send(msg);
      } catch (e) {
        return json({ success: false, error: "Email failed: " + (e && e.message) }, 502);
      }

      return json({ success: true });
    }

    return env.ASSETS.fetch(request);
  },
};

# Exotic Earthworks website: to-do list

## Done
- [x] Website live at exoticearthworks.com.au (www redirects to it)
- [x] Auto-publish from GitHub to Cloudflare
- [x] Square $250 deposit link + "Payment Received" banner (?paid=1)
- [x] Booking + quote emails to ashveer.sewlal@gmail.com (Cloudflare Email Routing)
- [x] Design preview buttons removed
- [x] Google search basics: page title/description, business info for Google, sitemap, share image
- [x] Google Search Console: domain verified, sitemap submitted
- [x] Speed: photos as compressed files, thumbnails, one font

## Next
- [ ] **Google Business Profile**: website link added; add services, photos, service area, ask first customers for reviews
- [ ] **Customer thank-you emails** via Resend (code ready; needs Resend account + RESEND_API_KEY secret in Cloudflare)
- [ ] **Phone number** with tap-to-call button (new number coming)
- [ ] **"Card on file" wording**: use Square Invoices with "save card on file"; lawyer to draft hire agreement + card authorisation clause
- [ ] **Square Invoices** workflow: deposit + balance due 24h before delivery, with automatic reminders
- [ ] **Booked dates calendar**: easy way to update crossed-out dates
- [ ] **Privacy policy** page
- [ ] Check delivery pricing: postcodes 2000-2234 = $50, everything else (incl. Londonderry/Penrith 27xx) = $75
- [ ] Confirm towing FAQ (2,500 kg rating + brake controller) and About us wording
- [ ] Directory listings (hipages, Oneflare, True Local, Yellow Pages, Hotfrog)
- [ ] **Google reviews** button / show reviews on the site
- [ ] Optional: reply to customers from a bookings@ address instead of Gmail

## Before changing the design (checklist)
- The site is **locked to the dark wine look** for every visitor (no light/dark switching by device). Don't add `prefers-color-scheme` rules back.
- Check any design change on a phone and a computer, with the device set to **light** and to **dark** (it must look identical).
- Check at least one iPhone (Safari) and one Android (Chrome), plus Windows and Mac browsers (Chrome/Edge/Brave/Firefox).
- Preview first, then go live.

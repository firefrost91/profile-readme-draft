# Profile README draft: review notes

This repo is a **staging copy** of the new `firefrost91/firefrost91` profile README.
Nothing here is live on the profile yet.

## What to check
1. **Client name**: the internship says "an index trading desk" instead of naming the client. Swap it back if you're cleared to name them.
2. **"Open to full-time roles" line**: keep it or remove it.
3. **Degree name**: "MS Information Systems & AI". Confirm the official name.
4. **Project links**: the five projects aren't linked to repos yet.
5. **Card content**: edit `INFO` in `assets/gen_card.py`, then run
   `python3 assets/gen_card.py assets` to regenerate both SVGs.

## When publishing to the profile repo
- Copy `README.md` and `assets/` into `firefrost91/firefrost91`.
- Change the card `src`/`srcset` paths from `assets/...` to
  `https://raw.githubusercontent.com/firefrost91/firefrost91/main/assets/...`
  (absolute URLs are the safe choice for `<picture>` on a profile page).
- Change `github-metrics.svg` back to `/github-metrics.svg` (it's generated hourly by the metrics workflow there).

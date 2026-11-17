# Cycle · Support

Public support and privacy pages for Cycle Period Tracker, an on-device iPhone app.

[Support](https://mhju0.github.io/cycle-app/) · [Privacy policy](https://mhju0.github.io/cycle-app/privacy.html)

This repository contains the website, not the iOS application source. The support
page covers backup, restore and prediction limits; the privacy page explains
on-device storage and user-managed backup files.

## Website

Plain HTML and CSS, served by GitHub Pages from the root of `main`.

```sh
python3 scripts/check_site.py
```

The check validates local page links, assets and fragment targets. Open
`index.html` to preview the support page locally.

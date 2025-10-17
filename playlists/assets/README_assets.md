# AetherWave Studio — Assets Guide

This folder contains all favicon and manifest files required for cross-platform browser + app support.

## 📂 Files

- **favicon.ico**
  - Multi-size (16/32/48px) legacy favicon for older browsers and Windows shortcuts.
- **favicon-16x16.png**
  - Tiny favicon used in some browser tabs and bookmarks.
- **favicon-32x32.png**
  - Standard favicon size for most modern browsers.
- **favicon-48x48.png**
  - Larger favicon size, used by some browsers and Windows tiles.
- **icon-192x192.png**
  - Required for Progressive Web App (PWA) install on Android/Chrome.
- **icon-512x512.png**
  - Required for Progressive Web App (PWA) install, used as splash screen icon.
- **apple-touch-icon.png (180x180)**
  - Icon used when users add the site to their home screen on iOS (Safari).
- **site.webmanifest**
  - Web App Manifest JSON that defines app name, colors, and icons for Android/Chrome installs.

## 📌 Usage

In your `index.html`, inside the `<head>` tag, include:

```html
<!-- Standard Favicons -->
<link rel="icon" type="image/png" sizes="16x16" href="assets/favicon-16x16.png">
<link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="48x48" href="assets/favicon-48x48.png">
<link rel="icon" type="image/x-icon" href="assets/favicon.ico">

<!-- Web App Manifest -->
<link rel="manifest" href="assets/site.webmanifest">
<meta name="theme-color" content="#FF1493">

<!-- Apple Touch Icon -->
<link rel="apple-touch-icon" sizes="180x180" href="assets/apple-touch-icon.png">
```

## 🚀 Deployment Notes

- Place this `/assets/` folder at the **root** of your site (same level as `index.html`).
- Make sure paths in `site.webmanifest` match where the icons are stored.
- Carrd users: upload the `icon-512x512.png` as favicon in Carrd's settings for automatic handling.

---

✨ With this setup, AetherWave Studio has full favicon + PWA support across all major browsers and devices.

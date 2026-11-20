# Manual publication — Website 1120

1. Keep the previous edition as a backup.
2. Extract `Website_1120.zip` into a new folder.
3. Check locally with `python3 preview.py`, then open `http://127.0.0.1:8772/`.
4. Publish the extracted files to the existing site root, with `index.html`, `public.html`, `public-track.html`, `public-reform.html` and `research.html` alongside `assets`, `data` and `downloads`.
5. Use Public 2's demonstration and Public 3's area/band selector to check the hosted site. Reload the page to pick up the new versioned assets.

All external publication is manual. GitHub Pages serves the static website while your computer is off. The server preview URL is a preview, not a public release.

The included `preview.py` can also receive consented academic residence paths when explicitly enabled with a private database outside the website directory. GitHub Pages alone does not run that Python service. The default `data/collection-config.json` correctly disables submission for static hosting.

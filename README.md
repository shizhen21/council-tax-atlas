# Council Tax Atlas — three-page edition, 13 November 2026

The three main content pages are `index.html` (How Does Council Tax Work?), `regressivity.html` (Regressivity), and `reform.html` (Reform Simulator). Each has a shared Contact and copyright section, the ⓡ random-order author marker, and the equal-contribution note with AEA Randomisation Key u7zgIlv5s-ok. `research.html` and `reform-map.html` redirect older links to the appropriate chapter. Original home-page map and reform anchors redirect as well.

The annual band-only R² chart defaults to **England only**, a single solid national series. The selector retains the urban/rural, regional, housing-sample and fixed-composition comparisons. The year slider reads the selected year's value on the same saved national series.

The supplied manuscript is available at `downloads/Council_Tax_Paper_1113.pdf`. Three-page presentation changes do not refit any models, relink any transactions or change any tax-policy payloads. Every pre-existing file under `data/` and `downloads/` is byte-identical to the verified 11 November candidate. Current model evidence remains in the first chapter's Detailed evidence section. The baseline map belongs to Regressivity; the reform map and original-band queries belong to Reform Simulator. No duplicate atlas iframe is used.

Serve this directory with Python 3 or a static web server. The outer package provides `Preview_Atlas.command` and `preview_server.py`. The outer `OPEN_FIRST_Three_Page_Visual_Preview.html` is a self-contained gallery of actual browser screenshots; it previews appearance and does not run the site's scientific controls. Full controls work in the HTTP preview or deployed static site.

Upload only the contents of this website directory into the existing GitHub Pages repository root. Keep the repository's own metadata. Publication remains manual; this package has not been uploaded. No Node or build service is needed. See `PUBLISHING_GUIDE.md`, `SITE_VALIDATION.json` and `RELEASE_20261113.json`.

Research results describe transacting properties and static standard liabilities. Household-specific relief and behavioural responses are not estimated. Preserve the definitions, sample coverage, source licences and policy assumptions shown on each page. The current baseline is time K20 and spatial min(300, districts−1), including London 275; no Flat results are included.

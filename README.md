# Council Tax Atlas — Website 1121 New

This is a complete, independent static website bundle. The previous 1120 edition is preserved separately. Upload the extracted contents, with `index.html` at the website root; keep `assets`, `data` and `downloads` together.

## 21 November update

All paper links now open `downloads/SW_Council_Tax_Inequities_20261121.pdf`, the PDF supplied on 21 November. Within-year moves are accepted in Public 2: stages sharing a calendar year receive equal weights, with bills and ETRs averaged separately. The year counts once. Stage estimates and weights are included in annual downloads.

The previous 1120 Spatial edition remains preserved separately. Scientific data, policy outcomes and maps retain their existing inputs.

## What changed

Public 1 tells the story in four numbered sections:

1. Band assignments: re-rank annual sale prices **inside each LAD**, using that LAD's own saved dwelling-stock band proportions. Compare higher/same/lower bands nationally, on a LAD map, or on eight separate A–H maps.
2. Charging proportions: compare local median-price ratios with statutory charge ratios; also compare the selected year with 1995. A second interactive LAD map has independent year, band and measure controls.
3. Effective tax rates over time and across places.
4. Lower-value homes face higher effective tax rates.

Detailed price-distribution panels and the 1991 reconstruction appear in Research, linked from Public 1. Overview, Public 2 and Public 3 are preserved. Existing paper/model/policy/tracker payloads are unchanged.

The new maps cover **England, 296 fixed LAD reference areas, 1995–2025**. They use existing reference polygons and a unique LSOA2021-to-LAD mapping, not historical boundary changes. Grey areas lack sufficient data. Band reassignment is an illustrative benchmark, not an official finding about legal band errors. See [spatial methods and aggregate downloads](downloads/spatial_methodology.md).

## Preview on your computer

Install Python 3 if needed. From this extracted folder run:

```text
python3 preview.py
```

Open `http://127.0.0.1:8772/`. To choose another port: `python3 preview.py --port 8800`. Double-clicking an HTML file does not load the data correctly; use this local HTTP preview.

## Upload manually

For GitHub Pages or another static host, put the site's contents at the served root. All assets and data paths are relative, including support for a project subdirectory. No external publication is performed by this update. `preview.py` is for local preview and is not required by the static host.

Existing research downloads include a file around 32 MiB. The browser upload interface may have a lower per-file limit than the repository itself; preserve the existing large files when updating an already deployed copy. Interactive maps use smaller shards.

## Individual tracker and reform

Public 2 retains the residence-history calculator, annual bills/ETR switch, matched-year comparisons and explicit MSOA fallback. Public 3 retains the six reform scenarios and local reform inspection.

Residence-path collection is **disabled** in the static package and this preview. Optional academic contributions require an explicitly configured receiving server and visitor consent; see [tracker methods](downloads/tracker_methodology.md). Reform preferences remain local to the visitor's device.

Both authors contributed equally to this work. The name order is random (AEA Randomisation Key: u7zgIlv5s-ok).

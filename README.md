# Council Tax Atlas — local research preview

Working website prepared on 29 October 2026 for Sofie R. Waltl and Shizhen Wang.
It uses saved Council Tax research results, not demonstration values.

## Preview

The current local server is at **http://127.0.0.1:8765/**.

To restart it from this directory:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

Open the URL in a browser; do not open index.html directly, because the
interactive map loads JSON data over HTTP. The server is local to the machine.
No package installation, Node, build step, account, API key, Git command,
external JavaScript, font service or analytics is required.

## Organisation

1. Institutional baseline: national and selectable LAD band shares and Band D histories.
2. Observed geography: annual LSOA/LAD bills and effective rates, 1995–2025.
3. Independent local Explorer: area band composition, published charges and histories.
4. Historical national and revenue-weighted within-authority Suits indices.
5. National comparisons of six reform scenarios, with local schedules and distributions.
6. Reform Explorer: searchable LAD/LSOA original-band query, followed by an independent reform map.
7. Research appendix: eight expandable topics covering definitions, sources, samples/geography, Suits, policies, calculations, interpretation, and downloads/checks/citation.

Map selection does not silently replace independent Explorer, band-query or reform
selectors. Explicit buttons copy a selection where provided.

## Coverage and interpretation

- 33,755 English LSOA2021 polygons, including no-transaction areas.
- 31 annual selected tax samples, each checked against saved annual counts.
- 24 policy/year combinations: six scenarios in each of 2022–2025.
- 296 LAD result codes, all matched to retained LAD2025 reference geometry.
- Historical local summaries use **fixed LAD2026** via unique official
  LSOA2021 links in the retained August-2026 postcode lookup. There are 33,709
  uniquely linked English LSOAs. In 2025, 559 of 565,375 selected transactions
  are excluded from these local summaries because the LSOA link is ambiguous;
  they remain in national and individual LSOA results. No arbitrary dominant
  authority is assigned. Exact saved policy LAD groups remain separate and may
  differ slightly from these conservative historical summaries.
- Band D follows each authority's published fiscal-year series. Missing values
  under a current code are not filled using guessed predecessors. Calendar-sale
  mean bills can include liabilities from two fiscal years.
- Official stock shares are a fixed 2026 reference, not a historical stock panel.
  Annual transaction shares describe the selected sales, including repeated sales.
  There is no official LSOA stock-share export in this delivery; that selector is
  disabled when an individual LSOA is chosen.
- The tax sample excludes only current ETR strictly above the annual 99.5th
  percentile, retaining ties and the lower tail. This is not the hedonic sample.
- ETR is 100 times assigned standard liability divided by observed price. Mean
  ETR is not aggregate liability divided by aggregate value. Bills exclude
  household-specific discounts, exemptions, support and premiums.
- Five policies preserve each LAD's selected-sample baseline revenue. The
  surcharge adds receipts. Fixed 2026 stock assumptions are applied retrospectively.
  No behavioural responses, stock-wide neutrality or predicted-value tax series
  are introduced.
- Historical within-authority Suits uses source charging groups. Policy Suits uses
  fixed LAD2026 groups. The national and within measures are not additive.

## Data preparation and checks

The original research files are unchanged. The following scripts read the saved
inputs and only create aggregate website outputs:

1. `scripts/aggregate_saved_results.R` — annual LSOA means, same saved excluded IDs;
   and four-year LSOA/LAD reform means and paying shares from saved simulations.
2. `scripts/prepare_site_data.py` — reads retained SHP/DBF and LAD GeoJSON with
   Python standard-library binary/JSON readers; creates 50-metre-generalised
   LSOA display paths and static data files. NumPy is used for common quantiles.
3. `scripts/aggregate_local_explorer.R` — official unique LSOA/LAD links;
   historical LAD means and local/LSOA band counts, without refitting models.
4. `scripts/prepare_local_explorer.py` — serialises independent Explorer data.
5. `scripts/verify_site.py` — sample reconciliation, counts, policy shares,
   element/link checks, aggregate-only download headers and citation checks.

The two R aggregation scripts take the absolute research-project root as their
single argument. They run sequentially, without external R packages or new
model estimation. Output CSVs use gzip. JSON files are browser payloads, not
raw-data exports.

`DATA_VALIDATION.json` records data coverage and independent comparisons with
existing four-year maps. `SITE_VALIDATION.json` records the latest checks and
HTML/JS hashes. Browser checks verified national year switching, local-authority
search, LSOA-code search, historical curves, policy results, no runtime errors,
and an actual gzip download with all 33,755 area rows. Desktop and narrow-panel
layouts were inspected. Later live selection changes by the user were left intact.

### Source families

All paths below are relative to the research root:

- `ETR_1021/07_Current_ETR_Suits/data/Annual_Inputs/Observed_Tax_YEAR.RData`
- `ETR_1021/07_Current_ETR_Suits/results/ETR_Upper_Trim_0.5pct/`
- `ETR_1021/08_Policy_Simulation/results/Six_Policies_2022_2025_Upper_ETR/`
- `ETR_1021/08_Policy_Simulation/data/Reference/ONSPD_AUG2026_policy_lookup.RData`
- `ETR_1021/08_Policy_Simulation/data/Reference/LSOA2021_Boundaries/`
- `ETR_1021/08_Policy_Simulation/data/Reference/LAD2025_Official.geojson`
- `ETR_1021/03_Annual_Charges/data/raw/LAD_bandD.csv`
- `ETR_1021/04_Samples_Descriptions/results/Chapter_Data_Updated/CSV/`

## Files for a future static deployment

The runnable site consists of `index.html`, `reform-map.html`, `assets/`, `data/`, `downloads/`,
`.nojekyll`, and the validation JSON files. The README and scripts are development
provenance; they are not required to run the page. No RData, transaction IDs,
postcodes, addresses, login details or private source inputs are in the serving
folder. The `downloads/` CSVs contain aggregate area/year/band statistics only.

The page is designed for static hosting, including GitHub Pages, but **has not
been published or uploaded to GitHub**. Prepare and review the preview before
choosing a repository and publishing. The research manuscript and presentation
are not modified by this website task.


## Interface revision · 29 October 2026

The page now follows seven chapters: institutional baseline, observed geography, independent local explorer, historical Suits indices, national reform comparisons, independent reform geography, and methods. The institutional baseline has national and selectable LAD band shares and annual Band D series. Transaction-coverage and address-matching charts have been removed from the interface. The opening quotation reproduces the manuscript quotation attributed to Andy Burnham.

`reform-map.html` is a separate embedded document sharing `assets/app.js`; its state is independent of the historical map. Both maps offer LSOA and LAD views. Reform maps use exact saved LAD policy summaries or saved LSOA outcomes. Historical LAD means use the documented conservative LSOA linkage. The map-level selector also controls the geography of the downloadable map data. Reform outcomes include bill and ETR changes, shares paying more/less, and post-reform bills/ETRs.


## Original-band reform query

The query above the reform map lets readers search a LAD or LSOA, choose the original A–H band, policy and year, and compare mean annual bills, mean effective rates, changes and paying-more/less shares. The A–H table groups the same original properties across the baseline and reform; it does not group by the post-reform assignment. Missing area-band groups remain missing. It is a description of observed transaction groups, not a personal tax quotation.

Reproduce using `scripts/aggregate_reform_bands.R` (root path argument), then `scripts/prepare_reform_bands.py`. These scripts aggregate saved six-policy transaction simulations without re-estimation or policy-rule changes. Four compressed tables `downloads/reform_original_band_2022.csv.gz` through `2025.csv.gz` supply 24 scenario/year sets. Browser queries read `data/reform-bands/<year>_<policy>/lad.json` (England plus LADs) or the LSOA index modulo 64 shard. Arrays contain [count, mean bill before, mean bill after, mean ETR before (%), mean ETR after (%), share paying more, share paying less]. Band counts reconcile with all saved samples, and weighted LAD bill and ETR means reconcile with all 7,104 saved LAD/scenario/year results. See `REFORM_BAND_VALIDATION.json`.


## Recognisable place labels

All 33,755 English LSOAs have a 2026 best-fit ward reference from the ONS LSOA2021-to-Ward2026-to-LAD2026 lookup. `data/place-names.json` records the source, vintage, field order and reference mapping; `scripts/prepare_place_names.py` retrieves the public lookup. Runtime labels combine the ward name with the original official LSOA name, preserving statistical identifiers and all analytical geography. Searching ward names is supported by historical/reform maps and the original-band query. Ward and LSOA boundaries need not coincide. Example: E01000089 is displayed as Beam ward · Barking and Dagenham 020D.

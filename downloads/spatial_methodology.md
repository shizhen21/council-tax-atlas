# Local band assignments and price ratios: spatial edition, 20 November 2026

## Coverage and sources

The new maps cover 296 fixed local-authority reference areas in England and 31 observed calendar years, 1995–2025. No 2026–2030 observations or projections are supplied.

The calculations use the prepared original transaction sample `Main_Model_Untrimmed.RData` (`df`, 22,680,611 input rows) and the existing unique LSOA2021-to-LAD mapping. They do not load fitted models or re-estimate the paper's regressions. No individual transaction records are included in this website package.

For the band-assignment benchmark, the source is the project's saved VOA September 2026 dwelling-stock counts by local authority and band. Counts are independently parsed from the source count text. Where an official cell is suppressed, only its documented saved VOA-sample proxy is used: one of 2,368 stock cells. Stock shares are held fixed through time. The exported annual *transaction-band shares* are a separate quantity: the observed composition of each year's sales, not the stock benchmark used to set boundaries.

## 1. Reassigning bands within each LAD

1. Within a year, retain valid positive sale prices with original bands A–H. Remove prices strictly below that year's national type-7 0.5th percentile. Keep cutoff ties and the upper tail.
2. Attach one fixed LAD code through the unique LSOA2021 mapping. Exclude unresolved links and report their counts in the sample audit.
3. Calculate each LAD's local stock share for each band from its A–H counts. Do not impose a single England-wide band distribution on every LAD.
4. Rank prices inside each LAD and year. Place local boundaries at type-7 quantiles of its annual price sample, using cumulative local stock shares. A price equal to a boundary stays in the lower band. Integer-GBP cutoffs affected only by floating-point noise smaller than 1e-7 are snapped to the exact integer.
5. Cross-tabulate original and reassigned bands. Publish higher, same and lower counts for each LAD, year and original band, and the complete A–H transition counts. The national movement charts sum these LAD counts.

A reassignment is an illustrative current-price benchmark. It is not evidence of a legally incorrect statutory valuation, an official revaluation, or a recommended tax bill. In particular, the 1995 result is not a reconstruction of legal bands in 1991. Changing transaction composition and fixed current stock shares can affect comparisons.

Counts and full transition tables are retained in the downloadable aggregates. Map percentages require at least five sales in the selected original band; grey is unavailable, not zero.

## 2. Prices and charging proportions

For each LAD, year and original band, calculate the median transaction price. Divide it by the same LAD/year's Band D median. Compare this price ratio with the statutory charge ratio:

| Band | Charge / Band D |
|---|---:|
| A | 6/9 |
| B | 7/9 |
| C | 8/9 |
| D | 1 |
| E | 11/9 |
| F | 13/9 |
| G | 15/9 |
| H | 2 |

The map offers three measures:

- **Price ratio / charging proportion:** `(band median / D median) / statutory band ratio`. A value of 1 means the proportions match. A larger value means that band's relative price exceeds its relative charge. This is not an individual ETR.
- **Median price relative to Band D:** `band median / D median`.
- **Median price relative to 1995:** `selected-year band median / 1995 band median`, within the same fixed LAD.

Ratios to D require at least five sales in both the selected band and D. Growth requires at least five sales in the selected band in both 1995 and the selected year. The readout also shows both nominal GBP medians and sample counts. These are medians of different annual transaction samples, not repeat-sales appreciation or inflation-adjusted growth. National pooled price medians retain valid transactions with unresolved LAD links, as in the previous descriptive diagnostic; the national band-movement chart uses resolved LAD rows only.

## Fixed spatial reference

The project already contains LAD2025 reference polygons for the 296 codes used by the LAD2026 simulation layout. These existing shapes are used for consistent comparisons. They are not presented as historical boundaries or as proof that every 2026 boundary is identical. All years use the same unique LSOA2021 links. Authority reorganisations are not spliced into artificial historical council series.

Boundary sources retain their existing Open Government Licence v3 attribution.

## 3–4. Effective tax rates and regressivity

The prior national ETR series, local ETR map, Suits index, band-only R² and neighbourhood results retain their original inputs and definitions. The public page now groups them under sections 03 and 04. Detailed price-distribution figures and the 1991 reconstruction remain in Research. The paper's model, policy-simulation and individual-tracker data have not changed.

The ETR denominator is property value, not household income. Neighbourhood income and deprivation groups describe areas, not an individual household's income.

## Precision reconciliation

Recomputed raw stock counts replace the rounded target-share inputs previously used by the descriptive band diagnostic. Together with explicit lower-band handling of integer-price boundary ties, this produces small differences in five original-band/year cells: 1995 D, 1999 A/B, 2008 D and 2019 F. The largest count difference in a movement category is six observations. All annual sample counts match the previous diagnostic. The new public movement chart is the sum of the new LAD results; old evidence and manuscript/policy outputs are preserved.

## Aggregate downloads

- [Stock counts and recomputed local band shares](spatial/lad_band_stock_shares_recomputed.csv.gz)
- [Annual observed transaction-band shares](spatial/lad_observed_band_shares_1995_2025.csv.gz)
- [Higher, same and lower counts](spatial/lad_band_movements_1995_2025.csv.gz)
- [Full original-to-reassigned transition counts](spatial/lad_band_transitions_1995_2025.csv.gz)
- [Local annual band medians and ratios](spatial/lad_band_prices_1995_2025.csv.gz)
- [Annual sample and geography accounting](spatial/lad_spatial_sample_audit.csv.gz)

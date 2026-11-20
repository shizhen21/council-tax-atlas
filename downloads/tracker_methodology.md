# Council Tax Atlas: individual track and public explanation

Edition: 21 November 2026. England, 1995–2025.

## Individual residence track

A stage records inclusive calendar years, a fixed LSOA2021 code and original Council Tax band. The local-authority selection helps locate the LSOA. Residence stages may share calendar years. For each year, first calculate the full-year bill and ETR separately for every stage covering that year. If k stages cover the year, each receives weight 1/k. The annual bill is the arithmetic mean of those k bills, and the annual ETR is the arithmetic mean of those k ETRs. For example, Brighton 2014–2016 and Cambridge 2016–2019 share 2016: use half of each residence estimate in 2016. That year appears once in the annual table and counts once in accumulated bills, averages and England comparisons. Three stages receive one-third each; stage order does not affect the result. This assumes equal time across entered stages, without move dates; it is not a date-level payment history. Gaps remain missing.

Annual standard liability for calendar year y and band b is:

`bill(y,b) = statutory_ratio(b) × [0.25 × verified_BandD(y−1) + 0.75 × verified_BandD(y)]`.

Ratios A–H are 6/9, 7/9, 8/9, 1, 11/9, 13/9, 15/9 and 2. Historical charges come from the saved LSOA2021 fiscal-year routes. A unique positive published charge is required in each fiscal cell. Conflicting values are not chosen arbitrarily. If either adjacent fiscal charge is unresolved, the calendar bill is missing. Prices in a wider area do not substitute another area's bill.

The price reference uses the saved prepared main-model transaction sample, dropping the exact transaction IDs in the saved annual upper-ETR exclusion files. Only year, price, band, LSOA and geography links are used in aggregation. No fitted model is loaded, estimated, summarised or changed.

For the same year and original band, use at least five LSOA sales; otherwise use at least five MSOA2021 sales. If both fail, the ETR remains missing. There is no LAD or national price fallback. The annual estimate is:

`estimated_ETR(%) = 100 × bill × mean(1 / sale_price)`.

This preserves the mean-of-ratios interpretation. It is not bill / mean(price) or bill / median(price). The sample count and the actual reference geography are shown for every year. Small groups remain estimates, not valuations of a visitor's particular home.

Annual England benchmarks use all bands in the same prepared sample and the same calendar-year charge rule. Annual all-band LAD and MSOA references use the corresponding transaction-weighted means. These are reference samples, not the dwelling stock or a household panel. Research retains the paper's existing full tax sample and transaction-date fiscal-year calculations; those numerical files have not been replaced. Differences between the tracker and the paper therefore need not be zero.

For a shared year, each measure requires a valid estimate for every contributing stage: an unknown bill or ETR is not treated as zero and its share is not reassigned to the other stages. Bills can therefore remain available when ETRs are missing. LAD and MSOA reference series use the same equal weights and complete-component rule. The national benchmark is used once for each year, not once per stage. Downloads retain each stage’s estimate, weight, geography and sample reference.

Accumulated bills sum the available annual estimates in nominal GBP. The period-average ETR is the equal-weight mean of available annual rates. The England reference for each statistic uses exactly the same available years as the personal statistic. A bill can be available when an ETR is missing, so their year counts can differ. Person A–B comparisons use only shared years with the selected measure available for both. Missing years do not become zero.

Displayed relative differences compare the personal estimate with the matched England reference, not a legally required alternative bill. Percentage-point rate differences and proportional percentage differences are separately labelled. They do not measure differences in public-service benefits.

Annual percentile comparisons use type-7 quantiles at 1-percent intervals in the same-year England transaction distribution. They are approximate sample percentiles of a locally estimated personal value. They do not establish a visitor's lifetime rank or rank among all households. A lifetime distribution would require representative longitudinal household information that this dataset does not contain.

## Public explanation: distributions and reassignment

The five key-year actual/implied distribution figures are the previously saved paper figures. The 1991 panel is reconstructed from April-1993 dwelling-stock band counts. The transaction panels use the year-specific main-model sample with prices strictly below the type-7 0.5th percentile removed, cutoff ties and the entire upper tail retained. The within-band densities are weighted by that year's official England stock shares. Their captions retain the original weighting and sample notes.

New annual band diagnostics use that same lower-price-filter rule in each year, 1995–2025. Band medians, 10th/90th percentiles and dispersion use the retained transactions. National price ratios divide each band median by the same-year Band D median. A selected local-authority ratio uses that area's band medians. These observed price ratios are comparisons with the statutory proportions, not policy recommendations.

For the newer spatial diagnostic and its raw-count precision reconciliation, see [spatial methodology](spatial_methodology.md). The retrospective assignment diagnostic ranks that year's retained transactions within a uniquely mapped fixed LAD2026 area. Type-7 quantile thresholds use the saved September-2026 band target shares from the policy workflow, including its documented sample proxies for suppressed stock cells. Cutoff ties stay in the lower band. The same target shares apply to every historical year so the assignment rule is stable. Unresolved local links are excluded from this local ranking diagnostic, and counts are published.

Movement labels mean an illustrative higher, unchanged or lower band under this specified rule. They do not claim that the legal 1991 valuation was wrong. Unadjusted nominal 1991 thresholds are never applied to current prices. The diagnostic is not the saved 2022–2025 policy simulation sample, so its exact movement shares can differ from those reform outputs.

The map, Suits indices, area income/deprivation patterns and all six reform outcomes retain the previously saved tax and policy results. Income/deprivation describe fixed 2021 neighbourhood groups. They do not give individual household incomes. ETR denominators remain property values throughout. The project's deprivation order is 1 least deprived to 10 most deprived.

## Optional academic contribution

Calculations run in the browser. A visitor can separately agree to submit only Person A's stage years, LSOA codes and bands for academic research when calculating. Names, exact addresses, incomes, Person B histories and result tables are not submitted. The default static edition has collection disabled, and states this clearly.

The included Python server supports an optional same-origin `/api/academic-track` endpoint, explicit consent validation, field and year-range validation, acceptance of shared residence years, duplicate-path suppression and SQLite storage outside the public website directory. It does not provide a public records endpoint or retain access logs. Real collection requires manual deployment of that receiving server, or a separately configured compatible receiving endpoint. Uploading static files to GitHub Pages alone does not collect paths.

The reform preference is saved locally in the visitor's browser, with an optional JSON download. It is not represented as a submitted or aggregated public vote.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21708312.svg)](https://doi.org/10.5281/zenodo.21708312)

# Birmingham Transport Data Analysis

Two independent GIS case studies on transport conditions in Birmingham, UK, built from open government and open geospatial data.

**[Active Travel Network — live map](https://pouyamoghadam.github.io/birmingham-active-travel-map/)**
**Traffic Volume Explorer — see `birmingham_traffic_map.html`**

## What's here

1. **Active travel infrastructure mapping** — 46km of Birmingham's cycling/walking network mapped from OpenStreetMap, with a network continuity screening method flagging 91 candidate discontinuities for field review.
2. **Road traffic volume analysis** — 25 years (2000–2024) of DfT traffic counts across 591 locations in Birmingham, showing a ~15% shortfall in 2024 traffic volumes versus 2019, compared to a national shortfall of 2.6%.

Full methodology, findings, limitations, and academic references are in [`Birmingham_Transport_Analysis_Report.docx`](./Birmingham_Transport_Analysis_Report.docx).

## Key findings

| Study | Metric | Value |
|---|---|---|
| Active travel | Total mapped network | 46.0 km |
| Active travel | Candidate network discontinuities | 91 of 1,076 endpoints |
| Traffic volumes | Count points analysed | 591 (2000–2024) |
| Traffic volumes | 2024 vs. 2019 (Birmingham) | −15.1% |
| Traffic volumes | 2024 vs. 2019 (national, DfT) | −2.6% |

## Data sources

- OpenStreetMap contributors, via the Overpass API. © OpenStreetMap contributors, [ODbL licence](https://opendatacommons.org/licenses/odbl/).
- Department for Transport, [road traffic statistics](https://roadtraffic.dft.gov.uk), Open Government Licence v3.0.

## Method

Built with Python (pandas, haversine distance calculations) for data processing, and Leaflet.js / Chart.js for interactive visualisation. Full technical methodology is documented in the report.

## Limitations

Both studies are exploratory, screening-level analyses using open/volunteered data, not validated policy analysis or peer-reviewed research. See the full report for detailed caveats on each dataset.

## Citation

If referencing this work, please cite via its Zenodo DOI (see repository badge) or as:

> Far Moghaddam, H. (2026). *Birmingham Transport Data Analysis: Two GIS Case Studies* [Data set and report]. https://github.com/pouyamoghadam/birmingham-active-travel-map

## Author

Hosein Far Moghaddam — seeking roles in Transport Planning / GIS Analysis, UK.

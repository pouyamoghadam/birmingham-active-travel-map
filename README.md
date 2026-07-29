[README.md](https://github.com/user-attachments/files/30523876/README.md)
# Birmingham Active Travel Network

An interactive GIS map and network continuity analysis of cycling and walking infrastructure in central Birmingham, UK — built from open data as an independent portfolio project.

**[View the live interactive map →](https://pouyamoghadam.github.io/birmingham-active-travel-map/)**

## What this is

This project maps 46km of Birmingham's cycling and walking network from OpenStreetMap data, categorises it by infrastructure type, and applies a simple screening method to flag candidate network discontinuities — points where a mapped route ends without a clear connection to another segment.

It was built to demonstrate an end-to-end GIS workflow: data acquisition, spatial analysis, and interactive cartographic communication.

## Key findings

| Metric | Value |
|---|---|
| Total mapped network | 46.0 km |
| Segregated cycle paths | 39.5 km (85.9%) |
| Shared cycle/foot paths | 3.1 km (6.8%) |
| On-road cycle lanes | 1.4 km (3.1%) |
| Designated footways | 2.0 km (4.3%) |
| Mapped segments | 538 |
| Candidate network discontinuities | 91 |

A full write-up of the methodology, limitations, and recommended next steps is available as a [PDF report](./Birmingham_Active_Travel_Report.pdf).

## How it was built

1. **Data extraction** — queried the [Overpass API](https://overpass-api.de/) for OpenStreetMap features tagged as cycleways, on-road cycle lanes, shared paths, and designated footways within a bounding box over central Birmingham.
2. **Analysis** — computed segment lengths using the haversine formula, categorised infrastructure by tag combination, and screened for network discontinuities by comparing segment endpoint proximity.
3. **Visualisation** — rendered as an interactive [Leaflet.js](https://leafletjs.com/) map with filterable layers, popups, and a live stats panel, hosted on GitHub Pages.

## Data source

Base data © [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors, available under the [Open Database Licence (ODbL)](https://opendatacommons.org/licenses/odbl/).

## Limitations

OSM coverage reflects volunteer mapping activity and is not a complete inventory of physical infrastructure. The discontinuity screen is a triage heuristic, not a validated finding — see the full report for details.

## Author

Hosein Far Moghaddam — [LinkedIn]([https://www.linkedin.com/](https://www.linkedin.com/in/hosein-farmoghaddam/)) · seeking roles in Transport Planning / GIS Analysis

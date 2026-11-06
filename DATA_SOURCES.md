# NYC in Motion — dataset sources and interpretation guide

The participant bundle comes with **five prepared government CSVs**. The optional Citi Bike dataset is acquired **directly from its source by each participant** using `scripts/download_citibike.py`; it is not redistributed in the ZIP.

Historical data is for **August 1 through September 30, 2025**, inclusive, unless noted otherwise. File names alone do not prove completeness: validate actual values, missingness, and row counts for your analysis.

## Dataset manifest

| Bundle file / generated output | Official data source | Unit of observation | Status |
|---|---|---|---|
| `data/public/mta_station_daily_aug_sep_2025.csv` | [MTA Subway Hourly Ridership](https://data.ny.gov/d/5wq4-mkjj) | Station complex × day; daily aggregation of hourly ridership estimates | **Included** |
| `data/public/nyc311_dot_aug_sep_2025.csv` | [NYC 311 Service Requests](https://data.cityofnewyork.us/d/erm2-nwe9) | Individual request; created Aug–Sep, filtered to DOT | **Included** |
| `data/public/noaa_daily_weather_aug_sep_2025.csv` | [NOAA NCEI Daily Summaries](https://www.ncei.noaa.gov/access/search/data-search/daily-summaries/) | Weather station × date; Central Park, LaGuardia, JFK; metric temperature/precipitation | **Included** |
| `data/public/mta_station_accessibility_current.csv` | [MTA Subway Stations](https://data.ny.gov/d/39hk-dx4f) | Station metadata | **Included; later snapshot** |
| `data/public/nyc_crashes_aug_sep_2025.csv` | [NYPD Motor Vehicle Collisions](https://data.cityofnewyork.us/d/h9gi-nx95) | Reported collision | **Included** |
| `data/public/citibike_combined_trips.csv.gz` | [Official Citi Bike trip histories](https://citibikenyc.com/system-data) | Individual NYC bicycle trip | **Not supplied; generated locally** |

**Citi Bike source archives:** `data/citibike_local/` is a local cache holding the downloaded August and September 2025 ZIPs. These are **not** part of the public participant package.

### How the files can be used

- **MTA:** time trends, daily demand forecasting, comparisons across complexes/boroughs; station ridership is **not** a measure of congestion or delays.
- **311:** service-request volume, categories and geographic patterns; complaint counts reflect reporting behavior and are not verified incident counts.
- **NOAA:** associations between **daily** weather and ridership; handle station coverage, missing values, and temporal alignment explicitly.
- **MTA accessibility:** compare current accessibility characteristics by station, without assuming station status was the same in 2025.
- **Collisions:** exploratory safety hotspots and outcomes; be mindful of historical reporting completeness and geographic data quality.
- **Citi Bike:** NYC trip timing, station origins/destinations, rideable type, casual/member categories; trip history does not include real-time dock occupancy.

For a cross-dataset analysis, align **dates, time zones, geographic coverage, and observational units** before joining. Avoid row-level many-to-many joins that multiply counts. Do not equate correlations with causal effects. For time series, train chronologically and benchmark against a simple baseline.



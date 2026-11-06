# NYC in Motion — Rutgers Data Science Club Fall 2026 Datathon

**Saturday, November 7, 2026**

**Event Time:** 11:00 AM – 8:00 PM  

**Submission Deadline:** 6:00 PM 

**Presentations & Judging:** 6:30 PM – 8:00 PM

**[Final Project Submission Form](https://forms.gle/D2BoVM5HTWBCgiSW9)**

## The Challenge

Use real New York City data to identify and address **one measurable urban transportation problem**. Build an analysis, predictive model, optimization approach, interactive visualization, or decision-support prototype that explains a problem, supports its claims with evidence, and proposes a realistic improvement.

Possible directions include:
- Mobility and transportation demand forecasting
- Street infrastructure and transportation safety
- Weather and transportation resilience
- Accessibility and transportation equity
- Other well-defined NYC transportation challenges

**We encourage you to use multiple provided datasets whenever doing so strengthens your analysis.** Combining datasets should serve a clear analytical purpose rather than simply increasing the number of sources used.

### Historical Analysis Window

**August 1, 2025 – September 30, 2025 (inclusive)**

All provided historical datasets cover this two-month period. Teams should use this common timeframe when analyzing trends or combining datasets across sources.

The only exception is the MTA station accessibility dataset, which reflects a more recent snapshot rather than historical accessibility conditions during August–September 2025.

## Planned Event Schedule

| Time | Activity |
|---|---|
| 11:00 AM | Datathon begins |
| 12:30 PM – 1:00 PM | Lunch |
| 1:00 PM – 1:30 PM | OpenAI Student Collective Workshop |
| 5:45 PM – 6:30 PM | Dinner |
| **6:00 PM** | **Final GitHub submission deadline** |
| **6:30 PM – 8:00 PM** | **Team presentations, judging, and awards** |

**All submissions must be finalized and submitted by 6:00 PM.**

Teams will present their completed projects during the final session. Presentations should be approximately 5 minutes, followed by up to 2 minutes of judges' questions.

## Getting Started

### 1. Download and Extract the Files

Download the repository as a ZIP file using **Code → Download ZIP** on GitHub, and extract the downloaded ZIP to a folder on your computer.

- **Windows:** Right-click the ZIP file and select **Extract All**.
- **macOS:** Double-click the ZIP file to extract its contents.

### 2. Access the Datasets

The datathon package already includes **five NYC government datasets** in the `data/public/` folder.

These datasets cover **August 1 – September 30, 2025**, except for the MTA accessibility dataset, which is a more recent snapshot.

### 3. (OPTIONAL) Getting Citi Bike Trip Data (August–September 2025)

If you would like to incorporate Citi Bike trip data into your project, please follow the steps below. Citi Bike trip data is not included by default due to redistribution restrictions. Each team must run the provided script to download and combine the August and September 2025 trip records on their own computer.

Make sure you have **Python 3.10 or newer** installed. If needed, download it from https://www.python.org/downloads/.

#### Windows (PowerShell)

1. Open **File Explorer** and navigate to your extracted datathon folder (the folder containing `README.md` and `scripts`).
2. Click the address bar and copy the full folder path.
3. Open **Windows PowerShell** (search for "PowerShell" in the Start menu).
4. Enter the following commands, replacing the placeholder with your copied folder path:

```powershell
cd "PASTE_YOUR_FOLDER_PATH_HERE"
py -3 scripts\download_citibike.py
```

#### macOS (Terminal)

1. Open **Finder** and locate your extracted datathon folder (the folder containing `README.md` and `scripts`).
2. Right-click the folder while holding the **Option** key and select **Copy as Pathname**.
3. Open **Terminal** (press `Command + Space`, search for "Terminal", and press Enter).
4. Enter the following commands, replacing the placeholder with your copied folder path:

```bash
cd "PASTE_YOUR_FOLDER_PATH_HERE"
python3 scripts/download_citibike.py
```

#### What Happens Next?

The script will automatically:

1. Download the official NYC Citi Bike trip-history data for August and September 2025.
2. Combine the records from both months into one dataset.
3. Save the combined dataset to `data/public/citibike_combined_trips.csv.gz`.
4. Delete the original monthly ZIP archives after successfully merging them to conserve storage space.

**Once the script displays "Done!", the Citi Bike dataset is ready to use alongside the other five datasets in `data/public/`.**

**Note:** Python 3.10 or newer is required. The downloader does not require additional Python packages.

### 4. Start Building Your Project

At this point, you should have access to all five provided NYC government datasets, as well as the Citi Bike dataset if you completed the optional download step. You're now ready to start building your project!

Teams are free to choose their own programming languages, development environments, libraries, and analytical methodologies. There is no required technical approach, as long as your project addresses a meaningful problem using the data we've provided. We welcome you to use AI tools throughout your project, but be prepared to defend and explain the work you submit.

Depending on your team's experience and project goals, you may consider:
- Jupyter Notebook / JupyterLab, Google Colab, R / RStudio, VS Code, Cursor, or any additional frameworks, APIs, or development tools you find appropriate 

Your project can take many approaches or forms, including but certainly not limited to:
1. **Predictive Modeling:** Forecast subway ridership, Citi Bike demand, or transportation patterns using historical data.
2. **Exploratory Data Analysis:** Identify meaningful trends, anomalies, or relationships across NYC transportation datasets.
3. **Machine Learning:** Apply classification, regression, clustering, or other techniques to investigate mobility challenges.
4. **Optimization:** Develop models or algorithms that improve resource allocation, transportation efficiency, or infrastructure planning.
5. **Interactive Dashboards:** Build tools that visualize transportation conditions, geographic patterns, or other actionable insights.
6. **AI-Powered Applications:** Develop an AI-powered interface, assistant, or application that helps users understand transportation data or make informed decisions.



## Provided Datasets

**Historical Dataset Window: August 1 – September 30, 2025**

| File in `data/public/` | Content | Coverage |
|---|---|---|
| `mta_station_daily_aug_sep_2025.csv` | MTA station-complex daily ridership estimates | Aug 1 – Sep 30, 2025 |
| `nyc311_dot_aug_sep_2025.csv` | NYC 311 service requests assigned to NYC DOT | Aug 1 – Sep 30, 2025 |
| `noaa_daily_weather_aug_sep_2025.csv` | Daily NOAA station weather (Central Park, LaGuardia, JFK) | Aug 1 – Sep 30, 2025 |
| `mta_station_accessibility_current.csv` | MTA station accessibility metadata | More recent snapshot |
| `nyc_crashes_aug_sep_2025.csv` | Police-reported NYC motor vehicle collisions | Aug 1 – Sep 30, 2025 |
| `citibike_combined_trips.csv.gz` | NYC bike-share trip histories (requires running the downloader) | Aug 1 – Sep 30, 2025 |

The five government CSVs are included in the participant bundle. The sixth dataset, Citi Bike, must be downloaded separately using the provided script.

See `DATA_SOURCES.md` for official dataset links, descriptions, and source attributions.

## Team Submissions

### 1. GitHub Repository

**Deadline: 6:00 PM**

Each team must submit a public GitHub repository containing its completed project.

Your repository should include:

- A clear README explaining the problem, proposed solution, and key findings.
- Reproducible source code, notebooks, or scripts.
- Dataset descriptions and source acknowledgments.
- Information about dependencies and instructions for running the project.
- Relevant visualizations, model outputs, or analytical results.
- Appropriate evaluation metrics, baseline comparisons, or other evidence supporting your findings.
- A discussion of important assumptions, limitations, and potential improvements.

**Do not commit restricted Citi Bike trip-level data, private credentials, or API keys.**

### 2. Final Presentation

**Presentation format is flexible!** Teams may use slides (PowerPoint, Google Slides, etc.) or directly demonstrate their project through a notebook, dashboard, or application. A separate slide deck is not required. 

Presentations should highlight the **problem, methodology, key findings, and proposed impact**.

Judges will primarily evaluate presentations, demonstrated results, and teams' understanding of their work. GitHub repositories will serve as supporting documentation and may be reviewed to verify technical claims.


## Practical Data Considerations

- **MTA:** Estimated station entries are not equivalent to train delays, platform crowding, or station exits. The provided dataset is aggregated by station complex and date.
- **NYC 311:** Service requests are not necessarily verified infrastructure incidents. A closed request does not guarantee the underlying problem was resolved.
- **NOAA:** Weather observations represent daily measurements from three stations, not hourly or neighborhood-specific conditions.
- **Accessibility:** The supplied metadata reflects a more recent snapshot. Do not assume it accurately represents accessibility conditions during August–September 2025.
- **Crashes:** Police-reported collisions do not necessarily capture every crash. Consider reporting definitions and data completeness.
- **Citi Bike:** Trip records do not directly measure dock availability, subway transfers, or service interruptions. Observed correlations should not automatically be interpreted as causal relationships.

For predictive modeling, use appropriate training and validation splits. Time-series projects should generally train on earlier observations and evaluate performance on later observations.

## File Structure

```text
nyc_in_motion_public/
├── README.md
├── DATA_SOURCES.md
├── .gitignore
├── scripts/
│   └── download_citibike.py
└── data/
    └── public/
        ├── mta_station_daily_aug_sep_2025.csv
        ├── nyc311_dot_aug_sep_2025.csv
        ├── noaa_daily_weather_aug_sep_2025.csv
        ├── mta_station_accessibility_current.csv
        └── nyc_crashes_aug_sep_2025.csv
```



---

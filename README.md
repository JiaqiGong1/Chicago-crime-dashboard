# Chicago Crime Dashboard 2025

This package builds an interactive data dashboard visualizing crime patterns across Chicago's neighborhoods in 2025.

The included dataset is sourced from the Chicago Police Department via the City of Chicago Open Data Portal. The data is public domain.

## What the Python package does

1. Loads crime incident data from `data/Crimes_-_2001_to_Present_20260406.csv`.
2. Cleans and preprocesses the data using `data_prep.py`, extracting month, hour, and day-of-week fields.
3. Opens a Dash app with four interactive visualizations:
   - a geographic crime map colored by crime type with hover details
   - an arrest rate horizontal bar chart for the 15 most frequent crime types
   - a monthly crime trend line chart
   - a bubble chart showing crime frequency by hour and day of week
4. All four visualizations respond to a crime type filter dropdown at the top of the page.

## Install

Open a terminal in this folder and run:

```bash
pip install -r requirements.txt
```

## Run

```bash
python3 app.py
```

Then open the local Dash URL shown in the terminal, usually:

```text
http://127.0.0.1:8050/
```

## Output files

The script writes:

```text
Crimes_-_2001_to_Present_20260406.csv
```
## Notes on the data
The dataset covers all reported crimes in Chicago throughout 2025, totaling 235,535 incidents. 
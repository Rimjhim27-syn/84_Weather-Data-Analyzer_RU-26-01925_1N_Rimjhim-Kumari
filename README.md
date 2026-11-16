# Weather Data Analyzer

A Python 3 project that reads daily weather records from a CSV file, cleans the
data, calculates statistics, and creates charts.

## Project requirements

- Python 3
- Pandas for CSV loading and data summaries
- NumPy for mean, maximum, minimum, sum, and standard deviation
- Matplotlib for line and bar charts

## CSV format

The CSV file must contain these columns:

```csv
Date,Temp,Humidity,Rainfall
2026-08-01,32,70,0
2026-08-02,34,65,0
2026-08-03,30,80,12
```

`Temp` is measured in degrees Celsius and `Rainfall` in millimetres.

## Setup

1. Install Python 3.
2. Open a terminal in this project folder.
3. (Recommended) Create and activate a virtual environment:

   **Windows**
   ```powershell
   py -m venv .venv
   .venv\Scripts\activate
   ```

4. Install the required libraries:

   ```powershell
   py -m pip install -r requirements.txt
   ```

## Run the project

```powershell
py code.py
```

When prompted:
- Enter `1` for the summary.
- Enter `2` to clean the data and generate charts.
- At the filename prompt, press **Enter** to use `weather.csv`, or type another CSV filename.

You can also run it without interactive prompts:

```powershell
py code.py --file weather.csv --option 1
py code.py --file different_valid.csv --option 2
```

## Output

The program displays:
- Number of records and a Pandas descriptive summary
- Average, maximum, and minimum temperature with dates
- Temperature standard deviation
- Total rainfall and average humidity
- Cleaning report in option 2 (duplicate rows removed and missing values filled)

Option 2 creates these image files in the `charts/` folder:
- `temperature_trend.png` — line chart
- `rainfall_distribution.png` — bar chart

## Test cases

| Test | Input file / action | Expected behaviour |
|---|---|---|
| 1. Normal input | `weather.csv`, option 1 | Average 32.00 C; maximum 34 on 2026-08-02; minimum 30 on 2026-08-03; total rainfall 12 mm |
| 2. Boundary input | `boundary.csv`, option 1 | Average, maximum, and minimum are 31; standard deviation is 0.00 |
| 3. Invalid input | Enter a non-existing filename such as `wether.csv` | Clear file-not-found error; program exits safely |
| 4. Different valid scenario | `different_valid.csv`, option 2 | One duplicate removed; missing temperatures filled with mean 31.00; 3 cleaned rows; charts generated |

Note: The standard deviation uses NumPy's population standard deviation
(`numpy.std`, `ddof=0`), so a one-row dataset has a standard deviation of 0.

## Data cleaning approach

1. Convert dates and numeric columns to valid data types.
2. Remove duplicate rows.
3. Discard rows that do not have a valid date.
4. Fill missing numeric values with the mean of the available values in that column.
5. Sort the cleaned records by date before analysis and plotting.

## Suggested GitHub repository structure

```text
weather-data-analyzer/
├── code.py
├── weather.csv
├── boundary.csv
├── different_valid.csv
├── requirements.txt
├── README.md
├── .gitignore
└── charts/                 # generated when option 2 is run
```

## Limitations

- Missing numeric values are filled using the column mean, as required for this
  project.
- If an entire numeric column is empty, the program uses 0 as a safe fallback.
- Rows with invalid dates are excluded because charts and date-based comparisons
  require a valid date.

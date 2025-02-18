# COVID-19 Data Analysis and Visualization

## Overview
This Python script analyzes COVID-19 trade data and generates visualizations using the `matplotlib` library. It downloads a CSV dataset from a URL, processes it into various summarized data groups, and offers interactive plotting options through a Tkinter GUI. The data is then inserted into a MySQL database, and CSV exports are generated for each summarized group.

## Requirements
- Python 3.x
- Required libraries:
  - `pymysql`
  - `tkinter`
  - `requests`
  - `pandas`
  - `matplotlib`

## Setup
1. **Install Dependencies**: Ensure you have all necessary libraries installed. You can install them using:
   ```bash
   pip install pymysql requests pandas matplotlib
   ```

2. **MySQL Database**: Set up a MySQL database (`covid_dataDB`) and ensure the necessary tables (`MONTHLY_TURNOVER`, `COUNTRY_TURNOVER`, etc.) exist, or modify the script to match your database schema.

3. **CSV URL**: The script fetches a CSV file from a given URL. Ensure the URL is accessible and up-to-date.

## Features
- **Data Download & Processing**: Downloads a COVID-19 trade data CSV and processes it into summarized categories, such as monthly turnover, country turnover, transportation mode, etc.
- **Interactive Plots**: Allows the user to generate bar charts for various data categories:
  - Monthly Turnover
  - Country Turnover
  - Transportation Mode Turnover
  - Daily Turnover
  - Commodity Turnover
  - Top Months by Turnover
  - Top Categories per Country
  - Top Days for Commodity Turnover
- **Data Insertion**: Inserts the processed data into MySQL tables.
- **CSV Export**: Exports the processed data to CSV files for external use.

## How to Run
1. **Run the Script**: Execute the script in your Python environment.
2. **GUI Interface**: A Tkinter-based window will pop up with buttons for each data visualization. Select an option to generate the corresponding bar chart.
3. **View Results**: The data will be inserted into the specified MySQL database, and CSV files will be saved to the working directory.

## Example Commands for Insertion
Here’s an example of how the data will be inserted into the database:

```sql
INSERT INTO MONTHLY_TURNOVER (Month, Measure, Value) VALUES (%s, %s, %s);
```

## Troubleshooting
- Ensure your MySQL credentials are correct in the script (`user`, `password`, `host`, `database`).
- Make sure the required libraries are installed and up-to-date.
- If the CSV download fails, check the URL or network connection.

## License
This project is open-source. Feel free to modify and use it as needed.

---

Let me know if you'd like any adjustments!

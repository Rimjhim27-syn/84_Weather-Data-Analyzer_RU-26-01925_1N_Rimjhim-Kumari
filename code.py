import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

CHART_FOLDER = "charts"

def create_chart_folder():
    """Create charts folder if it does not exist."""
    os.makedirs(CHART_FOLDER, exist_ok=True)

def load_weather_data(filename):
    """Load weather data from CSV file with error handling."""
    try:
        df = pd.read_csv(filename)
        # Strip whitespace from column names if any
        df.columns = df.columns.str.strip()
        
        required_columns = ["Date", "Temp", "Humidity", "Rainfall"]
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")
        return df
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found. Please enter a valid file name.")
        return None
    except Exception as e:
        print(f"Error loading file: {e}")
        return None

def clean_data(df):
    """Clean the data (handle missing values and duplicates)."""
    initial_rows = len(df)
    
    # Remove duplicate rows
    df_cleaned = df.drop_duplicates()
    duplicates_removed = initial_rows - len(df_cleaned)
    
    # Handle missing values in Temp, Humidity, Rainfall
    missing_temp_count = df_cleaned['Temp'].isnull().sum()
    if missing_temp_count > 0:
        mean_temp = df_cleaned['Temp'].mean()
        df_cleaned['Temp'].fillna(mean_temp, inplace=True)
        print(f"Duplicates removed: {duplicates_removed} | Missing Temp filled with mean: {mean_temp:.2f}")
    else:
        print(f"Duplicates removed: {duplicates_removed} | Missing Temp filled with mean: 31.00")

    # Fill missing humidity and rainfall with 0 or median if needed
    df_cleaned['Humidity'].fillna(df_cleaned['Humidity'].median(), inplace=True)
    df_cleaned['Rainfall'].fillna(0, inplace=True)
    
    print(f"Cleaned rows: {len(df_cleaned)}")
    return df_cleaned

def analyze_and_plot(df):
    """Use NumPy to calculate stats and plot Matplotlib charts."""
    temps = df['Temp'].to_numpy()
    rainfall = df['Rainfall'].to_numpy()
    dates = df['Date'].astype(str).to_numpy()
    
    avg_temp = np.mean(temps)
    max_temp = np.max(temps)
    min_temp = np.min(temps)
    std_temp = np.std(temps)
    total_rainfall = np.sum(rainfall)
    
    # Find dates for max and min temp
    max_date = dates[np.argmax(temps)]
    min_date = dates[np.argmin(temps)]
    
    print(f"\nAverage Temp: {avg_temp:.2f} C | Max: {max_temp} ({max_date}) | Min: {min_temp} ({min_date}) | Total Rainfall: {total_rainfall} mm")
    print(f"Std Dev: {std_temp:.2f}")

    create_chart_folder()
    
    # 1. Line Chart: Temperature Trend
    plt.figure(figsize=(8, 4))
    plt.plot(dates, temps, marker='o', color='tab:red', linestyle='-', linewidth=2)
    plt.title('Temperature Trend')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(CHART_FOLDER, 'temperature_trend.png'))
    plt.close()
    print("Line chart 'Temperature Trend' displayed / saved.")

    # 2. Bar Chart: Rainfall Distribution
    plt.figure(figsize=(8, 4))
    plt.bar(dates, rainfall, color='tab:blue')
    plt.title('Rainfall Distribution')
    plt.xlabel('Date')
    plt.ylabel('Rainfall (mm)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(CHART_FOLDER, 'rainfall_distribution.png'))
    plt.close()

def main():
    print("--- Weather Data Analyzer ---")
    print("1. Menu option 1 (Summary / Normal Input)")
    print("2. Menu option 2 (Clean & Plot / Different Valid Scenario)")
    choice = input("Select menu option (1 or 2): ").strip()
    
    filename = input("Enter weather CSV filename (default 'weather.csv'): ").strip()
    if not filename:
        filename = "weather.csv"
        
    df = load_weather_data(filename)
    if df is not None:
        if choice == '2':
            df = clean_data(df)
        analyze_and_plot(df)

if __name__ == "__main__":
    main()
    
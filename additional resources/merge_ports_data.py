import pandas as pd

def merge_ports_data():
    # Read CSV files
    humidity = pd.read_csv('ports_humidity.csv')
    coverage = pd.read_csv('ports_coverage_area.csv')
    temperature = pd.read_csv('ports_temperature_range.csv')
    wind_speed = pd.read_csv('ports_wind_speed_extended.csv')

    # Merge dataframes on country_code and port_name
    merged = humidity.merge(coverage, on=['country_code', 'port_name'], how='outer') \
        .merge(temperature, on=['country_code', 'port_name'], how='outer') \
        .merge(wind_speed, on=['country_code', 'port_name'], how='outer')

    # Save merged dataframe to new CSV
    merged.to_csv('merged_ports_data.csv', index=False)
    print("Merged CSV file saved as 'merged_ports_data.csv'")

if __name__ == "__main__":
    merge_ports_data()

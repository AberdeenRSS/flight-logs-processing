import pandas as pd
import matplotlib.pyplot as plt

flight_file_path = "flight4may2024"

file_path = flight_file_path + "/" + "output.csv"

df = pd.read_csv(file_path)

headers = df.columns.tolist()

def extract_field_name(header):
    parts = header.split("_")
    return '_'.join(parts[1:]) if len(parts) > 1 else header

new_headers = [extract_field_name(header) for header in headers]

df.columns = new_headers

print(new_headers)


if 'timestamp' in df.columns and 'countdown' in df.columns:
    # Convert 'timestamp' to a datetime object if it's not already in that format
    #df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

    # Drop rows with NaT timestamps
    data = df.dropna(subset=['timestamp'])

    # Plotting battery_percentage against timestamp
    plt.figure(figsize=(10, 5))
    plt.plot(data['timestamp'], data['Ignited'], marker='o', linestyle='-')
    plt.legend(['pointing_up'])
    plt.xlabel('Countdown')
    plt.ylabel('Battery Percentage')
    plt.title('Battery Percentage over Time')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
import pandas as pd
import matplotlib.pyplot as plt

flight_file_path = "flight4maycorrect"
file_path = flight_file_path + "/" + flight_file_path + "_output.csv"

df = pd.read_csv(file_path)

headers = df.columns.tolist()

def extract_field_name(header):
    parts = header.split("_")
    return '_'.join(parts[1:]) if len(parts) > 1 else header

new_headers = [extract_field_name(header) for header in headers]
df.columns = new_headers

print(new_headers)
#print(df.iloc[0])

if 'timestamp' in df.columns and 'countdown' in df.columns:
    # Convert 'timestamp' to a datetime object if it's not already in that format
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

    # Find the first row where countdown is not null
    first_valid_index = df['countdown'].first_valid_index()

    first_ignited_index = df['Ignited'].first_valid_index()

    # Slice the DataFrame from the first valid index to the end
    df = df.loc[first_ignited_index:]
    #print(data.iloc[0])

    # Plotting countdown against timestamp
    plt.figure(figsize=(10, 5))
    plt.plot(df['timestamp'], df['position-x'], marker="o", linestyle='-')

    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
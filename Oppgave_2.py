import pandas as pd
import yaml
import json

# Åpner json fil og lagrer som config
with open("config.yml") as yaml_fil:
    config = yaml.safe_load(yaml_fil)

# Henter ut data fra config
max_day = config["max_days_since_calibration"]
output = config["output_file"]

# Åpner Excel fil og lagrer som sensor
sensor_df = pd.read_excel("sensors.xlsx")
# Åpner csv fil og lagrer som calibration
calibration_df = pd.read_csv("calibrations.csv")

# Setter sammen excel og csv med felles rad "sensor_id"
merge_df = pd.merge(sensor_df, calibration_df, on = "sensor_id")


# Funksjon til å finne sensor_id som er utgått kontroll
def filter_data(merge_df, max_day):
    return merge_df[merge_df["days_since_calibration"] > max_day]

# Endrer fra dataframe til python
overdue_df = filter_data(merge_df, max_day)
overdue_list = overdue_df.to_dict(orient="records")

# Konverterer til json format og lager json fil
with open(output, "w") as json_fil:
    json.dump(overdue_list, json_fil, indent=2)

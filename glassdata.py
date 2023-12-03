# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 13:42:39 2023

@author: me
"""
import pandas as pd
import numpy as np
from datetime import datetime

filename = "fuellstandsensoren-glassammelstellen-weissglas"
filetype = ".xlsx"
total_glass_df = pd.read_excel(filename + filetype)

total_glass_df = total_glass_df.dropna(subset=["data_distance"])
total_glass_df = total_glass_df[total_glass_df["data_distance"] < 2000]
total_glass_df = total_glass_df.drop_duplicates(subset=["measured_at"])

total_glass_df["measured_at"] = pd.to_datetime(total_glass_df["measured_at"], utc=True)

total_glass_df["date"] = total_glass_df["measured_at"].dt.strftime("%Y-%m-%d")
total_glass_df["time"] = total_glass_df["measured_at"].dt.strftime("%H:%M:%S")
total_glass_df.sort_values(by="measured_at", ascending=True, inplace=True)

window_size = 5

total_glass_df["rolling_mean"] = total_glass_df["data_distance"].rolling(window=window_size, min_periods=1, center=True).mean()
total_glass_df["rolling_std"] = total_glass_df["data_distance"].rolling(window=window_size, min_periods=1, center=True).std()
total_glass_df["errorval"] = np.abs(total_glass_df["data_distance"] - total_glass_df["rolling_mean"]) > 2 * total_glass_df["rolling_std"]
total_glass_df = total_glass_df[~total_glass_df["errorval"]]

total_glass_df = total_glass_df.drop(["data", "name", "id", "location", "rolling_mean", "rolling_std", "errorval"], axis=1)

locations = {}
defectlist = []
monthly_df = pd.DataFrame(columns=["device_id", "measured_at", "avg/min"])

for value in total_glass_df["geo_point_2d"].unique():
    locations[value] = total_glass_df[total_glass_df["geo_point_2d"] == value].copy()
    locations[value].sort_values(by="measured_at", ascending=True, inplace=True)
    if (datetime.now() - datetime.strptime(locations[value]["date"].iloc[-1], "%Y-%m-%d")).days > 60:
        defectlist.append(locations[value]["device_id"].iloc[0])
        locations.pop(value)
        continue

    locations[value]["time_diff"] = locations[value]["measured_at"] - locations[value]["measured_at"].shift(1)
    locations[value]["time_diff"] = locations[value]["time_diff"].dt.total_seconds() / 60
    locations[value]["distance_diff"] = (
        locations[value]["data_distance"].rolling(window=7, min_periods=1, center=True).mean() - locations[value]["data_distance"].shift(1).rolling(window=7, min_periods=1, center=True).mean()
    )
    locations[value]["distance_diff"] = locations[value]["distance_diff"].clip(upper=0)
    locations[value] = locations[value].dropna(subset=["distance_diff"])
    # monthly_sum = locations[value].resample("M", on="measured_at").sum()
    # monthly_sum = monthly_sum.reset_index()
    # monthly_sum["avg/min"] = -(monthly_sum["distance_diff"] / monthly_sum["time_diff"])
    # monthly_sum = pd.concat([monthly_df, monthly_sum[["device_id", "measured_at", "avg/min"]]], ignore_index=True, axis=1)


# monthly_df["measured_at"] = pd.to_datetime(monthly_df["measured_at"]).dt.strftime("%Y-%m")
# monthly_df.to_excel("mothly_result_" + filename + filetype, index=False)

result_df = pd.DataFrame(columns=["Geo_Point_2D"])

for key, df in locations.items():
    df.drop(["measured_at"], axis=1, inplace=True)
    avg_diff = -df["distance_diff"] / df["time_diff"]
    new_row = pd.DataFrame(
        [{"Geo_Point_2D": key, "device_id": df["device_id"].iloc[0], "average_fill/min": avg_diff.mean(), "average_fill/h": avg_diff.mean() * 60, "average_fill/day": avg_diff.mean() * 1440}]
    )
    result_df = pd.concat([result_df, new_row], ignore_index=True)

result_df.to_excel("result_" + filename + filetype, index=False)

with open("defects_" + filename + ".txt", "w") as f:
    f.write("no data in last 2 months:\n")
    for defects in defectlist:
        f.write(str(defects) + "\n")

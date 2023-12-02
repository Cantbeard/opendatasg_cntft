# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 13:42:39 2023

@author: me
"""
import pandas as pd

total_glassentsorgung_path = "fuellstandsensoren-glassammelstellen-gruenglas.xlsx"
total_glass_df = pd.read_excel(total_glassentsorgung_path)

total_glass_df = total_glass_df.dropna(subset=["data_distance"])

total_glass_df["measured_at"] = pd.to_datetime(total_glass_df["measured_at"], utc=True)

total_glass_df["date"] = total_glass_df["measured_at"].dt.strftime("%Y-%m-%d")
total_glass_df["time"] = total_glass_df["measured_at"].dt.strftime("%H:%M:%S")
total_glass_df = total_glass_df.drop(["measured_at", "data", "device_id", "name", "id", "location"], axis=1)

total_glass_df = total_glass_df.sort_values(by=["date", "time"])

datetime_df = pd.to_datetime(total_glass_df["date"] + " " + total_glass_df["time"])
reference_time = pd.Timestamp("2020-01-01")
total_glass_df["time_difference_seconds"] = (datetime_df - reference_time).dt.total_seconds()
total_glass_df["geo_point_2d"] = total_glass_df["geo_point_2d"].astype("category")

locations = {}
for value in total_glass_df["geo_point_2d"].unique():
    locations[value] = total_glass_df[total_glass_df["geo_point_2d"] == value].copy()

loc_df = locations["47.43514, 9.39166"]
type(loc_df)
loc_df["diff"] = loc_df["data_distance"] - loc_df["data_distance"].shift(1)

emptied_df = loc_df[loc_df["diff"] > 500 and loc_df["data_distance"] != 2500]

print(emptied_df)

# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 22:37:01 2023

@author: me
"""

import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

people_path = "stada2.csv"
total_glassentsorgung_path = "entsorgungsstatistik-stadt-stgallen.csv"

peopledf = pd.read_csv(people_path)
peopledf = peopledf.drop(["GEBIET_NAME"], axis=1).transpose().reset_index()
peopledf.columns = ["year", "inhabitants"]
peopledf = peopledf[peopledf["year"] >= "2015"]

total_glass_df = pd.read_csv(total_glassentsorgung_path)
total_glass_df = total_glass_df["ID;Monat_Jahr;Abfallfraktion;Unterkategorie;Entsorgungsart;Abfuhrgebiet;Annahmestelle;Deponie Anlieferung;Gewicht in kg;Gewicht in t"].str.split(";", expand=True)
total_glass_df.columns = [f"{i}" for i in range(total_glass_df.shape[1])]
total_glass_df[["year", "month"]] = total_glass_df["1"].str.split("-", expand=True)
total_glass_df = total_glass_df.drop(["0", "1", "2", "4", "5", "6", "7", "9"], axis=1)
total_glass_df.columns = ["type", "weight", "year", "month"]
total_glass_df["weight"] = pd.to_numeric(total_glass_df["weight"], errors="coerce")
total_year = total_glass_df.groupby("year")[["weight", "month"]].sum().reset_index()

total_brownglass_df = total_glass_df[total_glass_df["type"] == "Braunglas"]
total_greenglass_df = total_glass_df[total_glass_df["type"] == "Grünglas"]
total_whiteglass_df = total_glass_df[total_glass_df["type"] == "Weissglas"]
total_year_brown = total_brownglass_df.groupby("year")["weight"].sum().reset_index()
total_year_green = total_greenglass_df.groupby("year")["weight"].sum().reset_index()
total_year_white = total_whiteglass_df.groupby("year")["weight"].sum().reset_index()

# ---------------------------------------------------------------------------------------------
sb.lineplot(x=total_year["year"], y=total_year["weight"], label="Total")
sb.lineplot(x=total_year_brown["year"], y=total_year_brown["weight"], label="Braunglas")
sb.lineplot(x=total_year_brown["year"], y=total_year_green["weight"], label="Grünglas")
sb.lineplot(x=total_year_brown["year"], y=total_year_white["weight"], label="Weissglas")

plt.xlabel("year")
plt.ylabel("weight in tons")
plt.title("glass collected 2015-2023 (2023 still ongoing)")
plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x / 1000:.0f} t"))
plt.savefig("totalplot.jpg", dpi=300, bbox_inches="tight")
plt.show()

# ---------------------------------------------------------------------------------------------
total_glass_df = total_glass_df.sort_values("month")
total_glass_df = total_glass_df.groupby(["month", "year"], as_index=False)["weight"].sum()

sb.lineplot(x="month", y="weight", hue="year", data=total_glass_df)

plt.xlabel("Month")
plt.ylabel("Weight")
plt.title("Weight in different Months for Different Years")
plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x / 1000:.0f} t"))
plt.savefig("permonth.jpg", dpi=300, bbox_inches="tight")
plt.show()
# ---------------------------------------------------------------------------------------------
# sb.lineplot(x=peopledf["year"], y=peopledf["inhabitants"], label="einwohner", color="black")

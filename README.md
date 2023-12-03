# glassplots.py
Generiert plots aus "entsorgungsstatistik-stadt-stgallen.xlsx" (permonth, totalplot)

# greenglassplot.ipynb
Jupyter notebook um überblick über grünglassdaten zu gewinnen (x = sekunden seit 2020-01-01, y = distanz)

# glassdata.py
Liest opendata excelfile ein (z.B. fuellstandsensoren-glassammelstellen-braunglas.xlsx) und erstellt daraus 
defects_fuellstandsensoren-glassammelstellen-_______glas.txt und
result_fuellstandsensoren-glassammelstellen-_______glas.xlsx 

## defects_fuellstandsensoren-glassammelstellen-_______glas.txt 
Liste der Sensor IDs, die in den letzten 2 monaten keine daten gesendet haben.

## result_fuellstandsensoren-glassammelstellen-_______glas.xlsx 
Tabelle der device_id, deren Geo_Point_2D koordinaten und durchschnittlichefüllungsgeschwindigkeit seit messbeginn
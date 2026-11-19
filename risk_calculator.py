# -*- coding: utf-8 -*-
"""
risk_calculator.py
Loads risks from a CSV, prints the risk table, and runs a simulation.

@author: dom
"""
import pandas as pd
import numpy as np

from risk import Risk
from simulation import simulate_year

### load the CSV
data = pd.read_csv("risks_provider.csv")

### turn each row into a Risk object
risks = []
for index, row in data.iterrows():
    r = Risk(row["Name"], row["Cost per Incident"], row["Incidents per Year"],
             row["Control Cost"], row["Removal"])
    risks.append(r)

### build the table
rows = []
for risk in risks:
    rows.append({"Risk": risk.risk, "Cost per Incident": risk.cost,
                 "Incidents per Year": risk.incidents, "Control Cost": risk.controls,
                 "Removal %": risk.removal * 100, "Yearly Cost": risk.yearly_price(),
                 "Incidents After": risk.control_reduction(),
                 "Cost After Control": risk.cost_with_control(),
                 "Net Benefit": risk.net_benefit(), "Worth It?": risk.worth()})

table = pd.DataFrame(rows)
df_sorted = table.sort_values(by="Yearly Cost", ascending=False)
df_print = df_sorted.copy()

price_cols = ["Cost per Incident", "Control Cost", "Yearly Cost",
              "Cost After Control", "Net Benefit"]
for col in price_cols:
    df_print[col] = df_print[col].map("${:,.0f}".format)

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", None)
print(df_print)

### simulation: many simulated years for one risk
print("\n ---- Simulation ----")
YEARS = 100000
chosen = risks[0]          # Network Server Hacking

results = []
for i in range(YEARS):
    results.append(simulate_year(chosen))

print("Risk:", chosen.risk)
print("Mean yearly loss:      ${:,.0f}".format(np.mean(results)))
print("Median yearly loss:    ${:,.0f}".format(np.median(results)))
print("95th percentile loss:  ${:,.0f}".format(np.percentile(results, 95)))
print("99th percentile loss:  ${:,.0f}".format(np.percentile(results, 99)))

# Cybersecurity-Risk-Calculator
A risk calculator that uses data from HHS Breach as well as some theoretical data to run a simulation on wether or not to invest in a certain kind of cybersecurity protection




# Healthcare Provider Cyber Risk Calculator

A Python project that estimates the yearly cost of cyber risks for a reference healthcare provider and tests whether security controls are worth paying for. I built it to practice Python classes, loading data from CSV files, pandas tables, and Monte Carlo simulation, and to practice the economics of security decisions: expected loss, control cost, and net benefit.

The inputs are built from my own analysis of real HHS breach data, plus clearly labeled assumptions. This is a learning project, not a forecast for any real organization.

## The reference organization

A healthcare provider with about 500 employees. Existing controls are basic antivirus and a firewall. Every risk below is a breach of patient data, split by type using how often each type shows up in provider breaches reported to HHS.

## Data

Breach shares and sizes come from my earlier project, [HHS Breach Analysis](#), which uses the HHS Office for Civil Rights Breach Portal (breaches affecting 500 or more people). For this project I kept the 5,843 reports filed by healthcare providers, and the 5,745 that list exactly one of the five main breach types.

| Breach type | Reports | Median people affected | Share of provider breaches |
|---|---|---|---|
| Hacking/IT Incident | 3,593 | 8,175 | 62.5% |
| Unauthorized Access/Disclosure | 1,084 | 1,617 | 18.9% |
| Theft | 796 | 2,000 | 13.9% |
| Loss | 175 | 1,729 | 3.0% |
| Improper Disposal | 97 | 1,772 | 1.7% |

I split hacking further using the Location column: 2,215 breaches at a network server (median 12,723 people), 1,048 at email (median 4,243), and the remaining 330 as other hacking.

Breach sizes are very skewed. For provider hacking, the 50th, 90th and 99th percentile sizes are about 8,175, 146,000 and 1.6 million people, and the largest is 10.3 million. A typical breach is small, but a few are enormous.

## How the model works

For each risk:

* **Yearly cost** = incidents per year × cost per incident
* **Cost with control** = incidents after control × cost per incident + control cost
* **Net benefit** = yearly cost − cost with control, which simplifies to incidents × cost × removal − control cost
* **Worth it?** is Yes if net benefit is above zero

The simulation replaces the single averages with random draws. For one simulated year:

1. The number of incidents is drawn from a Poisson distribution, using the incidents per year as the average.
2. Each incident's cost is drawn from a lognormal distribution. The median is the risk's cost per incident, and sigma is 2.25, fitted to the spread of the HHS provider hacking sizes.
3. The costs are added up to get the year's total loss.

## Inputs and assumptions

Everything in `risks_provider.csv` is documented in its Source column. Here is what is real and what is assumed.

| Input | Source |
|---|---|
| Breach type shares | Calculated from HHS provider data |
| Median breach sizes | Calculated from HHS provider data |
| Sigma of 2.25 for cost spread | Fitted to HHS provider hacking size percentiles |
| Breaches per year for the organization: **0.1** | **Assumption.** About one every ten years. No published figure was found. |
| Cost per record: **$77.50** | **Assumption.** Scaled so the simulated average breach costs about $6.64M, matching the IBM Cost of a Data Breach 2026 healthcare average (reported through secondary summaries, not checked against the IBM report). |
| Control costs and removal percentages | **Assumptions.** My own estimates for controls such as MFA and monitoring, email filtering, and device encryption. |

| Risk | Cost per incident | Incidents per year | Control cost | Removal |
|---|---|---|---|---|
| Network Server Hacking | $986,032 | 0.0386 | $30,000 | 35% |
| Email Hacking | $328,832 | 0.0182 | $12,000 | 40% |
| Other Hacking | $633,562 | 0.0057 | $8,000 | 25% |
| Unauthorized Access | $125,318 | 0.0189 | $15,000 | 30% |
| Theft | $155,000 | 0.0139 | $8,000 | 60% |
| Loss and Disposal | $135,625 | 0.0047 | $5,000 | 50% |

## Findings

**1. At median costs, no control pays for itself.**
At a breach rate of 0.1 per year, the expected yearly loss for each risk is small compared with the yearly control cost, so every row comes out No. Network Server Hacking is the closest, with a yearly cost of about $38,000 against a control that saves about $13,000 for $30,000.

**2. The median hides the tail, and the tail changes the answer.**
The mean of a lognormal with sigma 2.25 is about 12.6 times its median. Using the mean cost instead of the median, the expected total loss across all six risks is about $664,000 per year, which equals 0.1 breaches times IBM's $6.64M average. On that basis the controls for Network Server Hacking, Email Hacking, Other Hacking and Theft come out positive, while Unauthorized Access and Loss and Disposal stay negative. These expected values are worked out from the formula, and I have not yet confirmed them by simulating all six risks.

**3. Simulated results are noisy because breaches are rare.**
Running the simulation for Network Server Hacking, the mean yearly loss changed a lot between runs, from about $700,000 to about $1.4M with 10,000 years (before costs were rescaled). Only about 390 breaches occur in 10,000 simulated years, and a few huge ones dominate the average. More simulated years give steadier results. The median and 95th percentile yearly loss are both $0, because a breach happens in only about 4% of years.

**4. The answer depends heavily on the assumptions.**
Moving from median to mean costs, or from $160 to $77.50 per record, changes which controls look worth buying. A better conclusion than a single answer is that controls pay off when breaches are frequent enough or costly enough, and the table shows how far each one is from that point. For example, Network Server Hacking would break even at roughly 2.3 times the assumed incident rate at median costs.

## Limitations

* The breach rate, control costs and removal percentages are assumptions and are not from a source.
* HHS only lists breaches of 500 or more people, so smaller incidents are missing from the shares and sizes.
* A real breach's cost is not a flat amount per record. The cost per record is a single scaled number applied to every breach size.
* Sigma of 2.25 is fitted to hacking breaches and applied to every risk.
* The model counts only breach costs. Controls can also reduce fines, downtime and reputation damage, which are not included.
* Incident counts in the HHS data are reports, and one incident can be filed as several reports.

## Files

* `risk.py`: the `Risk` class with methods for yearly cost, control reduction, cost with control, net benefit, and worth it
* `simulation.py`: `simulate_year(risk)`, which returns the total loss for one simulated year
* `risk_calculator.py`: loads the CSV, builds the `Risk` objects, prints the risk table, and runs the simulation
* `risks_provider.csv`: the six risks with inputs and sources

## How to run it

1. Install Python with pandas and numpy (I used Spyder through Anaconda)
2. Keep all four files in the same folder and set that folder as the working directory
3. Run `risk_calculator.py`. It prints the risk table and the simulation results

## Next steps

* Simulate all six risks together and report the mean, median, 95th and 99th percentile of total yearly loss
* Run the simulation with and without controls and compare
* Test the breach rate at 0.05, 0.1, 0.3 and 0.5 and see which controls flip
* Test the removal percentages and cost per record the same way
* Plot a histogram of simulated yearly losses
* Replace the assumed controls with sourced effectiveness numbers

## Tools

Python, pandas, numpy

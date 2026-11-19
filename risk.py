# -*- coding: utf-8 -*-
"""
risk.py
One Risk object holds the inputs for a single cyber risk and
the methods that turn those inputs into dollars.

@author: dom
"""


class Risk:

    def __init__(self, risk_name, cost_per_incident, incidents_year,
                 cost_of_controls, risk_removal):
        self.risk = risk_name
        self.cost = cost_per_incident
        self.incidents = incidents_year
        self.controls = cost_of_controls
        self.removal = risk_removal

    def yearly_price(self):
        # expected loss per year with no control
        return self.incidents * self.cost

    def control_reduction(self):
        # incidents per year left after the control
        return self.incidents * (1 - self.removal)

    def cost_with_control(self):
        # remaining expected loss plus what the control costs
        return self.control_reduction() * self.cost + self.controls

    def net_benefit(self):
        # loss avoided minus control cost: positive means the control is worth it
        return self.yearly_price() - self.cost_with_control()

    def worth(self):
        if self.net_benefit() > 0:
            return "Yes"
        else:
            return "No"

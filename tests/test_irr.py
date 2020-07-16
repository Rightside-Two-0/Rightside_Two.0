#!/usr/bin/env python3
from calc_irr import calc_irr
from calc_irr import mortgage

calc = calc_irr()
calc.cost_rev(asking=240000,improvements=0,units=12,average_rent=500,sqft=10000)
calc.financing_assumptions(equity_per=0.3,seller_carry_per=0,interest_rate=5.0,amort_period=30,seller_carry_rate=8.0,seller_carry_term=60)
calc.revenues(rent_increase=0.02,expense_increase=0.025,vac_rate=10.0,extra_income=0)
calc.expenses(repairs=60,management=0,tax=0,insure=0,payroll=0,utils=0,gen_admin=0,pro_fees=0,ads=0,cap_x=1850,other_x=30000)
interest = calc.calc_interest(start=12, end=0)
calc.deal(percent_rightside=0.45)
calc.calc_future_unit_worth()
print(calc.cash_on_cash*100)

print('testing in progress...')
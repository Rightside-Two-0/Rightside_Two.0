#!/usr/bin/env python3
import mortgage
import datetime
import numpy as np
from itertools import islice
from openpyxl import load_workbook
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ask = 0
land = 0
building = 0
improvements_cost = 0
closing_costs = 0
acquisition_fee = 0
num_units = 0
ave_rent_monthly = 0
gross_rents = 0
total_purchase = 0
owners_equity_percent = 0
owners_equity_value = 0
seller_financing_percent = 0
seller_financing_value = 0
financing_amount = 0
interest_rate_yearly = 0.0
interest_rate_monthly = 0.0
amort_period_yearly = 0
amort_period_monthly = 0
payment_annual = 0
payment_monthly = 0
seller_financing_rate = 0.0
seller_financing_term = 0.0
total_sqft = 0
ave_sqft_unit = 0
ave_rent_sqft = 0
ave_cost_sqft = 0
ave_unit_cost = 0
cap_rate = 0
gross_rent_multiplier = 0
expense_unit = 0
expense_sqft = 0
cash_on_cash = 0.0
rental_increase_projection = 0.0
operating_expense_projection = 0.0
gross_scheduled_income = 0
vacancy_rate = 0.0
vacancy_rate_value = 0
net_rental_income = 0
other_income = 0
gross_income = 0
repairs_maintenance = 0
property_mang_fee = 0
taxes = 0
insurance = 0
salaries_wages = 0
utilities = 0
general_admin = 0
professional_fees = 0
advertising = 0
capital_reserves = 0
other = 0
total_operating_expenses = 0
noi = 0
interest_loan = 0.0
principle_paid = 0
seller_financing_cost = 0
total_interest_cost = 0
income_tax_rate = 0
depreciation_expense = 0
total_tax_deductions = 0
net_income_before_taxes = 0
expected_tax_bill = 0
net_after_tax = 0
#~~~~~~~~~~~~~~~~~~~~~~~~
investment_unit = 0
closing_fees = 0
acquisition_cost = 0
down = 0
five_years_unit = 0
ten_years_unit = 0
twenty_years_unit = 0
thirty_years_unit = 0
five_years_total = 0
ten_years_total = 0
twenty_years_total = 0
thirty_years_total = 0
roi = 0.0
roi_yr = 0.0
roi_month = 0.0
opportunity_percent = 0
opportunity_value = 0
creating_value = 0
creating_units = 0
expecting_rightside = 0
expecting_rightside_percent = 0
rightside_percent_coc = 0.0
investors_percent_coc = 0.0
investors_percent = 0
investors_value = 0
first_yr_returns_investors = 0
first_yr_returns_rightside = 0
contributing_value = 0
contributing_units = 0
expecting_investors = 0
expecting_investors_percent = 0
min_investment_investor = 0
min_investment_unit = 0
initial_investment = 0
year_1_cashflow_percent = 0
year_1_cashflow_value = 0
year_2_cashflow_percent = 0
year_2_cashflow_value = 0
year_3_cashflow_percent = 0
year_3_cashflow_value = 0
year_4_cashflow_percent = 0
year_4_cashflow_value = 0
year_5_cashflow_percent = 0
year_5_cashflow_value = 0
year_6_refinance = 0
repay_debts = 0
profits = 0
cash_profits = 0
percentage_5yr = 0
irr_cashflow_1_unit = 0
irr_cashflow_1_value = 0
irr_pv_1yr = 0
irr_cashflow_2_unit = 0
irr_cashflow_2_value = 0
irr_pv_2yr = 0
irr_cashflow_3_unit = 0
irr_cashflow_3_value = 0
irr_pv_3yr = 0
irr_cashflow_4_unit = 0
irr_cashflow_4_value = 0
irr_pv_4yr = 0
irr_cashflow_5_unit = 0
irr_cashflow_5_value = 0
irr_pv_5yr = 0
irr_cashout = 0
irr_cashout_unit = 0
irr_cashout_pv = 0
total_pv = 0
total_pv_unit = 0
npv = 0
npv_unit = 0
irr = 0
m = None
# workbook = load_workbook(filename='Template2.0.xlsx')
# sheet = workbook.active

def cost_rev(asking, improvements, units, average_rent, sqft):
    global ask, improvements_cost, num_units, ave_rent_monthly, land, building, closing_costs, acquisition_fee, gross_rents, total_sqft
    ask = asking
    improvements_cost = improvements
    num_units = units
    ave_rent_monthly = average_rent
    land = ask * 0.2
    building = ask * 0.8
    closing_costs = ask * 0.035
    acquisition_fee = ask * 0.001
    gross_rents = num_units * ave_rent_monthly
    total_sqft = sqft
def financing_assumptions(equity_per, seller_carry_per, interest_rate, amort_period, seller_carry_rate, seller_carry_term):
    global m, total_purchase, ask, improvements_cost, owners_equity_percent, seller_financing_percent, owners_equity_value, seller_financing_value, financing_amount, interest_rate_yearly, interest_rate_monthly, amort_period_yearly, amort_period_monthly, payment_monthly, payment_annual, seller_financing_rate, seller_financing_term
    total_purchase = ask - improvements_cost
    owners_equity_percent = equity_per
    seller_financing_percent = seller_carry_per
    owners_equity_value = total_purchase * owners_equity_percent
    seller_financing_value = total_purchase * seller_carry_per
    financing_amount = total_purchase - (owners_equity_value + seller_financing_value)
    interest_rate_yearly = interest_rate
    interest_rate_monthly = interest_rate_yearly / 12
    amort_period_yearly = amort_period
    amort_period_monthly = amort_period_yearly * 12
    m=mortgage.Mortgage(interest=(interest_rate_yearly/100), amount=financing_amount, months=amort_period_monthly)
    payment_monthly = m.monthly_payment()
    payment_annual = payment_monthly * 12
    seller_financing_rate = seller_carry_rate
    seller_financing_term = seller_carry_term
def revenues(rent_increase, expense_increase, vac_rate, extra_income):
    global rental_increase_projection, operating_expense_projection, vacancy_rate, gross_scheduled_income, num_units, gross_rents, vacancy_rate_value, net_rental_income, other_income, gross_income
    rental_increase_projection = rent_increase
    operating_expense_projection = expense_increase
    vacancy_rate = vac_rate
    gross_scheduled_income = num_units * gross_rents
    vacancy_rate_value = gross_scheduled_income * vacancy_rate/100
    net_rental_income = gross_scheduled_income - vacancy_rate_value
    other_income = extra_income
    gross_income = other_income + net_rental_income
def expenses(repairs, management, tax, insure, payroll, utils, gen_admin, pro_fees, ads, cap_x, other_x):
    global financing_amount, repairs_maintenance, property_mang_fee, taxes, insurance, salaries_wages, general_admin, professional_fees, advertising, capital_reserves, other, gross_income, total_operating_expenses, noi, net_income_before_taxes
    repairs_maintenance = repairs
    property_mang_fee = management
    taxes = tax
    insurance = insure
    salaries_wages = payroll
    utilities = utils
    general_admin = gen_admin
    professional_fees = pro_fees
    advertising = ads
    capital_reserves = cap_x
    other = other_x
    total_operating_expenses = repairs_maintenance+property_mang_fee+taxes+insurance+salaries_wages+utilities+general_admin+professional_fees+advertising+capital_reserves+other
    noi = gross_income - total_operating_expenses
    net_income_before_taxes = noi-(float(payment_annual)+seller_financing_cost)
def calc_interest(start, end):
    global m, interest_rate_yearly, financing_amount, amort_period_monthly
    if end == 0:
        interest = sum(month[1] for month in islice(m.monthly_payment_schedule(), 12))
    else:
        interest = sum(month[1] for month in islice(m.monthly_payment_schedule(), start, end))
    return interest
def deal(percent_rightside):
    global opportunity_percent, opportunity_value, net_income_before_taxes, investment_unit, creating_units, total_sqft, contributing_units, investors_percent, rightside_percent_coc, investors_percent_coc, first_yr_returns, first_yr_returns_rightside, contributing_value
    investors_percent = 1 - percent_rightside
    contributing_units = total_sqft * investors_percent
    investment_unit = (owners_equity_value+((total_purchase*0.035)+(total_purchase*0.01)))/contributing_units
    contributing_value = investment_unit * contributing_units
    opportunity_percent = percent_rightside
    opportunity_value = net_income_before_taxes * opportunity_percent
    creating_units = investment_unit * (total_sqft - contributing_units)
    creating_value = investment_unit * creating_units
    first_yr_returns_investors = net_income_before_taxes * investors_percent
    first_yr_returns_rightside = net_income_before_taxes * percent_rightside
    investors_percent_coc = first_yr_returns_investors / contributing_value
    cash_on_cash = net_income_before_taxes / contributing_value
    rightside_percent_coc = cash_on_cash - investors_percent_coc
    min_investment_investor = "{0:.0f}".format(owners_equity_value / 35)
    min_investment_unit = "{0:.0f}".format(float(min_investment_investor) / investment_unit)
def offer():
    global total_purchase, contributing_value, closing_costs, acquisition_cost, down, five_years_unit, ten_years_unit, twenty_years_unit, thirty_years_unit, five_years_total, ten_years_total, twenty_years_total, thirty_years_total, roi, roi_yr, roi_month
    calc_future_unit_worth()
    closing_costs = total_purchase * 0.035
    acquisition_cost = contributing_value * 0.01
    down = contributing_value - (closing_costs + acquisition_cost)
def key_ratios():
    global total_sqft, num_units, gross_rents, total_purchase, gross_income, ave_cost_sqft, ave_sqft_unit, ave_rent_sqft, ave_unit_cost, gross_rent_multiplier, expense_sqft, expense_unit, cash_on_cash, total_operating_expenses, net_income_before_taxes, contributing_value
    ave_sqft_unit = total_sqft / num_units
    ave_rent_sqft = total_sqft / gross_rents
    ave_cost_sqft = total_purchase / total_sqft
    ave_unit_cost = total_purchase / num_units
    gross_rent_multiplier = total_purchase / gross_income
    expense_unit = total_operating_expenses / num_units
    expense_sqft = total_operating_expenses / total_sqft
    cash_on_cash = (net_income_before_taxes) / (investment_unit * contributing_units)*100
def calc_future_unit_worth():
    global contributing_value, noi, gross_scheduled_income, rental_increase_projection, operating_expense_projection, total_operating_expenses, total_sqft, financing_amount, five_years_unit, ten_years_unit, twenty_years_unit, thirty_years_unit, five_years_total, ten_years_total, twenty_years_total, thirty_years_total, roi, roi_month, roi_yr, investors_percent_coc, first_yr_returns_investors, profits, cash_profits, percentage_5yr, net_income_before_taxes, expected_tax_bill, net_after_tax, irr
    gross_scheduled_income_2yr = (gross_scheduled_income * rental_increase_projection) + gross_scheduled_income
    gross_scheduled_income_3yr = (gross_scheduled_income_2yr * rental_increase_projection) + gross_scheduled_income_2yr
    gross_scheduled_income_4yr = (gross_scheduled_income_3yr * rental_increase_projection) + gross_scheduled_income_3yr
    gross_scheduled_income_5yr = (gross_scheduled_income_4yr * rental_increase_projection) + gross_scheduled_income_4yr
    total_operating_expenses_2yr = (total_operating_expenses * operating_expense_projection) + total_operating_expenses
    total_operating_expenses_3yr = (total_operating_expenses_2yr * operating_expense_projection) + total_operating_expenses_2yr
    total_operating_expenses_4yr = (total_operating_expenses_3yr * operating_expense_projection) + total_operating_expenses_3yr
    total_operating_expenses_5yr = (total_operating_expenses_4yr * operating_expense_projection) + total_operating_expenses_4yr
    noi_1yr = noi
    noi_2yr = gross_scheduled_income_2yr - total_operating_expenses_2yr
    noi_3yr = gross_scheduled_income_3yr - total_operating_expenses_3yr
    noi_4yr = gross_scheduled_income_4yr - total_operating_expenses_4yr
    noi_5yr = gross_scheduled_income_5yr - total_operating_expenses_5yr

    interest_1yr = calc_interest(12, 0)
    interest_2yr = calc_interest(12, 24)
    interest_3yr = calc_interest(24, 36)
    interest_4yr = calc_interest(36, 48)
    interest_5yr = calc_interest(48, 60)

    principle_paid_1yr = payment_annual - interest_1yr
    principle_paid_2yr = payment_annual - interest_2yr
    principle_paid_3yr = payment_annual - interest_3yr
    principle_paid_4yr = payment_annual - interest_4yr
    principle_paid_5yr = payment_annual - interest_5yr
    total_principle_5yrs = int(principle_paid_1yr+principle_paid_2yr+principle_paid_3yr+principle_paid_4yr+principle_paid_5yr)

    five_years_unit = ((noi_5yr/0.075)-(financing_amount-(total_principle_5yrs)))/total_sqft
    ten_years_unit = ((noi_5yr/0.075)+((noi_5yr/0.075)*0.015*5)-(financing_amount*0.81))/total_sqft
    twenty_years_unit = ((noi_5yr/0.075)+((noi_5yr/0.075)*0.015*15)-(financing_amount*0.51))/total_sqft
    thirty_years_unit = ((noi_5yr/0.075)+((noi_5yr/0.075)*0.015*25))/total_sqft
    five_years_total = five_years_unit * total_sqft
    ten_years_total = ten_years_unit * total_sqft
    twenty_years_total = twenty_years_unit * total_sqft
    thirty_years_toal = thirty_years_unit * total_sqft
    roi = "{0:.2f}".format(thirty_years_toal / contributing_value)
    roi_yr = "{0:.2f}".format(float(roi)*100 / 30)
    roi_month = "{0:.2f}".format(float(roi)*100 / 360)

    #~~~~~~~~~5-year~~performance~~~~~~~~~~~~~~~~~
    year_1_cashflow_percent = investors_percent_coc
    year_1_cashflow_value = first_yr_returns_investors
    net_income_before_taxes_2yr = noi_2yr+(-float(payment_annual)+seller_financing_cost)
    year_2_cashflow_percent = (net_income_before_taxes_2yr / contributing_value) * investors_percent
    year_2_cashflow_value = net_income_before_taxes_2yr * investors_percent
    net_income_before_taxes_3yr = noi_3yr+(-float(payment_annual)+seller_financing_cost)
    year_3_cashflow_percent = (net_income_before_taxes_3yr / contributing_value) * investors_percent
    year_3_cashflow_value = net_income_before_taxes_3yr * investors_percent
    net_income_before_taxes_4yr = noi_4yr+(-float(payment_annual)+seller_financing_cost)
    year_4_cashflow_percent = (net_income_before_taxes_4yr / contributing_value) * investors_percent
    year_4_cashflow_value = net_income_before_taxes_4yr * investors_percent
    net_income_before_taxes_5yr = noi_5yr+(-float(payment_annual)+seller_financing_cost)
    year_5_cashflow_percent = net_income_before_taxes_5yr * investors_percent
    year_5_cashflow_value = net_income_before_taxes_5yr * investors_percent
    refi_loan = (noi_5yr / 0.075) * 0.7
    payoff_amount = financing_amount-(total_principle_5yrs)+owners_equity_value
    profits = refi_loan - payoff_amount
    cash_profits = year_1_cashflow_value+year_2_cashflow_value+year_3_cashflow_value+year_4_cashflow_value+year_5_cashflow_value+profits
    percentage_5yr = (cash_profits / contributing_value) * 100

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~IRR~~~~~~~~~~~~~~~~~~~~~~
    net_after_tax = net_income_before_taxes - expected_tax_bill
    after_tax_1yr = net_after_tax
    irr_cashflow_1_value = after_tax_1yr * investors_percent
    irr_cashflow_1_unit = irr_cashflow_1_value / contributing_units
    irr_pv_1yr = irr_cashflow_1_value/(1+(interest_rate_yearly/100))**5
    after_tax_2yr = net_income_before_taxes_2yr - expected_tax_bill
    irr_cashflow_2_value = after_tax_2yr * investors_percent
    irr_cashflow_2_unit = irr_cashflow_2_value / contributing_units
    irr_pv_2yr = irr_cashflow_2_value/(1+(interest_rate_yearly/100))**5
    after_tax_3yr = net_income_before_taxes_3yr - expected_tax_bill
    irr_cashflow_3_value = after_tax_3yr * investors_percent
    irr_cashflow_3_unit = irr_cashflow_3_value / contributing_units
    irr_pv_3yr = irr_cashflow_3_value/(1+(interest_rate_yearly/100))**5
    after_tax_4yr = net_income_before_taxes_4yr - expected_tax_bill
    irr_cashflow_4_value = after_tax_4yr * investors_percent
    irr_cashflow_4_unit = irr_cashflow_4_value / contributing_units
    irr_pv_4yr = irr_cashflow_4_value/(1+(interest_rate_yearly/100))**5
    after_tax_5yr = net_income_before_taxes_5yr - expected_tax_bill
    irr_cashflow_5_value = after_tax_5yr * investors_percent
    irr_cashflow_5_unit = irr_cashflow_5_value / contributing_units
    irr_pv_5yr = irr_cashflow_5_value/(1+(interest_rate_yearly/100))**5
    irr_cashout = profits
    irr_cashout_unit = profits / contributing_units
    irr_cashout_pv = irr_cashout/(1+(interest_rate_yearly/100))**5
    total_pv_unit = irr_cashflow_1_unit+irr_cashflow_2_unit+irr_cashflow_3_unit+irr_cashflow_4_unit+irr_cashflow_5_unit
    total_pv = irr_cashflow_1_value+irr_cashflow_2_value+irr_cashflow_3_value+irr_cashflow_4_value+irr_cashflow_5_value+irr_cashout
    npv_unit = total_pv_unit+investment_unit
    npv = total_pv-contributing_value
    initial_investment = -contributing_value
    cashflows = [initial_investment, irr_pv_1yr, irr_pv_2yr, irr_pv_3yr, irr_pv_4yr, irr_pv_5yr, irr_cashout]
    irr = round(np.irr(cashflows),4)*100
def main():
    global m, irr, interest_loan, interest_rate_yearly, financing_amount, amort_period_monthly
    cost_rev(asking=240000,improvements=0,units=12,average_rent=500,sqft=10000)
    financing_assumptions(equity_per=0.3,seller_carry_per=0,interest_rate=5.0,amort_period=30,seller_carry_rate=8.0,seller_carry_term=60)
    revenues(rent_increase=0.02,expense_increase=0.025,vac_rate=10.0,extra_income=0)
    expenses(repairs=60,management=0,tax=0,insure=0,payroll=0,utils=0,gen_admin=0,pro_fees=0,ads=0,cap_x=1850,other_x=30000)
    interest_loan = calc_interest(start=12, end=0)
    deal(percent_rightside=0.45)
    offer()
    key_ratios()
    print('coc:', cash_on_cash)
    print('IRR:', str(irr)+'%')
    print('noi:', noi)
    print('entry price', investment_unit)
    print('5 year price', five_years_unit)
    print('10 year price', ten_years_unit)
    if irr >= 15.00:
        print('Initiall looks like it might be a good deal!')
        # write values and then save
        # Save the spreadsheet
        # workbook.save(filename='deals/deal'+str(datetime.datetime.now().timestamp())+'.xlsx')

if __name__ == '__main__':
    main()

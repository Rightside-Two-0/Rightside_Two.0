#!/usr/bin/env python3
from tests import mortgage
import datetime
import numpy as np
from itertools import islice

class calc_irr():
    def __init__(self):
        self.ask = 0
        self.land = 0
        self.building = 0
        self.improvements_cost = 0
        self.closing_costs = 0
        self.acquisition_fee = 0
        self.num_units = 0
        self.ave_rent_monthly = 0
        self.gross_rents = 0
        self.total_purchase = 0
        self.owners_equity_percent = 0
        self.owners_equity_value = 0
        self.seller_financing_percent = 0
        self.seller_financing_value = 0
        self.financing_amount = 0
        self.interest_rate_yearly = 0.0
        self.interest_rate_monthly = 0.0
        self.amort_period_yearly = 0
        self.amort_period_monthly = 0
        self.payment_annual = 0
        self.payment_monthly = 0
        self.seller_financing_rate = 0.0
        self.seller_financing_term = 0.0
        self.total_sqft = 0
        self.ave_sqft_unit = 0
        self.ave_rent_sqft = 0
        self.ave_cost_sqft = 0
        self.ave_unit_cost = 0
        self.cap_rate = 0
        self.gross_rent_multiplier = 0
        self.expense_unit = 0
        self.expense_sqft = 0
        self.cash_on_cash = 0.0
        self.rental_increase_projection = 0.0
        self.operating_expense_projection = 0.0
        self.gross_scheduled_income = 0
        self.vacancy_rate = 0.0
        self.vacancy_rate_value = 0
        self.net_rental_income = 0
        self.other_income = 0
        self.gross_income = 0
        self.repairs_maintenance = 0
        self.property_mang_fee = 0
        self.taxes = 0
        self.insurance = 0
        self.salaries_wages = 0
        self.utilities = 0
        self.general_admin = 0
        self.professional_fees = 0
        self.advertising = 0
        self.capital_reserves = 0
        self.other = 0
        self.total_operating_expenses = 0
        self.noi = 0
        self.interest_loan = 0.0
        self.principle_paid = 0
        self.seller_financing_cost = 0
        self.total_interest_cost = 0
        self.income_tax_rate = 0
        self.depreciation_expense = 0
        self.total_tax_deductions = 0
        self.net_income_before_taxes = 0
        self.expected_tax_bill = 0
        self.net_after_tax = 0
        #~~~~~~~~~~~~~~~~~~~~~~~~
        self.investment_unit = 0
        self.closing_fees = 0
        self.acquisition_cost = 0
        self.down = 0
        self.five_years_unit = 0
        self.ten_years_unit = 0
        self.twenty_years_unit = 0
        self.thirty_years_unit = 0
        self.five_years_total = 0
        self.ten_years_total = 0
        self.twenty_years_total = 0
        self.thirty_years_total = 0
        self.roi = 0.0
        self.roi_yr = 0.0
        self.roi_month = 0.0
        self.opportunity_percent = 0
        self.opportunity_value = 0
        self.creating_value = 0
        self.creating_units = 0
        self.expecting_rightside = 0
        self.expecting_rightside_percent = 0
        self.rightside_percent_coc = 0.0
        self.investors_percent_coc = 0.0
        self.investors_percent = 0
        self.investors_value = 0
        self.first_yr_returns_investors = 0
        self.first_yr_returns_rightside = 0
        self.contributing_value = 0
        self.contributing_units = 0
        self.expecting_investors = 0
        self.expecting_investors_percent = 0
        self.min_investment_investor = 0
        self.min_investment_unit = 0
        self.initial_investment = 0
        self.year_1_cashflow_percent = 0
        self.year_1_cashflow_value = 0
        self.year_2_cashflow_percent = 0
        self.year_2_cashflow_value = 0
        self.year_3_cashflow_percent = 0
        self.year_3_cashflow_value = 0
        self.year_4_cashflow_percent = 0
        self.year_4_cashflow_value = 0
        self.year_5_cashflow_percent = 0
        self.year_5_cashflow_value = 0
        self.year_6_refinance = 0
        self.repay_debts = 0
        self.profits = 0
        self.cash_profits = 0
        self.percentage_5yr = 0
        self.irr_cashflow_1_unit = 0
        self.irr_cashflow_1_value = 0
        self.irr_pv_1yr = 0
        self.irr_cashflow_2_unit = 0
        self.irr_cashflow_2_value = 0
        self.irr_pv_2yr = 0
        self.irr_cashflow_3_unit = 0
        self.irr_cashflow_3_value = 0
        self.irr_pv_3yr = 0
        self.irr_cashflow_4_unit = 0
        self.irr_cashflow_4_value = 0
        self.irr_pv_4yr = 0
        self.irr_cashflow_5_unit = 0
        self.irr_cashflow_5_value = 0
        self.irr_pv_5yr = 0
        self.irr_cashout = 0
        self.irr_cashout_unit = 0
        self.irr_cashout_pv = 0
        self.total_pv = 0
        self.total_pv_unit = 0
        self.npv = 0
        self.npv_unit = 0
        self.irr = 0
        self.m = None
    def cost_rev(self, asking, improvements, units, average_rent, sqft):
        self.ask = asking
        self.improvements_cost = improvements
        self.num_units = units
        self.ave_rent_monthly = average_rent
        self.land = self.ask * 0.2
        self.building = self.ask * 0.8
        self.closing_costs = self.ask * 0.035
        self.acquisition_fee = self.ask * 0.001
        self.gross_rents = units * self.ave_rent_monthly
        self.total_sqft = sqft
    def financing_assumptions(self, equity_per, seller_carry_per, interest_rate, amort_period, seller_carry_rate, seller_carry_term):
        self.total_purchase = self.ask - self.improvements_cost
        self.owners_equity_percent = equity_per
        self.seller_financing_percent = seller_carry_per
        self.owners_equity_value = self.total_purchase * self.owners_equity_percent
        self.seller_financing_value = self.total_purchase * seller_carry_per
        self.financing_amount = self.total_purchase - (self.owners_equity_value + self.seller_financing_value)
        self.interest_rate_yearly = interest_rate
        self.interest_rate_monthly = self.interest_rate_yearly / 12
        self.amort_period_yearly = amort_period
        self.amort_period_monthly = self.amort_period_yearly * 12
        self.m=mortgage.Mortgage(interest=(self.interest_rate_yearly/100), amount=self.financing_amount, months=self.amort_period_monthly)
        self.payment_monthly = self.m.monthly_payment()
        self.payment_annual = self.payment_monthly * 12
        self.seller_financing_rate = seller_carry_rate
        self.seller_financing_term = seller_carry_term
    def revenues(self, rent_increase, expense_increase, vac_rate, extra_income):
        self.rental_increase_projection = rent_increase
        self.operating_expense_projection = expense_increase
        self.vacancy_rate = vac_rate/100
        self.gross_scheduled_income = self.num_units * self.gross_rents
        self.vacancy_rate_value = self.gross_scheduled_income * self.vacancy_rate
        self.net_rental_income = self.gross_scheduled_income - self.vacancy_rate_value
        self.other_income = extra_income
        self.gross_income = self.other_income + self.net_rental_income
    def expenses(self, repairs, management, tax, insure, payroll, utils, gen_admin, pro_fees, ads, cap_x, other_x):
        self.repairs_maintenance = repairs
        self.property_mang_fee = management
        self.taxes = tax
        self.insurance = insure
        self.salaries_wages = payroll
        self.utilities = utils
        self.general_admin = gen_admin
        self.professional_fees = pro_fees
        self.advertising = ads
        self.capital_reserves = cap_x
        self.other = other_x
        self.total_operating_expenses = self.repairs_maintenance+self.property_mang_fee+self.taxes+self.insurance+self.salaries_wages+self.utilities+self.general_admin+self.professional_fees+self.advertising+self.capital_reserves+self.other
        self.noi = self.gross_income - self.total_operating_expenses
        self.net_income_before_taxes = self.noi-(float(self.payment_annual)+self.seller_financing_cost)
    def calc_interest(self, start, end):
        if end == 0:
            self.interest = sum(month[1] for month in islice(self.m.monthly_payment_schedule(), 12))
        else:
            self.interest = sum(month[1] for month in islice(self.m.monthly_payment_schedule(), start, end))
        return self.interest
    def deal(self, percent_rightside):
        self.investors_percent = 1 - percent_rightside
        self.contributing_units = self.total_sqft * self.investors_percent
        if self.contributing_units == 0:
            self.contributing_units = 1
        self.investment_unit = (self.owners_equity_value+((self.total_purchase*0.035)+(self.total_purchase*0.01)))/self.contributing_units
        self.contributing_value = self.investment_unit * self.contributing_units
        self.opportunity_percent = percent_rightside
        self.opportunity_value = self.net_income_before_taxes * self.opportunity_percent
        self.creating_value = self.investment_unit * (self.total_sqft - self.contributing_units)
        self.creating_units = self.total_sqft - self.contributing_units
        self.first_yr_returns_investors = self.net_income_before_taxes * self.investors_percent
        self.first_yr_returns_rightside = self.net_income_before_taxes * percent_rightside
        self.investors_percent_coc = self.first_yr_returns_investors / self.contributing_value
        self.cash_on_cash = self.net_income_before_taxes / self.contributing_value
        self.rightside_percent_coc = self.cash_on_cash - self.investors_percent_coc
        self.min_investment_investor = "{0:.0f}".format(self.owners_equity_value / 35)
        self.min_investment_unit = "{0:.0f}".format(float(self.min_investment_investor) / self.investment_unit)
    def offer(self):
        self.calc_future_unit_worth()
        self.closing_costs = self.total_purchase * 0.035
        self.acquisition_cost = self.contributing_value * 0.01
        self.down = self.contributing_value - (self.closing_costs + self.acquisition_cost)
    def key_ratios(self):
        self.ave_sqft_unit = self.total_sqft / self.num_units
        self.ave_rent_sqft = self.total_sqft / self.gross_rents
        self.ave_cost_sqft = self.total_purchase / self.total_sqft
        self.ave_unit_cost = self.total_purchase / self.num_units
        self.gross_rent_multiplier = self.total_purchase / self.gross_income
        self.expense_unit = self.total_operating_expenses / self.num_units
        self.expense_sqft = self.total_operating_expenses / self.total_sqft
    def calc_future_unit_worth(self):
        self.gross_scheduled_income_2yr = (self.gross_scheduled_income * self.rental_increase_projection) + self.gross_scheduled_income
        self.gross_scheduled_income_3yr = (self.gross_scheduled_income_2yr * self.rental_increase_projection) + self.gross_scheduled_income_2yr
        self.gross_scheduled_income_4yr = (self.gross_scheduled_income_3yr * self.rental_increase_projection) + self.gross_scheduled_income_3yr
        self.gross_scheduled_income_5yr = (self.gross_scheduled_income_4yr * self.rental_increase_projection) + self.gross_scheduled_income_4yr
        self.total_operating_expenses_2yr = (self.total_operating_expenses * self.operating_expense_projection) + self.total_operating_expenses
        self.total_operating_expenses_3yr = (self.total_operating_expenses_2yr * self.operating_expense_projection) + self.total_operating_expenses_2yr
        self.total_operating_expenses_4yr = (self.total_operating_expenses_3yr * self.operating_expense_projection) + self.total_operating_expenses_3yr
        self.total_operating_expenses_5yr = (self.total_operating_expenses_4yr * self.operating_expense_projection) + self.total_operating_expenses_4yr
        self.noi_1yr = self.noi
        self.noi_2yr = self.gross_scheduled_income_2yr - self.total_operating_expenses_2yr - self.vacancy_rate_value
        self.noi_3yr = self.gross_scheduled_income_3yr - self.total_operating_expenses_3yr - self.vacancy_rate_value
        self.noi_4yr = self.gross_scheduled_income_4yr - self.total_operating_expenses_4yr - self.vacancy_rate_value
        self.noi_5yr = self.gross_scheduled_income_5yr - self.total_operating_expenses_5yr - self.vacancy_rate_value

        self.interest_1yr = self.calc_interest(12, 0)
        self.interest_2yr = self.calc_interest(12, 24)
        self.interest_3yr = self.calc_interest(24, 36)
        self.interest_4yr = self.calc_interest(36, 48)
        self.interest_5yr = self.calc_interest(48, 60)

        self.principle_paid_1yr = self.payment_annual - self.interest_1yr
        self.principle_paid_2yr = self.payment_annual - self.interest_2yr
        self.principle_paid_3yr = self.payment_annual - self.interest_3yr
        self.principle_paid_4yr = self.payment_annual - self.interest_4yr
        self.principle_paid_5yr = self.payment_annual - self.interest_5yr
        self.total_principle_5yrs = int(self.principle_paid_1yr+self.principle_paid_2yr+self.principle_paid_3yr+self.principle_paid_4yr+self.principle_paid_5yr)

        self.five_years_unit = ((self.noi_5yr/0.075)-(self.financing_amount-(self.total_principle_5yrs)))/self.total_sqft
        self.ten_years_unit = ((self.noi_5yr/0.075)+((self.noi_5yr/0.075)*0.015*5)-(self.financing_amount*0.81))/self.total_sqft
        self.twenty_years_unit = ((self.noi_5yr/0.075)+((self.noi_5yr/0.075)*0.015*15)-(self.financing_amount*0.51))/self.total_sqft
        self.thirty_years_unit = ((self.noi_5yr/0.075)+((self.noi_5yr/0.075)*0.015*25))/self.total_sqft
        self.five_years_total = self.five_years_unit * self.total_sqft
        self.ten_years_total = self.ten_years_unit * self.total_sqft
        self.twenty_years_total = self.twenty_years_unit * self.total_sqft
        self.thirty_years_toal = self.thirty_years_unit * self.total_sqft
        self.roi = "{0:.2f}".format(self.thirty_years_toal*100 / self.contributing_value)
        self.roi_yr = "{0:.2f}".format(float(self.roi)*100 / 30)
        self.roi_month = "{0:.2f}".format(float(self.roi) / 360)
        
        #~~~~~~~~~5-year~~performance~~~~~~~~~~~~~~~~~
        self.year_1_cashflow_percent = self.investors_percent_coc
        self.year_1_cashflow_value = self.first_yr_returns_investors
        self.net_income_before_taxes_2yr = self.noi_2yr+(-float(self.payment_annual)+self.seller_financing_cost)
        self.year_2_cashflow_percent = (self.net_income_before_taxes_2yr / self.contributing_value) * self.investors_percent
        self.year_2_cashflow_value = self.net_income_before_taxes_2yr * self.investors_percent
        self.net_income_before_taxes_3yr = self.noi_3yr+(-float(self.payment_annual)+self.seller_financing_cost)
        self.year_3_cashflow_percent = (self.net_income_before_taxes_3yr / self.contributing_value) * self.investors_percent
        self.year_3_cashflow_value = self.net_income_before_taxes_3yr * self.investors_percent
        self.net_income_before_taxes_4yr = self.noi_4yr+(-float(self.payment_annual)+self.seller_financing_cost)
        self.year_4_cashflow_percent = (self.net_income_before_taxes_4yr / self.contributing_value) * self.investors_percent
        self.year_4_cashflow_value = self.net_income_before_taxes_4yr * self.investors_percent
        self.net_income_before_taxes_5yr = self.noi_5yr+(-float(self.payment_annual)+self.seller_financing_cost)
        self.year_5_cashflow_percent = (self.net_income_before_taxes_5yr / self.contributing_value) * self.investors_percent
        self.year_5_cashflow_value = self.net_income_before_taxes_5yr * self.investors_percent
        self.refi_loan = (self.noi_5yr / 0.075) * 0.7
        self.payoff_amount = self.financing_amount-(self.total_principle_5yrs)+self.owners_equity_value
        self.profits = self.refi_loan - self.payoff_amount
        self.cash_profits = self.year_1_cashflow_value+self.year_2_cashflow_value+self.year_3_cashflow_value+self.year_4_cashflow_value+self.year_5_cashflow_value+self.profits
        self.percentage_5yr = (self.cash_profits / self.contributing_value) * 100

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~IRR~~~~~~~~~~~~~~~~~~~~~~
        self.net_after_tax = self.net_income_before_taxes - self.expected_tax_bill
        self.after_tax_1yr = self.net_after_tax
        self.irr_cashflow_1_value = self.after_tax_1yr * self.investors_percent
        self.irr_cashflow_1_unit = self.irr_cashflow_1_value / self.contributing_units
        self.irr_pv_1yr = self.irr_cashflow_1_value/(1+(self.interest_rate_yearly/100))**5
        self.after_tax_2yr = self.net_income_before_taxes_2yr - self.expected_tax_bill
        self.irr_cashflow_2_value = self.after_tax_2yr * self.investors_percent
        self.irr_cashflow_2_unit = self.irr_cashflow_2_value / self.contributing_units
        self.irr_pv_2yr = self.irr_cashflow_2_value/(1+(self.interest_rate_yearly/100))**5
        self.after_tax_3yr = self.net_income_before_taxes_3yr - self.expected_tax_bill
        self.irr_cashflow_3_value = self.after_tax_3yr * self.investors_percent
        self.irr_cashflow_3_unit = self.irr_cashflow_3_value / self.contributing_units
        self.irr_pv_3yr = self.irr_cashflow_3_value/(1+(self.interest_rate_yearly/100))**5
        self.after_tax_4yr = self.net_income_before_taxes_4yr - self.expected_tax_bill
        self.irr_cashflow_4_value = self.after_tax_4yr * self.investors_percent
        self.irr_cashflow_4_unit = self.irr_cashflow_4_value / self.contributing_units
        self.irr_pv_4yr = self.irr_cashflow_4_value/(1+(self.interest_rate_yearly/100))**5
        self.after_tax_5yr = self.net_income_before_taxes_5yr - self.expected_tax_bill
        self.irr_cashflow_5_value = self.after_tax_5yr * self.investors_percent
        self.irr_cashflow_5_unit = self.irr_cashflow_5_value / self.contributing_units
        self.irr_pv_5yr = self.irr_cashflow_5_value/(1+(self.interest_rate_yearly/100))**5
        self.irr_cashout = self.profits
        self.irr_cashout_unit = self.profits / self.contributing_units
        self.irr_cashout_pv = self.irr_cashout/(1+(self.interest_rate_yearly/100))**5
        self.total_pv_unit = self.irr_cashflow_1_unit+self.irr_cashflow_2_unit+self.irr_cashflow_3_unit+self.irr_cashflow_4_unit+self.irr_cashflow_5_unit
        self.total_pv = self.irr_cashflow_1_value+self.irr_cashflow_2_value+self.irr_cashflow_3_value+self.irr_cashflow_4_value+self.irr_cashflow_5_value+self.irr_cashout
        self.npv_unit = self.total_pv_unit+self.investment_unit
        self.npv = self.total_pv-self.contributing_value
        self.initial_investment = -self.contributing_value
        self.cashflows = [self.initial_investment, self.irr_pv_1yr, self.irr_pv_2yr, self.irr_pv_3yr, self.irr_pv_4yr, self.irr_pv_5yr, self.irr_cashout]
        self.irr = round(np.irr(self.cashflows),4)*100
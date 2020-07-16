#!/usr/bin/env python3
from openpyxl import load_workbook
get_data = load_workbook('../deals/current_test.xlsx',data_only=True)
print(get_data)
sheet_data = get_data.active
print(sheet_data['A1'].value)
print(sheet_data['A2'].value)
print(sheet_data['A3'].value)
print(sheet_data['B4'].value)

#~~~~~~~~~~~~~~~>
yr1_unit = sheet_data['P6'].value
yr2_unit = sheet_data['P11'].value
yr3_unit = sheet_data['P12'].value
yr4_unit = sheet_data['P13'].value
yr5_unit = sheet_data['P14'].value
coc = sheet_data['N14'].value
irr = sheet_data['W35'].value
print('year 1 unit price: ', yr1_unit)
print('year 2 unit price: ', yr2_unit)
print('year 3 unit price: ', yr3_unit)
print('year 4 unit price: ', yr4_unit)
print('year 5 unit price: ', yr5_unit)
print('coc:', coc)
print('irr:', irr)
print('You rock young man! --> keep going!')

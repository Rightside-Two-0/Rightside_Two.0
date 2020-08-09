#!/usr/bin/env python3
import camelot
import pandas as pd

file = 'document.pdf'
tables = camelot.read_pdf(file)
print("Total tables extracted:", tables.n)
print('Number of tables:', tables.n)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# https://medium.com/@umerfarooq_26378/python-for-pdf-ef0fac2808b0
# import PyPDF2
#
# pdf_file = open('north_.pdf', 'rb')
# pdf_reader = PyPDF2.PdfFileReader(pdf_file)
# for i in range(pdf_reader.numPages):
#     page = pdf_reader.getPage(i)
#     print(page.extractText())

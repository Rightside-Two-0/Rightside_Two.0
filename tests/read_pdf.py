#!/usr/bin/env python3
# import tabula
# import pandas as pd
#
# df = tabula.read_pdf("testing_this.pdf", pages=6)
# print(df)
# # print(df.head())

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# https://medium.com/@umerfarooq_26378/python-for-pdf-ef0fac2808b0
import PyPDF2

pdf_file = open('north_.pdf', 'rb')
pdf_reader = PyPDF2.PdfFileReader(pdf_file)
for i in range(pdf_reader.numPages):
    page = pdf_reader.getPage(i)
    print(page.extractText())

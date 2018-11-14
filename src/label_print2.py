#!/bin/env python
# -*- coding:utf-8 -*-

from fpdf import FPDF
# https://github.com/reingart/pyfpdf/tree/master/docs/reference

pdf = FPDF('P', 'mm',(131, 198))
# define one column and one row margins
#pdf.set_margins(3,3)
pdf.set_font('Arial','B',7)

pdf.add_page()
#define total rows containing labels
rows = 7
# define total columns containing labels
cols = 3
#define column size and tweak it empirically
columnsize=(131.0/rows) + 5.0

print columnsize
print columnsize*3

# define serial number start
serial=0

for i in range(rows):

    for j in range(cols):
        text="SN: 00-%03i" % serial
        serial+=1
        pdf.set_font('Arial','B',8)
        pdf.cell(columnsize,0,text, align="C", border = 1)
    pdf.ln()
    for j in range(cols):
        pdf.set_font('Arial','B',6)
        pdf.cell(columnsize,7,"|B|F|D|O|C|L|V|", align="C")
    pdf.ln()
    for j in range(cols):
        pdf.cell(columnsize,(198/20)-6,"")
    pdf.ln()

pdf.output('labels.pdf','F')

#!/bin/env python
# -*- coding:utf-8 -*-
'''
Print PAT labels on supplied sheet.
'''

import labels
import os
from reportlab.graphics import shapes
import reportlab.lib.pagesizes
from reportlab.platypus import  Table, TableStyle

# Create an custom portrait  sheet with 3 columns and 7 rows of
# labels. Each label is 90mm x 25mm with a 2mm rounded corner. The margins are
# automatically calculated.
specs = labels.Specification(131, 198, 3, 7, 38, 25, corner_radius=2)


def draw_label(label, width, height, obj):
    # Just convert the object to a string and print this at the bottom left of
    # the label.
    label.add(shapes.String(8, 25,  str(obj[0]), fontName="Helvetica", fontSize=8))
    label.add(shapes.String(80, 25, str(obj[1]), fontName="Helvetica", fontSize=8))
    label.add(shapes.String(8, 4,   str(obj[2]), fontName="Helvetica", fontSize=8))
    label.add(shapes.String(55, 4,  str(obj[3]), fontName="Helvetica", fontSize=8))

# Create the sheet.
sheet = labels.Sheet(specs, draw_label, border=True)

# Add a couple of labels.
obj = ["AV1001","MFE", "2018-08-08", "20019-08-08"]
sheet.add_label(obj)
sheet.add_label(obj)
sheet.add_label(obj)


# We can also add each item from an iterable.
#sheet.add_labels(range(2, 22))

# Note that any oversize label is automatically trimmed to prevent it messing up
# other labels.
#sheet.add_label("Oversized label here")

# Save the file and we are done.
sheet.save('basic.pdf')
print("{0:d} label(s) output on {1:d} page(s).".format(sheet.label_count, sheet.page_count))
# This SHOULD scale and print, but it doesn't
#lpr -o fit-to-page -o InputSlot=ManualAdj -o media=Custom.130x195mm basic.pdf
# Or after modding the ppd file.
#lpr -o InputSlot=ManualAdj  -o media=Statement basic.pdf

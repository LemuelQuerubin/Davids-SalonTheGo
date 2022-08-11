# Help
# this func draws a ruler in the pdf to serve as a guide
def drawMyRuler(pdf):
    pdf.drawString(100,810, 'x100')
    pdf.drawString(200,810, 'x200')
    pdf.drawString(300,810, 'x300')
    pdf.drawString(400,810, 'x400')
    pdf.drawString(500,810, 'x500')

    pdf.drawString(10,100, 'y100')
    pdf.drawString(10,200, 'y200')
    pdf.drawString(10,300, 'y300')
    pdf.drawString(10,400, 'y400')
    pdf.drawString(10,500, 'y500')
    pdf.drawString(10,600, 'y600')
    pdf.drawString(10,700, 'y700')
    pdf.drawString(10,800, 'y800')

# Content ######################################################################
fileName = 'MyDoc.pdf'
documentTitle = 'Document title!'
title = 'Tasmanian Devil'
subTitle = 'The largest carnivorous marsupial'

textLines = [
    'The Tasmanian devil (Sarcophilus harrisii) is',
    'a carnivorous marsupial of the family',
    'Dasyuride.' 
]

image = 'tasmanianDevil.jpg'
# 0) Create document ######################################################################
from reportlab.pdfgen import canvas
pdf = canvas.Canvas(fileName)
pdf.setTitle(documentTitle)

drawMyRuler(pdf)
# 1) TITLE ######################################################################
# for font in pdf.getAvailableFonts():  # gets availble fonts
#     print(font)
# REGISTER A NEW FONT
# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.pdfbase import pdfmetrics

# pdfmetrics.registerFont(
#     TTFont('abc', 'SakBunderan.ttf')
# )
# pdf.setFont('abc')
pdf.setFont('Times-Bold', 36)

# pdf.drawString(270,770, title) # this will display the title at this position
pdf.drawCentredString(300,770, title) #calculates the center based on given X axis

# 2) SUB TITLE ######################################################################
pdf.setFillColorRGB(0,0,255) # sets the font color
pdf.setFont("Helvetica", 26)
pdf.drawCentredString(290,720, subTitle)

# 3) DRAW A LINE ######################################################################
pdf.line(30, 710, 550, 710) #550 and 710 are coordinates for the end of the line

# 4) TEXT OBJECT :: for large amounts of text ######################################################################
from reportlab.lib import colors

text = pdf.beginText(40, 680)
text.setFont("Courier", 18)
text.setFillColor(colors.red)
for line  in textLines:
    text.textLine(line)

# 5) DRAW A IMAGE ######################################################################
pdf.drawInlineImage (image, 130, 400)
pdf.drawText(text)
pdf.save()

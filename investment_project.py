import os
import docx
import datetime
from num2words import num2words
from dateutil.relativedelta import relativedelta
import pandas as pd
import openpyxl as opxl
import numpy as np
import matplotlib.pyplot as plt
from docx2pdf import convert

#os.chdir("files/")
doc = docx.Document('files/Template.docx')


def comma_separate(a):
    a = str(a)
    i = -1
    b = ''

    length = len(a)
    while length > 0:
        b = ',' + ''.join(reversed(a[i:i-3:-1]))  + b
        length -= 3
        i -= 3

    return b.strip(',')


def get_the_date(k):
    l = str(k)

    g = l[11:13]

    if g == '00':
        time = f"12{l[13:16]}am"

    elif  int(g)> 0 and int(g) < 12:
        time = f"{g}{l[13:16]}am"

    elif int(g) == 12:
        time = f"{g}{l[13:16]}pm"

    elif int(g)> 12:
        h = int(g)-12
        if h < 10:
            h = f"0{h}"
        time = f"{h}{l[13:16]}pm"
    else:
        pass

    if l[5:7] == '01':
        x = 'January'
    elif l[5:7] == '02':
        x = 'February'
    elif l[5:7] == '03':
        x = 'March'
    elif l[5:7] == '04':
        x = 'April'
    elif l[5:7] == '05':
        x = 'May'
    elif l[5:7] == '06':
        x = 'June'
    elif l[5:7] == '07':
        x = 'July'
    elif l[5:7] == '08':
        x = 'August'
    elif l[5:7] == '09':
        x = 'September'
    elif l[5:7] == '10':
        x = 'October'
    elif l[5:7] == '11':
        x = 'November'
    elif l[5:7] == '12':
        x = 'December'
    else:
        pass

    if l[9] == '1':
        y = 'st'
    elif l[9] == '2':
        y = 'nd'
    elif l[9] == '3':
        y = 'rd'
    else:
        y = 'th'

    if l[8:10] == '11' or l[8:10] == '12' or l[8:10] == '13':
        y = 'th'

    date = f"{l[8:10]}{y} of {x}, {l[0:4]}"
    
    return (time, date)



def create_mou(name, capital):
    name = name.upper().center(1)
    capital = str(capital).replace(',', '')
    capital_words = str(num2words(int(capital))).replace('-', ' ').upper()
    roi = int(int(capital) * 0.2 + int(capital))
    roi_words = str(num2words(roi)).replace('-', ' ').upper()
    date = get_the_date(datetime.datetime.now())
    pay_date = get_the_date(datetime.datetime.now()+relativedelta(days = 31))


    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            if 'OLUREMI DANIEL YINKA' in run.text:
                run.text = run.text.replace('MR OLUREMI DANIEL YINKA', name)

            if '12th of February, 2020' in run.text:
                run.text = run.text.replace('12th of February, 2020', date[1])
                
            if '12th of March, 2020' in run.text:
                run.text = run.text.replace('12th of March, 2020', pay_date[1])
                
            if 'FIFTY THOUSAND NAIRA ONLY (N50,000)' in run.text:
                run.text = run.text.replace('FIFTY THOUSAND NAIRA ONLY (N50,000)', capital_words+ f" NAIRA ONLY (₦{comma_separate(capital)})")

            if 'SIXTY FIVE THOUSAND NAIRA ONLY (N65,000)' in run.text:
                run.text = run.text.replace('SIXTY FIVE THOUSAND NAIRA ONLY (N65,000)', roi_words+ f" NAIRA ONLY (₦{comma_separate(roi)})")
        
        
    doc.save(f"files/{name + ' MOU'}.docx")
    convert(f"files/{name + ' MOU'}.docx")
             

             
    wb = opxl.load_workbook("files/Book1 - Copy.xlsx")
    sheet = wb['Sheet1']
    max_row = sheet.max_row
    sheet.cell(max_row+1, 1).value = 'JI-'+str(int(sheet.cell(max_row, 1).value[3:]) + 1)

    correction = [sheet.cell(max_row+1, 1).value, name, comma_separate(capital), ", ".join(date), 
                  comma_separate(int(int(capital) * 0.2)), comma_separate(roi), pay_date[1]]
    l = 0
    for i in sheet.rows:
        if l == max_row:
            b = 0
            for cell in i: 
                cell.value = correction[b]
                b += 1
        else:
            l += 1
            
    wb.save("files/Book1 - Copy.xlsx")
         

#create_mou('Mr. Oluwabuba Victor', 120000)         
#df = pd.read_csv("files/New.csv")
#df.loc[df.index[-1]+1] = ['JI-'+str(int(df.iloc[-1][0][3:]) + 1), name, comma_separate(capital), 
#                          ", ".join(date), comma_separate(int(int(capital) * 0.2)), comma_separate(roi), pay_date[1]]
#df.to_csv('files/New.csv', index= False)

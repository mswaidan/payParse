from flask import Flask
import csv
from io import StringIO

def writeCsv(listname):
    data = StringIO()  
    #csvFile =  open('parsed.csv', 'w')
    fieldnames = ['Date', 'Description', 'Amount']
    writer = csv.DictWriter(data, fieldnames=fieldnames)
    writer.writeheader()
    for item in listname:
        writer.writerow({
            'Date': item['Date'],
            'Description':item['Description'],
            'Amount' : item['Amount']
        })
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)
        
    return data

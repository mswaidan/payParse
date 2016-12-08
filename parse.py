import csv
import json

def toList(filename):
    csvFile = open(filename, encoding='utf-8-sig')
    reader = csv.DictReader(csvFile,skipinitialspace=True,quoting=csv.QUOTE_ALL)
    return list(reader)

def ppClean(listname):
    for item in listname:
        if item['Status'] == 'Pending':
            listname.remove(item)
    return listname

def ppParse(listname):
    newList = []
    for item in listname:
        if item['Type'] == 'Auto-sweep':
            newItem = {
                'Amount' : item['Gross'],
                'Description' : 'Transfer from PP to Bank',
                'Date' : item['Date']
            }
            newList.append(newItem)
        elif item['Type'] == 'Express Checkout Payment':
            newItem1 = {
                'Amount' : item['Gross'],
                'Description' : 'Payment from ' + item['Name'],
                'Date' : item['Date']
            }
            newItem2 = {
                'Amount' : item['Fee'],
                'Description' : 'Fee for ' + item['Name'],
                'Date' : item['Date']
            }
            newList.extend((newItem1,newItem2))
        elif item['Type'][:12] == 'Bank Deposit':
            newItem = {
                'Amount' : item['Gross'],
                'Description' : 'Transfer Bank to PP',
                'Date' : item['Date']
            }
            newList.append(newItem)
        elif item['Type'] == 'General Payment':
            newItem = {
                'Amount' : item['Gross'],
                'Description' : 'Payment from ' + item['Name'],
                'Date' : item['Date']
            }
            newList.append(newItem)
    return newList

def eParse(listname):
    newList = []
    for item in listname:
        newItem = {
            'Amount' : '-' + item['Fees'],
            'Description' : 'Etsy Payment Processing Fee for ' + item['Buyer'],
            'Date' : item['Order Date']
        }
        newList.append(newItem)
    return newList


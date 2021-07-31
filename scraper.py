#!/usr/bin/env python
import json
import urllib
import gspread 
import sys, os
import requests
from datetime import date
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials

# Print on same line 
# Print Bitcoin - 
# Then print the price next to it

print('Beginning Scraping')

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
# stockHook = 'https://hooks.slack.com/services/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'
gChats = 'https://chat.googleapis.com/v1/spaces/AAAAmwdvl68/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=cyO_SMzAU9COFut22UmNeHIRPY9m3UyrpqHAkQo8Gz0%3D'

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('StockTracking-3020849a6ece.json', scope)
client = gspread.authorize(creds)
sheet = client.open('Stock Tracking').sheet1
data = sheet.get_all_records()

date = date.today()
values = []
btcValue = 0
tslaValue = 0
usdValue = 0.0
etherValue = 0

def bitcoin():

    global btcValue
    URL = f"https://www.google.com/search?q=bitcoin"

    headers = {"user-agent" : USER_AGENT}
    resp = requests.get(URL, headers=headers)
    
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")

        for divs in soup.find_all('div', class_='dDoNo ikb4Bb gsrt gzfeS'):

            spans = divs.find('span', class_='DFlfde SwHCTb')
            price = spans.text
            btcValue = int(price[:3] + price[4:7])
            values.append(str(btcValue))
            print('Bitcoin - ' + str(btcValue))

def dollar():
    
    global usdValue
    URL = f"https://www.google.com/search?q=dollar+to+rand"

    headers = {"user-agent" : USER_AGENT}
    resp = requests.get(URL, headers=headers)
    
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")

        for divs in soup.find_all('div', class_='dDoNo ikb4Bb gsrt gzfeS'):

            spans = divs.find('span', class_='DFlfde SwHCTb')
            price = spans.text
            usdValue = float(price[:2] + '.' + price[3:5])
            values.append(str(usdValue))

            print('Dollar - ' + str(usdValue))

def tesla():
    
    global tslaValue
    URL = f"https://www.google.com/search?q=tesla+stock+price"

    headers = {"user-agent" : USER_AGENT}
    resp = requests.get(URL, headers=headers)
    
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")

        for divs in soup.find_all('div', class_='wGt0Bc'):

            spans = divs.find('span', class_='IsqQVc NprOob XcVN5d wT3VGc')
            price = spans.text
            tslaValue = float(price[:3])
            values.append(str(tslaValue))

            print('Tesla - ' + str(tslaValue))

def ethereum():

    global etherValue
    URL = f"https://www.google.com/search?q=ethereum+to+zar"

    headers = {"user-agent" : USER_AGENT}
    resp = requests.get(URL, headers=headers)
    
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")

        for divs in soup.find_all('div', class_='dDoNo ikb4Bb gsrt gzfeS'):

            spans = divs.find('span', class_='DFlfde SwHCTb')
            price = spans.text
            etherValue = int(price[:2] + price[3:6])
            values.append(str(btcValue))

            print('Ethereum - ' + str(etherValue))

def comparison():

    # Yesterday's values from Google Sheets
    btcOld = int(sheet.cell(2,2).value)
    usdOld = float(sheet.cell(2,3).value)
    tslaOld = float(sheet.cell(2,4).value)
    etherOld = float(sheet.cell(2,5).value)

    # Calculating difference in Values
    btcDiff = btcValue - btcOld
    usdDiff = usdValue - usdOld
    tslaDiff = tslaValue - tslaOld
    etherDiff = etherValue - etherOld

    # Calculating % difference in values
    if btcValue != '0':
        btcPerc = str((btcDiff / btcOld) * 100)
        btcPerc = btcPerc[:4]

        btcDiff = str(btcDiff)
        btcDiff = btcDiff[:6]

    if usdValue != '0':
        usdPerc = str((usdDiff / usdOld) * 100)
        usdPerc = usdPerc[:4]

        usdDiff = str(usdDiff)
        usdDiff = usdDiff[:4]

    if tslaValue != '0':
        tslaPerc = str((tslaDiff / tslaOld) * 100)
        tslaPerc = tslaPerc[:4]

        tslaDiff = str(tslaDiff)
        tslaDiff = tslaDiff[:4]

    if etherValue != '0':
        etherPerc = str((etherDiff / etherOld) * 100)
        etherPerc = etherPerc[:4]

        etherDiff = str(etherDiff)
        etherDiff = etherDiff[:5]

    # Terminal Print layout
    print('\nBitcoin Price - \tR' + str(btcValue) + '\t\tChange - \t' + str(btcPerc) + '%' + '\t\tDifference = \tR' + str(btcDiff) +
            '\nUS Dollar to Rand - \tR' + str(usdValue) + '\t\tChange - \t' + str(usdPerc) + '%' + '\t\tDifference = \tR' + str(usdDiff) +
            '\nTesla Price - \t\t$' + str(tslaValue) + '\t\tChange - \t' + str(tslaPerc) + '%' + '\t\tDifference = \t$' + str(tslaDiff) +
            '\nEthereum Price - \tR' + str(etherValue) + '\t\tChange - \t' + str(etherPerc) + '%' + '\t\tDifference = \t$' + str(etherDiff))

    input('Do you want to upload results?\n')

    # Google Chats Message
    message = { 'text' : '\nBitcoin Price - \t\tR' + str(btcValue) + '\tDifference - ' + str(btcPerc) + '%' + '\t\tChange = \t' + str(btcDiff) +
                            '\nUS Dollar to Rand - \tR' + str(usdValue) + '\t\tDifference - ' + str(usdPerc) + '%' + '\t\tChange = \t' + str(usdDiff) +
                            '\nTesla Price - \t\t\t$' + str(tslaValue) + '\t\tDifference - ' + str(tslaPerc) + '%' + '\t\tChange = \t' + str(tslaDiff) +
                            '\nEthereum Price - \t\tR' + str(etherValue) + '\t\tDifference - ' + str(etherPerc) + '%' + '\t\tChange = \t' + str(etherDiff)
    }
    requests.post(gChats, data=json.dumps(message))

    values = [str(date), str(btcValue), str(usdValue), str(tslaValue), str(etherValue)]
    sheet.insert_row(values, 2)

try:

    bitcoin()
    dollar()
    tesla()
    ethereum()
    comparison()

except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    input('\nError (' + str(exc_tb.tb_lineno) + ') - ' + str(e))

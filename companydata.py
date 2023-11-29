from selenium import webdriver
from bs4 import BeautifulSoup
import time

import csv


StockSymbol = input("Enter the stock symbol: ")
time.sleep(2)
driver = webdriver.Chrome()
# Navigate to the website
url = f"https://merolagani.com/CompanyDetail.aspx?symbol={StockSymbol}#0"
try:
    driver.get(url)
except:
    print("Invalid Stock Symbol")
    exit()

'''
Get the page source after the button click
'''
try:
    button = driver.find_element("xpath",
                                 '// *[@id= "ctl00_ContentPlaceHolder1_CompanyDetail1_lnkHistoryTab"]'
                                 )
    button.click()

    time.sleep(2)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    table = soup.find_all(
        'table', class_='table table-bordered table-striped table-hover')
except Exception as e:
    print(e)
    print("Data Not Found")
    exit()

headers = [i.text for i in table[0].find_all('th')]
# remove trailing newlines from headers
headers = [i.replace('\n', '') for i in headers]
print(headers)

data = [[i.text for i in row.find_all('td')]
        for row in table[0].find_all('tr')]
driver.quit()
print(" ......... Generating CSV File OF Company Data ............ ")
time.sleep(2)
try:
    with open(f'{StockSymbol}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)
        print("Done")
    file.close()
except Exception as e:
    print(e)
    print("Error in generating CSV file")

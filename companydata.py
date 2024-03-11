from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
import csv

StockSymbol = input("Enter the stock symbol: ")
time.sleep(2)
driver = webdriver.Chrome()
url = f"https://merolagani.com/CompanyDetail.aspx?symbol={StockSymbol}#0"
driver.get(url)
print (" ......... Fetching Data From Merolagani ............ ")

button = driver.find_element(By.XPATH,
    '//*[@id="ctl00_ContentPlaceHolder1_CompanyDetail1_lnkHistoryTab"]'
)
button.click()

time.sleep(2)

page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')
table = soup.find_all('table', class_='table table-bordered table-striped table-hover')

headers = [i.text.replace('\n', '') for i in table[0].find_all('th')]
print(headers)

data = [[i.text for i in row.find_all('td')] for row in table[0].find_all('tr')]

driver.quit()

print(" ......... Generating CSV File OF Company Data ............ ")
time.sleep(2)

try:
    with open(f'{StockSymbol}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)
        print("Done")
except Exception as e:
    print(e)
    print("Error in generating CSV file")


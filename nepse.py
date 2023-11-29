from bs4 import BeautifulSoup
import requests
# import lxml
import csv
# Site Url
URL = "https://merolagani.com/LatestMarket.aspx"

# make get request to fetch the raw html content
conn = requests.get(URL)
soup = BeautifulSoup(conn.text, 'lxml')

table = soup.find('table', class_='table table-hover live-trading sortable')

headers = [i.text for i in table.find_all('th')]

print(headers)
data = [j for j in table.find_all(
    'tr', {"class": ["decrease-row", "increase-row", "nochange-row"]})]

result = [{headers[index]: cell.text for index,
           cell in enumerate(row.find_all('td'))} for row in data]

# writing the data in CSV file with headers and their respective values
with open('nepse.csv', 'w') as f:
    try:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(result)
        print("CSV file created successfully and data written successfully")
    except Exception as e:
        print(e)

f.close()

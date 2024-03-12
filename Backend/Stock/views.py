
from django.shortcuts import render
from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import requests 
import pandas as pd 
import numpy as np
from tensorflow.keras.layers import LSTM
from .utils import preprocess_data, train_lstm_model
from .forms import UploadFileForm
import json
import csv
import time

def index(request):
 
    URL = "https://merolagani.com/LatestMarket.aspx"

    # Make GET request to fetch the raw HTML content
    conn = requests.get(URL)
    soup = BeautifulSoup(conn.text, 'html.parser')

    table = soup.find('table', class_='table table-hover live-trading sortable')

    headers = [i.text for i in table.find_all('th')]

    data = []
    for row in table.find_all('tr', {"class": ["decrease-row", "increase-row", "nochange-row"]}):
        row_data = {}
        cells = row.find_all('td')
        row_data['row_class'] = row['class'][0]  # Extracting row class for styling
        for index, cell in enumerate(cells):
            row_data[headers[index]] = cell.text
        data.append(row_data)

    return render(request, 'Stock/index.html', {'headers': headers, 'data': data})




def scrape_news(request):
    # URL of the webpage to scrape
    url = "https://merolagani.com/NewsList.aspx"
    
    # Fetch the HTML content of the webpage
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
    
        news_elements = soup.find_all("div", class_="media-news media-news-md clearfix")
        
        # Extract news titles, links, and images
        news_list = []
        for news in news_elements:
            title = news.find("h4", class_="media-title").text.strip()
            link = news.find("a")["href"]
            image = news.find("img")
            if image:
                image_url = image["src"]
            else:
                # If image is not available, provide a default image URL
                image_url = "https://via.placeholder.com/150"
            news_list.append({"title": title, "link": link, "image_url": image_url})
        
        # Pass the news list to the template for rendering
        context = {"news_list": news_list}
        return render(request, "Stock/news.html", context)
    else:
   
        return render(request, "Stock/error.html")


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            df = pd.read_csv(csv_file)
            df['Date'] = pd.to_datetime(df['Date'])
            df = df.set_index('Date')
            df = df.dropna()
            sequence_length = 10
            scaler, X_train, _, y_train, _ = preprocess_data(df, sequence_length)
            model = train_lstm_model(X_train, y_train)
            latest_data = df.tail(sequence_length)
            latest_scaled = scaler.transform(latest_data[['Open']])
            latest_scaled = np.array(latest_scaled).reshape((1, sequence_length, 1))
            tomorrow_prediction = model.predict(latest_scaled)
            tomorrow_prediction = scaler.inverse_transform(tomorrow_prediction)
            dates = df.index[-50:].strftime('%Y-%m-%d').tolist()
            actual_prices = df['Open'].values[-50:].tolist()
            predicted_prices = model.predict(X_train[-50:]).flatten().tolist()
            data = {
                'dates': dates,
                'actual_prices': actual_prices,
                'predicted_prices': predicted_prices,
                'tomorrow_prediction':float(tomorrow_prediction[0][0])
            }
            print (data.get('predicted_prices')[0])
            
            return render(request, 'Stock/prediction.html', {'data': json.dumps(data)})     
    else:
        form = UploadFileForm()
    return render(request, 'Stock/upload.html', {'form': form})


def download_data(request):
    if request.method == 'POST':
        StockSymbol = request.POST.get('stock_symbol')
        
        # Configure Chrome options for headless browsing
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Initialize Chrome WebDriver with configured options
        driver = webdriver.Chrome(options=chrome_options)
        
        # Visit the URL
        url = f"https://merolagani.com/CompanyDetail.aspx?symbol={StockSymbol.upper()}#0"  # Convert symbol to uppercase
        driver.get(url)
        print(" ......... Fetching Data From Merolagani ............ ")

        # Wait for the button to be clickable
        button = driver.find_element(By.XPATH,
            '//*[@id="ctl00_ContentPlaceHolder1_CompanyDetail1_lnkHistoryTab"]'
        )
        button.click()

        # Wait for some time to let the page load
        time.sleep(2)

        # Get page source and parse with BeautifulSoup
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        table = soup.find_all('table', class_='table table-bordered table-striped table-hover')

        # Extract headers and data from the table
        headers = [i.text.replace('\n', '') for i in table[0].find_all('th')]
        data = [[i.text for i in row.find_all('td')] for row in table[0].find_all('tr')]

        # Quit WebDriver
        driver.quit()

        print(" ......... Generating CSV File OF Company Data ............ ")

        # Write data to CSV file
        try:
            with open(f'{StockSymbol}.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                writer.writerows(data)
            print("Done")
            # Provide the CSV file for download
            with open(f'{StockSymbol}.csv', 'rb') as csvfile:
                response = HttpResponse(csvfile, content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename="{StockSymbol}.csv"'
                return response
        except Exception as e:
            print(e)
            return HttpResponse("Error in generating or downloading CSV file")
    else:
        return render(request, 'Stock/upload.html')
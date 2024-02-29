# views.py

from django.shortcuts import render
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

import matplotlib.pyplot as plt
from io import StringIO
import pickle
import joblib


from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

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
        
        # Parse the HTML content
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Find the elements containing news articles
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







def create_dataset(df_scaled, look_back=1):
    x_train = []
    y_train = []
    for i in range(len(df_scaled) - look_back):
        x_train.append(df_scaled[i:i + look_back])
        y_train.append(df_scaled[i + look_back])
    return x_train, y_train

def predict_stock(request):
    # Load the pickled model
    model = joblib.load('Model/lstm.joblib')
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        
        df = pd.read_csv(csv_file)
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.set_index('Date')
        df = df.dropna()
        
        # Preprocessing
        scaler = MinMaxScaler()
        df_scaled = scaler.fit_transform(df[['Open']])
        sequence_length = 10
        X, y = create_dataset(df_scaled, sequence_length)

        train_size = int(len(X) * 0.8)
        X_train, X_test = np.array(X[:train_size]), np.array(X[train_size:])
        y_train, y_test = np.array(y[:train_size]), np.array(y[train_size:])

        # Make predictions using the loaded model
        train_predictions = model.predict(X_train)
        test_predictions = model.predict(X_test)

        train_predictions = scaler.inverse_transform(train_predictions)
        y_train_original = scaler.inverse_transform(y_train.reshape(-1, 1))

        test_predictions = scaler.inverse_transform(test_predictions)
        y_test_original = scaler.inverse_transform(y_test.reshape(-1, 1))

        # Plotting
        plt.figure(figsize=(12, 6))
        plt.plot(df.index[sequence_length:sequence_length+len(y_train)], y_train_original, label='Actual Train Data')
        plt.plot(df.index[sequence_length:sequence_length+len(y_train)], train_predictions, label='Train Predictions')

        test_index = df.index[sequence_length + train_size:sequence_length + train_size + len(y_test)]
        plt.plot(test_index, y_test_original, label='Actual Test Data')
        plt.plot(test_index, test_predictions, label='Test Predictions')

        plt.title('Stock Price Prediction')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.savefig('predicted_plot.png')

        latest_data = df.tail(sequence_length)
        latest_scaled = scaler.transform(latest_data[['Open']])
        latest_scaled = np.array(latest_scaled).reshape((1, sequence_length, 1))
        tomorrow_prediction = model.predict(latest_scaled)
        tomorrow_prediction = scaler.inverse_transform(tomorrow_prediction)


        # Render the prediction result template
        return render(request, 'Stock/prediction_result.html', {'prediction': tomorrow_prediction[0, 0], 'plot_image': 'predicted_plot.png'})

    return render(request, 'Stock/upload_csv.html')
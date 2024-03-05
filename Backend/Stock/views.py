# views.py

from django.shortcuts import render
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import model_from_json
from tensorflow.keras.models import load_model

from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.models import Sequential
import matplotlib.pyplot as plt
from .utils import preprocess_data, train_lstm_model, plot_predictions
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup


from .forms import UploadFileForm



# json_file = open('Model/model.json', 'r')
# loaded_model_json = json_file.read()
# json_file.close()

# print("Loaded model from disk")
 
# evaluate loaded model on test data
# loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])



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



def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                csv_file = request.FILES['file']
                df = pd.read_csv(csv_file)
                df['Date'] = pd.to_datetime(df['Date'])
                df = df.set_index('Date')
                df = df.dropna()

                sequence_length = 10
                scaler, X_train, X_test, y_train, y_test = preprocess_data(df, sequence_length)
                model = train_lstm_model(X_train, y_train)

                train_predictions, test_predictions = model.predict(X_train), model.predict(X_test)
                train_predictions = scaler.inverse_transform(train_predictions)
                test_predictions = scaler.inverse_transform(test_predictions)

                plot_path = plot_predictions(df, sequence_length, train_predictions, test_predictions)

                latest_data = df.head(sequence_length)
                latest_scaled = scaler.transform(latest_data[['Open']])
                latest_scaled = np.array(latest_scaled).reshape((1, sequence_length, 1))
                tomorrow_prediction = model.predict(latest_scaled)
                tomorrow_prediction = scaler.inverse_transform(tomorrow_prediction)

                return render(request, 'Stock/prediction_result.html', {'predicted_price': tomorrow_prediction[0], 'plot_path': plot_path})

            except Exception as e:
                error_message = f"An error occurred: {str(e)}"
                return render(request, 'Stock/upload.html', {'form': form, 'error_message': error_message})
    else:
        form = UploadFileForm()
    return render(request, 'Stock/upload.html', {'form': form})
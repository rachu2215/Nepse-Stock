# views.py

from django.shortcuts import render
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import matplotlib.pyplot as plt
from io import StringIO

def create_dataset(df_scaled, look_back=1):
    x_train = []
    y_train = []
    for i in range(len(df_scaled) - look_back):
        x_train.append(df_scaled[i:i + look_back])
        y_train.append(df_scaled[i + look_back])
    return x_train, y_train

def predict_stock(request):
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

        # Split data into train and test sets
        train_size = int(len(X) * 0.8)
        X_train, X_test = np.array(X[:train_size]), np.array(X[train_size:])
        y_train, y_test = np.array(y[:train_size]), np.array(y[train_size:])

        # Model creation
        model = Sequential()
        model.add(LSTM(50, activation='sigmoid', return_sequences=True, input_shape=(sequence_length, 1)))
        model.add(LSTM(50, activation='sigmoid'))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')

        # Training
        model.fit(X_train, y_train, epochs=50, batch_size=32, verbose=0)

        # Make predictions
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

        # Plot testing data
        test_index = df.index[sequence_length + train_size:sequence_length + train_size + len(y_test)]
        plt.plot(test_index, y_test_original, label='Actual Test Data')
        plt.plot(test_index, test_predictions, label='Test Predictions')

        plt.title('Stock Price Prediction')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.savefig('predicted_plot.png')

        df = df.sort_index(ascending=False)

        # Scale the most recent data
        latest_data = df.head(sequence_length)
        latest_scaled = scaler.transform(latest_data[['Open']])

        # Reshape the scaled data
        latest_scaled = np.array(latest_scaled).reshape((1, sequence_length, 1))

        # Predict tomorrow's price
        tomorrow_prediction = model.predict(latest_scaled)
        tomorrow_prediction = scaler.inverse_transform(tomorrow_prediction)

        print("Tomorrow's predicted price:", tomorrow_prediction[0, 0])

        return render(request, 'Stock/prediction_result.html', {'prediction': tomorrow_prediction[0, 0]})

    return render(request, 'Stock/upload_csv.html')

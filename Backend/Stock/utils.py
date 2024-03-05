import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt

def preprocess_data(df, sequence_length):
    scaler = MinMaxScaler()
    df_scaled = scaler.fit_transform(df[['Open']])

    X, y = [], []
    for i in range(len(df_scaled) - sequence_length):
        X.append(df_scaled[i:i + sequence_length])
        y.append(df_scaled[i + sequence_length])
    X, y = np.array(X), np.array(y)

    train_size = int(len(X) * 0.8)
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]

    return scaler, X_train, X_test, y_train, y_test

def train_lstm_model(X_train, y_train):
    model = Sequential()
    model.add(LSTM(50, activation='sigmoid', return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(LSTM(50, activation='sigmoid'))
    model.add(Dense(1))
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
    model.fit(X_train, y_train, epochs=50, batch_size=32, verbose=2)
    return model

def plot_predictions(df, sequence_length, train_predictions, test_predictions):
    plt.figure(figsize=(12, 6))
    plt.plot(df.index[sequence_length:sequence_length + len(train_predictions)], train_predictions, label='Train Predictions')
    plt.plot(df.index[sequence_length + len(train_predictions):], test_predictions, label='Test Predictions')
    plt.plot(df['Open'], label='Actual Prices')
    plt.legend()
    plot_path = 'static/prediction_plot.png'
    plt.savefig(plot_path)
    plt.close()
    return plot_path

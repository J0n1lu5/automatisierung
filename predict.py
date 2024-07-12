import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

class LinearRegressionModel:
    def __init__(self, csv_path):
        self.data = pd.read_csv(csv_path).dropna()
        self.data = self.data.loc[:, ~self.data.columns.str.contains('^Unnamed')]  # Entferne Spalten, die mit 'Unnamed' beginnen
        self.model = LinearRegression()

    def train_model(self):
        y = self.data['final_weight_grams']
        X = self.data.drop(columns=['final_weight_grams'])
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(self.X_train, self.y_train)

    def get_training_results(self):
        coefficients = self.model.coef_
        intercept = self.model.intercept_
        train_mse, test_mse = self.calculate_mse()
        mse_df = self.calculate_feature_mse()
        return coefficients, intercept, train_mse, test_mse, mse_df

    def calculate_mse(self):
        y_pred_train = self.model.predict(self.X_train)
        y_pred_test = self.model.predict(self.X_test)
        train_mse = mean_squared_error(self.y_train, y_pred_train)
        test_mse = mean_squared_error(self.y_test, y_pred_test)
        return train_mse, test_mse

    def calculate_feature_mse(self):
        feature_mse = {}
        y = self.data['final_weight_grams']
        for column in self.data.columns.drop('final_weight_grams'):
            X = self.data[[column]]
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model = LinearRegression()
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            feature_mse[column] = mse
        mse_df = pd.DataFrame.from_dict(feature_mse, orient='index', columns=['MSE'])
        mse_df = mse_df.reset_index().rename(columns={'index': 'Feature'})
        return mse_df

    def predict_final_weight(self, second_csv_path):
        second_data = pd.read_csv(second_csv_path)
        second_data = second_data.loc[:, ~second_data.columns.str.contains('^Unnamed')]  # Entferne Spalten, die mit 'Unnamed' beginnen
        predictions = self.model.predict(second_data)
        self.second_data_with_predictions = second_data.copy()
        self.second_data_with_predictions['predicted_final_weight'] = predictions

    def save_predictions(self, matriculation_numbers):
        filename = f"reg_{'-'.join(matriculation_numbers)}.csv"
        self.second_data_with_predictions.to_csv(filename, index=False)
        return filename

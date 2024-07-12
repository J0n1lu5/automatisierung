import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

class LinearRegressionModel:
    def __init__(self, csv_path):
        self.data = pd.read_csv(csv_path).dropna()
        self.data = self.data.loc[:, ~self.data.columns.str.contains('^Unnamed')]
        self.model = None
        self.best_model_name = None
        self.best_model = None
        self.coefficients = None
        self.intercept = None

    def train_model(self):
        y = self.data['final_weight_grams']
        X = self.data.drop(columns=['final_weight_grams'])
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.evaluate_models()

    def evaluate_models(self):
        results = []
        y = self.data['final_weight_grams']
        X = self.data.drop(columns=['final_weight_grams'])
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        models = {
            'Linear': LinearRegression(),
            'Ridge': Ridge(),
            'SVR': SVR()
        }

        best_model_name = None
        best_test_mse = float('inf')

        for model_name, model in models.items():
            model.fit(X_train, y_train)
            y_pred_train = model.predict(X_train)
            y_pred_test = model.predict(X_test)
            train_mse = mean_squared_error(y_train, y_pred_train)
            test_mse = mean_squared_error(y_test, y_pred_test)
            results.append({
                'Modell-Typ': model_name,
                'MSE-Wert (Training)': train_mse,
                'MSE-Wert (Test)': test_mse
            })

            if test_mse < best_test_mse:
                best_test_mse = test_mse
                best_model_name = model_name
                self.best_model = model

        self.best_model_name = best_model_name
        self.coefficients = self.best_model.coef_ if hasattr(self.best_model, 'coef_') else None
        self.intercept = self.best_model.intercept_ if hasattr(self.best_model, 'intercept_') else None
        return results, best_model_name, best_test_mse

    def get_training_results(self):
        if self.best_model is None:
            raise ValueError("Model is not trained yet. Call train_model() first.")
        train_mse, test_mse = self.calculate_mse(self.best_model)
        mse_df = self.calculate_feature_mse()
        return train_mse, test_mse, mse_df

    def calculate_mse(self, model):
        y_pred_train = model.predict(self.X_train)
        y_pred_test = model.predict(self.X_test)
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
        if self.best_model is None:
            raise ValueError("Model is not trained yet. Call train_model() first.")
        second_data = pd.read_csv(second_csv_path)
        second_data = second_data.loc[:, ~second_data.columns.str.contains('^Unnamed')]
        predictions = self.best_model.predict(second_data)
        self.second_data_with_predictions = second_data.copy()
        self.second_data_with_predictions['predicted_final_weight'] = predictions

    def save_predictions(self, matriculation_numbers):
        filename = f"reg_{'-'.join(matriculation_numbers)}.csv"
        self.second_data_with_predictions.to_csv(filename, index=False)
        return filename

    def get_model_formula(self):
        if self.coefficients is None or self.intercept is None:
            raise ValueError("Model is not trained yet. Call train_model() first.")
        formula = "y = " + " + ".join([f"{coef}*x{i}" for i, coef in enumerate(self.coefficients, start=1)]) + f" + {self.intercept}"
        return formula

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from mqtt_client import MQTTClient
from database_storage import Database
from predict import LinearRegressionModel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd


class MainApp(tk.Tk):
    def __init__(self, db_path):
        super().__init__()
        self.title("Industrial IoT UI")
        self.geometry("800x600")
        self.configure(bg='#f0f0f0')

        self.db = Database(db_path)

        self.frames = {}
        self.mqtt_settings = {
            "broker": "158.180.44.197",
            "port": 1883,
            "topic": "iot1/teaching_factory_fast/#",
            "username": "bobm",
            "password": "letmein"
        }
        for F in (StartPage, MQTTConfigPage, PlotPage, PredictionPage):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if page_name == "PlotPage":
            frame.update_table_options()

    def update_mqtt_settings(self, broker, port, topic, username, password):
        self.mqtt_settings["broker"] = broker
        self.mqtt_settings["port"] = int(port)
        self.mqtt_settings["topic"] = topic
        self.mqtt_settings["username"] = username
        self.mqtt_settings["password"] = password

    def on_connection_lost(self):
        messagebox.showerror("MQTT Error", "Lost connection to the MQTT broker!")

    def on_timeout(self):
        messagebox.showerror("MQTT Timeout", "No messages received for 20 seconds!")

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='#f0f0f0')

        label = tk.Label(self, text="Willkommen! Wählen Sie eine Seite:", font=("Helvetica", 16), bg='#f0f0f0')
        label.pack(pady=20)

        # Create a container frame to hold the buttons
        button_container = tk.Frame(self, bg='#f0f0f0')
        button_container.pack(pady=20, fill="both", expand=True)

        buttons = [
            ("MQTT Config", "MQTTConfigPage"),
            ("Plot", "PlotPage"),
            ("Prediction", "PredictionPage")
        ]

        for i, (text, page) in enumerate(buttons):
            button = tk.Button(button_container, text=text, command=lambda p=page: controller.show_frame(p),
                               font=("Helvetica", 12), bg="#4CAF50", fg="white", activebackground="#45a049",
                               activeforeground="white", width=15, height=2)
            button.grid(row=i, column=0, pady=5, padx=5, sticky="w")

        # Toggle Button für Start/Stop Recording
        self.is_recording = False
        self.toggle_button = tk.Button(button_container, text="Start Recording", command=self.toggle_recording,
                                       font=("Helvetica", 12), bg="#4CAF50", fg="white", activebackground="#45a049",
                                       activeforeground="white", width=20, height=2)
        self.toggle_button.grid(row=0, column=1, pady=5, padx=5, sticky="e")

        # Compute recording button
        self.compute_button = tk.Button(button_container, text="Compute Data", command=self.compute,
                                        font=("Helvetica", 12),
                                        bg="#4CAF50", fg="white", activebackground="#45a049",
                                        activeforeground="white", width=20, height=2)
        self.compute_button.grid(row=1, column=1, pady=5, padx=5, sticky="e")

    def toggle_recording(self):
        self.is_recording = not self.is_recording
        if self.is_recording:
            self.toggle_button.config(text="Stop Recording", bg="#FF6347", activebackground="#FF4500")
            self.start_recording()
        else:
            self.toggle_button.config(text="Start Recording", bg="#4CAF50", activebackground="#45a049")
            self.stop_recording()

    def compute(self):
        print("Computing Data...")
        Format_data = Database('data.json')
        Format_data.format_data()

    def start_recording(self):
        broker = self.controller.mqtt_settings["broker"]
        port = self.controller.mqtt_settings["port"]
        topic = self.controller.mqtt_settings["topic"]
        username = self.controller.mqtt_settings["username"]
        password = self.controller.mqtt_settings["password"]
        self.mqtt_client = MQTTClient(broker, port, topic, username, password)
        self.mqtt_client.set_on_timeout_callback(self.controller.on_timeout)
        self.mqtt_client.client.on_disconnect = self.controller.on_connection_lost
        self.mqtt_thread = threading.Thread(target=self.mqtt_client.start)
        self.mqtt_thread.start()

    def stop_recording(self):
        if hasattr(self, 'mqtt_client'):
            self.mqtt_client.stop()
            self.mqtt_thread.join()


class MQTTConfigPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='#f0f0f0')
        label = tk.Label(self, text="MQTT Config", font=("Helvetica", 16), bg='#f0f0f0')
        label.pack(pady=20)

        # Frame für Eingabefelder
        entry_frame = tk.Frame(self, bg='#f0f0f0')
        entry_frame.pack(pady=20)

        tk.Label(entry_frame, text="Broker Address:", font=("Helvetica", 12), bg='#f0f0f0').grid(row=0, column=0,
                                                                                                 pady=5, sticky="e")
        self.broker_address_entry = tk.Entry(entry_frame, font=("Helvetica", 12), width=30)
        self.broker_address_entry.grid(row=0, column=1, pady=5)
        self.broker_address_entry.insert(0, controller.mqtt_settings["broker"])

        tk.Label(entry_frame, text="Port:", font=("Helvetica", 12), bg='#f0f0f0').grid(row=1, column=0, pady=5,
                                                                                       sticky="e")
        self.port_entry = tk.Entry(entry_frame, font=("Helvetica", 12), width=30)
        self.port_entry.grid(row=1, column=1, pady=5)
        self.port_entry.insert(0, controller.mqtt_settings["port"])

        tk.Label(entry_frame, text="Topic:", font=("Helvetica", 12), bg='#f0f0f0').grid(row=2, column=0, pady=5,
                                                                                        sticky="e")
        self.topic_entry = tk.Entry(entry_frame, font=("Helvetica", 12), width=30)
        self.topic_entry.grid(row=2, column=1, pady=5)
        self.topic_entry.insert(0, controller.mqtt_settings["topic"])

        tk.Label(entry_frame, text="Username:", font=("Helvetica", 12), bg='#f0f0f0').grid(row=3, column=0, pady=5,
                                                                                           sticky="e")
        self.username_entry = tk.Entry(entry_frame, font=("Helvetica", 12), width=30)
        self.username_entry.grid(row=3, column=1, pady=5)
        self.username_entry.insert(0, controller.mqtt_settings["username"])

        tk.Label(entry_frame, text="Password:", font=("Helvetica", 12), bg='#f0f0f0').grid(row=4, column=0, pady=5,
                                                                                           sticky="e")
        self.password_entry = tk.Entry(entry_frame, font=("Helvetica", 12), show='*', width=30)
        self.password_entry.grid(row=4, column=1, pady=5)
        self.password_entry.insert(0, controller.mqtt_settings["password"])

        # Submit button
        submit_button = tk.Button(entry_frame, text="Submit", command=self.submit, font=("Helvetica", 12),
                                  bg="#4CAF50", fg="white", activebackground="#45a049",
                                  activeforeground="white", width=20, height=2)
        submit_button.grid(row=5, column=0, columnspan=2, pady=10)

        button = tk.Button(self, text="Zurück zur Startseite", command=lambda: controller.show_frame("StartPage"),
                           font=("Helvetica", 12), bg="#4CAF50", fg="white", activebackground="#45a049",
                           activeforeground="white", width=20, height=2)
        button.pack(pady=10)

    def submit(self):
        broker_address = self.broker_address_entry.get()
        port = self.port_entry.get()
        topic = self.topic_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.controller.update_mqtt_settings(broker_address, port, topic, username, password)
        print(f"Updated MQTT settings: Broker Address: {broker_address}, Port: {port}, Topic: {topic}, Username: {username}, Password: {'*' * len(password)}")


class PlotPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='#f0f0f0')
        label = tk.Label(self, text="Plot", font=("Helvetica", 16), bg='#f0f0f0')
        label.pack(pady=20)

        self.canvas = None

        # Dropdown-Menü zur Auswahl der Tabelle und Spalten
        self.table_var = tk.StringVar(self)
        self.plot_type_var = tk.StringVar(self, value='line')
        self.num_values_var = tk.IntVar(value=50)

        table_label = tk.Label(self, text="Tabelle:", font=("Helvetica", 12), bg='#f0f0f0')
        table_label.pack(pady=5)
        self.table_menu = tk.OptionMenu(self, self.table_var, '')
        self.table_menu.pack(pady=5)

        plot_type_label = tk.Label(self, text="Diagrammtyp:", font=("Helvetica", 12), bg='#f0f0f0')
        plot_type_label.pack(pady=5)
        plot_type_options = ['line', 'bar', 'scatter']
        self.plot_type_menu = tk.OptionMenu(self, self.plot_type_var, *plot_type_options)
        self.plot_type_menu.pack(pady=5)

        num_values_label = tk.Label(self, text="Anzahl der letzten Werte:", font=("Helvetica", 12), bg='#f0f0f0')
        num_values_label.pack(pady=5)
        self.num_values_scale = tk.Scale(self, from_=1, to=500, orient="horizontal", variable=self.num_values_var)
        self.num_values_scale.pack(pady=5)

        plot_button = tk.Button(self, text="Plotten", command=self.plot, font=("Helvetica", 12), bg="#4CAF50",
                                fg="white", activebackground="#45a049", activeforeground="white", width=20, height=2)
        plot_button.pack(pady=10)

        back_button = tk.Button(self, text="Zurück zur Startseite", command=lambda: controller.show_frame("StartPage"),
                                font=("Helvetica", 12), bg="#4CAF50", fg="white", activebackground="#45a049",
                                activeforeground="white", width=20, height=2)
        back_button.pack(pady=10)

    def update_table_options(self):
        tables = self.controller.db.get_tables()
        menu = self.table_menu['menu']
        menu.delete(0, 'end')
        for table in tables:
            menu.add_command(label=table, command=lambda value=table: self.set_table(value))

    def set_table(self, table):
        self.table_var.set(table)

    def plot(self):
        table_name = self.table_var.get()
        plot_type = self.plot_type_var.get()
        num_values = self.num_values_var.get()

        df = self.controller.db.read_data(table_name)
        print(f"Columns in DataFrame: {df.columns.tolist()}")  # Debug statement to show columns

        # Ensure 'datetime' is in datetime format
        df['datetime'] = pd.to_datetime(df['datetime'])
        df = df.tail(num_values)

        fig, ax = plt.subplots(figsize=(6, 4))  # Change the figsize to your desired width and height

        if plot_type == 'line':
            ax.plot(df['datetime'], df['value'], marker='o')
        elif plot_type == 'bar':
            ax.bar(df['datetime'], df['value'])
        elif plot_type == 'scatter':
            ax.scatter(df['datetime'], df['value'])
        else:
            raise ValueError("Unsupported plot type. Choose from 'line', 'bar', or 'scatter'.")

        ax.set_title(f'{plot_type.capitalize()} Plot of Value vs Time in {table_name}')
        ax.set_xlabel('Time')
        ax.set_ylabel('Value')
        ax.grid(True)

        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        self.canvas = FigureCanvasTkAgg(fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(pady=20)


class PredictionPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='#f0f0f0')

        label = tk.Label(self, text="Prediction", font=("Helvetica", 16), bg='#f0f0f0')
        label.pack(pady=20)

        self.model = None
        self.csv_path = None
        self.second_csv_path = None

        self.upload_button = tk.Button(self, text="Upload Training CSV", command=self.upload_csv,
                                       font=("Helvetica", 12), bg="#4CAF50", fg="white", activebackground="#45a049",
                                       activeforeground="white", width=20, height=2)
        self.upload_button.pack(pady=10)

        self.train_button = tk.Button(self, text="Train Model", command=self.train_model, state='disabled',
                                      font=("Helvetica", 12), bg="#4CAF50", fg="white", activebackground="#45a049",
                                      activeforeground="white", width=20, height=2)
        self.train_button.pack(pady=10)

        self.result_label = tk.Label(self, text="", font=("Helvetica", 12), bg='#f0f0f0')
        self.result_label.pack(pady=10)

        self.upload_second_button = tk.Button(self, text="Upload Prediction CSV", command=self.upload_second_csv,
                                              state='disabled',
                                              font=("Helvetica", 12), bg="#4CAF50", fg="white",
                                              activebackground="#45a049",
                                              activeforeground="white", width=20, height=2)
        self.upload_second_button.pack(pady=10)

        self.predict_button = tk.Button(self, text="Predict Final Weight", command=self.predict_final_weight,
                                        state='disabled',
                                        font=("Helvetica", 12), bg="#4CAF50", fg="white", activebackground="#45a049",
                                        activeforeground="white", width=20, height=2)
        self.predict_button.pack(pady=10)

        self.save_button = tk.Button(self, text="Save Predictions", command=self.save_predictions, state='disabled',
                                     font=("Helvetica", 12), bg="#4CAF50", fg="white", activebackground="#45a049",
                                     activeforeground="white", width=20, height=2)

        self.save_button.pack(pady=10)

        self.mse_table_frame = tk.Frame(self, bg='#f0f0f0')
        self.mse_table_frame.pack(pady=10)

        self.best_model_label = tk.Label(self, text="", font=("Helvetica", 12), bg='#f0f0f0')
        self.best_model_label.pack(pady=10)

        self.model_formula_label = tk.Label(self, text="", font=("Helvetica", 12), bg='#f0f0f0')
        self.model_formula_label.pack(pady=10)

        button = tk.Button(self, text="Zurück zur Startseite", command=lambda: controller.show_frame("StartPage"),
                           font=("Helvetica", 12), bg="#4CAF50", fg="white", activebackground="#45a049",
                           activeforeground="white", width=20, height=2)
        button.pack(pady=10)

    def upload_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.csv_path = file_path
            self.model = LinearRegressionModel(self.csv_path)
            self.train_button.config(state='normal')
            self.result_label.config(text="Training CSV file uploaded successfully.")

    def train_model(self):
        if self.model:
            self.model.train_model()
            train_mse, test_mse, mse_df = self.model.get_training_results()

            self.result_label.config(
                text=f"Model trained successfully.\nTrain MSE: {train_mse}\nTest MSE: {test_mse}")
            self.save_button.config(state='normal')
            self.upload_second_button.config(state='normal')

            self.show_mse_table(mse_df)
            self.show_model_comparison_table()
            self.show_model_formula()

    def show_mse_table(self, mse_df):
        table_frame = tk.Frame(self, bg='#f0f0f0')
        table_frame.pack(pady=10)

        tree = ttk.Treeview(table_frame, columns=('Feature', 'MSE'), show='headings')
        tree.heading('Feature', text='Feature')
        tree.heading('MSE', text='MSE')

        for index, row in mse_df.iterrows():
            tree.insert('', tk.END, values=(row['Feature'], row['MSE']))

        tree.pack()

    def show_model_comparison_table(self):
        results, best_model_name, best_test_mse = self.model.evaluate_models()

        table_frame = tk.Frame(self.mse_table_frame, bg='#f0f0f0')
        table_frame.pack(pady=10)

        tree = ttk.Treeview(table_frame, columns=('Modell-Typ', 'MSE-Wert (Training)', 'MSE-Wert (Test)'), show='headings')
        tree.heading('Modell-Typ', text='Modell-Typ')
        tree.heading('MSE-Wert (Training)', text='MSE-Wert (Training)')
        tree.heading('MSE-Wert (Test)', text='MSE-Wert (Test)')

        for result in results:
            tree.insert('', tk.END, values=(result['Modell-Typ'], result['MSE-Wert (Training)'], result['MSE-Wert (Test)']))

        tree.pack()

        self.best_model_label.config(text=f"Best Model: {best_model_name} with Test MSE: {best_test_mse}")

    def show_model_formula(self):
        formula = self.model.get_model_formula()
        self.model_formula_label.config(text=f"Model Formula: {formula}")

    def upload_second_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.second_csv_path = file_path
            self.predict_button.config(state='normal')
            self.result_label.config(text="Prediction CSV file uploaded successfully.")

    def predict_final_weight(self):
        if self.model and self.second_csv_path:
            self.model.predict_final_weight(self.second_csv_path)
            self.result_label.config(text="Predictions made successfully.")
            self.save_button.config(state='normal')

    def save_predictions(self):
        if self.model:
            matriculation_numbers = self.get_matriculation_numbers()
            filename = self.model.save_predictions(matriculation_numbers)
            self.result_label.config(text=f"Predictions saved successfully as {filename}")

    def get_matriculation_numbers(self):
        # change later first its hardcoded
        return ['2110602034', '654321', '112233']


if __name__ == "__main__":
    app = MainApp('formatted_data.json')  # Specify the path to your database here
    app.mainloop()
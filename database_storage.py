import serializer
from tinydb import TinyDB
import pandas as pd
import os
import shutil


class Database:
    def __init__(self, db_path):
        self.db = TinyDB(db_path)

    def store_data(self, data, topic_name):
        # store data
        print(f"Storing data in topic {topic_name}: {data}")
        self.db.table(topic_name).insert(data)

    def read_data(self, table_name):
        # Read data for the specific table
        table = self.db.table(table_name)
        records = []
        for item in table.all():
            for key, value in item.items():
                datetime_str, data_value = value
                records.append({'datetime': datetime_str, 'value': data_value})

        df = pd.DataFrame(records)
        return df

    def get_tables(self):
        return self.db.tables()

    def format_data(self):
        if not os.path.exists('data'):
            os.makedirs('data')

        # for each table in the database create a csv file
        for table in self.db.tables():
            # create a dataframe
            df = pd.DataFrame(self.db.table(table).all())
            # save the dataframe to a csv file
            print(table)
            name = "data/" + "_".join(table.split("/")[-2:]) + ".csv"
            print("__")
            # print(df.head())
            df.to_csv(name, index=False)

        # load the csv files
        df_temperature = pd.read_csv("data/teaching_factory_fast_temperature.csv")
        df_vib_red = pd.read_csv("data/dispenser_red_vibration.csv")
        df_vib_green = pd.read_csv("data/dispenser_green_vibration.csv")
        df_vib_blue = pd.read_csv("data/dispenser_blue_vibration.csv")
        df_fill_red = pd.read_csv("data/teaching_factory_fast_dispenser_red.csv")
        df_fill_green = pd.read_csv("data/teaching_factory_fast_dispenser_green.csv")
        df_fill_blue = pd.read_csv("data/teaching_factory_fast_dispenser_blue.csv")
        df_final_weight = pd.read_csv("data/scale_final_weight.csv")

       #CSV for linear regression

        temperature = df_temperature["temperature_C"]
        vib_red = df_vib_red["vibration-index"]
        vib_green = df_vib_green["vibration-index"]
        vib_blue = df_vib_blue["vibration-index"]
        fill_red = df_fill_red["fill_level_grams"]
        fill_green = df_fill_green["fill_level_grams"]
        fill_blue = df_fill_blue["fill_level_grams"]
        final_weight = df_final_weight["final_weight"]

        formatted_data = pd.DataFrame({
            'temperature_mean_C': temperature,
            'vibration-index_red_vibration': vib_red,
            'vibration-index_green_vibration': vib_green,
            'vibration-index_blue_vibration': vib_blue,
            'fill_level_grams_red': fill_red,
            'fill_level_grams_green': fill_green,
            'fill_level_grams_blue': fill_blue,
            'final_weight_grams': final_weight
        })

        formatted_data.to_csv('formatted_data.csv', index=False)


       #everything for tinydb

        # Check if 'time' column exists in each dataframe
        def check_time_column(df, value_column):
            if 'time' not in df.columns:
                raise KeyError(f"'time' column not found in DataFrame for {value_column}")

        check_time_column(df_temperature, 'temperature_C')
        check_time_column(df_vib_red, 'vibration-index')
        check_time_column(df_vib_green, 'vibration-index')
        check_time_column(df_vib_blue, 'vibration-index')
        check_time_column(df_fill_red, 'fill_level_grams')
        check_time_column(df_fill_green, 'fill_level_grams')
        check_time_column(df_fill_blue, 'fill_level_grams')
        check_time_column(df_final_weight, 'final_weight')

        # Function to create tuples
        def create_tuples(df, value_column):
            df['time'] = pd.to_datetime(df['time'], unit='s')
            df['time'] = df['time'].astype(str)  # Convert time to string
            df[value_column] = list(zip(df['time'], df[value_column]))
            return df[[value_column]].to_dict(orient='records')

        temperature_records = create_tuples(df_temperature, 'temperature_C')
        vib_red_records = create_tuples(df_vib_red, 'vibration-index')
        vib_green_records = create_tuples(df_vib_green, 'vibration-index')
        vib_blue_records = create_tuples(df_vib_blue, 'vibration-index')
        fill_red_records = create_tuples(df_fill_red, 'fill_level_grams')
        fill_green_records = create_tuples(df_fill_green, 'fill_level_grams')
        fill_blue_records = create_tuples(df_fill_blue, 'fill_level_grams')
        final_weight_records = create_tuples(df_final_weight, 'final_weight')

        # Write the formatted data to a new TinyDB database
        new_db = TinyDB('formatted_data.json')

        new_db.table('temperature').insert_multiple(temperature_records)
        new_db.table('vibration_red').insert_multiple(vib_red_records)
        new_db.table('vibration_green').insert_multiple(vib_green_records)
        new_db.table('vibration_blue').insert_multiple(vib_blue_records)
        new_db.table('fill_red').insert_multiple(fill_red_records)
        new_db.table('fill_green').insert_multiple(fill_green_records)
        new_db.table('fill_blue').insert_multiple(fill_blue_records)
        new_db.table('final_weight').insert_multiple(final_weight_records)

        if os.path.exists('data/'):
            shutil.rmtree('data/')
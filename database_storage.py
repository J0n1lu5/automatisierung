import serializer
from tinydb import TinyDB
import pandas as pd
import os
import shutil

class Database:
    def __init__(self, db_path):
        self.db = TinyDB(db_path)


    def store_data(self, data,topic_name):
       #store data
       print(f"Storing data in topic {topic_name}: {data}")
       self.db.table(topic_name)
       self.db.table(topic_name).insert(data)
       

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

        temperature = df_temperature["temperature_C"]
        vib_red = df_vib_red["vibration-index"]
        vib_green = df_vib_green["vibration-index"]
        vib_blue = df_vib_blue["vibration-index"]
        fill_red = df_fill_red["fill_level_grams"]
        fill_green = df_fill_green["fill_level_grams"]
        fill_blue = df_fill_blue["fill_level_grams"]
        final_weight = df_final_weight["final_weight"]

        formatted_data = pd.DataFrame({
            'temperature_C': temperature,
            'vibration-index_red': vib_red,
            'vibration-index_green': vib_green,
            'vibration-index_blue': vib_blue,
            'fill_level_grams_red': fill_red,
            'fill_level_grams_green': fill_green,
            'fill_level_grams_blue': fill_blue,
            'final_weight_grams': final_weight
        })

        formatted_data.to_csv('formatted_data.csv', index=False)

        if os.path.exists('data/'):
            shutil.rmtree('data/')
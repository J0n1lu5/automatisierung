from tinydb import TinyDB, Query
import pandas as pd


class FormatData:
   def __init__ (self):
      self.db = TinyDB('data.json')

    def load_data(self):
for table in db.tables():
    # create a dataframe
    df = pd.DataFrame(db.table(table).all())
    # save the dataframe to a csv file
    print(table)
    name ="data/"+"_".join(table.split("/")[-2:])+".csv"
    print("__")
    #print(df.head())
    df.to_csv(name, index=False)

#load the csv files
df_temperature = pd.read_csv("data/teaching_factory_fast_temperature.csv")
df_vib_red = pd.read_csv("data/dispenser_red_vibration.csv")
df_vib_green = pd.read_csv("data/dispenser_green_vibration.csv")
df_vib_blue = pd.read_csv("data/dispenser_blue_vibration.csv")
df_fill_red = pd.read_csv("data/teaching_factory_fast_dispenser_red.csv")
df_fill_green = pd.read_csv("data/teaching_factory_fast_dispenser_green.csv")
df_fill_blue = pd.read_csv("data/teaching_factory_fast_dispenser_blue.csv")
df_final_weight = pd.read_csv("data/scale_final_weight.csv")
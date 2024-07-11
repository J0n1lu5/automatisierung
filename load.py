
from tinydb import TinyDB, Query
import pandas as pd
db = TinyDB('data.json')

# for each table in the database create a csv file
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


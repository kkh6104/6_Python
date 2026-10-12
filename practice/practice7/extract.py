
import os
import pandas as pd



def dir_file(name):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),"data", name)

def raw_bikes_df():
    return pd.read_csv(dir_file("raw-bikes.csv"), dtype=str, keep_default_na=False)

def raw_rentals_df():
    return pd.read_csv(dir_file("raw-rentals.csv"), dtype=str, keep_default_na=False)

def raw_stations_df():
    return pd.read_csv(dir_file("stations.csv"), dtype=str, keep_default_na=False)
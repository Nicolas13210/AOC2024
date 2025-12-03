import pandas as pd
import numpy as np

def exo1(file_path):
    df = pd.read_csv(file_path, sep="   ", header=None)
    df[0] = sorted(df[0])
    df[1] = sorted(df[1])
    df["distance"] = np.abs(df[0] - df[1])
    distance = df["distance"].sum()
    print(distance)

def get_distance(x,occurences):
    if x in occurences:
        return occurences[x] *x
    return 0

def exo2(file_path):
    df = pd.read_csv(file_path, sep="   ", header=None)
    df[0] = sorted(df[0])
    df[1] = sorted(df[1])
    occurences = df[1].value_counts()
    df["distance"] = df[0].apply(lambda x: get_distance(x,occurences))
    distance = df["distance"].sum()
    print(distance)
    


exo2("day1/input.txt")
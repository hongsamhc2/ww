import numpy as np
import tensorflow as tf
from tensorflow.python.client import device_lib
from tensorflow import keras
import pandas as pd
df = pd.read_csv('.\\DB\\CSV\\daily\\DA000020_ch.csv')


#data = df.iloc[0].values.reshape(1,-1)
def add_feature(df):
    windows = [5,10,20,60,120]
    for window in windows:
        df[f'close_ma{window}'] = df['close'].rolling(window).mean()
        df[f'volume_ma{window}'] = df['volume'].rolling(window).mean()
        df[f'close_ma_latio{window}'] = (df['close'] - df[f'close_ma{window}']) / df[f'close_ma{window}']
        df[f'volume_ma_latio{window}'] = (df['volume'] - df[f'volume_ma{window}']) / df[f'volume_ma{window}']
    data = df.iloc[-1]

    return data.values



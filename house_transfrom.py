import pandas as pd
import numpy as np

def transform_data(filepath):
    df = pd.read_csv(filepath)
    
    df = df[~df.duplicated()]
    df['Qiymet'] = pd.to_numeric(df['Qiymet'], errors='coerce')
    df['Tarix'] = pd.to_datetime(df['Tarix'], errors='coerce')
    df['Baxış'] = pd.to_numeric(df['Baxış'], errors='coerce')
    df['Mərtəbə'] = df['Mərtəbə'].apply(lambda x: x.replace('Mərtəbə', ''))
    
    # Split the 'Mərtəbə' column into two new columns
    df[['Ümumi Mərtəbə sayı', 'Mərtəbə']] = df['Mərtəbə'].str.split('/', expand=True)

    # Convert the new columns to numeric types if necessary
    df['Ümumi Mərtəbə sayı'] = pd.to_numeric(df['Ümumi Mərtəbə sayı'])
    df['Mərtəbə'] = pd.to_numeric(df['Mərtəbə'])
    df['Sahə'] = df['Sahə'].apply(lambda x: x.replace('m2', ''))
    df['Sahə'] = pd.to_numeric(df['Sahə'], errors='coerce')
    df['Otaq sayı'] = df['Otaq sayı'].apply(lambda x: x.replace('otaq', ''))
    df['Otaq sayı'] = pd.to_numeric(df['Otaq sayı'], errors='coerce')
    df['Çıxarış'] = df['Çıxarış'].replace({
        'Kupça': 'var',
        'Kupçasız': 'yox',
        'Çıxarış': np.nan
    })
    df['Adres1'] = df['Adres1'] + ' ' + df['Adres2']
    df = df.drop(columns=['Adres2'])
    df = df.rename(columns={'Adres1': 'Adres'})

    print(df.shape)
    print(df.columns)
    print(df.isnull().sum())

    return df

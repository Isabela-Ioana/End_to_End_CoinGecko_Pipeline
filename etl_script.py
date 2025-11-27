from datetime import datetime
import json
import requests
import time
import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
load_dotenv()

connection_string= f"postgresql://{os.getenv("db_user")}:{os.getenv("db_password")}@{os.getenv("db_host")}:{os.getenv("db_port")}/{os.getenv("db_database")}"

def load_api_key():
    with open("key.json") as f:
        key=json.load(f)
    return key["coingecko_api_key"]


def extract_crypto_data():
    api_key=load_api_key()
    url="https://api.coingecko.com/api/v3/coins/markets"
    headers={
        "x-cg-demo-api-key" : api_key
    }
    params={
        "vs_currency" : "usd",
        "order" : "market_cap_desc",
        "per_page" : 50
    }

    try:
        response= requests.get(url,headers=headers,params=params)
        if response.status_code!=200:
            raise Exception(f"API request failed with code: {response.status_code}")
        
        data= response.json()
        df=pd.DataFrame(data)
        df["etl_timestamp"]=datetime.now()  

        return df
   
    except Exception as e:
        print("ERROR on obtaining data!")
        return None


def transform_data(df):
    
    columns_to_keep=[
        "id","symbol","name","current_price","market_cap","total_volume",
        "price_change_24h", "price_change_percentage_24h", "last_updated",
        "etl_timestamp"
    ]

    df=df[columns_to_keep]
    columns_tobenumeric=["current_price","market_cap","total_volume",
       "price_change_24h", "price_change_percentage_24h"]
    for col in columns_tobenumeric:
        df.loc[:,col]=pd.to_numeric(df[col],errors="coerce")

    columns_tobedate=["last_updated", "etl_timestamp"]
    for col in columns_tobedate:
        df.loc[:,col]=pd.to_datetime(df[col],errors="coerce")

    columns_tobepositive=["current_price", "market_cap", "total_volume"]
    for col in columns_tobepositive:
        if (df[col]<0).any():
            raise ValueError(f"Column {col} has negative value/s!")
    
    if df.duplicated(subset=["id"]).any():
        raise ValueError("Duplicate IDs have been found!")



    df = df.dropna(subset=["id", "symbol", "current_price"])

    return df
     


def load_to_postgres(df):
    if df is None or df.empty:
        print("No data to upload")
    
    try:
        engine=create_engine(connection_string)
        with engine.connect() as connection:
            df.to_sql('crypto_prices',con=connection,if_exists='append',index=False)

        print(f"Imported {len(df)} lines in the database!")

    except Exception as e:
        print(f"Error {e} for data base")

if __name__=="__main__":

    print("----- ETL started ----- ")
    
    while True:

        try:
            print(f"\n {datetime.now().strftime('%H:%M:%S')} ---New uploadings--- ")

            df_extracted=extract_crypto_data()
            if df_extracted is not None:
                df_cleaned= transform_data(df_extracted)
                load_to_postgres(df_cleaned)



            
            print(" Upload done! ")
            print(" Sleeping for 60 seconds ")
            time.sleep(60)
        
        except KeyboardInterrupt:
            print("You pressed stop.")
            break

        except Exception as e:
            print(f"Unexpected error {e}")
            time.sleep(60)
        

  
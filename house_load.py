import pandas as pd
from sqlalchemy import create_engine

def load_data_to_postgresql(filepath, db_url, table_name):
    try:
        # Load the transformed data from CSV
        df = pd.read_csv(filepath)
        
        # Create a SQLAlchemy engine
        engine = create_engine(db_url)
        
        # Load data into PostgreSQL table
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Data successfully loaded into {table_name} table.")
    except Exception as e:
        print(f"Error loading data to PostgreSQL: {e}")

# Example usage
if __name__ == "__main__":
    filepath = '/mnt/c/Users/Nurhan/Desktop/house_airflow/extracted_data2.csv'
    db_url = 'postgresql+psycopg2://etl_airflow:etl_house_data@localhost:5432/house_data'
    table_name = 'house_data'
    load_data_to_postgresql(filepath, db_url, table_name)

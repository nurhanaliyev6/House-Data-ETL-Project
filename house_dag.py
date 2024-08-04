from airflow import DAG 
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from house_extract import *
from house_transfrom import transform_data
from house_load import load_data_to_postgresql

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'scrape_yeniemlak',
    default_args=default_args,
    description='A simple web scraping DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 7, 28),
    catchup=False,
)

# Define the tasks
def scrape_links_task(**context):
    base_url = 'https://yeniemlak.az'
    pages = get_all_pages()
    links = scrape_links(pages, base_url)
    context['ti'].xcom_push(key='links', value=links)

def get_information_task(**context):
    links = context['ti'].xcom_pull(key='links', task_ids='scrape_links_task')
    data = get_information(links)
    context['ti'].xcom_push(key='data', value=data)

def save_data_task(**context):
    data = context['ti'].xcom_pull(key='data', task_ids='get_information_task')
    # Use an absolute path
    filepath = '/mnt/c/Users/Nurhan/Desktop/house_airflow/extracted_data2.csv'
    save_data(data, filepath)

def transform_data_task(**context):

    #filepath = context['ti'].xcom_pull(key='filepath', task_ids='save_data_task')
    #print('Main filepath is',filepath)

    filepath2='/mnt/c/Users/Nurhan/Desktop/house_airflow/extracted_data2.csv'
    #if filepath is not None:
     #   transformed_df = transform_data(filepath)
      #  transformed_df.to_csv(filepath, index=False)
       # print("Data transformed filepath1 and saved to 'extracted_data2.csv'")
    if filepath2 is not None:
        transformed_df = transform_data(filepath2)
        transformed_df.to_csv(filepath2, index=False)
        print("Filepath2 worked and saved to 'extracted_data2.csv'")
    else:
        print("Invalid file path received. Data transformation skipped.")



def load_data_to_postgresql_task(**context):
    filepath = '/mnt/c/Users/Nurhan/Desktop/house_airflow/extracted_data2.csv'
    db_url = 'postgresql+psycopg2://etl_airflow:etl_airflow@localhost:5432/house_data'  # Update with your details
    table_name = 'house_data'
    if filepath is not None:
        load_data_to_postgresql(filepath, db_url, table_name)
        print('Done, It is loaded')
    else:
        print("No filepath provided. Data loading skipped.")





scrape_links_op = PythonOperator(
    task_id='scrape_links_task',
    python_callable=scrape_links_task,
    provide_context=True,
    dag=dag,
)

get_information_op = PythonOperator(
    task_id='get_information_task',
    python_callable=get_information_task,
    provide_context=True,
    dag=dag,
)

save_data_op = PythonOperator(
    task_id='save_data_task',
    python_callable=save_data_task,
    provide_context=True,
    dag=dag,
)

transform_data_op = PythonOperator(
    task_id='transform_data_task',
    python_callable=transform_data_task,
    provide_context=True,
    dag=dag,
)

load_data_op = PythonOperator(
    task_id='load_data_to_postgresql_task',
    python_callable=load_data_to_postgresql_task,
    provide_context=True,
    dag=dag,
)

# Set task dependencies
scrape_links_op >> get_information_op >> save_data_op >> transform_data_op >> load_data_op


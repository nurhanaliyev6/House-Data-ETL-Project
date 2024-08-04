
![Screenshot (421)](https://github.com/user-attachments/assets/f7b64abe-df0c-441d-89d9-7b9d6c970c5f)


# House-Data-ETL-Project

This project is an ETL (Extract, Transform, Load) pipeline for scraping, transforming, and loading house data into a PostgreSQL database using Apache Airflow. The project aims to demonstrate data engineering concepts such as web scraping, data transformation, and workflow orchestration.

Table of Contents
1.Project Overview
2. Architecture
3. Setup and Installation
4. Airflow DAGs
5. Database Schema
6. Usage
7. Notes

## Project Overview
This project scrapes house data from the [web](https://yeniemlak.az/) (Only houses of Sumgait), transforms it to a usable format, and loads it into a PostgreSQL database. The entire process is orchestrated using Apache Airflow. Note: Whole process is done for educational process.

## Architecture
Scraping: The project uses requests and BeautifulSoup to scrape house data from a website.
Transformation: The scraped data is cleaned and transformed using pandas.
Loading: The transformed data is loaded into a PostgreSQL database using SQLAlchemy.
Orchestration: Apache Airflow orchestrates the entire ETL process through a series of DAGs (Directed Acyclic Graphs).

## Setup and Installation
### Prerequisites
Python 3.8+
PostgreSQL
Apache Airflow

## Installation Steps
Clone the Repository
git clone https://github.com/nurhanaliyev6/House-Data-ETL-Project.git
cd House-Data-ETL-Project

Create a Virtual Environment
python -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`

Install Dependencies
pip install -r requirements.txt

Set Up Airflow
airflow db init
airflow users create \
    --username admin \
    --password admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com

Set Up PostgreSQL
CREATE DATABASE house_data;
CREATE USER etl_airflow WITH ENCRYPTED PASSWORD 'etl_house_data';
GRANT ALL PRIVILEGES ON DATABASE house_data TO etl_airflow;


Configure Airflow Connections
Add the PostgreSQL connection in the Airflow UI under Admin > Connections:  (or you can handle in .cfg file)

Conn Id: postgres_default
Conn Type: Postgres
Host: localhost
Schema: house_data
Login: etl_airflow
Password: etl_house_data
Port: 5432

## Airflow DAGs
The Airflow DAGs are defined in the dags/ directory. The main DAG files are:
house_dag.py: Orchestrates below files. extracting, transform, and loading.
house_extract.py: Manages the scraping from https://yeniemlak.az/.
house_transfrom.py : Handles the data transformation process.
house_load.py: Manages the data loading into PostgreSQL.

## Database Schema
The database schema for the house data is as follows:

Table: house_data
Qiymet: Numeric
Tarix: Timestamp
Baxış: Numeric
Elan: Text
Emlak: Text
Kateqoriya: Text
Mərtəbə: Numeric
Sahə: Numeric
Otaq sayı: Numeric
Çıxarış: Text
İpoteka: Text
Adres: Text
Ümumi Mərtəbə sayı: Numeric

## Usage
Start Airflow Scheduler and Web Server
airflow scheduler -D
airflow webserver -D

Trigger the DAGs
Go to the Airflow UI (http://localhost:8080) and trigger the DAGs in the following order:
scrape_links_op >> get_information_op >> save_data_op >> transform_data_op >> load_data_op

Verify Data in PostgreSQL

psql -U etl_airflow -d house_data

Connect to your PostgreSQL database and verify the data is loaded correctly:
SELECT * FROM house_data;

## Notes
Handling 429 Status Code:
When making too many requests to the website, we might encounter a 429 status code, which means "Too Many Requests". To handle this, consider implementing a delay between requests which also has bad effects. I have added time.sleep(2) which is 2 seconds delay when extracting information from a link. I have scraped 100 pages and each page contains 50 houses.For a page it take 50 *2 s= 100 second. And 100 pages * 100 s= 10000 s / 3600 s + plus additional computation= 2 h 40 m roughly 3 hr. So it finishes this process in 3 hr.

PS: Purpose of this project is to show big picture of etl design and orchestrating with airflow.














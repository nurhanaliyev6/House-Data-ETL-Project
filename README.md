


# House-Data-ETL-Project

![Screenshot (421)](https://github.com/user-attachments/assets/f7b64abe-df0c-441d-89d9-7b9d6c970c5f)

This project is an ETL (Extract, Transform, Load) pipeline for scraping, transforming, and loading house data into a PostgreSQL database using Apache Airflow. The project aims to demonstrate data engineering concepts such as web scraping, data transformation, and workflow orchestration.

# Table of Contents
1.Project Overview <br>
2. Architecture <br>
3. Setup and Installation <br>
4. Airflow DAGs <br>
5. Database Schema <br>
6. Usage <br>
7. Notes <br>

## Project Overview
This project scrapes house data from the [yeniemlak](https://yeniemlak.az/) (Only houses of Sumgait), transforms it to a usable format, and loads it into a PostgreSQL database. The entire process is orchestrated using Apache Airflow. Note: Whole process is done for educational process.

## Architecture
Scraping: The project uses requests and BeautifulSoup to scrape house data from a website. <br>
Transformation: The scraped data is cleaned and transformed using pandas. <br>
Loading: The transformed data is loaded into a PostgreSQL database using SQLAlchemy. <br>
Orchestration: Apache Airflow orchestrates the entire ETL process through a series of DAGs (Directed Acyclic Graphs). 

## Setup and Installation 
### Prerequisites
Python 3.8+ <br>
PostgreSQL <br>
Apache Airflow <br>

## Installation Steps
Clone the Repository <br>
`git clone https://github.com/nurhanaliyev6/House-Data-ETL-Project.git` <br>
`cd House-Data-ETL-Project` <br>

Create a Virtual Environment <br>
`python -m venv venv` <br>
`source venv/bin/activate `   # On Windows use `venv\Scripts\activate` <br>

Install Dependencies <br>
`pip install -r requirements.txt` <br>

Set Up Airflow <br>
`airflow db init`<br>
`airflow users create \ <br>
    --username admin \ <br>
    --password admin \ <br>
    --firstname Admin \ <br>
    --lastname User \ <br>
    --role Admin \ <br>
    --email admin@example.com` <br>
<br>
Set Up PostgreSQL <br>
`CREATE DATABASE house_data; ` <br>
`CREATE USER etl_airflow WITH ENCRYPTED PASSWORD 'etl_house_data';` <br>
`GRANT ALL PRIVILEGES ON DATABASE house_data TO etl_airflow;` <br>


Configure Airflow Connections <br>
Add the PostgreSQL connection in the Airflow UI under Admin > Connections:  (or you can handle in .cfg file) <br>

Conn Id: postgres_default <br>
Conn Type: Postgres <br>
Host: localhost <br>
Schema: house_data <br>
Login: etl_airflow <br>
Password: etl_house_data <br>
Port: 5432 <br>

## Airflow DAGs <br>
The Airflow DAGs are defined in the dags/ directory. The main DAG files are: <br>
house_dag.py: Orchestrates below files. extracting, transform, and loading. <br>
house_extract.py: Manages the scraping from https://yeniemlak.az/. <br>
house_transfrom.py : Handles the data transformation process. <br>
house_load.py: Manages the data loading into PostgreSQL. <br>

## Database Schema <br>
The database schema for the house data is as follows: <br>

Table: house_data <br>
Qiymet: Numeric <br>
Tarix: Timestamp <br> 
Baxış: Numeric <br>
Elan: Text <br>
Emlak: Text <br> 
Kateqoriya: Text <br>
Mərtəbə: Numeric <br>
Sahə: Numeric <br>
Otaq sayı: Numeric <br>
Çıxarış: Text <br>
İpoteka: Text <br>
Adres: Text <br>
Ümumi Mərtəbə sayı: Numeric <br>

## Usage <br>
Start Airflow Scheduler and Web Server <br>
`airflow scheduler -D` <br>
`airflow webserver -p 8080` <br>

Trigger the DAGs <br>
Go to the Airflow UI (http://localhost:8080) and trigger the DAGs in the following order: <br>
scrape_links_op >> get_information_op >> save_data_op >> transform_data_op >> load_data_op

Verify Data in PostgreSQL <br>

`psql -U etl_airflow -d house_data` <br>

Connect to your PostgreSQL database and verify the data is loaded correctly: <br>
`SELECT * FROM house_data;` <br>

## Notes <br>
Handling 429 Status Code:
When making too many requests to the website, we might encounter a 429 status code, which means "Too Many Requests". To handle this, consider implementing a delay between requests which also has bad effects. I have added time.sleep(2) which is 2 seconds delay when extracting information from a link. I have scraped 139 pages and each page contains 25 houses.For a page it take 25 *2 s= 50 second. And 139 pages * 50 s= 6950 s / 3600 s + plus additional computation= 2 h 20 roughly.
<br>
PS: Purpose of this project is to show big picture of etl design and orchestrating with airflow.














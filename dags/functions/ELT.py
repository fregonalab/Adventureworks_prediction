from airflow.providers.postgres.hooks.postgres import PostgresHook
import csv
import pandas as pd

def extract():
    hook = PostgresHook(postgres_conn_id="Adventureworks", schema = "Adventureworks")
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sales.salesorderdetail")
    with open("dags/data/get_orders.txt", "w") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)
    cursor.close()
    conn.close()

def load():
    read_txt = pd.read_csv('dags/data/get_orders.txt')
    read_txt.to_csv('dags/data/load_orders.csv', index=None)

def transform():
    df = pd.read_csv('dags/data/load_orders.csv')
    df.drop(['salesorderid','salesorderdetailid', 'carriertrackingnumber', 'specialofferid', 'rowguid', 'unitpricediscount'], axis = 1, inplace=True)
    df.to_csv('dags/data/orders.csv')
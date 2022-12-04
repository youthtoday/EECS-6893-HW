from datetime import datetime as dt, timedelta
import datetime
import yfinance as yf
from airflow import DAG
from airflow.operators.python import PythonOperator
from sklearn import linear_model
import csv

####################################################
# DEFINE PYTHON FUNCTIONS
####################################################
aapl_err = 0
googl_err = 0
meta_err = 0
msft_err = 0
amzn_err = 0
work_day = True
today = datetime.date.today()

def predict_high(stock_name, today):
    stock = yf.Ticker(stock_name)
    data = stock.history(start=today+datetime.timedelta(days=-30), end=today, interval="1d")
    size = data.shape[0]
    data_x = data.iloc[size-11:size-1, 0:4]
    data_y = data.iloc[size-10:size, 1]
    regr = linear_model.LinearRegression()
    regr.fit(data_x, data_y)
    test_x = [data.iloc[size-1, 0:4]]
    pred = regr.predict(test_x)
    return pred


def get_error(stock_name, today):
    pred = predict_high(stock_name, today)
    stock = yf.Ticker(stock_name)
    data = stock.history(start=today + datetime.timedelta(days=-30), end=today, interval="1d")
    size = data.shape[0]
    gt = data.iloc[size - 1, 2]
    error = (pred[0] - gt) / gt
    return error

def is_workday():
    global work_day
    if yf.Ticker('aapl').history(start=today + datetime.timedelta(days=-1), end=today, interval="1d").empty:
        work_day = False

def process(**kwargs):
    stock_name = kwargs['key']
    if stock_name == "aapl":
        global aapl_err
        aapl_err = get_error(stock_name, today)
    elif stock_name == "googl":
        global googl_err
        googl_err = get_error(stock_name, today)
    elif stock_name == "meta":
        global meta_err
        meta_err = get_error(stock_name, today)
    elif stock_name == "msft":
        global msft_err
        msft_err = get_error(stock_name, today)
    else:
        global amzn_err
        amzn_err = get_error(stock_name, today)


def write_to_csv():
    errors = [today + datetime.timedelta(days=-1), aapl_err, googl_err, meta_err, msft_err, amzn_err]
    with open('text.csv', mode='a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(errors)

############################################
# DEFINE AIRFLOW DAG (SETTINGS + SCHEDULE)
############################################

default_args = {
    'owner': 'lijie',
    'depends_on_past': False,
    'email': ['lh3158@columbia.edu'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=30),
}

with DAG(
        'stock_airflow',
        default_args=default_args,
        description='A simple toy DAG',
        schedule_interval=timedelta(days=1),
        start_date=dt(2021, 1, 1, 7, 0),
        catchup=False,
        tags=['example'],
) as dag:
    ##########################################
    # DEFINE AIRFLOW OPERATORS
    ##########################################

    begin = PythonOperator(
        task_id='work_day',
        python_callable=is_workday,
    )

    task1 = PythonOperator(
        task_id='aapl',
        python_callable=process,
        op_kwargs={'key': 'aapl'},
    )

    task2 = PythonOperator(
        task_id='googl',
        python_callable=process,
        op_kwargs={'key': 'googl'},
    )

    task3 = PythonOperator(
        task_id='meta',
        python_callable=process,
        op_kwargs={'key': 'meta'},
    )

    task4 = PythonOperator(
        task_id='msft',
        python_callable=process,
        op_kwargs={'key': 'msft'},
    )

    task5 = PythonOperator(
        task_id='amzn',
        python_callable=process,
        op_kwargs={'key': 'amzn'},
    )

    task6 = PythonOperator(
        task_id='write_csv',
        python_callable=write_to_csv,
    )

    ##########################################
    # DEFINE TASKS HIERARCHY
    ##########################################
    # task dependencies

    begin >> [task1, task2, task3, task4, task5]
    [task1, task2, task3, task4, task5] >> task6


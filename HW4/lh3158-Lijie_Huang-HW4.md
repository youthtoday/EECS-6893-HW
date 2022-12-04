# EECS 6893 Big Data Analytics HW4 <br>Data Analytics Pipeline

> Nov 29th, 2022
> Lijie Huang
> lh3158

## Task 1 Helloworld
### Q1.1 
Read through the tutorial slides and install Airflow either on your local laptop or on a VM of GCP. You can also use google cloud composer if you know how to use that.
#### (1) 
Provide screenshots of terminals after you successfully start the webserver and scheduler.

![](https://tva1.sinaimg.cn/large/008vxvgGgy1h8ihjgivn8j31do0pw46l.jpg)

![](https://tva1.sinaimg.cn/large/008vxvgGgy1h8ihn8xh5kj318n0u0alc.jpg)

#### (2) 
Provide screenshots of the web browser after you successfully login and see the DAGs.
![](https://tva1.sinaimg.cn/large/008vxvgGgy1h8ihoegid2j31970u0q70.jpg)
### Q1.2 
Run helloworld with SequentialExecutor and LocalExecutor.
#### (1) 
Provide screenshots of Tree, Graph, and Gantt of each executor. 

*Answer:*
For SequentialExecutor
![](https://tva1.sinaimg.cn/large/008vxvgGgy1h8j8i7i3rdj327g0rgjum.jpg)

![](https://tva1.sinaimg.cn/large/008vxvgGgy1h8j8ioe8jqj31y60u0wiq.jpg)

![](https://tva1.sinaimg.cn/large/008vxvgGgy1h8j8iyd752j327a0qmgou.jpg)

For LocalExecutor
![](https://tva1.sinaimg.cn/large/008vxvgGgy1h8j8yzppkvj327c0p00vl.jpg)

![](https://tva1.sinaimg.cn/large/008vxvgGgy1h8j8zam2e7j32740tg0x3.jpg)

![](https://tva1.sinaimg.cn/large/008vxvgGgy1h8j8zjc3pxj32760majui.jpg)

#### (2) 
Explore other features and visualizations you can find in the Airflow UI. Choose two features/visualizations (other than tree, graph, and Gantt), explain their functions and how they help monitor and troubleshoot the pipeline, use helloword as an example.

*Answer:*
**Task Duration**: The duration of your different tasks over the past N runs. This view lets you find outliers and quickly understand where the time is spent in your DAG over many runs. For example, in helloworld case, I can see t2_2 spend the most time to execute.
![](https://tva1.sinaimg.cn/large/008vxvgGgy1h8j93zxctwj31v50u00tu.jpg)

**DAG Details**: It helps you to know the real time details about the program, including max active runs, concurrency and tasks count. For example, in helloworld case, I can see the concurrency is 16 and the total tasks are 7. All tasks are successfully finished.
![](https://tva1.sinaimg.cn/large/008vxvgGgy1h8j97seqomj31270u0ac3.jpg)

## Task 2 Build workflows
### Q2.1
Implement the DAG below
![](https://tva1.sinaimg.cn/large/008vxvgGgy1h8ica6v7hsj31a60negna.jpg)
For each kind of operator, use at least 3 different commands. For example, you can choose sleep, print, count functions for Python operators, and echo, run bash script, run python file for Bash operators.
#### (1) 
Provide screenshots of Tree and Graph in airflow. (10 pts)

![](https://tva1.sinaimg.cn/large/008vxvgGgy1h8jbx6qiz8j31v90u076o.jpg)

![](https://tva1.sinaimg.cn/large/008vxvgGgy1h8jasgakppj31ws0ra41g.jpg)

#### (2) 
Manually trigger the DAG, and provide screenshots of Gantt. (10 pts)

![](https://tva1.sinaimg.cn/large/008vxvgGgy1h8jau54jwaj31tu0u0wgk.jpg)

#### (3) 
Schedule the first run immediately and running the program every 30 minutes. Describe how you decide the start date and schedule interval. Provide screenshots of running history after two repeats (first run + 2 repeats). On your browser, you can find the running history. (5 pts)

*Answer:*
The scheduler runs the job one 'schedule_interval' AFTER the start date, at the END of the period. So I set the param 'start_date' to datetime(2021, 1, 1), which means the job starts immediately. Another param 'schedule_interval' determins the period betwin two repeating jobs. So I set 'schedule_interval' to 30 minitues as timedelta(minutes=30).
![](https://tva1.sinaimg.cn/large/008vxvgGgy1h8jfzh2mjhj324y0mq78r.jpg)

### Q2.2 
Stock price fetching, prediction, and storage every day (25 pts)
(1) Schedule fetching the stock price of [AAPL, GOOGL, FB, MSFT, AMZN] at 7:00 AM every day. Use Yahoo! Finance data downloader https://pypi.org/project/yfinance/.
(2) Preprocess data if you think necessary.
(3) Train/update 5 linear regression models for stock price prediction for these 5 corporates. Each linear model takes the “open price”, “high price”, “low price”, “close price”, “volume” of the corporate in the past ten days as the features and predicts the “high price” for the next day.
(4) Every day if you get new data, calculate the relative errors, i.e., (prediction yesterday - actual price today) / actual price today, and update the date today and 5 errors into a table, e.g., a csv file.
(5) Provide screenshots of your code. Describe briefly how to build this workflow, e.g., what the DAG is, how you manage the cross tasks communication, how you setup scheduler…

*Answer:*

```python
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
```
Generated csv file so far.
![](https://tva1.sinaimg.cn/large/008vxvgGgy1h8n270sne6j31ja070tcl.jpg)

Firstly, task "begin" decides whether yesterday is a valid work day with trading data. If yesterday is not a work day, the global variable "work_day" would be changed to False. After task "begin" finishes, task1 to task5 would start simutaniously, calculating the prediction and the error between prediction and ground true of 5 company respectively. Each task's query stock is decided by the passing parameters. After the error of each company's stock is calculated, the error would be written into corresponding global variables. After all 5 tasks finishes, the last task would collect 5 error variables and write them into the csv file if the "work_day" is True.

To make the job run at 7 am every morning, I make the settings be schedule_interval = timedelta(days=1) and start_date = datetime(2021, 1, 1, 7, 0).
![](https://tva1.sinaimg.cn/large/008vxvgGgy1h8n2duvej7j30lm0kmq3h.jpg)

## Task 3 Written parts (15 pts)
### Q3.1 
Answer the question (5 pts)
#### (1) 
What are the pros and cons of SequentialExecutor, LocalExecutor, CeleryExecutor, KubernetesExecutor? (10%)

*Answer:*
*SequentialExecutor*

+ Pros
	- It's simple and straightforward to set up.
	- It's a good way to test DAGs while they're being developed.
+ Cons
	- It isn't scalable.
	- It is not possible to perform many tasks at the same time.
	- Unsuitable for use in production

*LocalExecutor*
+ Pros
	- It's straightforward and easy to set up.
	- It's cheap and resource light.
	- It still offers parallelism.
+ Cons
	- It's less scalable.
	- It's dependent on a single point of failure.

*CeleryExecutor*
- Pros
	- High availability
	- Built for horizontal scaling
	- Worker Termination Grace Period
- Cons
	- It's pricier
	- It takes some work to set up
	- Worker maintenance

*KubernetesExecutor*

- Pros
	- Cost and resource efficient
	- Fault tolerant
	- Task-level configurations
	- No interruption to running tasks if a deploy is pushed
- Cons
	- Kubernetes familiarity as a potential barrier to entry
	- An overhead of a few extra seconds per task for a pod to spin up

### Q3.2 
Draw the DAG of your group project (10 pts)
(1) Formulate it into at least 5 tasks
(2) Task names (functions) and their dependencies
(3) How do you schedule your tasks?

*Answer:*

![](https://tva1.sinaimg.cn/large/008vxvgGgy1h8n3u633ghj31mq0rw420.jpg)

We use a fixed dataset, so the airflow job only needs to execute once. The dependencies of the tasks are shown in the picture above.
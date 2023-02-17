import os
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup
from datetime import datetime
from random import randint
from airflow.operators.email_operator import EmailOperator
from airflow.hooks.postgres_hook import PostgresHook
from datetime import timedelta
from StartDjangoServerOperator import StartDjangoServerOperator

import numpy as np
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
import pandas as pd
import matplotlib.pyplot as plt

n_lookback = 60
n_forecast = 30
    
def choose_branch_two(ti):
    accuracies = ti.xcom_pull(task_ids=[
        'new_data_visualisation',
        'prediction_visualisation',
    ])
    best_accuracy = max(accuracies)
    if (best_accuracy > 0):
        return 'good_accuracy'
    return 'bad_accuracy'


def _training_model():
    return randint(1, 10)

def predict_and_store(**kwargs):
    df = yf.download(tickers=['AAPL'], period='10y')
    y = df['Close'].fillna(method='ffill')
    y = y.values.reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaler = scaler.fit(y)
    y = scaler.transform(y)

    # load the saved LSTM model
    model = load_model('/opt/airflow/Website/models/lstm_model_nextmonth_apple_100_64.h5')
    
    # make the prediction

    X = []
    Y = []
    for i in range(n_lookback, len(y) - n_forecast + 1):
        X.append(y[i - n_lookback: i])
        Y.append(y[i: i + n_forecast])
    X = np.array(X)
    Y = np.array(Y)
    X_ = y[- n_lookback:]
    X_ = X_.reshape(1, n_lookback, 1)

    Y_ = model.predict(X_).reshape(-1, 1)
    Y_ = scaler.inverse_transform(Y_)

    # store the results in the PostgreSQL database
    hook = PostgresHook(postgres_conn_id='postgres_default')
    conn = hook.get_conn()
    cursor = conn.cursor()

    # delete all records in the table before inserting new records
    cursor.execute("DELETE FROM stock_price_predictions")
    
    for i in range(n_forecast):
        cursor.execute("INSERT INTO stock_price_predictions (timestamp, price) VALUES (%s, %s)", 
                       (datetime.now(), Y_[i].item()))
    conn.commit()
    cursor.close()

def plot_data_task(**kwargs):
    # retrieve the data from the database
    hook = PostgresHook(postgres_conn_id='postgres_default')
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, price FROM stock_price_predictions")
    results = cursor.fetchall()
    cursor.close()
    
    # convert the data to a dataframe format
    predictions = np.array(results)[:, 1]

    # plot the data
    df = yf.download(tickers=['AAPL'], period='10y')

    # organize the results in a data frame
    df_past = df[['Close']].reset_index()
    df_past.rename(columns={'index': 'Date', 'Close': 'Actual'}, inplace=True)
    df_past['Date'] = pd.to_datetime(df_past['Date'])
    df_past['Forecast'] = np.nan
    df_past['Forecast'].iloc[-1] = df_past['Actual'].iloc[-1]

    df_future = pd.DataFrame(columns=['Date', 'Actual', 'Forecast'])
    df_future['Date'] = pd.date_range(start=df_past['Date'].iloc[-1] + pd.Timedelta(days=1), periods=n_forecast)
    df_future['Forecast'] = predictions.flatten()
    df_future['Actual'] = np.nan

    plt.figure(figsize=(16,6))
    last_90 = pd.concat([df_past, df_future]).iloc[-90:]
    last_180 = pd.concat([df_past, df_future]).iloc[-180:]
    plt.plot(last_180['Date'], last_180['Actual'], label='Actual')
    plt.plot(last_180['Date'], last_180['Forecast'], label='Forecast')

    plt.title('Apple Stock Price Prediction')
    plt.xlabel('Date', fontsize=18)
    plt.ylabel('Apple Stock Price')

    # Adjusting the xticks
    plt.xticks(rotation=45)
    plt.xlim(last_180['Date'].min(), last_180['Date'].max())
    xticks = pd.date_range(start=last_180['Date'].min(), end=last_180['Date'].max(), freq='W')
    plt.xticks(xticks, xticks.strftime("%b-%d-%Y"))

    plt.legend()
    
    # save the plot to an HTML file
    filename = '/opt/airflow/Website/static/stock_price_predictions.jpg'
    plt.savefig(filename)
    filename = '/opt/airflow/Website/static/stock_price_predictions.jpg'
    with open(filename, 'wb') as f:
        plt.savefig(f)
    os.chmod(filename, 0o664)

    return 1


with DAG("draft_workflow_two",
    start_date=datetime(2023, 2 ,10), 
    schedule_interval='1d', 
    ##schedule_interval='*/30 * * * *', 
    catchup=False) as dag:
    
    with TaskGroup('runModel') as runModel:
        check_for_trained_model = BashOperator(
            task_id="check_for_trained_model",
            bash_command=" echo 'check_for_trained_model'"
        )
        get_DB_data = BashOperator(
            task_id="get_new_data",
            bash_command=" echo 'get_DB_data'"
        )
        feed_to_model = PythonOperator(
            task_id="feed_to_model",
            python_callable=predict_and_store

        )


        
    with TaskGroup(group_id='webApplicationTrackingModelPerformance', prefix_group_id=False) as web_application_tracking_model_performance:
        new_data_visualisation = PythonOperator(
            task_id="new_data_visualisation",
            python_callable=_training_model
        )

        prediction_visualisation = PythonOperator(
            task_id="prediction_visualisation",
            python_callable=plot_data_task
        )

        run_django_website = BashOperator(
            task_id='start_server',
            bash_command='cd /opt/airflow/Website/ && python manage.py runserver 0.0.0.0:8000',
        )
        
    with TaskGroup(group_id='modelValidation', prefix_group_id=False) as modelValidation:

        validate_model = BranchPythonOperator(
            task_id="validate_model",
            python_callable=choose_branch_two
        )
   
    
        good_accuracy = BashOperator(
            task_id="good_accuracy",
            bash_command="echo 'good_accuracy'"
        )

        bad_accuracy = BashOperator(
            task_id="bad_accuracy",
            bash_command=" echo 'bad_accuracy'"
        )

    
    with TaskGroup('furtherAction') as furtherAction:
        deploy_new_model = BashOperator(
            task_id="deploy_new_model",
            bash_command=" echo 'deploy_new_model'"
        )
        fallback_to_deployed_model = BashOperator(
            task_id="fallback_to_deployed_model",
            bash_command=" echo 'fallback_to_deployed_model'"
        )
        
        alert_email = EmailOperator(
            task_id='alert_email',
            to='test@mail.com',
            subject='Alert Mail',
            html_content=""" Mail Test """,
            )
            
        merge_new_data_with_old = BashOperator(
            task_id="merge_new_data_with_old",
            bash_command=" echo 'merge_new_data'"
        )
        
        serve_prediction = BashOperator(
            task_id="serve_prediction",
            bash_command=" echo 'serve_prediction'"
        )
    


    get_DB_data >> new_data_visualisation
    check_for_trained_model >> get_DB_data >> feed_to_model
    new_data_visualisation >> validate_model
    validate_model >> [good_accuracy, bad_accuracy]
    feed_to_model >> prediction_visualisation >> run_django_website 
    prediction_visualisation >> validate_model
    good_accuracy >> [deploy_new_model,merge_new_data_with_old]
    bad_accuracy >> [fallback_to_deployed_model,alert_email]
    deploy_new_model >> serve_prediction

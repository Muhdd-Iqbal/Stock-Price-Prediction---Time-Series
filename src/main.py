from data_loader import DataLoader
from data_preprocessing import Preprocessing
from modeling import TrainProphet, ForecastProphet
from hypertuning import ProphetTuner
import pandas as pd
from datetime import datetime, timedelta
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.metrics import mean_absolute_percentage_error


def RunForecast():
    loader = DataLoader("BBCA", "2020-01-01", "2026-03-20") #You can set the date range 
    df = loader.load_data()

    preparation = Preprocessing()

    df_resample = preparation.run(df)

    #Model Training
    train = TrainProphet(df_resample, window=670) #use a rolling window of the latest 670 data points
    TrainProphet(df_resample)
    train_res=train.run()

    # Use this if using Hypertuning Parameter
    
    """
    df_tuner = df_resample.copy()
    df_tuner = df_tuner.rename(columns={"Date": "ds", "Close": "y"})

    tuner = ProphetTuner(df_tuner)
    best, all_results = tuner.tune()

    params = {k: v for k, v in best.items() if k != 'rmse'}

    train = TrainProphet(df_resample, params['changepoint_prior_scale'], params['seasonality_prior_scale'],params['mode_seasonality'],params['fourier_order'])
    TrainProphet(df_resample)
    train_res=train.run()

    """
    # Load model and cutoff date from training 
    model = train_res[0]
    end_date_train = train_res[1]

    start_forecast_date = (datetime.strptime(end_date_train, '%Y-%m-%d')+ timedelta(days=1)).strftime('%Y-%m-%d')
    end_forecast_date = (datetime.strptime(end_date_train, '%Y-%m-%d')+ timedelta(days=5)).strftime('%Y-%m-%d')

    # Forecast the data
    forecast = ForecastProphet(model, start_forecast_date, end_forecast_date)
    df_forecast = forecast.run().reset_index(drop=True)
    
    #compare with actual data

    min_date_ = df_forecast['ds'].min().strftime('%Y-%m-%d')
    max_date_ = df_forecast['ds'].max().strftime('%Y-%m-%d')

    loader_act = DataLoader("BBCA", min_date_, max_date_)
    df_act = loader_act.load_data()
    df_act['Date'] = df_act.index
    df_act = df_act[['Date','Close']]
    df_act.reset_index(drop=True, inplace=True)
    df_act = pd.DataFrame({'Date':df_act.iloc[:,0].tolist(), 'Close':df_act.iloc[:,1].tolist()})

    # Combine actual and forecast results
    df_merge = pd.merge(df_forecast[['ds','yhat']], df_act, how='left', left_on='ds', right_on = 'Date')
    df_merge = df_merge[['ds','yhat','Close']].dropna()
    return df_merge, df_forecast, model

if __name__ == "__main__":
    df_merge, df_forecast, model = RunForecast()
    print(df_merge)
    
    # Evaluation
    rmse = mean_squared_error(df_merge['Close'], df_merge['yhat'])
    mae = mean_absolute_error(df_merge['Close'], df_merge['yhat'])
    mape = mean_absolute_percentage_error(df_merge['Close'], df_merge['yhat']) * 100

    print("----------------------------------------------------")
    print("Metrics Evaluation")
    print('rmse:', rmse, ", mae:", mae, ", mape:", mape )
from prophet import Prophet
from datetime import datetime, timedelta

class TrainProphet:
    def __init__(self, data, changepoint_prior_scale=2, seasonality_prior_scale=10, seasonality_mode='multiplicative', fourier_order=15, window=1300, n_periods=5):
        self.init_data = data
        self.window = window
        self.n_periods = n_periods
        self.changepoint_prior_scale = changepoint_prior_scale
        self.seasonality_prior_scale = seasonality_prior_scale
        self.fourier_order = fourier_order
        self.seasonality_mode = seasonality_mode 
        
    def Training(self):
        window = self.window
        n_periods = self.n_periods 
        final_df = self.init_data
        
        #forecast_end = final_df['Date'].max()
        forecast_end = final_df['ds'].max()
    
        #final_df = final_df[['Date','Close']].rename(columns={'Date':'ds', 'Close':'y'})
        #self.final_df = final_df.set_index('ds')
        
        start_idx = len(final_df) - n_periods
        
        list_model = []
        
        for i in range(start_idx, len(final_df)+1, n_periods): 
            y = final_df.iloc[i-window:i]
            
            m = Prophet(
                changepoint_prior_scale=self.changepoint_prior_scale,
                seasonality_prior_scale=self.seasonality_prior_scale,
                seasonality_mode= self.seasonality_mode,
                yearly_seasonality=False, weekly_seasonality=False, daily_seasonality=False
            )
            
            m.add_seasonality(name='monthly', period=30.5, fourier_order=self.fourier_order)
            m.add_seasonality(name='weekly', period=7, fourier_order=self.fourier_order)
            m.add_seasonality(name='yearly', period=35, fourier_order=self.fourier_order)
            
            m.fit(y)
        
        self.forecast_end = forecast_end.strftime('%Y-%m-%d')
        self.model = m
        
    def run(self):
        self.Training()
        return self.model, self.forecast_end
    
class ForecastProphet:
    def __init__(self, model, start_forecast_date, end_forecast_date,n_periods=5):
        self.model = model 
        self.init_start_date = datetime.strptime(start_forecast_date, '%Y-%m-%d')
        self.init_end_date = datetime.strptime(end_forecast_date, '%Y-%m-%d')
        self.n_periods = n_periods 
        
        
    def Forecasting(self):
        total_day = (self.init_end_date-self.init_start_date).days+1
        
        forecast_end = (self.init_start_date - timedelta(days=1)).strftime('%Y-%m-%d')
        
        if total_day == self.n_periods:
            
            if (datetime.strptime(forecast_end, '%Y-%m-%d')).strftime('%A') == 'Friday':
                additional_day = 0
            elif (datetime.strptime(forecast_end, '%Y-%m-%d')).strftime('%A')  == 'Thursday':
                additional_day = 1
            elif (datetime.strptime(forecast_end, '%Y-%m-%d')).strftime('%A')  == 'Wednesday':
                additional_day = 2
            elif (datetime.strptime(forecast_end, '%Y-%m-%d')).strftime('%A') == 'Tuesday':
                additional_day = 3
            else:
                additional_day = 4
            print("additional day=", additional_day)
            
            load_model = self.model 
            future = load_model.make_future_dataframe(periods=additional_day+self.n_periods, freq='B')
        
            df_forecast = load_model.predict(future)#[['ds','yhat','yhat_lower','yhat_upper','trend']]
            df_forecast = df_forecast.tail(additional_day+self.n_periods)
            self.df_forecast = df_forecast
        else:
            print("Check the date range forecasting")
        
    def run(self):
        self.Forecasting()
        return getattr(self, 'df_forecast', None)
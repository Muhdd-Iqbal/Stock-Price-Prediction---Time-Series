import pandas as pd

class Preprocessing:
    def CleanData(self, df):
        df["Date"] = df.index
        df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]
        df.reset_index(drop=True, inplace=True)
        
        list1 = df.iloc[:,0].tolist()
        list2 = df.iloc[:,1].tolist()
        list3 = df.iloc[:,2].tolist()
        list4 = df.iloc[:,3].tolist()
        list5 = df.iloc[:,4].tolist()
        list6 = df.iloc[:,5].tolist()

        self.data= pd.DataFrame({'Date':list1, 'Open':list2, 'High':list3,
              'Low':list4, 'Close':list5, 'Volume':list6})
        
        
    def DataPreparation(self):
        df = self.data[['Date','Close']].copy()

        df = df.rename(columns={
            'Date': 'ds',
            'Close': 'y'
        })

        df['ds'] = pd.to_datetime(df['ds'])

        self.df_resample = df
        # df = self.data
        # df = df[['Date','Close']]
        # end_date = df['Date'].max()
        
        # list_data = []
        # res_data = df.copy()
        # res_data.set_index('Date', inplace=True)
        
        # full_range = pd.date_range(start=res_data.index.min(), end = end_date, freq='B')
        
        # df_resample = res_data.reindex(full_range)
        # df_resample['Close'] = df_resample.fillna(0)
        # df_resample = df_resample.reset_index().rename(columns={'index':'Date'})
        
        # list_data.append(df_resample)
        
        # self.df_resample = pd.concat(list_data, ignore_index=True)
    
    def run(self, df):
        self.CleanData(df)
        self.DataPreparation()
        return self.df_resample
        
        
        
        
        
        
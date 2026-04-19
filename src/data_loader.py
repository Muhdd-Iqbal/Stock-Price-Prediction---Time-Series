import yfinance as yf

class DataLoader:
    def __init__(self, ticker, start, end):
        self.ticker = ticker
        self.start = start
        self.end = end
    
    def load_data(self):
        df = yf.download(self.ticker,start=self.start, end=self.end, progress=False)
        return df
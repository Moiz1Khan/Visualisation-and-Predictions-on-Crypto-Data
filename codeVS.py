import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests

class CryptoData:
    def __init__(self):
        self.df_bitcoin = None
        self.df_ethereum = None
        self.df_ripple = None
    
    def dataScrap(self, pair):
        url = f'https://api.kraken.com/0/public/OHLC?pair={pair}&interval=1440'
        data = requests.get(url).json()
        ohlc_data = data['result'][pair]
        df = pd.DataFrame(ohlc_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s') 
        df.to_csv(f'{pair}_data.csv', index=True)
        return df

    def dataScrapBitcoin(self):
        self.df_bitcoin = self.dataScrap('XXBTZUSD')
        return self.df_bitcoin.head()

    def dataScrapEthereum(self):
        self.df_ethereum = self.dataScrap('XETHZUSD')
        return self.df_ethereum.head()

    def dataScrapRipple(self):
        self.df_ripple = self.dataScrap('XXRPZUSD')
        return self.df_ripple.head()

    def MissingValues(self, df):
        missing_values = df.isnull().sum()
        return missing_values

    def LogReturns(self, df):
        df['close'] = pd.to_numeric(df['close'])
        df['LogReturns'] = np.log(df['close'] / df['close'].shift(1))
        return df['LogReturns']

    def Analysis(self, df):
        returns = self.LogReturns(df)
        mean = returns.mean()
        print('Mean Of The Logarithmic returns: ', mean)
        median = returns.median()
        print('Median Of The Logarithmic returns: ', median)
        std = returns.std()
        print('Standard Deviation Of The Logarithmic returns: ', std)

    def MaxReturnDate(self, df):
        returns = self.LogReturns(df)
        maxReturnDate = df.loc[returns.idxmax(),'timestamp']
        return maxReturnDate
    
    def PlotHistoricalPrices(self, df, label):
        plt.figure(figsize=(6, 3))
        plt.plot(df['timestamp'], df['close'], label=f'Closing Price ({label})',color='green')
        plt.title(f'{label} Historical Prices')
        plt.xlabel('Date')
        plt.ylabel('Closing Price')
        plt.legend()
        plt.show()
        
    def PlotLogReturns(self, df, label):
        plt.figure(figsize=(6, 3))
        plt.plot(df['timestamp'], df['LogReturns'], label=f'Logarithmic Returns ({label})',color='red')
        plt.title(f'{label} Logarithmic Returns')
        plt.xlabel('Date')
        plt.ylabel('Logarithmic Returns')
        plt.legend()
        plt.show()

    def CorrelationMatrix(self):
        returns_bitcoin = self.LogReturns(self.df_bitcoin)
        returns_ethereum = self.LogReturns(self.df_ethereum)
        returns_ripple = self.LogReturns(self.df_ripple)
        correlation_matrix = pd.concat([returns_bitcoin, returns_ethereum, returns_ripple], axis=1).corr()
        plt.figure(figsize=(6, 4))
        sns.heatmap(correlation_matrix, annot=True, cmap='Set2', fmt=".5f", linewidths=.1)
        plt.title('Correlation Matrix of Returns')
        plt.show()
        return correlation_matrix
    
    def MeanReturnsBarChart(self):
        returns_bitcoin = self.LogReturns(self.df_bitcoin)
        returns_ethereum = self.LogReturns(self.df_ethereum)
        returns_ripple = self.LogReturns(self.df_ripple)
        mean_returns = [returns_bitcoin.mean(), returns_ethereum.mean(), returns_ripple.mean()]
        cryptocurrencies = ['Bitcoin', 'Ethereum', 'Ripple']
        plt.figure(figsize=(4, 3))
        sns.barplot(x=cryptocurrencies, y=mean_returns, palette='Set1')
        plt.title('Mean Returns of Cryptocurrencies')
        plt.xlabel('Cryptocurrency')
        plt.ylabel('Mean Returns')
        plt.show()
        
    def DisplayInfo(self, df, label):
        print(f'\n{label} Data:')
        print('No Missing Values:')
        print(self.MissingValues(df))
        print('Analysis:')
        self.Analysis(df)
        print(f'Date with the highest return ({label}): ', self.MaxReturnDate(df))
        self.PlotHistoricalPrices(df, label)
        self.PlotLogReturns(df, label)

def main():
    crypto_data = CryptoData()

    while True:
        print("\nMenu:")
        print("1. Bitcoin")
        print("2. Ethereum")
        print("3. Ripple")
        print("4. Correlation Matrix")
        print("5. BarChart")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            print('\nFetching Bitcoin data...')
            print(crypto_data.dataScrapBitcoin())
            crypto_data.DisplayInfo(crypto_data.df_bitcoin, 'Bitcoin')

        elif choice == '2':
            print('\nFetching Ethereum data...')
            print(crypto_data.dataScrapEthereum())
            crypto_data.DisplayInfo(crypto_data.df_ethereum, 'Ethereum')

        elif choice == '3':
            print('\nFetching Ripple data...')
            print(crypto_data.dataScrapRipple())
            crypto_data.DisplayInfo(crypto_data.df_ripple, 'Ripple')

        elif choice == '4':
            print('\nCorrelation Matrix between Bitcoin, Ethereum, and Ripple Returns:')
            print(crypto_data.CorrelationMatrix())

        elif choice == '5':
            crypto_data.MeanReturnsBarChart()
            break
            
        elif choice == '6':
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()

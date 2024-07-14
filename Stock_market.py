import yfinance as yf
import pandas as pd

class StockPortfolio:
    def __init__(self):
        self.portfolio = pd.DataFrame(columns=["Ticker", "Shares", "Price"])

    def add_stock(self, ticker, shares):
        try:
            stock = yf.Ticker(ticker)
            stock_info = stock.history(period='1d')
            if stock_info.empty:
                raise ValueError(f"Failed to retrieve price for {ticker}.")
            price = stock_info['Close'].iloc[-1]
            if ticker in self.portfolio["Ticker"].values:
                self.portfolio.loc[self.portfolio["Ticker"] == ticker, "Shares"] += shares
            else:
                new_row = pd.DataFrame({"Ticker": [ticker], "Shares": [shares], "Price": [price]})
                self.portfolio = pd.concat([self.portfolio, new_row], ignore_index=True)
            print(f"Added {shares} shares of {ticker} at {price:.2f} per share.")
        except Exception as e:
            print(f"An error occurred while adding stock: {e}")

    def remove_stock(self, ticker, shares):
        if ticker in self.portfolio["Ticker"].values:
            current_shares = self.portfolio.loc[self.portfolio["Ticker"] == ticker, "Shares"].values[0]
            if shares >= current_shares:
                self.portfolio = self.portfolio[self.portfolio["Ticker"] != ticker]
                print(f"Removed all shares of {ticker}.")
            else:
                self.portfolio.loc[self.portfolio["Ticker"] == ticker, "Shares"] -= shares
                print(f"Removed {shares} shares of {ticker}.")
        else:
            print(f"{ticker} not found in portfolio.")

    def get_portfolio(self):
        for index, row in self.portfolio.iterrows():
            ticker = row['Ticker']
            shares = row['Shares']
            try:
                stock = yf.Ticker(ticker)
                stock_info = stock.history(period='1d')
                if stock_info.empty:
                    raise ValueError(f"Failed to retrieve current price for {ticker}.")
                current_price = stock_info['Close'].iloc[-1]
                self.portfolio.at[index, 'Price'] = current_price
                print(f"{ticker}: {shares} shares @ {current_price:.2f} per share")
            except Exception as e:
                print(f"An error occurred while retrieving data for {ticker}: {e}")

    def get_total_value(self):
        total_value = 0
        for index, row in self.portfolio.iterrows():
            ticker = row['Ticker']
            shares = row['Shares']
            try:
                stock = yf.Ticker(ticker)
                stock_info = stock.history(period='1d')
                if stock_info.empty:
                    raise ValueError(f"Failed to retrieve current price for {ticker}.")
                current_price = stock_info['Close'].iloc[-1]
                total_value += shares * current_price
            except Exception as e:
                print(f"An error occurred while retrieving data for {ticker}: {e}")
        print(f"Total portfolio value: ${total_value:.2f}")
        return total_value

# Example usage
if __name__ == "__main__":
    portfolio = StockPortfolio()
    portfolio.add_stock("AAPL", 15)  # Corrected ticker symbol for Apple Inc.
    portfolio.add_stock("GOOGL", 5)  # Corrected ticker symbol for Alphabet Inc.
    portfolio.get_portfolio()
    portfolio.remove_stock("AAPL", 5)
    portfolio.get_portfolio()
    portfolio.get_total_value()

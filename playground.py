import pandas as pd

def calculate_rsi(prices, period=14):
    """
    Calculate the Relative Strength Index (RSI) for a given stock price data.

    :param prices: List of daily closing prices.
    :param period: Number of days to consider for RSI calculation (default is 14).
    :return: RSI value.
    """


    price_changes = prices.diff().dropna()

    print(price_changes)

    gains = price_changes.where(price_changes > 0, 0)
    losses = -price_changes.where(price_changes < 0, 0)

    avg_gain = gains[gains > 0].mean()  
    avg_loss = losses[losses > 0].mean()

 

    print(avg_gain)
    print(avg_loss)

    rs = avg_gain / avg_loss if avg_loss != 0 else float('inf')
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

# Example usage:
HDFC=[ 1,509.25	, 1,494.70	, 1,531.30	, 1,512.20	, 1,507.60	, 1,511.70	, 1,510.75	, 1,509.80	,1,529.50	,1,520.10	,1,532.25	,1,519.60	,1,522.65, 1509.90 	]
IRFC=[141.70, 141.95, 141.00, 144.10, 147.75, 149.00, 150.25, 158.05,160.90,157.25,158.80,157.10,155.65, 151.25]
prices = pd.Series(IRFC)
rsi_value = calculate_rsi(prices)
print("RSI:", rsi_value)




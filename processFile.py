# import pandas as pd
# import numpy as np

# def calculate_mac(data, period=20, multiplier=1.5):
#     # Calculate the moving average
#     print(data['Close'].rolling(window=period, min_periods=1).mean())
#     data['MA'] = data['Close'].rolling(window=period, min_periods=1).mean()
    
#     # Calculate the average true range (ATR) or standard deviation
#     data['ATR'] = data['High'] - data['Low']
#     data['ATR'] = data['ATR'].rolling(window=period, min_periods=1).mean()
    
#     # Calculate the upper and lower bands
#     data['UpperBand'] = data['MA'] + multiplier * data['ATR']
#     data['LowerBand'] = data['MA'] - multiplier * data['ATR']
    
#     return data

# # Example usage:
# # Assuming 'data' is a pandas DataFrame containing OHLC (Open, High, Low, Close) data
# # and 'period' and 'multiplier' are the parameters for the Moving Average Channel
# data = pd.DataFrame({
#     'Close': [100, 102, 105, 103, 104, 106, 107, 108, 110, 109],
#     'High': [102, 104, 106, 105, 107, 109, 110, 111, 112, 111],
#     'Low': [98, 100, 103, 101, 102, 104, 105, 106, 108, 107]
# })

# mac_data = calculate_mac(data)
# print(mac_data)


# import pandas as pd
# import nselib

# # Get trading holiday calendar data
# data = nselib.trading_holiday_calendar()

# # Convert data to a DataFrame
# df = pd.DataFrame(data)

# # Write DataFrame to an Excel file
# excel_file_path = "trading_holidays.xlsx"
# df.to_excel(excel_file_path, index=False)

# print("Data has been written to", excel_file_path)

# import pandas as pd
# from nselib import derivatives
# from nselib import capital_market

# dataDerivatives = derivatives.fno_bhav_copy(trade_date='02-05-2024')
# # dataCapitalMarket = capital_market.fno_equity_list()



# df=pd.DataFrame(dataDerivatives)
# df.to_excel('fno_bhav_copy.xlsx', index=False)


#######################################################################################################################################################


# import pandas as pd
# from nselib import derivatives
# from nselib import capital_market

# # Function to calculate Fibonacci pivot points
# def calculate_fibonacci_pivot_points(high, low, close):
#     pivot_point = (high + low + close) / 3
#     s1 = pivot_point - 0.382 * (high - low)
#     r1 = pivot_point + 0.382 * (high - low)
#     return s1, r1

# # Get data
# # dataDerivatives = derivatives.fno_bhav_copy(trade_date='02-05-2024')
# dataDerivatives = capital_market.bhav_copy_equities(trade_date='02-05-2024')
# df = pd.DataFrame(dataDerivatives)

# # # Calculate Fibonacci pivot points and add them to DataFrame
# df['Fibonacci_S1'], df['Fibonacci_R1'] = calculate_fibonacci_pivot_points(df['HIGH'], df['LOW'], df['CLOSE'])

# # # Write the DataFrame to a new Excel file
# df[['SYMBOL', 'HIGH', 'LOW', 'CLOSE', 'Fibonacci_R1', 'Fibonacci_S1']].to_excel('bhav_copy_equities.xlsx', index=False)
# # df.to_excel('bhav_copy_equities.xlsx', index=False)

# print(dataDerivatives)


#######################################################################################################################################################

# import pandas as pd
# from nselib import capital_market
# from stockList import symbols
# from PivotPointStandards import calculate_fibonacci_pivot_points
# from liveDataScrapping import get_live_data



# # Get data
# dataDerivatives = capital_market.price_volume_data(symbol='ABB')
# df = pd.DataFrame(dataDerivatives)

# # Create an empty list to store DataFrames for each symbol
# dfs = []

# for symbol in symbols:
#     filtered_df = df[(df['SYMBOL'] == symbol) & (df['SERIES'] == 'EQ')]

#     # Check if data for the symbol exists
#     if not filtered_df.empty:
#         # Calculate Fibonacci pivot points for the filtered data
#         filtered_df.loc[:, 'Fibonacci_S1'], filtered_df.loc[:, 'Fibonacci_R1'] = calculate_fibonacci_pivot_points(filtered_df['HIGH'], filtered_df['LOW'], filtered_df['CLOSE'])


#         # Append the filtered DataFrame to the list
#         dfs.append(filtered_df[['SYMBOL', 'HIGH', 'LOW', 'CLOSE', 'Fibonacci_R1', 'Fibonacci_S1']])
#         dfs.append(filtered_df)
#     else:
#         print(f"No data found for symbol {symbol}")

# # Concatenate all DataFrames in the list
# combined_df = pd.concat(dfs)

# # Write the combined DataFrame to a new Excel file
# combined_df.to_excel('test.xlsx', index=False)
# print("Combined pivot points saved to FnO_R1_S1.xlsx")


#######################################################################################################################################################
from FnoSpreadSheet import get_data_set, write_to_worksheet
import pandas as pd
# from nselib import trading_holiday_calendar

def process_data(r1s1_df):
    CMPdf = get_data_set()
    CMPdf['CMP'] = CMPdf['CMP'].apply(parse_numeric_or_keep)
    CMPdf['CHANGE'] = CMPdf['CHANGE'].apply(parse_numeric_or_keep)
    r1s1_df['Fibonacci_S1'] = r1s1_df['Fibonacci_S1'].apply(parse_numeric_or_keep)
    r1s1_df['Fibonacci_R1'] = r1s1_df['Fibonacci_R1'].apply(parse_numeric_or_keep)


    CMPdf.reset_index(drop=True, inplace=True)
    r1s1_df.reset_index(drop=True, inplace=True)

    buy_df = r1s1_df[(pd.to_numeric(CMPdf['CMP'], errors='coerce') > r1s1_df['Fibonacci_R1']) & 
                 ((pd.to_numeric(CMPdf['CHANGE'], errors='coerce') >= 1.5) & 
                  (pd.to_numeric(CMPdf['CHANGE'], errors='coerce') <= 3))]

    sell_df = r1s1_df[(pd.to_numeric(CMPdf['CMP'], errors='coerce') < r1s1_df['Fibonacci_S1']) & 
                    ((pd.to_numeric(CMPdf['CHANGE'], errors='coerce') >= -3) & 
                    (pd.to_numeric(CMPdf['CHANGE'], errors='coerce') <= -1.5))]
    if not buy_df.empty:

        buy_df.loc[buy_df.index, 'CMP'] = CMPdf.loc[buy_df.index, 'CMP']
        buy_df.loc[buy_df.index, 'CHANGE'] = CMPdf.loc[buy_df.index, 'CHANGE']

        # buy_df['TradeType'] = 'Hold'

        # # Conditionally assign values based on criteria
        # filtered_df.loc[CMPdf['CMP'] > r1s1_df['Fibonacci_R1'], 'TradeType'] = 'Buy'
        # filtered_df.loc[CMPdf['CMP'] < r1s1_df['Fibonacci_S1'], 'TradeType'] = 'Sell'
    buy_df_serializable = buy_df.applymap(lambda x: x.item() if isinstance(x, pd.Series) else x)  
    write_to_worksheet(buy_df_serializable , 'BuyStocks')
    if not sell_df.empty:
        sell_df.loc[sell_df.index, 'CMP'] = CMPdf.loc[sell_df.index, 'CMP']
        sell_df.loc[sell_df.index, 'CHANGE'] = CMPdf.loc[sell_df.index, 'CHANGE']

        # sell_df['TradeType'] = 'Hold'

        # # Conditionally assign values based on criteria
        # filtered_df.loc[CMPdf['CMP'] > r1s1_df['Fibonacci_R1'], 'TradeType'] = 'Buy'
        # filtered_df.loc[CMPdf['CMP'] < r1s1_df['Fibonacci_S1'], 'TradeType'] = 'Sell' 
    sell_df_serializable = sell_df.applymap(lambda x: x.item() if isinstance(x, pd.Series) else x)         
    write_to_worksheet(sell_df_serializable , 'SellStocks')


# def process_holiday_calendra():
#     df=trading_holiday_calendar();
#     df['tradingDate'] = pd.to_datetime(df['tradingDate'], format='%d-%b-%Y')
#     return df['tradingDate'].dt.date.to_list()
    
def parse_numeric_or_keep(value):
    try:
        return pd.to_numeric(value)
    except ValueError:
        return value    
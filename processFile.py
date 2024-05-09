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
    CMPdf=get_data_set()
    CMPdf['CMP']=pd.to_numeric(CMPdf['CMP'])
    CMPdf['CHANGE'] = pd.to_numeric(CMPdf['CHANGE'])
    r1s1_df['Fibonacci_S1'] = pd.to_numeric(r1s1_df['Fibonacci_S1'])
    r1s1_df['Fibonacci_R1'] = pd.to_numeric(r1s1_df['Fibonacci_R1'])
    # PREVLOWHIGHCLOSEdf['CLOSE'] = pd.to_numeric(PREVLOWHIGHCLOSEdf['CLOSE'])

    # PREVLOWHIGHCLOSEdf['s1'],PREVLOWHIGHCLOSEdf['r1'] =(calculate_fibonacci_pivot_points(PREVLOWHIGHCLOSEdf['HIGH'], PREVLOWHIGHCLOSEdf['LOW'], PREVLOWHIGHCLOSEdf['CLOSE']))


    CMPdf.reset_index(drop=True, inplace=True)
    r1s1_df.reset_index(drop=True, inplace=True)

    filtered_df = r1s1_df[(CMPdf['CMP'] > r1s1_df['Fibonacci_R1']) & (CMPdf['CHANGE'] >= 1.5) & (CMPdf['CHANGE'] <= 2.5) ]
    # if not filtered_df.empty:
    #     filtered_df = filtered_df.copy()  # Create a copy of the DataFrame slice
    #     filtered_df.loc[:, 'CMP'] = CMPdf['CMP'].values[:len(filtered_df)]
    #     filtered_df.loc[:, 'CHANGE'] = CMPdf['CHANGE'].values[:len(filtered_df)]
    if not filtered_df.empty:
        filtered_df.loc[filtered_df.index, 'CMP'] = CMPdf.loc[filtered_df.index, 'CMP']
    write_to_worksheet(filtered_df, 'FilteredStocks')


# def process_holiday_calendra():
#     df=trading_holiday_calendar();
#     df['tradingDate'] = pd.to_datetime(df['tradingDate'], format='%d-%b-%Y')
#     return df['tradingDate'].dt.date.to_list()
    
    
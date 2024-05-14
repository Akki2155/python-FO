import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from PivotPointStandards import calculate_fibonacci_pivot_points
from datetime import datetime
import pytz

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

credentials={
  "type": "service_account",
  "project_id": "fnospreadsheet",
  "private_key_id": "13ca6bc7c1af8eaa4e7b15d8bde4f11547e82d8f",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC4w4Q5xpxTD0gq\nCkKLNqgfykLs2JYNww7MRgcURl4cpp8R1KF4s+x/i1icv2pHkYjGuY9C5RQKra6U\ny3NkMd6vg3F/rc3TUB/EsJCWiIOackJ/A5wrTdVp20xDZq/wz9ABSrsPr4mGMA3V\nyAiESUmPDzcVnl/i5i+dBdJClkmxiJmmPlE99NQrjFAwvOGOfykz7+Zrd7khqTn5\nc7Y1FMZH4ZEJtbb5u5Nv+cSYmbHAkud4zgiPuujNY5r9PTIFMNDPEzbOfh7DVOAA\nyCnhb36/IvsILlJFY+Su91ZWPdzFvcsSnGZGq8yk0CZABqOJ3s9gC/AWI1RFklrk\nPPTgwlkHAgMBAAECggEADsxw2PR8oosiTg+1UGjdIsgJ/+YXGrIUC4N+X1QwMd5H\nS7UlW8Fu1gZnX2Krf2D7kg3cbiYNVWT04JZtFHTexQhjp6+C7APKZPAkHJKBlqDD\n4mAmetzIlP/LcMiW8KmhxkC3O+SPliUKLqR6Hiev5xqiYFkSOAkU04sFp29Z0V4g\nQ3oE6Uxi/0y0oTTiJPSlSaQ8OYqETY5JaSV+YHfro35ZiAwf+fyiArGIdZGjz+fB\nSY5mIuyKU4SGmlfUx4Ub0NRlOtqYPY8sW3+TtuMklGfm7ncAlt1cw8GGtgjI5ZZt\nLmq5eBHY6zbDaYq3+KBdzhyu74BvXiPopRtsbSWhcQKBgQD3YFn+8TGI1UiP8xQP\n5jI0TxxAPQNgdK74aXFlaKUWthCg40dqY5nZqrOa2MdMp3J5diGTTFsHkNJ+Y6AM\nvpxMsmXGijfrSxf66Ej+MNc9KXOQxML8JJhcNilna1cZX+K+JwMk7X8SCBz0BPWi\nW7f9ryumvGlNTcLOrThFmwI1kQKBgQC/NGToeobascNLjj4V826vamXHFFGEJnmB\ngLdfLemMPXxi9XmKFnB49taSGFmlppRrP3bNU04yXsULpp9PVJ1w18eythhJt6aX\nRn1fP8wqOtQIY6BxphfNcVIC3pqB1VPKftz6PGjatz8FULSkc8135AtOogrHpSQN\nNbj57V55FwKBgCW9Dz2zcgkb8Jv1S2Q5jAMq5nZuWGuIoYDIJUKBOl5CnDrPMX/r\nffcU8Z134L+y8+XPvcOI7II098fMTwhis9mHhbtKLsm4hQoEEc6liNCN2FGHku+A\nbbXzlVFvsLPwStkTfolNqgsILdKURxzjvSf4Z0Jij/X5HPUGvATyZt3hAoGBAKmD\nU+rfpesBKjkz9EsVtI2D8JOcqeBVE+gCK5AQbjvMzxgUtRn9Zt13SSfguqmnk3G5\npCPItUzmxB7eK+LzC1ndk8gWtFW2odT/w2rMbr8JxK1jVf0r2XJkAudUXvq4HD8s\nVdDr+bHeP9sAgAZEPGcMIBIoixIQkHO9qy64iMclAoGAU241RO04HnyXVg+OOu/V\nWl1RWdnqQNzNAh3Z4/S+Zs2XB0Y8yJyiXkPjxFQwHB57KnnBmc/vb7oIiKWk5kRa\nsKBsWFw4SGMCXpPFRahYS01RFb18mPy5Fq0504rgABrRpaoa361WYVgK14XRkO0j\n60UvNJUWtSBr2IzXqxspnLA=\n-----END PRIVATE KEY-----\n",
  "client_email": "fnospreadsheet@fnospreadsheet.iam.gserviceaccount.com",
  "client_id": "103378409125654953905",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/fnospreadsheet%40fnospreadsheet.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)
client = gspread.authorize(credentials)
spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1jjlWLGDRbfQ3Vf0IO5eJTG_UcwIhnvpdYs7ktswiUFQ')


def get_data_set():
    CMP = spreadsheet.get_worksheet(0)
    CMPVALUES = CMP.get_all_values()
    CMPVALUESdf = pd.DataFrame(CMPVALUES[1:], columns=CMPVALUES[0])
    return CMPVALUESdf


def get_prev_LOW_HIGH_CLOSE():
    prevLOWHIGH = spreadsheet.get_worksheet(3)
    PREVLOWHIGHVALUES = prevLOWHIGH.get_all_values()

    prevLOWHIGHVALUESdf = pd.DataFrame(PREVLOWHIGHVALUES[1:], columns=PREVLOWHIGHVALUES[0])
    return prevLOWHIGHVALUESdf


def write_to_worksheet(dataframe, worksheet_name):
    try:
        worksheet = spreadsheet.worksheet(worksheet_name)
    except gspread.exceptions.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows=1, cols=1)

    if dataframe.empty:
        print("DataFrame is empty. Clearing worksheet:", worksheet_name)
        # historyLog = spreadsheet.get_worksheet(4)
        # current_time = datetime.now().astimezone(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S %Z')

        # dataframe['SYMBOL'] = 'No Data' 
        # dataframe['EXCHANGE'] = 'No Data'
        # dataframe['PRICE OPEN'] = 'No Data'
        # dataframe['HIGH'] = 'No Data'
        # dataframe['LOW'] = 'No Data'
        # dataframe['CLOSE'] = 'No Data'
        # dataframe['Fibonacci_S1'] = 'No Data'  
        # dataframe['Fibonacci_R1'] = 'No Data'    
        # dataframe['TIMESTAMP'] = current_time
        
        # historyValues = [dataframe.columns.tolist()] + dataframe.values.tolist()
        
        # spreadsheet.values_append("'" + historyLog.title + "'!A1", 
        #                         params={'valueInputOption': 'RAW'}, 
        #                         body={'values': historyValues})
        
        worksheet.clear()
        return
    
    worksheet.clear()

    print("Writing to worksheet:", worksheet_name)
    current_time = datetime.now().astimezone(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S %Z')
    dataframe['TIMESTAMP'] = current_time
    values = [dataframe.columns.tolist()] + dataframe.values.tolist()

    # historyLog = spreadsheet.get_worksheet(4) 

    # # Define the background colors for Buy and Sell entries
    # buy_color = {'red': 0, 'green': 1, 'blue': 0, 'alpha': 0}
    # sell_color = {'red': 1, 'green': 0, 'blue': 0, 'alpha': 0}

    # # Get the range of the TradeType column
    # trade_type_range = f'B2:B{len(dataframe) + 1}'  # Assuming TradeType column starts from B2
    
    # # Prepare the request to add conditional formatting for Buy and Sell entries
    # requests = []
    # requests.append({
    #     'addConditionalFormatRule': {
    #         'rule': {
    #             'ranges': [{
    #                 'sheetId': worksheet.id,
    #                 'startRowIndex': 1,
    #                 'endRowIndex': len(dataframe) + 1,
    #                 'startColumnIndex': dataframe.columns.get_loc('TradeType'),
    #                 'endColumnIndex': dataframe.columns.get_loc('TradeType') + 1,
    #             }],
    #             'booleanRule': {
    #                 'condition': {
    #                     'type': 'TEXT_CONTAINS',
    #                     'values': [{'userEnteredValue': 'Buy'}],
    #                 },
    #                 'format': {
    #                     'backgroundColor': buy_color,
    #                 },
    #             },
    #         },
    #         'index': 0,
    #     }
    # })
    # requests.append({
    #     'addConditionalFormatRule': {
    #         'rule': {
    #             'ranges': [{
    #                 'sheetId': worksheet.id,
    #                 'startRowIndex': 1,
    #                 'endRowIndex': len(dataframe) + 1,
    #                 'startColumnIndex': dataframe.columns.get_loc('TradeType'),
    #                 'endColumnIndex': dataframe.columns.get_loc('TradeType') + 1,
    #             }],
    #             'booleanRule': {
    #                 'condition': {
    #                     'type': 'TEXT_CONTAINS',
    #                     'values': [{'userEnteredValue': 'Sell'}],
    #                 },
    #                 'format': {
    #                     'backgroundColor': sell_color,
    #                 },
    #             },
    #         },
    #         'index': 1,
    #     }
    # })

    # # Execute the requests
    # batch_update_body = {'requests': requests}
    # spreadsheet.batch_update(dataframe)

    # Update data
    spreadsheet.values_update("'" + worksheet.title + "'!A1", params={'valueInputOption': 'RAW'}, body={'values': values})

def end_of_the_sheet(sheet_name):
    endOfDaySheet = spreadsheet.get_worksheet(1)
    endOfDayData = endOfDaySheet.get_all_values()
    endOfDayData_df = pd.DataFrame(endOfDayData[1:], columns=endOfDayData[0])

    current_time = datetime.now().astimezone(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S %Z')

    endOfDayData_df['HIGH'] = pd.to_numeric(endOfDayData_df['HIGH'], errors='coerce')
    endOfDayData_df['LOW'] = pd.to_numeric(endOfDayData_df['LOW'], errors='coerce')
    endOfDayData_df['CLOSE'] = pd.to_numeric(endOfDayData_df['CLOSE'], errors='coerce')

    endOfDayData_df.dropna(subset=['HIGH', 'LOW', 'CLOSE'], inplace=True)

    endOfDayData_df.loc[:, 'Fibonacci_S1'], endOfDayData_df.loc[:, 'Fibonacci_R1']=calculate_fibonacci_pivot_points(endOfDayData_df['HIGH'], endOfDayData_df['LOW'], endOfDayData_df['CLOSE'])
    endOfDayData_df.loc[:,'TIMESTAMP'] = current_time
    values = [endOfDayData_df.columns.tolist()] + endOfDayData_df.values.tolist()

    R1S1SHEET=spreadsheet.worksheet(sheet_name)
    R1S1SHEET.clear()
    spreadsheet.values_update("'" + R1S1SHEET.title + "'!A1", params={'valueInputOption': 'RAW'}, body={'values': values})

def get_r1_s1_values(sheet_name):
    R1S1SHEET =spreadsheet.worksheet(sheet_name)
    R1S1SHEETVALUES = R1S1SHEET.get_all_values()
    R1S1SHEETVALUESdf = pd.DataFrame(R1S1SHEETVALUES[1:], columns=R1S1SHEETVALUES[0])
    return R1S1SHEETVALUESdf    

def clear_history_log():
    historyLog = spreadsheet.get_worksheet(4)
    historyLog.clear()
    print("History log cleared.")
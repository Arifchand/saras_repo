# package import statement
from SmartApi import SmartConnect #or from smartapi.smartConnect import SmartConnect
import pyotp 
from logzero import logger
import pandas as pd
from datetime import datetime, timedelta
import asyncio
import numpy as np
import pytz 

def flag_pattern(data, seventy_percent):
    # Find high and low volumes and check c_value condition
    threshold = seventy_percent  # Adjust this as needed to define "high" volume

    results=[]

    # Loop through data to identify two high volumes and check condition
    i=0
    j=0
    for i in range(len(data)):
        #print(f"i: {i}")
        if((i+j) < len(data)):
            i=i+j

        first_high = None
    
        # Find first high volume
        if data[i][5] > threshold:
            first_high = (i, data[i][0], data[i][4], data[i][5])
            #print(f"first_high : {first_high}")
            print(f"index : {first_high}")
            # Search for second high volume after first high
            for j in range(i+1, len(data)):
                if data[j][5] > threshold:
                    second_high = (j, data[j][0], data[j][4], data[j][5])
                    #print(f"second_high:{second_high}")
                
                    # Check if volumes between the first and second high are lower
                    is_lower = all(data[k][5] < threshold for k in range(i+1, j))
                    
                    # Check if second c_value is greater than first c_value
                    if is_lower and second_high[2] > first_high[2]:
                        results.append({
                            '1st_peak':i,
                            '1st_peak_DT': first_high[1],
                            '1st_peak_close': first_high[2],
                            '2nd_peak':j,
                            '2nd_peak_DT': second_high[1],
                            '2nd_peak_close': second_high[2]
                        })
    for i in results:
        print(i)

def Do_login():
    token = '76F3AXOS25UKUDHNRVRQJE3OAI'
    myotp= pyotp.TOTP(token).now()
    print(myotp)
    #login api call

    obj=SmartConnect(api_key="5WVLHRQB")
    data = obj.generateSession("P51657588","1995",pyotp.TOTP(token).now())
    refreshToken= data['data']['refreshToken']

    #fetch the feedtoken
    feedToken=obj.getfeedToken()

    #fetch User Profile
    print("Fetch User details: ------------------------------------------------------------")
    userProfile= obj.getProfile(refreshToken)
    print(userProfile)
    print("--------------------------------------------------------------------------------")
    return obj

def select_date_range():
    noof_days =2000
    stock_timeframe=list()
    thirty_days_ago = datetime.now() - timedelta(days=noof_days)
    from_date = thirty_days_ago.strftime("%Y-%m-%d %H:%M")
    stock_timeframe.append(from_date)
    to_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    stock_timeframe.append(to_date)
    print(f"from date:{from_date}")
    print(f"to_date :{to_date}")
    return stock_timeframe

def print_date_range():
    noof_days =1000
    thirty_days_ago = datetime.now() - timedelta(days=noof_days)
    from_date = thirty_days_ago.strftime("%Y-%m-%d %H:%M")
    to_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"from date:{from_date}")
    print(f"to_date :{to_date}")

def getStockData(profile_object, stock_token, stock_symbol):
    noof_days =2000
    thirty_days_ago = datetime.now() - timedelta(days=noof_days)
    from_date = thirty_days_ago.strftime("%Y-%m-%d %H:%M")
    to_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    #print(f"from date:{from_date}")
    #print(f"to_date :{to_date}")

#"20789", MOtison 5477 GRSE 3563 ADANIGREEN

    #Historic api
    candleParams={
        "exchange": "NSE",
        "symboltoken": str(stock_token),
        "interval": "ONE_DAY",
        "fromdate": from_date,
        "todate": to_date
    }

    candledetails=profile_object.getCandleData(candleParams)
    #print("Open High Low Close")
    #print(candledetails['data'])
    #logger.info(f"Histori)cal Data: {candledetails}")
    return candledetails['data']

def calculate_max_and_percentage(data):
    # Calculate the maximum and 75% of the maximum value
    sixth_elements = [entry[5] for entry in data]
    max_value = max(sixth_elements)
    seventy_percent = 0.7 * max_value
    print(f"max_value: {max_value}")
    print(f"seventy_percent: {seventy_percent}")
    return max_value, seventy_percent

def flag_with_deviation(data):
    # Convert the simulated data into a DataFrame
    df = pd.DataFrame(data, columns=["Date", "open", "high", "low", "Close", "Volume"])
    
    # Ensure 'Date' column is in datetime format
    df['Date'] = pd.to_datetime(df['Date'])

    # Step 1: Calculate average volume
    average_volume = df['Volume'].mean()
    print(f'Average Volume: {average_volume}')

    # Step 2: Identify peaks above average volume
    peaks = df[df['Volume'] > average_volume]

    # Step 3: Calculate average of identified peaks
    if not peaks.empty:
        average_peak_volume = peaks['Volume'].mean()
        print(f'Average Peak Volume: {average_peak_volume}')

        # Step 4: Identify secondary peaks above average of peaks
        secondary_peaks = peaks[(peaks['Volume'] > average_peak_volume) & (peaks['Close'] > peaks['open'])]

        # Step 5: Check deviations between Close values of peaks with at least 20 days gap
        results = []
        i=0
        j=0
        # Define today's date
        today = datetime.now(pytz.timezone('Asia/Kolkata'))
        for i in range(len(secondary_peaks)):
            if (i+j)<len(secondary_peaks):
                i = i+j
            
            date1, c_value1, volume1 = secondary_peaks.iloc[i][['Date', 'Close', 'Volume']]
            if ((today) - date1).days > 300:
               continue

            for j in range(i + 1, len(secondary_peaks)):
                date2, c_value2, volume2 = secondary_peaks.iloc[j][['Date', 'Close', 'Volume']]
                # Check if the second peak is within 180 days from today
                #if (today - date2).days > 300:
                #    continue

                if abs((date2 - date1).days) >= 60:
                    # Collect all C_values between the two peaks
                    values_between = df[(df['Date'] > date1) & (df['Date'] < date2)]['Close']

                    # Calculate the deviation as the difference between the peak values and the average of values in between
                    if not values_between.empty:
                        avg_between = values_between.mean()
                        #deviation1 = abs(c_value1 - avg_between)
                        #deviation2 = abs(c_value2 - avg_between)
                        std_between =  values_between.std()

                        within_10_percent = std_between <= 0.025 * avg_between
                        flag = True if within_10_percent else False
                        if flag == True and (c_value2>c_value1):
                            results.append({
                                'Peak 1': {'Date': date1, 'C_Value': c_value1, 'Volume': volume1},
                                'Peak 2': {'Date': date2, 'C_Value': c_value2, 'Volume': volume2},
                                'std deviation': std_between, 'Flag': flag
                            })
                        break

        # Print results
        #for result in results:
        #    print(result)

    else:
        print("No peaks above the average volume were found.")

    # Return only the latest value
    if results:
        # Sort results by the date of the first peak (latest first)
        latest_result = sorted(results, key=lambda x: x['Peak 1']['Date'], reverse=True)[0]
        print("Latest Peak Result:")
        print(latest_result)
    else:
        print("No valid peaks found.")


def main():
    obj=Do_login()
    print_date_range()
    

    data=getStockData(obj, 20789, "MOTION")
    #data=getStockData(obj, 19585, "BSE")
    print(data)
    #print(data)

    # Run all tasks concurrently
    #max_value, seventy_percent = calculate_max_and_percentage(data)
    #flag_pattern(data, seventy_percent)
    flag_with_deviation(data)

if __name__ == "__main__":
    main()

'''
                  
    # Find elements greater than 75% of max
    greater_indices_task = asyncio.create_task(find_elements_greater_than(seventy_five_percent))
    greater_indices = await greater_indices_task
                    
    # Compare 5th elements of consecutive greater 6th elements
    comparisons_task = asyncio.create_task(compare_fifth_elements(greater_indices))
    comparisons = await comparisons_task
                    
    # Output results
    print(f"Maximum of 6th elements: {max_value}")
    print(f"75% of the maximum value: {seventy_five_percent}")
    print(f"Indices of elements greater than 75% of max: {greater_indices}")
    print(f"Comparisons of 5th elements: {comparisons}")
'''

# Run the asynchronous main function

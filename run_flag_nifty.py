import flag1_updated
import pandas as pd
import time

df = pd.read_csv("filtered_file.csv", usecols=['token', 'symbol'])
print("-----------------------------------------------------------------")
print("                  SARAS FLAG PATTERN DEMO                        ")
print("-----------------------------------------------------------------")

obj=flag1_updated.Do_login()
print("Login Successful")
flag1_updated.print_date_range()
for i in range(200):  
    print("------------------------------------------------------")
    print(f"SYMBOL: {df['symbol'][i]} SYMBOLTKEN: {df['token'][i]}")  
    data=flag1_updated.getStockData(obj, df['token'][i], df['symbol'][i])
    #max_value, seventy_percent = flag1.calculate_max_and_percentage(data)
    flag1_updated.flag_with_deviation(data)
    time.sleep(2)
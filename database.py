import psycopg2 as ps
import pandas as pd
import requests

# used for controlling postgresql database
class database:
  # When calling the class, the variables in the __init__ function are also inputted by the user
  def __init__(self, host, user, password, database, port):
    self.host = host
    self.user = user
    self.password = password
    self.database = database
    self.port = port
  
  def connect(self):
    connection = ps.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
    return connection

  def stock_data(self, symbol):

    # retriving json file with price and volume data
    time_series_daily = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey=YW9W7ZBX5RBNC6V7'
    overview = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey=YW9W7ZBX5RBNC6V7'

    # requesting data from link
    r_time_series_daily = requests.get(time_series_daily)
    r_overview = requests.get(overview)

    # sticking data into a json file from that link
    time_series_data = r_time_series_daily.json()
    overview_data = r_overview.json()

    # converting json keys into list and then deleting unecessary keys
    keys = list(overview_data.keys())
    del keys[1:13]
    del keys[29:-1]
    del keys[-1]

    # command when called inserts data from json file into database
    command = f'''
        insert into public.overview_data (
            symbol, 
            marketcapitalization, 
            ebitda, 
            peratio, 
            pegratio, 
            bookvalue, 
            dividendpershare, 
            dividendyield, 
            eps, 
            revenuepersharettm, 
            profitmargin, 
            operatingmarginttm, 
            returnonassetsttm, 
            returnonequityttm, 
            revenuettm, 
            grossprofitttm, 
            dilutedepsttm, 
            quarterlyearningsgrowthyoy, 
            quarterlyrevenuegrowthyoy, 
            analysttargetprice, 
            trailingpe, 
            forwardpe, 
            pricetosalesratiottm, 
            pricetobookratio, 
            evtorevenue, 
            evtoebitda, 
            beta, 
            yearly_weekhigh, 
            yearly_weeklow
        )  
        values (
            '{overview_data[keys[0]]}',
            {overview_data[keys[1]]},
            {overview_data[keys[2]]},
            {overview_data[keys[3]]},
            {overview_data[keys[4]]},
            {overview_data[keys[5]]},
            {overview_data[keys[6]]},
            {overview_data[keys[7]]},
            {overview_data[keys[8]]},
            {overview_data[keys[9]]},
            {overview_data[keys[10]]},
            {overview_data[keys[11]]},
            {overview_data[keys[12]]},
            {overview_data[keys[13]]},
            {overview_data[keys[14]]},
            {overview_data[keys[15]]},
            {overview_data[keys[16]]},
            {overview_data[keys[17]]},
            {overview_data[keys[18]]},
            {overview_data[keys[19]]},
            {overview_data[keys[20]]},
            {overview_data[keys[21]]},
            {overview_data[keys[22]]},
            {overview_data[keys[23]]},
            {overview_data[keys[24]]},
            {overview_data[keys[25]]},
            {overview_data[keys[26]]},
            {overview_data[keys[27]]},
            {overview_data[keys[28]]}
        );    
        '''
    self.insert(command)

    # returns last 30 trading days
    trade_dates = list(time_series_data['Time Series (Daily)'].keys())[0:30]
    
    trade_dates = trade_dates[::-1]
    # iterating through the last 30 trading dates to put price and volume data into database
    for dates in trade_dates:
        open = time_series_data['Time Series (Daily)'][dates]['1. open']
        high = time_series_data['Time Series (Daily)'][dates]['2. high']
        low = time_series_data['Time Series (Daily)'][dates]['3. low']
        close = time_series_data['Time Series (Daily)'][dates]['4. close']
        volume = time_series_data['Time Series (Daily)'][dates]['6. volume']
        
        command = f'''
            insert into public.all_stock_data (
            symbol,    
            trade_date,
            open_price,
            high_price,
            low_price,
            close_price,
            volume
            )
            values (
            '{symbol}',
            '{dates}',
            {open},
            {high},
            {low},
            {close},
            {volume}
            );
        '''
        self.insert(command)

  # function that selects required data requested from user and inserts it into a pandas dataframe for manipulation
  def select_to_df(self, command):
    # connecting to database
    connection = self.connect()
    try:
        # executing command in database
        cursor = connection.cursor()
        cursor.execute(command)
        print('Connected to database!')
        # creating columns and rows for pandas dataframe
        all_data = []
        columns = []
        
        for column in cursor.description:
          columns.append(column[0])
        for rows in cursor.fetchall():
          all_data.append(dict(zip(columns, rows)))
        
        # creating pandas dataframe
        connection.commit()
        return pd.DataFrame(all_data)
        
    except Exception as error:
      print('Execution Failed: ', error)
    finally:
      connection.close()

  def insert(self, command):
    connection = self.connect()
    try:
        cursor = connection.cursor()
        cursor.execute(command)
        print('Inserted Successfully')
        connection.commit()
    except Exception as error:
        print('Insert Failed: ', error)
    finally:
        connection.close()

# Variables are empty so other people cannot see private database information
db = database('db.bit.io', 'aditya16dhiman', 'v2_443VN_G3sgHuvR6ShwbeDZZ2xQe2X', 'aditya16dhiman.stockdb', '5432')
print(db.connect())
# print(db.select_to_df('''
# select symbol, trade_date, open_price, high_price, low_price, close_price, volume
# from public.all_stock_data
# '''))
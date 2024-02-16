import psycopg2 as ps
import pandas as pd
import os
from dotenv import load_dotenv
from stockmarketdata import smd

# used for controlling postgresql database
class database:
  # When calling the class, the variables in the __init__ function are also inputted by the user
  def __init__(self, host: str, user, password, database, port, api_key) -> None:
    self.host = host
    self.user = user
    self.password = password
    self.database = database
    self.port = port
    self.api_key = api_key
  
  def connect(self) -> None:
    connection = ps.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
    return connection

  def insert_data(self, symbol):

    # obtaining data from all_data file
    time_series_data = smd.TIME_SERIES_DAILY(symbol)
    overview_data = smd.COMPANY_OVERVIEW(symbol)

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
    self.execute(command)

    # returns last 30 trading days
    trade_dates = list(time_series_data['Time Series (Daily)'].keys())[0:30]
    
    trade_dates = trade_dates[::-1]
    # iterating through the last 30 trading dates to put price and volume data into database
    for dates in trade_dates:
        open = time_series_data['Time Series (Daily)'][dates]['1. open']
        high = time_series_data['Time Series (Daily)'][dates]['2. high']
        low = time_series_data['Time Series (Daily)'][dates]['3. low']
        close = time_series_data['Time Series (Daily)'][dates]['4. close']
        volume = time_series_data['Time Series (Daily)'][dates]['5. volume']
        
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
        self.execute(command)

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

  def execute(self, command):
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

load_dotenv()

HOST = os.getenv('HOST')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
DATABASE = os.getenv('DATABASE')
PORT = os.getenv('PORT')
API_KEY = os.getenv('API_KEY')

print(HOST, USER, PASSWORD, DATABASE, PORT, API_KEY)
# Variables are empty so other people cannot see private database information
db = database(HOST, USER, PASSWORD, DATABASE, PORT, API_KEY)
print(db.connect())
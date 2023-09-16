from flask import Flask, render_template, jsonify, request
from database import db
from calculations import calc

# initializing flask application, specifying html folder
app = Flask(__name__,  template_folder="frontend")

# creating app route for the home screen
@app.route('/')
def interface():
    return render_template('home.html')

# creating app route for stock report screen, using GET method to get stock ticker symbol from search bar
@app.route('/stock_report', methods=['GET'])
def stock_report():

    # requesting stock ticker symbol
    symbol = request.args.get('symbol')

    # obtaining time series data from database
    time_series_data = db.select_to_df(f'''
    select * from public.all_stock_data where symbol = '{symbol}' ''')

    # obtaining overview data from database
    overview_data = db.select_to_df(f'''
    select * from public.overview_data where symbol = '{symbol}' ''')

    # obtaining various data points to put into calculations functions
    beta = overview_data['beta'][0]
    yearly_weekhigh = overview_data['yearly_weekhigh'][0]
    yearly_weeklow = overview_data['yearly_weeklow'][0]
    current_price = time_series_data['close_price'][29]
    peg_ratio = overview_data['pegratio'][0]
    dividend_yield = overview_data['dividendyield'][0]
    prices = time_series_data['close_price']

    # putting data into calculations functions
    beta = calc.beta_Volatility(beta)
    high_low = calc.yearly_high_low_BullBear(yearly_weekhigh, yearly_weeklow, current_price)
    peg = calc.peg_ratio_BullBear(peg_ratio)
    dividend = calc.dividend_yield_Volatility(dividend_yield)
    prices = list(time_series_data['close_price'])
    dates = list(time_series_data['trade_date'])
    cv = calc.volatility_variation(prices)

    # rendering stock screen template, passing calculations to the stock report template
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    return render_template('stock_report.html', beta=beta, high_low=high_low, peg=peg, dividend=dividend, prices=prices, dates=dates , symbol=symbol, cv=cv)


@app.route('/settings', methods=['GET'])
def settings():

    symbol = request.args.get('symbol')
    insert_status = 'Not Active'

    try:
        db.stock_data(symbol)
        insert_status = 'Successful'
    except:
        insert_status = 'Failed'
    
    return render_template('settings.html', insert_status=insert_status)

if __name__ == '__main__':
    app.run(debug=True)
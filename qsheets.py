# import all the required dependencies
from dateutil.relativedelta import relativedelta
from datetime import date, datetime, timedelta
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from questrade_api import Questrade
import argparse
import pandas as pd
from pandas.io.json import json_normalize

# import the script settings
import qsheets_settings as qs

# load market holidays into global list
def holidays():
    """ returns a list of market holidays

    Returns
    -------
    list
        list of market holiday dates
    """

    holidays = []

    with open( qs.HOLIDAYS, 'r') as filehandle:
        for line in filehandle:
            h = date.fromisoformat( line[:-1])
            holidays.append( h)
    return holidays

def go_back_to_last_trading_day( d):
    """Returns the last valid trading day

    Parameters
    ----------
    d : date
        The requested trading day

    Returns
    -------
    date
        The last valid trading day before the requested input day. Can be the same date.
    """

    while d.weekday() == 5 or d.weekday() == 6 or d in holidays(): 
        d = d - relativedelta( days = 1)
    return d


def return_dates( td):
    """Computes and returns the dates for the return values (years) defined in settings

    Parameters
    ----------
    d : date
        The requested trading day

    Returns
    -------
    list
        List of return dates based on the years specified in settings
    """

    return_dates = []

    for r in qs.RETURNYEARS:
        d = td - relativedelta( years = r)      # go back X years
        d = go_back_to_last_trading_day( d)     # make sure it is a trading day
        return_dates.append( d)

    return return_dates


def prices( q, symbol, ndays=1, day=date.today()):
    """Retrieves date, open, low, high, close, volume information for given date(s) from Questrade

    This function is the main interface to Questrade. It looks up the internal stock id
    for a given symbol string and returns ohlc + volume for the symbol. By default
    it returns a candle for the current day. Note that this is realtime data, even without
    purchasing any additional data packages. It is essentially a snap quote for a symbol.
    Note that the symbol convention does not necessarily follow the Questrade IQ Edge convention,
    e.g. for TSX Venture the API wants a ".V" suffix whereas IQ Edge uses ".VN". An example:
    For EXRO Technologies the symbol is "EXRO.VN" in IQ Edge, but the API requires
    "EXRO.V" (this follows the Yahoo Finance nomenclauture)

    Parameters
    ----------
    q : Questrade API object (as defined in questrade_api interface)
        Instance of main Questrade API object. Must the authenticated.
    symbol: str
        Name of stock symbol. Follows Yahoo Finance convention
    ndays: int
        Number of days/candles to retrieve. Questrade limit is 2,000 candles (roughly 2,800 days) per call
        default is 1
    day: date
        Starting date. If run on a weekend or market holiday the day will be last trading day

    Returns
    -------
    dataframe
        Pandas dataframe table of prices  (start,open,high,low,close,colume) given the input parameters
        By default the table only contains one row with the values for the last trading day / current day
    """

    id = q.symbols_search( prefix=symbol)['symbols'][0]['symbolId']

    d2 = go_back_to_last_trading_day( day)
    dt2 = d2.isoformat() + 'T23:23:59-07:00'
    d1 = d2 - timedelta( days=ndays-1)
    dt1 = d1.isoformat() + 'T00:00:00-07:00'

    df = json_normalize( q.markets_candles( id, startTime=dt1, endTime=dt2, interval='OneDay'), record_path =['candles'])
    if len( df.index) > 0:
        df = df.drop(['VWAP','end'], axis=1)
        df = df[['start','open','high','low','close','volume']]
        df = df.sort_values(['start'], ascending=False)

    return df

def quotes( q, client):
    """Populates the content of all the sheets in the Google Sheet named OHLCData in settings

    This function traverses all the sheets in the document and populates columns B thru E starting
    at row 2. Column A must contain a valid symbol strings (e.g. SU.TO, EXRO.V, AAPL, etc.)

    Parameters
    ----------
    q : Questrade object
        Instance of main Questrade API object. Must be authenticated.
    client: gspread object
        This object provides the interface to Google Sheets. Must be authenticated.
    """

    for doc in qs.DOCS:
        
        try:
            spreadsheet = client.open( doc['name'])
        except:
            print( 'Document', doc['name'], 'does not exist')
        else:
            print( '++++++++++++++++++++++')
            print( '+ Doc:', spreadsheet.title)
            print( '++++++++++++++++++++++')
            # Data sheet
            try:
                data = spreadsheet.worksheet( doc['quotesheet'])
            except:
                print( 'sheet:', doc['quotesheet'], 'does not exist in the document', doc['name'])
            else:
                print( '+', data.title)
                print( '+', datetime.now().strftime( '%b-%d-%Y %H:%M:%S'))
                print( '++++++++++++++++++++++')
                symbols = data.get( 'A2:A')
                arr = []
                for stock in symbols:
                    ohlc = []
                    p = prices( q, stock[0])
                    if len( p.index) > 0:
                        ohlc.append( float( p.at[0,'open']))
                        ohlc.append( float( p.at[0,'high']))
                        ohlc.append( float( p.at[0,'low']))
                        ohlc.append( float( p.at[0,'close']))
                        arr.append( ohlc) 
                        print( str( stock[0]), ' - ', '${:,.2f}'.format( p.at[0,'close']))
                        data.update( 'B2:E101', arr)
                time.sleep( qs.SLEEPTIME)
            # Sparkline sheet
            try:
                data = spreadsheet.worksheet( doc['slsheet'])
            except:
                print( 'sheet:', doc['slsheet'], 'does not exist in the document', doc['name'])
            else:
                print( '++++++++++++++++++++++')
                print( '+', data.title)
                print( '+', datetime.now().strftime( '%b-%d-%Y %H:%M:%S'))
                print( '++++++++++++++++++++++')
                symbols = data.col_values( 1)
                arr = []
                for stock in symbols:
                    print( stock)
                    p = prices( q, stock, 60)
                    arr.append( p['close'].tolist())
                data.update( 'B1:BZ100', arr)
                time.sleep( qs.SLEEPTIME)
            # Returns sheet
            try:
                data = spreadsheet.worksheet( doc['returnsheet'])
            except:
                print( 'sheet:', doc['slsheet'], 'does not exist in the document', doc['name'])
            else:
                print( '++++++++++++++++++++++')
                print( '+', data.title)
                print( '+', datetime.now().strftime( '%b-%d-%Y %H:%M:%S'))
                print( '++++++++++++++++++++++')
                td = go_back_to_last_trading_day( date.today())
                dates = return_dates( td)
                symbols = data.get( 'A2:A')
                arr = []
                for stock in symbols:
                    s = str( stock[0])
                    print( s)
                    ret = []
                    for d in dates:
                        p = prices( q, s, 1, d)
                        if len( p.index) > 0:
                            print( d.isoformat() + '   close: ' + '${:.2f}'.format( p.at[0,'close']))
                            ret.append( p.at[0, 'close'])
                    arr.append( ret)
                data.update( 'B2:Z100', arr)
  
def parse_args():

    parser = argparse.ArgumentParser( description='Trading Sheets updater')
    parser.add_argument('-c','--continuous')
    return parser.parse_args()

def main():

    args = parse_args()

    # authorize Questrade API after creating a new token
    #q = Questrade( refresh_token='SKmIASNtWxSTyoKy2tmx-oCFK_zH0bge0')

    # after first run comment out the statement above and use:
    q = Questrade()

    print( q)

    #Authorize the API
    scope = [
         'https://www.googleapis.com/auth/drive',
         'https://www.googleapis.com/auth/drive.file'
         ]
        
    file_name = 'client_key.json'
    creds = ServiceAccountCredentials.from_json_keyfile_name( file_name, scope)
    client = gspread.authorize( creds)

    if args.continuous:
        while True:
            quotes( q, client)
    else:
        quotes(q, client)

if __name__ == '__main__':
    main()

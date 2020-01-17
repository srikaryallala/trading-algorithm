# Imports
from quantopian.algorithm import attach_pipeline, pipeline_output
from quantopian.pipeline import Pipeline, CustomFactor
import quantopian.pipeline.filters as Filters
import quantopian.pipeline.factors as Factors
import pandas as pd
import numpy as np
from quantopian.pipeline.data.builtin import USEquityPricing
 
 
# Stocks to be traded
MY_STOCKS = symbols('AAPL', 'ACN', 'AMZN', 'T', 'CSCO', 'CMCSA',
         'EBAY', 'FB', 'GOOG', 'HPQ', 'INTC', 'IBM',
         'MSFT', 'ORCL', 'QCOM', 'TXN', 'TWX', 'FOXA', 'VZ', 'DIS',
         'ADBE', 'ADI', 'ADSK', 'AKAM', 'AMAT', 'APH', 'AVGO',
         'CA', 'CBS', 'CERN', 'CRM', 'CTL', 'CTSH', 'CTXS', 'DISCA',
         'DISCK', 'DNB', 'EA', 'EXPE', 'FFIV', 'FIS', 'FISV',
         'FLIR', 'GCI', 'INTU', 'IPG', 'JNPR', 'KLAC', 'LLTC',
         'LRCX', 'LVLT', 'MCHP', 'MSI', 'MU', 'NFLX', 'NTAP',
         'NVDA', 'NWSA', 'OMC', 'PAYX', 'PBI', 'PCLN', 'RHT', 'STX',
         'SYMC', 'TDC', 'TEL', 'TRIP', 'VIAB', 'VRSN', 'WDC',
         'WIN', 'XLNX', 'YHOO', 'XRX')
 
# Position weights
WEIGHT = 1.0 / len(MY_STOCKS)
 
def initialize(context): 
    # Attach the pipeline
    attach_pipeline(pipe_definition(context), name='my_data')
  
    # Schedule trading frequency
    schedule_function(trade, date_rules.every_day(), time_rules.market_open())
 
    # Schedule data recording frequency
    schedule_function(record_vars, date_rules.every_day(), time_rules.market_close())
 
         
def pipe_definition(context):  
    # Initialize trading universe
    universe = Filters.StaticAssets(MY_STOCKS)
    
    # Record close price of stocks
    close_price = USEquityPricing.close.latest
 
    # Record Simple Moving Averages for short and long-terms
    smaRecent = Factors.SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=100, mask=universe)
    smaLong = Factors.SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=200, mask=universe) 
 
    # Return pipeline with columns and screen specified
    return Pipeline(
            columns = {
            'close_price' : close_price,
            'smaRecent' : smaRecent,
            'smaLong' : smaLong,
            },
            screen = universe,
            )
    
 
def before_trading_start(context, data):
    # Get a dataframe for our pipeline data
    context.output = pipeline_output('my_data')
       
   
def trade(context, data):
    
    # Buy stocks if long-term SMA is greater than the short-term SMA
    open_rules = 'smaLong > smaRecent'
    open_these = context.output.query(open_rules).index.tolist()
 
    for stock in open_these:
        if stock not in context.portfolio.positions and data.can_trade(stock):
            order_target_percent(stock, WEIGHT)
    
    # Close stocks if vice-versa
    close_rules = 'smaLong < smaRecent'
    close_these = context.output.query(close_rules).index.tolist()
 
    for stock in close_these:
        if stock in context.portfolio.positions and data.can_trade(stock):
            order_target_percent(stock, WEIGHT)
 
                  
 
def record_vars(context, data):
    # Record positions
    record(leverage=context.account.leverage,
           positions=len(context.portfolio.positions))

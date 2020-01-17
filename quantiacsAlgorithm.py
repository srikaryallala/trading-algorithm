import numpy

def myTradingSystem(DATE, OPEN, HIGH, LOW, CLOSE, VOL, OI, P, R, RINFO, exposure, equity, settings):
    ''' This system uses trend following techniques to allocate capital into the desired equities'''

    nMarkets=CLOSE.shape[1]

    periodLong=200 #%[200:10:300]#
    periodShort=10 #%[20:10:100]#

    smaLong=numpy.nansum(CLOSE[-periodLong:,:],axis=0)/periodLong
    smaRecent=numpy.nansum(CLOSE[-periodShort:,:],axis=0)/periodShort

    longEquity= numpy.array(smaRecent > smaLong)
    shortEquity= ~longEquity

    pos=numpy.zeros((1,nMarkets))
    pos[0,longEquity]=1
    pos[0,shortEquity]=0.5

    weights = pos/numpy.nansum(abs(pos))

    return weights, settings


def mySettings():
    ''' Define your trading system settings here '''

    settings= {}


    # Futures Contracts

    settings['markets'] = ['AAPL', 'ACN', 'AMZN', 'T', 'CSCO', 'CMCSA',
		 'EBAY', 'FB', 'GOOG', 'GOOGL', 'HPQ', 'INTC', 'IBM',
		 'MSFT', 'ORCL', 'QCOM', 'TXN', 'TWX', 'FOXA', 'VZ', 'DIS',
		 'ADBE', 'ADI', 'ADSK', 'AKAM', 'AMAT', 'APH', 'AVGO',
		 'CA', 'CBS', 'CERN', 'CRM', 'CTL', 'CTSH', 'CTXS', 'DISCA',
		 'DISCK', 'DNB', 'EA', 'EXPE', 'FFIV', 'FIS', 'FISV',
		 'FLIR', 'GCI', 'INTU', 'IPG', 'JNPR', 'KLAC', 'LLTC',
		 'LRCX', 'LVLT', 'MCHP', 'MSI', 'MU', 'NFLX', 'NTAP',
		 'NVDA', 'NWSA', 'OMC', 'PAYX', 'PBI', 'PCLN', 'RHT', 'STX',
		 'SYMC', 'TDC', 'TEL', 'TRIP', 'VIAB', 'VRSN', 'WDC',
		 'WIN', 'XLNX', 'YHOO', 'XRX']
    settings['endInSample'] = '20191224'
    settings['beginInSample'] = '20100101'
    # settings['beginInSample'] = '20120506'
    # settings['endInSample'] = '20150506'
    settings['lookback'] = 504
    settings['budget'] = 1000000
    settings['slippage'] = 0.05

    return settings

# Evaluate trading system defined in current file.
if __name__ == '__main__':
    from toolkit import quantiacsWeb
    results = quantiacsWeb.runtsWeb(__file__)
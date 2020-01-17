import numpy

def myTradingSystem(DATE, OPEN, HIGH, LOW, CLOSE, VOL, OI, P, R, RINFO, exposure, equity, settings):

    nMarkets=CLOSE.shape[1]

    periodLong=200
    periodShort=10

    #Calculates Simple Moving Average for Short and Long periods
    smaLong=numpy.nansum(CLOSE[-periodLong:,:],axis=0)/periodLong
    smaRecent=numpy.nansum(CLOSE[-periodShort:,:],axis=0)/periodShort

    #Goes long if short-term SMA is greater than long-term and short if vice-versa
    longEquity= numpy.array(smaRecent > smaLong)
    shortEquity= ~longEquity

    pos=numpy.zeros((1,nMarkets))
    #Places positions
    pos[0,longEquity]=1
    pos[0,shortEquity]=0.5

    weights = pos/numpy.nansum(abs(pos))

    return weights, settings


def mySettings():
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
    settings['lookback'] = 504
    settings['budget'] = 1000000
    settings['slippage'] = 0.05

    return settings

# Evaluate trading system defined in current file.
if __name__ == '__main__':
    from toolkit import quantiacsWeb
    results = quantiacsWeb.runtsWeb(__file__)

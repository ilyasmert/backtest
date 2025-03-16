import backtrader as bt
import datetime
import argparse
from strategies import HedgeSMACrossoverModified

def run_backtest(csvfile, dtformat='%Y.%m.%d %H:%M'):
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(1_000_000.0)
    cerebro.addstrategy(HedgeSMACrossoverModified)

    data_long = bt.feeds.GenericCSVData(
        dataname=csvfile,
        dtformat=dtformat,
        datetime=0,
        fromdate=datetime.datetime(2025, 1, 28),
        todate=datetime.datetime(2025, 3, 2),
        timeframe=bt.TimeFrame.Minutes,
        compression=1,
        time=-1,
        open=1,
        high=2,
        low=3,
        close=4,
        volume=5,
        openinterest=-1,
        header=False
    )
    data_long._name = "LongFeed"

    data_short = bt.feeds.GenericCSVData(
        dataname=csvfile,
        dtformat=dtformat,
        datetime=0,
        timeframe=bt.TimeFrame.Minutes,
        compression=1,
        time=-1,
        open=1,
        high=2,
        low=3,
        close=4,
        volume=5,
        openinterest=-1,
        header=False
    )
    data_short._name = "ShortFeed"

    cerebro.adddata(data_long)
    cerebro.adddata(data_short)
    
    print("Starting Portfolio Value:", cerebro.broker.getvalue())
    cerebro.run()
    print("Final Portfolio Value:", cerebro.broker.getvalue())
    cerebro.plot(style='candlestick', numfigs=1, volume=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', required=True, help='resampled_data.csv')
    args = parser.parse_args()
    run_backtest(args.data)

import backtrader as bt
import argparse
from strategies import SMACrossover

def run_backtest(csvfile, dtformat='%Y.%m.%d %H:%M'):
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(1_000_000.0)

    cerebro.addstrategy(SMACrossover)

    data = bt.feeds.GenericCSVData(
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
        header=0
    )

    cerebro.adddata(data)

    print("Starting Portfolio Value:", cerebro.broker.getvalue())
    cerebro.run()
    print("Final Portfolio Value:", cerebro.broker.getvalue())

    cerebro.plot()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', required=True, help='Path to your 1-min CSV file')
    args = parser.parse_args()

    run_backtest(args.data)

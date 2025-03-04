import backtrader as bt
import argparse
from strategies import SMACrossover

def run_backtest(csvfile, dtformat='%Y.%m.%d %H:%M'):
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(1_000_000.0)

    # Add our strategy
    cerebro.addstrategy(SMACrossover)

    # Create data feed
    data = bt.feeds.GenericCSVData(
        dataname=csvfile,
        dtformat=dtformat,
        datetime=0,
        timeframe=bt.TimeFrame.Minutes,
        period = bt.TimeFrame.Ticks,
        compression = 1,
        time=-1,
        open=1,
        high=2,
        low=3,
        close=4,
        volume=5,
        openinterest=-1,
        # If your CSV has no header row, specify:
        header=0,
        # fromdate=datetime.datetime(2025, 1, 1),
        # todate=datetime.datetime(2025, 1, 31),
    )

    cerebro.adddata(data)

    print("Starting Portfolio Value:", cerebro.broker.getvalue())
    cerebro.run()
    print("Final Portfolio Value:", cerebro.broker.getvalue())

    # Optionally plot
    cerebro.plot()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', required=True, help='Path to your 1-min CSV file')
    args = parser.parse_args()

    run_backtest(args.data)

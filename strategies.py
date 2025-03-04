import backtrader as bt

class SMACrossover(bt.Strategy):
    params = (
        ('fast_period', 10),
        ('slow_period', 30),
    )

    def __init__(self):
        # Calculate 2 SMAs on the single data feed (self.datas[0])
        self.sma_fast = bt.indicators.SimpleMovingAverage(
            self.datas[0],
            period=self.p.fast_period
        )
        self.sma_slow = bt.indicators.SimpleMovingAverage(
            self.datas[0],
            period=self.p.slow_period
        )

        # We'll use a simple cross indicator
        self.crossover = bt.indicators.CrossOver(self.sma_fast, self.sma_slow)
        
    def notify_order(self, order):
        if order.status in [order.Completed]:
            print(f"{self.data.datetime.datetime(0)}: Order Completed")
        elif order.status in [order.Rejected, order.Margin, order.Canceled]:
            print(f"{self.data.datetime.datetime(0)}: Order Rejected/Margin/Canceled")


    def next(self):
        # If we don't have a position and the fast SMA crosses above slow
        if not self.position:
            if self.crossover > 0:
                self.buy()
                print(f"{self.data.datetime.datetime(0)}: BUY at {self.data.close[0]}")
        else:
            # If we do have a position and the fast SMA crosses below slow
            if self.crossover < 0:
                self.sell()
                print(f"{self.data.datetime.datetime(0)}: SELL at {self.data.close[0]}")

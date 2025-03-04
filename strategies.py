import backtrader as bt

class SMACrossover(bt.Strategy):
    params = (
        ('fast_period', 10),
        ('slow_period', 30),
    )

    def __init__(self):
        # Calculate 2 SMAs on the single data feed (self.datas[0])
        self.sma_fast = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.p.fast_period
        )
        self.sma_slow = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.p.slow_period
        )

        # We'll use a simple cross indicator
        self.crossover = bt.indicators.CrossOver(self.sma_fast, self.sma_slow)

    def notify_order(self, order):
        if order.status in [order.Completed]:
            print(f"{self.data.datetime.datetime(0)}: Order Completed")
        elif order.status in [order.Rejected, order.Margin, order.Canceled]:
            print(f"{self.data.datetime.datetime(0)}: Order Rejected/Margin/Canceled")

    def next(self):
        # -----------
        # CASE 1: No position
        # -----------
        if not self.position:
            # If the fast SMA crosses above slow => open a Long
            if self.crossover > 0:
                print(f"{self.data.datetime.datetime(0)}: LONG signal at {self.data.close[0]}")
                self.buy()
            # If the fast SMA crosses below slow => open a Short
            elif self.crossover < 0:
                print(f"{self.data.datetime.datetime(0)}: SHORT signal at {self.data.close[0]}")
                self.sell()

        # -----------
        # CASE 2: Already in a position (either long or short)
        # -----------
        else:
            # If we have a LONG position and get a SHORT signal, switch to short
            if self.position.size > 0 and self.crossover < 0:
                print(f"{self.data.datetime.datetime(0)}: SWITCH to SHORT at {self.data.close[0]}")
                self.close()   # close the existing long
                self.sell()    # open a short

            # If we have a SHORT position and get a LONG signal, switch to long
            elif self.position.size < 0 and self.crossover > 0:
                print(f"{self.data.datetime.datetime(0)}: SWITCH to LONG at {self.data.close[0]}")
                self.close()   # close the existing short
                self.buy()     # open a long

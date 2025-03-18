import backtrader as bt

class HedgeSMACrossoverModified(bt.Strategy):
    params = (
        # For both sides, use SMA(7) and SMA(50)
        ('fast_period', 7),
        ('slow_period', 50),
        # Exit thresholds (as decimals)
        ('profit_target', 0.05),    # 5% favorable move
        ('stop_loss', 0.02),        # 2% adverse move
    )

    def __init__(self):
        # Long feed: datas[0]
        self.sma_long_fast = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.p.fast_period, plot=True)
        self.sma_long_slow = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.p.slow_period, plot=True)
        self.crossover_long = bt.indicators.CrossOver(self.sma_long_fast, self.sma_long_slow, plot=True)

        # Short feed: datas[1]
        self.sma_short_fast = bt.indicators.SimpleMovingAverage(self.datas[1], period=self.p.fast_period, plot=True)
        self.sma_short_slow = bt.indicators.SimpleMovingAverage(self.datas[1], period=self.p.slow_period, plot=True)
        self.crossover_short = bt.indicators.CrossOver(self.sma_short_fast, self.sma_short_slow, plot=True)

        # We'll store entry prices for each side:
        self.long_entry_price = None
        self.short_entry_price = None

    def notify_order(self, order):
        dt = order.data.datetime.datetime(0)
        if order.status in [order.Completed]:
            print(f"{dt}: Order Completed on {order.data._name}")
        elif order.status in [order.Rejected, order.Margin, order.Canceled]:
            print(f"{dt}: Order Rejected/Margin/Canceled on {order.data._name}")

    def next(self):
        #print(f"LongFeed time: {self.datas[0].datetime.datetime(0)} | "
         # f"ShortFeed time: {self.datas[1].datetime.datetime(0)}")
        long_data = self.datas[0]
        pos_long = self.getposition(long_data).size
        price_long = long_data.close[0]
        if pos_long == 0:
            # Enter long if SMA(7) crosses up SMA(50)
            if self.crossover_long > 0:
                print(f"{long_data.datetime.datetime(0)}: LONG signal on {long_data._name} at {price_long}")
                self.buy(data=long_data, size=1)
                self.long_entry_price = price_long
        else:
            # Exit long if price moves 5% in favor or 2% against the entry
            if self.long_entry_price:
                # For a long, a favorable move is an increase, an adverse move is a decrease.
                if price_long >= self.long_entry_price * (1 + self.p.profit_target):
                    print(f"{long_data.datetime.datetime(0)}: LONG profit target reached at {price_long} (entry: {self.long_entry_price})")
                    self.close(data=long_data)
                    self.long_entry_price = None
                elif price_long <= self.long_entry_price * (1 - self.p.stop_loss):
                    print(f"{long_data.datetime.datetime(0)}: LONG stop loss triggered at {price_long} (entry: {self.long_entry_price})")
                    self.close(data=long_data)
                    self.long_entry_price = None
            # Also, if the SMA crossover reverses, you might choose to exit.
            elif self.crossover_long < 0:
                print(f"{long_data.datetime.datetime(0)}: LONG exit signal on {long_data._name} at {price_long}")
                self.close(data=long_data)
                self.long_entry_price = None

        # Process ShortFeed (datas[1])
        short_data = self.datas[1]
        pos_short = self.getposition(short_data).size
        price_short = short_data.close[0]
        if pos_short == 0:
            # Enter short if SMA(7) crosses down SMA(50)
            if self.crossover_short < 0:
                print(f"{short_data.datetime.datetime(0)}: SHORT signal on {short_data._name} at {price_short}")
                self.sell(data=short_data, size=1)
                self.short_entry_price = price_short
        else:
            # For a short, a favorable move is a drop and an adverse move is a rise.
            if self.short_entry_price:
                if price_short <= self.short_entry_price * (1 - self.p.profit_target):
                    print(f"{short_data.datetime.datetime(0)}: SHORT profit target reached at {price_short} (entry: {self.short_entry_price})")
                    self.close(data=short_data)
                    self.short_entry_price = None
                elif price_short >= self.short_entry_price * (1 + self.p.stop_loss):
                    print(f"{short_data.datetime.datetime(0)}: SHORT stop loss triggered at {price_short} (entry: {self.short_entry_price})")
                    self.close(data=short_data)
                    self.short_entry_price = None
            elif self.crossover_short > 0:
                print(f"{short_data.datetime.datetime(0)}: SHORT exit signal on {short_data._name} at {price_short}")
                self.close(data=short_data)
                self.short_entry_price = None

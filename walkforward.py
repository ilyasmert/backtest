import backtrader as bt
import datetime as dt
import argparse
from strategies import HedgeSMACrossoverModified

# Define a function to run a backtest for a given date window and parameters
def run_backtest_with_params(csvfile, dtformat, fromdate, todate, params):
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(1_000_000.0)
    # Add our strategy with the given parameters
    cerebro.addstrategy(HedgeSMACrossoverModified,
                        long_fast=params['long_fast'],
                        long_slow=params['long_slow'],
                        short_fast=params['short_fast'],
                        short_slow=params['short_slow'])
    
    # Create a single data feed using the given date window
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
        header=0,
        fromdate=fromdate,
        todate=todate
    )
    cerebro.adddata(data)
    cerebro.run()
    return cerebro.broker.getvalue()

# Function to optimize the strategy parameters in the in-sample period
def optimize_in_sample(csvfile, dtformat, fromdate, todate, param_grid):
    cerebro = bt.Cerebro(optreturn=False)
    cerebro.broker.setcash(1_000_000.0)
    # Add optimization strategy with parameter grid using optstrategy
    cerebro.optstrategy(
        HedgeSMACrossoverModified,
        long_fast=param_grid['long_fast'],
        long_slow=param_grid['long_slow'],
        short_fast=param_grid['short_fast'],
        short_slow=param_grid['short_slow']
    )
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
        header=0,
        fromdate=fromdate,
        todate=todate
    )
    cerebro.adddata(data)
    
    # Run optimization (here using a single CPU for reproducibility)
    optimized_runs = cerebro.run(maxcpus=1)
    
    # Choose best parameters based on final portfolio value
    best_value = -float('inf')
    best_params = None
    for opt_run in optimized_runs:
        strat = opt_run[0]  # only one strategy per run in this case
        final_value = strat.broker.getvalue()
        if final_value > best_value:
            best_value = final_value
            best_params = {
                'long_fast': strat.params.long_fast,
                'long_slow': strat.params.long_slow,
                'short_fast': strat.params.short_fast,
                'short_slow': strat.params.short_slow,
            }
    print(f"In-sample {fromdate} to {todate} optimization: best final value = {best_value}, best params = {best_params}")
    return best_params

def walk_forward(csvfile, dtformat, overall_start, overall_end, in_sample_days, out_sample_days, param_grid):
    results = []
    current_start = overall_start
    while current_start + dt.timedelta(days=in_sample_days+out_sample_days) <= overall_end:
        in_start = current_start
        in_end = in_start + dt.timedelta(days=in_sample_days)
        out_start = in_end
        out_end = out_start + dt.timedelta(days=out_sample_days)
        
        # Optimize on the in-sample period
        best_params = optimize_in_sample(csvfile, dtformat, in_start, in_end, param_grid)
        # Test out-of-sample with best parameters
        out_value = run_backtest_with_params(csvfile, dtformat, out_start, out_end, best_params)
        print(f"Out-of-sample {out_start} to {out_end}: final value = {out_value}")
        results.append({
            'in_start': in_start, 'in_end': in_end,
            'out_start': out_start, 'out_end': out_end,
            'best_params': best_params, 'out_value': out_value
        })
        # Roll forward: move start to the beginning of out-of-sample period
        current_start = out_start
    return results

if __name__ == '__main__':
    import datetime as dt
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--data', required=True, help='Path to your 1-min CSV file')
    args = parser.parse_args()

    # Example datetime format – adjust if needed
    dtformat = '%Y.%m.%d %H:%M'

    # Define an in-sample period (for example, Jan 1, 2025 to Jan 16, 2025)
    in_sample_start = dt.datetime(2025, 1, 1)
    in_sample_end   = dt.datetime(2025, 2, 1)

    # Define a sample parameter grid for optimization:
    param_grid = {
        'long_fast': range(45, 56, 5),    # 45, 50, 55
        'long_slow': range(190, 211, 10), # 190, 200, 210
        'short_fast': range(7, 11, 1),     # 7, 8, 9, 10
        'short_slow': range(20, 24, 1),    # 20, 21, 22, 23
    }

    # Run the optimization on the in-sample period
    best_params = optimize_in_sample(args.data, dtformat, in_sample_start, in_sample_end, param_grid)

    print("Best in-sample parameters found:")
    print(best_params)

import time
import datetime as dt
import pandas as pd
from pybit.unified_trading import HTTP

def fetch_kline_data(symbol, start_dt, end_dt, interval='1', category='linear'):
    session = HTTP(testnet=False)  # or True for testnet
    start_ms = int(start_dt.timestamp() * 1000)
    end_ms   = int(end_dt.timestamp() * 1000)

    all_df = pd.DataFrame()

    while True:
        resp = session.get_kline(
            category=category,
            symbol=symbol,
            interval=interval,
            start=start_ms,
            end=end_ms,       # v5 get_kline supports 'end'
            limit=200         # up to 200 bars
        )

        if resp.get('retCode', -1) != 0:
            print("Error:", resp.get('retMsg'))
            break

        result = resp.get('result', {})
        if not result or 'list' not in result or not result['list']:
            break

        df_chunk = pd.DataFrame(result['list'], columns=[
            'startTime','open','high','low','close','volume','turnover'
        ])
        # Convert timestamp from ms to datetime
        df_chunk['startTime'] = pd.to_datetime(df_chunk['startTime'], unit='ms')
        df_chunk.set_index('startTime', inplace=True)
        # Convert numeric fields
        for col in ['open','high','low','close','volume','turnover']:
            df_chunk[col] = pd.to_numeric(df_chunk[col], errors='coerce')

        # Append
        all_df = pd.concat([all_df, df_chunk])
        all_df.drop_duplicates(inplace=True)
        all_df.sort_index(inplace=True)

        # If we got fewer than 200 bars, likely done
        if len(df_chunk) < 200:
            break

        # Advance start_ms beyond the last returned bar
        last_ts = int(df_chunk.index[-1].timestamp() * 1000) + 1
        if last_ts >= end_ms:
            break
        start_ms = last_ts

        # Polite pause
        time.sleep(0.1)

    return all_df

if __name__ == "__main__":
    symbol = "BTCUSDT"
    start_date = dt.datetime(2025,1,1)
    end_date   = dt.datetime(2025,1,2)

    df = fetch_kline_data(symbol, start_date, end_date, interval='1')
    print(df.head())
    print(df.tail())
    print(f"Fetched {len(df)} rows.")

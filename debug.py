import csv

with open('BTCUSDT_1_2025-01-01_2025-01-31.csv', 'r') as f:
    reader = csv.reader(f)
    for idx, row in enumerate(reader):
        # print(idx, row)
        # Check row length
        if len(row) != 6:
            print("Row has != 6 columns!", row)
        if idx > 3000000:
            break  # just preview the first ~30 lines

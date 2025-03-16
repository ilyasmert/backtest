import csv

with open('resampled_data.csv', 'r') as f:
    reader = csv.reader(f)
    for idx, row in enumerate(reader):
        # print(idx, row)
        
        print("Row: ", row)
        if idx > 3000000:
            break  # just preview the first ~30 lines

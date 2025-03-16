import csv
from datetime import datetime
import sys

def filter_four_hour_data(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        for row in reader:
            # Parse the timestamp (assumes format: YYYY.MM.DD HH:MM)
            try:
                ts = datetime.strptime(row[0], '%Y.%m.%d %H:%M')
            except ValueError as e:
                print(f"Error parsing timestamp '{row[0]}': {e}")
                continue

            # Check if the minute is 00 and the hour is divisible by 4 (i.e., 0, 4, 8, 12, 16, 20)
            if ts.minute == 0 and ts.hour % 4 == 0:
                writer.writerow(row)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python filter_csv.py input.csv output.csv")
    else:
        input_csv = sys.argv[1]
        output_csv = sys.argv[2]
        filter_four_hour_data(input_csv, output_csv)

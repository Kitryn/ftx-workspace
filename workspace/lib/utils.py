from pathlib import Path
import csv

def construct_csv_path(base_path, exchange_id, pair_id, timeframe):
    filename = '%s-%s-%s.csv' % (exchange_id, pair_id, timeframe)
    return base_path.joinpath(filename)

def write_to_csv(path, data):
    with path.open('w', newline='') as f:
        field_names = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        csvWriter = csv.writer(f)
        csvWriter.writerow(field_names)
        csvWriter.writerows(data)

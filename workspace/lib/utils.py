from pathlib import Path
import csv
import pandas as pd


def construct_csv_path(base_path, exchange_id, pair_id, timeframe):
    filename = '%s-%s-%s.csv' % (exchange_id, pair_id, timeframe)
    return base_path.joinpath(filename)


def write_to_csv(path, data):
    with path.open('w', newline='') as f:
        field_names = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        csvWriter = csv.writer(f)
        csvWriter.writerow(field_names)
        csvWriter.writerows(data)

def merge_csv(path, data):
    df = pd.read_csv(path, header=0).astype({'timestamp': 'int64'})
    headers = df.columns.tolist()
    
    # Incoming data is an array of arrays with no column headers
    df_to_merge = pd.DataFrame(data, columns=headers).astype({
        'timestamp': 'int64'})

    # The data MUST overlap
    min1 = df['timestamp'].min()
    min2 = df_to_merge['timestamp'].min()
    if min1 not in df_to_merge['timestamp'].values and min2 not in df['timestamp'].values:
        raise Exception('Time periods not mergeable without gaps')

    df = pd.concat([df, df_to_merge]) \
        .astype({'timestamp': 'int64'}) \
        .drop_duplicates('timestamp') \
        .sort_values('timestamp') \
        .reset_index(drop=True)
    
    df.to_csv(path, index=False)


# Used for testing -- extract into unit test another time
# if __name__ == "__main__":
#     path1 = Path('./data/1.csv')
#     path2 = Path('./data/2.csv')
#     data1 = []
#     data2 = []
#     with path1.open('r') as f:
#         reader = csv.reader(f)
#         _ = next(reader)
#         for line in reader:
#             data1.append(line)

#     with path2.open('r') as f:
#         reader = csv.reader(f)
#         _ = next(reader)
#         for line in reader:
#             data2.append(line)
#     merge_csv(path2, data1)

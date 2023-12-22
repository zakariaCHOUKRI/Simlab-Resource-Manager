import pandas as pd

def process_partition_data(partition_data):
    columns = ['Partition', 'AvailableCPUs', 'AvailableGPUs']
    data = [line.split('|') for line in partition_data.split('\n')]
    df = pd.DataFrame(data, columns=columns)
    return df

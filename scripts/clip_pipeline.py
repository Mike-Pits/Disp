import pandas as pd
block = pd.read_clipboard(sep='\t')

COLUMN_NAMES = [l for l in range(0, 102)]
df = pd.DataFrame(columns=COLUMN_NAMES, index=[0])

list_data = block.T.reset_index().values

for i in range(len(list_data[0])):
    if list_data[0][i].split()[0].isdigit():
        df.iloc[0, int(list_data[0][i].split()[0])] = ' '.join(list_data[0][i].split()[1:][:])
    else:
        df.iloc[0, 101] = list_data[0][i]

print(df.dropna(axis=1))

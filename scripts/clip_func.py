import pandas as pd

def clip():
    block = pd.read_clipboard(sep='\t')

    COLUMN_NAMES = [l for l in range(0, 104)]
    df = pd.DataFrame(columns=COLUMN_NAMES, index=[0])

    list_data = block.T.reset_index().values

    for i in range(len(list_data[0])):
        if list_data[0][i].split()[0].isdigit():
            df.iloc[0, int(list_data[0][i].split()[0])] = ' '.join(list_data[0][i].split()[1:][:])
        elif list_data[0][i].split()[0] == 'т/к':
            df.iloc[0, 0] = list_data[0][i][4:]
        elif list_data[0][i].split()[0].lower() == 'дисп':
            df.iloc[0, 102] = list_data[0][i].split()[1]
        else:
            df.iloc[0, 103] = list_data[0][i]
    
    return df


print(clip())
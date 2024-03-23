import pandas as pd

def saveExcel(data, path):
    df = pd.DataFrame(pd.DataFrame.from_dict(data, orient='index').values.T, columns=list(data.keys()))
    df.to_excel(path, index=False)

def saveCsv(data, path):
    df = pd.DataFrame(data)
    df.to_csv(path, index=False)

if __name__ == "__main__":
    data = {
        'index': [1, 2, 3, 4],
        'value': ['A', 'B', 'C']
    }
    df = pd.DataFrame(pd.DataFrame.from_dict(data, orient='index').values.T, columns=list(data.keys()))
    
    df.to_excel('output.xlsx', index=False)
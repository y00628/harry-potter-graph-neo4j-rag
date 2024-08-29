import pandas as pd

def combine_data():
    
    excel_file = './data/book-1_character_relations_new.xlsx'

    xls = pd.ExcelFile(excel_file)
    
    combined_df = pd.DataFrame()
    
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        df = df.apply(pd.to_numeric, errors='ignore')
        combined_df = pd.concat([combined_df, df], ignore_index=True)

    combined_df = combined_df.groupby('name').max()
    combined_df = combined_df.drop(columns=combined_df.columns[-4:])
    combined_df = combined_df[~combined_df.index.isin(['James Potter', 'Lily Potter', 'Lee Jordan'])]
    combined_df['classmate'] = combined_df['classmate'].astype(int)
    
    csv_file = './data/combined_data.csv'
    combined_df.to_csv(csv_file, index=True)



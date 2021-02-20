"""
Checkpoint 1b

*First complete the steps in checkpoint1a.pdf

Here you will create a script to preprocess the data given in starbucks.csv. You may want to use
a jupyter notebook or python terminal to develop your code and test each function as you go... 
you can import this file and its functions directly:

    - jupyter notebook: include the lines `%autoreload 2` and `import preprocess`
                        then just call preprocess.remove_percents(df) to test
                        
    - python terminal: run `from importlib import reload` and `import preprocess`
                       each time you modify this file, run `reload(preprocess)`

Once you are finished with this program, you should run `python preprocess.py` from the terminal.
This should load the data, perform preprocessing, and save the output to the data folder.

"""
import pandas as pd


def remove_percents(df, col):
    def erase_percents(data):
        if isinstance(data, str):
            if '%' in data:
                return float(data[:len(data) - 1])
        return data
        
    df[col] = df[col].apply(erase_percents)
    return df


def fill_zero_iron(df):   
    def fill_zero(data):
        if pd.isna(data):
            return 0.00
        else:
            return float(data)         
    
    df['Iron (% DV)'] = df['Iron (% DV)'].apply(fill_zero)
    return df
    

def fix_caffeine(df):
    # had trouble with pd's median() and mean(), so I made my own function
    def find_mean():
        count = 0
        curr_sum = 0
        for data in df['Caffeine (mg)']:
            if pd.isna(data): # if data == 'NaN' or varies'
                pass
            elif str(data).lower() == "varies":
                pass
            else:
                count += 1
                curr_sum += float(data)
        return curr_sum / count
        
    def fill_caffeine(data):
        if pd.isna(data):
            return 0.00
        elif str(data).lower() == 'varies':
            return mean
        else:
            return float(data)         
    
    mean = find_mean()
    df['Caffeine (mg)'] = df['Caffeine (mg)'].apply(fill_caffeine)
    return df


def standardize_names(df):
    def standardize(string):
        char = 0
        while char < len(string):
            if string[char] == ' ':
                pass
            elif string[char] == '_':
                string = string[: char] + ' ' + string[char + 1:]
            elif string[char] == '(':
                string = string[: char - 1] # get rid of ( ) and the preceding space
            char += 1
        return string.lower()
            
    col_names_new = []
    for col_name in list(df.columns):
        col_names_new.append(standardize(col_name))
        
    df.columns = col_names_new
    return df


def fix_strings(df, col):
    def turn_lower_alpha(string):
        string_copy = string.replace(' ', '')
        if not string_copy.isalpha():
            char = 0
            while char < len(string):
                if string[char] == ' ':
                    pass
                elif not string[char].isalpha():
                    string = string[: char] + string[char + 1:]
                    char = char - 1
                char += 1 
        return string.lower()
    
    df[col] = df[col].apply(turn_lower_alpha)
    return df


def main():
    
    # first, read in the raw data
    df = pd.read_csv('../data/starbucks.csv')
    
    # the columns below represent percent daily value and are stored as strings with a percent sign, e.g. '0%'
    # complete the remove_percents function to remove the percent symbol and convert the columns to a numeric type
    pct_DV = ['Vitamin A (% DV)', 'Vitamin C (% DV)', 'Calcium (% DV)', 'Iron (% DV)']
    for col in pct_DV:
        df = remove_percents(df, col)
    
    # the column 'Iron (% DV)' has missing values when the drink has no iron
    # complete the fill_zero_iron function to fix this
    df = fill_zero_iron(df)

    # the column 'Caffeine (mg)' has some missing values and some 'varies' values
    # complete the fix_caffeine function to deal with these values
    # note: you may choose to fill in the values with the mean/median, or drop those values, etc.
    df = fix_caffeine(df)
    
    # the columns below are string columns... starbucks being starbucks there are some fancy characters and symbols in their names
    # complete the fix_strings function to convert these strings to lowercase and remove non-alphabet characters
    names = ['Beverage_category', 'Beverage']
    for col in names:
        df = fix_strings(df, col)
    
    # the column names in this data are clear but inconsistent
    # complete the standardize_names function to convert all column names to lower case and remove the units (in parentheses)
    df = standardize_names(df)
    
    # now that the data is all clean, save your output to the `data` folder as 'starbucks_clean.csv'
    # you will use this file in checkpoint 2
    df.to_csv('../data/starbucks_clean.csv')
    

if __name__ == "__main__":
    main()

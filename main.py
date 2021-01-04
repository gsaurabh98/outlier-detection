import json

import pandas as pd
from outlier import outlier_correction
from outlier import outlier_detection


def main(dataframe, config):
    '''
        This function correct the outliers present in the numeric features

        Parameters
        ------------
        dataframe: pd.DataFrame
            pandas dataframe
        config: dict
            dictionary of outlier correction method

        Returns
        ------------
        pd.dataFrame
            pandas dataframe
    '''

    indexes, _ = outlier_detection(dataframe, config['outlier_detection'])

    df = outlier_correction(dataframe, config['outlier_correction'], indexes)

    return df


if __name__ == '__main__':
    df = pd.read_csv('input.csv')
    df = df.fillna(value=1000)

    with open('config.json', 'r') as con:
        config = json.load(con)

    output_df = main(df, config)
    output_df.to_csv('output.csv', sep=',', index=False)

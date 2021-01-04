import numpy as np


def outlier_detection(dataframe,
                      numeric_features,
                      config):
    '''
    This function detect the outliers present in the numeric features

    Parameters
    ------------
    dataframe: pd.DataFrame
        pandas dataframe
    numeric_features: list
        list of numeric features
    config: dict
        dictionary of outlier detection method

    Returns
    ------------
    dict
        outlier index and outlier count
    '''

    outlier_index = {}
    outlier_count = {}

    for col in numeric_features:

        if config[col].lower() == 'factor method':
            index_list = []
            data_mean, data_std, data_median = dataframe[col].mean(), \
                                               dataframe[col].std(), \
                                               dataframe[
                                                   col].median()
            cut_off = data_std * 3.0
            lower, upper = data_mean - cut_off, data_mean + cut_off
            count = 0
            for index, value in dataframe[col].iteritems():
                if value < lower or value > upper:
                    index_list.append(index)
                    count = count + 1
            outlier_count.update({col: count})
            outlier_index.update({col: index_list})

        elif config[col].lower() == 'z-score':

            index_list = []
            threshold = 3
            count = 0
            for index, value in dataframe[col].iteritems():
                z_scores = (value - np.mean(dataframe[col])) / np.std(
                    dataframe[col])
                if z_scores > threshold:
                    index_list.append(index)
                    count = count + 1
            outlier_count.update({col: count})
            outlier_index.update({col: index_list})

        elif config[col].lower() == 'inter-quartile range':

            index_list = []
            q25, q75 = np.percentile(dataframe[col], 25), np.percentile(
                dataframe[col], 75)
            iqr = q75 - q25
            cut_off = iqr * 1.5
            lower, upper = q25 - cut_off, q75 + cut_off
            count = 0
            for index, value in dataframe[col].iteritems():
                if value < lower or value > upper:
                    count = count + 1
            outlier_count.update({col: count})
            outlier_index.update({col: index_list})

    return outlier_index, outlier_count

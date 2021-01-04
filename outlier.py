import numpy as np


def outlier_detection(dataframe,
                      config):
    '''
    This function detect the outliers present in the numeric features

    Parameters
    ------------
    dataframe: pd.DataFrame
        pandas dataframe
    config: dict
        dictionary of outlier detection method

    Returns
    ------------
    dict
        outlier index and outlier count
    '''

    outlier_index = dict()
    outlier_count = dict()

    for col in config.keys():

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


def outlier_correction(dataframe,
                       config,
                       indexes):
    '''
        This function correct the outliers present in the numeric features

        Parameters
        ------------
        dataframe: pd.DataFrame
            pandas dataframe
        config: dict
            dictionary of outlier correction method
        indexes: dict
            dictionary of outlier indexes


        Returns
        ------------
        pd.dataFrame
            pandas dataframe
    '''

    df = dataframe.copy()
    for col_name in config.keys():

        if config[col_name].lower() == 'mean':
            df.loc[indexes[col_name], col_name] = round(df[col_name].mean(), 2)

        elif config[col_name].lower() == "median":
            df.loc[indexes[col_name], col_name] = round(df[col_name].median(),
                                                        2)

        elif config[col_name].lower() == "min":
            df.loc[indexes[col_name], col_name] = round(dataframe[
                                                            col_name].min(), 2)

        elif config[col_name].lower() == "max":
            df.loc[indexes[col_name], col_name] = round(dataframe[
                                                            col_name].max(), 2)

        elif config[col_name].lower() == "delete":
            df.drop(df.index[indexes[col_name]], axis=0,
                    inplace=True)

        elif config[col_name].lower() == 'ignore':
            pass

    return df

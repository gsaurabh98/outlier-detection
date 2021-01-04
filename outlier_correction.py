def outlier_correction(dataframe,
                       numeric_features,
                       config,
                       indexes):
    '''
        This function correct the outliers present in the numeric features

        Parameters
        ------------
        dataframe: pd.DataFrame
            pandas dataframe
        numeric_features: list
            list of numeric features
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
    for col_name in numeric_features:

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

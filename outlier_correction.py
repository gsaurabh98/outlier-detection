    def outlier_detection_strategy(self, data_from_ui, dataFrame,
                                   list_of_numrical_cols, ods_dict):

        outlier_list = []
        index_list_df = []
        col_outlier_index_dict = {}
        col_outlier_count_dict = {}
        col_outlier_upper_dict = {}

        for col in list_of_numrical_cols:

            ods_strategy = ods_dict[col]

            if ods_strategy == 'Factor Method':
                index_list = []
                data_mean, data_std, data_median = dataFrame[col].mean(), \
                                                   dataFrame[col].std(), \
                                                   dataFrame[
                                                       col].median()
                cut_off = data_std * 3.0
                lower, upper = data_mean - cut_off, data_mean + cut_off
                col_outlier_upper_dict.update({col: upper})
                count = 0
                for index, value in dataFrame[col].iteritems():
                    if value < lower or value > upper:
                        index_list.append(index)
                        index_list_df.append(index)
                        outlier_list.append(value)
                        count = count + 1
                col_outlier_count_dict.update({col: count})
                col_outlier_index_dict.update({col: index_list})

            elif ods_strategy == 'Z-score':

                index_list = []
                threshold = 3
                mean = np.mean(dataFrame[col])
                std = np.std(dataFrame[col])
                count = 0
                for index, value in dataFrame[col].iteritems():
                    z_scores = (value - mean) / std
                    if z_scores > threshold:
                        index_list.append(index)
                        index_list_df.append(index)
                        outlier_list.append(value)
                        count = count + 1
                col_outlier_count_dict.update({col: count})
                col_outlier_index_dict.update({col: index_list})
                col_outlier_upper_dict.update({col: z_scores})

            elif ods_strategy == 'Inter-Quartile Range':

                index_list = []
                q25, q75 = np.percentile(dataFrame[col], 25), np.percentile(
                    dataFrame[col], 75)
                iqr = q75 - q25
                cut_off = iqr * 1.5
                lower, upper = q25 - cut_off, q75 + cut_off
                count = 0
                col_outlier_upper_dict.update({col: upper})
                for index, value in dataFrame[col].iteritems():
                    if value < lower or value > upper:
                        index_list.append(index)
                        outlier_list.append(value)
                        count = count + 1
                col_outlier_count_dict.update({col: count})
                col_outlier_index_dict.update({col: index_list})

        return dataFrame, col_outlier_index_dict, col_outlier_upper_dict, col_outlier_count_dict



        def outlier_correction_strategy(self, data_from_ui, dataFrame,
                                    list_of_numerical_columns, ocs_dict,
                                    col_outlier_index_dict,
                                    col_outlier_upper_dict):

        if 'customCorrectionStrategy' in data_from_ui:
            ocs_custom_dict = data_from_ui['customCorrectionStrategy']

        index_list_df = []

        for col_name in list_of_numerical_columns:
            ocs_strategy = ocs_dict[col_name]
            col_ol_index_list = col_outlier_index_dict[col_name]
            index_list_df.extend(col_ol_index_list)

            if ocs_strategy == 'Mean':
                dataFrame.loc[col_ol_index_list, col_name] = round(dataFrame[
                                                                       col_name].mean(),
                                                                   2)

            elif ocs_strategy == "Median":
                dataFrame.loc[col_ol_index_list, col_name] = round(dataFrame[
                                                                       col_name].median(),
                                                                   2)

            elif ocs_strategy == "Delete data":
                dataFrame.drop(dataFrame.index[col_ol_index_list], axis=0,
                               inplace=True)
                dataFrame.reset_index(drop=True)

            elif ocs_strategy == "Lower bound":
                dataFrame.loc[col_ol_index_list, col_name] = round(dataFrame[
                                                                       col_name].min(),
                                                                   2)

            elif ocs_strategy == "Upper bound":
                dataFrame.loc[col_ol_index_list, col_name] = \
                    round(col_outlier_upper_dict[col_name], 2)

            elif ocs_strategy == 'No strategy':
                pass

            elif ocs_strategy.lower() == 'custom':
                dataFrame.loc[col_ol_index_list, col_name] = \
                    round(float(ocs_custom_dict[col_name]), 2)

                pass

        outlier_preview_df = pd.DataFrame(dataFrame,
                                          columns=dataFrame.columns,
                                          index=index_list_df)

        return dataFrame, outlier_preview_df
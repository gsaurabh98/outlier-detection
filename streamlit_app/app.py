# command : streamlit run app.py

import pandas as pd
import streamlit as st
from outlier import outlier_detection
from outlier import outlier_correction

st.title('Outliers Detection/Correction')

st.markdown(
    '<span><i>Outlier is an observation that lies an abnormal distance from other values!</i></span>',
    unsafe_allow_html=True)
st.text('')
st.text('')

st.sidebar.markdown('<b>Upload Dataset</b>', unsafe_allow_html=True)
st.sidebar.markdown(
    '<span style=" font-size:13px" >Dataset must contain numeric features!</span>',
    unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("Choose a csv file", type="csv")

if uploaded_file is not None:
    dataframe = pd.read_csv(uploaded_file)

    columns = dataframe.select_dtypes(include='number').columns.tolist()
    if not len(columns) > 0:
        st.sidebar.markdown(
            '<span style="color:red; font-size:18px" >No numeric features found, please upload different dataset.</span>',
            unsafe_allow_html=True)
    else:
        st.markdown('<b>Dataset sample</b>', unsafe_allow_html=True)
        st.table(dataframe.head())

        st.write(
            '<style>div.Widget.row-widget.stRadio > div{flex-direction:row;}</style>',
            unsafe_allow_html=True)

        features = st.sidebar.multiselect('Select features', columns, key=None)

        detection_method = st.sidebar.selectbox(
            "Select outlier detection method",
            ('Factor Method', 'Z-Score', 'Inter-Quartile Range')
        )

        correction_method = st.sidebar.selectbox(
            "Select outlier correction method",
            ('Mean', 'Median', 'Std', 'Min', 'Max', 'Delete', 'Ignore')
        )

        if st.sidebar.button('Submit', key="check_outlier"):

            outlier_indexes, outlier_count = outlier_detection(dataframe,
                                                              features,
                                                              detection_method)
            
            print('outlier_indexes',outlier_indexes)

            unique_indexes = list(
                set([v for values in outlier_indexes.values() for v in values]))


            df = pd.DataFrame(outlier_count, index=['count'])

            if df.loc['count'].sum() == 0:
                st.markdown(
                    '<span style="color:green; font-size:20px" >No outliers found !!</span>',
                    unsafe_allow_html=True)

            else:
                st.markdown('<b>Outlier(s) count</b>', unsafe_allow_html=True)
                st.table(df)
                
                st.markdown('<b>Outlier(s) Index</b>', unsafe_allow_html=True)
                st.json(outlier_indexes)

                st.markdown('<b>Outlier(s) Dataset</b>',
                            unsafe_allow_html=True)
                output = outlier_correction(dataframe, features,
                                            outlier_indexes, correction_method)

                df = output.loc[output.index.isin(unique_indexes)]
                st.table(df)


                # def highlight_cols(s, features):
                #     if s.name in features:
                #         return ['color: {}'.format('green')] * len(s)
                #     return [''] * len(s)
                #
                #
                # st.table(df.style.apply(highlight_cols, features=features))

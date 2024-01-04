#Author : Sanjay Sreenivas S
import streamlit as st
from snowflake.snowpark.context import get_active_session

st.title("Mutual Fund Analysis - Streamlit Edition")
st.write(
   """To access information on mutual funds, please select your preferred option. The data presented here is sourced from the fund details table in the application package. However, the Streamlit app retrieves this data from a snowflake view that is loaded from our internal stage data. This stage data is in turn loaded from the Kaggle Mutual Funds India-Detailed dataset..
   """
)
session = get_active_session()
data_frame = session.sql("SELECT * FROM fund_package.fund_data.mutual_fund_details;")
queried_data = data_frame.to_pandas()
queried_data['RATING'] = queried_data['RATING'].astype(int)
min_rating, max_rating = st.slider(
    "Select Rating Range",
    min_value=int(queried_data['RATING'].min()),
    max_value=int(queried_data['RATING'].max()),
    value=(int(queried_data['RATING'].min()), int(queried_data['RATING'].max()))
)
fund_age_range = st.slider(
    "Select Fund Age Range",
    min_value=int(queried_data['FUND_AGE_YR'].min()),
    max_value=int(queried_data['FUND_AGE_YR'].max()),
    value=(int(queried_data['FUND_AGE_YR'].min()), int(queried_data['FUND_AGE_YR'].max()))
)

risk_level_range = st.slider(
    "Select Risk Level Range",
    min_value=int(queried_data['RISK_LEVEL'].min()),
    max_value=int(queried_data['RISK_LEVEL'].max()),
    value=(int(queried_data['RISK_LEVEL'].min()), int(queried_data['RISK_LEVEL'].max()))
)

selected_amc = st.selectbox("Select AMC Name", ['All'] + list(queried_data['AMC_NAME'].unique()))
selected_categories = st.multiselect("Select Category", ['All'] + list(queried_data['CATEGORY'].unique()))
selected_column = st.selectbox("Select a column for the bar chart", ['AMC_NAME', 'CATEGORY', 'SCHEME_NAME'])
filtered_data = queried_data[
    (queried_data['RATING'] >= min_rating) & (queried_data['RATING'] <= max_rating) &
    (queried_data['FUND_AGE_YR'] >= fund_age_range[0]) & (queried_data['FUND_AGE_YR'] <= fund_age_range[1]) &
    (queried_data['RISK_LEVEL'] >= risk_level_range[0]) & (queried_data['RISK_LEVEL'] <= risk_level_range[1]) &
    ((queried_data['AMC_NAME'] == selected_amc) | (selected_amc == "All")) &
    (queried_data['CATEGORY'].isin(selected_categories) | ('All' in selected_categories))
]
st.dataframe(filtered_data, use_container_width=True)
st.subheader("Bar Chart based on selected column")
st.bar_chart(filtered_data[selected_column].value_counts())
st.subheader("Trend Graphs based on Returns")
st.line_chart(filtered_data[['RETURNS_1YR', 'RETURNS_3YR', 'RETURNS_5YR']])

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime

# Initialize session state for storing data
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=['timestamp', 'value'])

# Page title and description
st.title('Data Recording & Visualization Tool')
st.write('Enter numerical values to record and visualize them in real-time')

# Input section
with st.container():
    col1, col2 = st.columns([3, 1])
    with col1:
        new_value = st.number_input('Enter a numerical value:', key='value_input')
    with col2:
        if st.button('Record Value'):
            # Add new value to the dataframe
            new_row = pd.DataFrame({
                'timestamp': [datetime.now()],
                'value': [new_value]
            })
            st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)
            st.rerun()

# Display data and visualizations if we have data
if not st.session_state.data.empty:
    # Statistical information
    st.subheader('Statistical Summary')
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Mean', f"{st.session_state.data['value'].mean():.2f}")
    with col2:
        st.metric('Median', f"{st.session_state.data['value'].median():.2f}")
    with col3:
        st.metric('Standard Dev', f"{st.session_state.data['value'].std():.2f}")
    with col4:
        st.metric('Count', len(st.session_state.data))

    # Time series chart
    st.subheader('Time Series Visualization')
    fig_time = px.line(st.session_state.data, 
                       x='timestamp', 
                       y='value',
                       title='Values Over Time')
    st.plotly_chart(fig_time, use_container_width=True)

    # Distribution histogram
    st.subheader('Value Distribution')
    fig_dist = px.histogram(st.session_state.data, 
                           x='value',
                           title='Value Distribution',
                           nbins=20)
    st.plotly_chart(fig_dist, use_container_width=True)

    # Raw data display
    st.subheader('Recorded Data')
    st.dataframe(st.session_state.data.sort_values('timestamp', ascending=False),
                 hide_index=True,
                 use_container_width=True)

    # Clear data button
    if st.button('Clear All Data'):
        st.session_state.data = pd.DataFrame(columns=['timestamp', 'value'])
        st.rerun()
else:
    st.info('No data recorded yet. Start by entering values above.')

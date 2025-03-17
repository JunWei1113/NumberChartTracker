import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime

# Initialize session state for storing data
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=['timestamp', 'type', 'value'])

# Page title and description
st.title('血糖與胰島素劑量記錄系統')
st.write('記錄血糖值和胰島素劑量的變化')

# Input section
with st.container():
    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        glucose_value = st.number_input('血糖值 (mg/dL):', 
                                      key='glucose_input',
                                      min_value=0.0)
    with col2:
        insulin_value = st.number_input('胰島素劑量 (單位):', 
                                      key='insulin_input',
                                      min_value=0.0)
    with col3:
        if st.button('送出資料'):
            # Add new values to the dataframe
            new_rows = pd.DataFrame({
                'timestamp': [datetime.now(), datetime.now()],
                'type': ['血糖', '胰島素'],
                'value': [glucose_value, insulin_value]
            })
            st.session_state.data = pd.concat([st.session_state.data, new_rows],
                                            ignore_index=True)
            st.rerun()

# Display warning for glucose levels
if not st.session_state.data.empty:
    latest_glucose = st.session_state.data[st.session_state.data['type'] == '血糖']['value'].iloc[-1] \
        if len(st.session_state.data[st.session_state.data['type'] == '血糖']) > 0 else None

    if latest_glucose is not None:
        if latest_glucose < 90:
            st.warning('⚠️ 警告：血糖過低！')
        elif latest_glucose > 120:
            st.warning('⚠️ 警告：血糖過高！')
        else:
            st.success('✅ 血糖在正常範圍內')

# Display data and visualizations if we have data
if not st.session_state.data.empty:
    # Statistical information
    st.subheader('統計摘要')

    # Create separate statistics for glucose and insulin
    glucose_data = st.session_state.data[st.session_state.data['type'] == '血糖']
    insulin_data = st.session_state.data[st.session_state.data['type'] == '胰島素']

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('**血糖數據**')
        if not glucose_data.empty:
            st.metric('平均值', f"{glucose_data['value'].mean():.1f} mg/dL")
            st.metric('最新值', f"{glucose_data['value'].iloc[-1]:.1f} mg/dL")
            st.metric('記錄筆數', len(glucose_data))

    with col2:
        st.markdown('**胰島素數據**')
        if not insulin_data.empty:
            st.metric('平均值', f"{insulin_data['value'].mean():.1f} 單位")
            st.metric('最新值', f"{insulin_data['value'].iloc[-1]:.1f} 單位")
            st.metric('記錄筆數', len(insulin_data))

    # Time series chart
    st.subheader('時間序列視覺化')
    fig_time = px.line(st.session_state.data,
                      x='timestamp',
                      y='value',
                      color='type',
                      title='數值變化趨勢')
    st.plotly_chart(fig_time, use_container_width=True)

    # Distribution charts
    st.subheader('數值分布')
    col1, col2 = st.columns(2)

    with col1:
        if not glucose_data.empty:
            fig_glucose = px.histogram(glucose_data,
                                     x='value',
                                     title='血糖值分布',
                                     nbins=20)
            st.plotly_chart(fig_glucose, use_container_width=True)

    with col2:
        if not insulin_data.empty:
            fig_insulin = px.histogram(insulin_data,
                                     x='value',
                                     title='胰島素劑量分布',
                                     nbins=20)
            st.plotly_chart(fig_insulin, use_container_width=True)

    # Raw data display
    st.subheader('記錄數據')
    st.dataframe(st.session_state.data.sort_values('timestamp',
                                                  ascending=False),
                hide_index=True,
                use_container_width=True)

    # Clear data button
    if st.button('清除所有數據'):
        st.session_state.data = pd.DataFrame(columns=['timestamp', 'type', 'value'])
        st.rerun()
else:
    st.info('尚未有記錄的數據。請在上方輸入數值開始記錄。')
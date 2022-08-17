# web development
import streamlit as st
# read csv, df manipulation
import pandas as pd 
# Visualize Results as plots
import matplotlib.pyplot as plt
# Date time format
import datetime as dt 
from plotly import graph_objs as go
from prophet import Prophet
# Pull in financial information
import yfinance as yf
from web3 import Web3
from pathlib import Path
import json

# Get w3 object
w3 = Web3(Web3.HTTPProvider(st.secrets['WEB3_PROVIDER_URI_OLD']))

# Define and load public rinkeby deployed contract
def load_contract():

    # Load Art Gallery ABI
    with open(Path('../contracts/NFA_abi.json')) as f:
        NFA_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = st.secrets["SMART_CONTRACT_ADDRESS"]

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=NFA_abi
    )
    # Return the contract from the function
    return contract
contract=load_contract()

# Load streamlit page configuration

st.set_page_config(
    page_title="NotFinancialAdvice - Prophet",
    page_icon="📊",
    layout= "wide"    
)

# Test for non-Token Holder test
#0xBe4c620D68ED45cd7b0381eD2FD975dd7946b367 - No NFA Tokens
#0x3Db2D37545C7b89E9A93b8D05c8805a0Ccb4780f - NFA Token exist
NFA_0b = contract.functions.balanceOf('0xBe4c620D68ED45cd7b0381eD2FD975dd7946b367',int(0)).call() 
NFA_1b = contract.functions.balanceOf('0xBe4c620D68ED45cd7b0381eD2FD975dd7946b367',int(1)).call() 
NFA_2b = contract.functions.balanceOf('0xBe4c620D68ED45cd7b0381eD2FD975dd7946b367',int(2)).call()
NFA_allb = NFA_0b + NFA_1b + NFA_2b

if NFA_allb <= 0:
    st.write("# Welcome to NotFinancialAdvice! 👋")
    st.markdown(
    """
    This page is token restricted and content has been redacted
        
    """
    )


else:


    # dashboard title
    # st.title("NotFinanialAdvice Streamlit Finance Dashboard")
    st.title("NotFinanialAdvice")


    tickers = ('AXP', 'AMGN', 'AAPL', 'BA', 'CAT', 'CSCO', 'CVX', 'GS',	'HD', 'HON', 'IBM', 'INTC', 'JNJ', 'KO', 'JPM', 'MCD', 'MMM', 'MRK', 'MSFT', 'NKE', 'PG', 'TRV', 'UNH','CRM', 'VZ', 'V', 'WBA', 'WMT', 'DIS', 'DOW')
    dropdown = st.sidebar.selectbox('Pick your asset', tickers)

    start = st.sidebar.date_input('Start', value = pd.to_datetime('2021-01-01'))
    end = st.sidebar.date_input('End', value = pd.to_datetime('today'))

    df = yf.download(dropdown,start,end).Close

    # Create a Prophet model for model_dow
    model_dow = Prophet(yearly_seasonality=True)

    # format 'dow_prophet_model' to fit the prophet functions parameters. 
    dow_prophet_model = df.reset_index()
    dow_prophet_model.columns = ['ds', 'y']

    # Fit the Prophet model for dow data
    model_dow.fit(dow_prophet_model)

    # Forecast one year of weekly future trends data for the Future dow Closing Prices 
    future_dow = model_dow.make_future_dataframe(periods=52, freq="W")

    # Make predictions for forecast_dow using the future_dow DataFrame
    forecast_dow = model_dow.predict(future_dow).set_index('ds')
    forecast_dow_figures = forecast_dow.reset_index()

    # Plot predictions for our forecast_dow DataFrame for the 52 week period 
    forecast_dow_predictions = forecast_dow[['yhat', 'yhat_lower', 'yhat_upper']].iloc[-52:,:]

    # Use the plot_components function to visualize the forecast results 
    figures = model_dow.plot_components(forecast_dow_figures)

    # # Set the datetime index of the forecast_dow data, using the ds column
    # forecast_dow_index = forecast_dow.set_index("ds")


    start = pd.to_datetime('today').strftime('%Y-%m-%d')
    time_delta = dt.timedelta(days = 20)
    end = (pd.to_datetime(start) + time_delta).strftime('%Y-%m-%d')

    forecast_future_month = forecast_dow.loc[start:end][["yhat_upper", "yhat_lower", "yhat"]]

    # Replace the column names to something less technical sounding
    forecast_future_month = forecast_future_month.rename(
        columns={
            "yhat_upper": "Best Case",
            "yhat_lower": "Worst Case", 
            "yhat": "Most Likely Case"
        }
    )

    ############################################
    # Dashboard 

    ############################################
    # plot 1 not sccaled 
    # st.title("Prophet Forecast")
    # st.pyplot(model_dow.plot(forecast_dow_figures))

    # plot 2 not scaled
    # st.title(f"{dropdown} Prophet Forecast Predictions")
    # fig, ax = plt.subplots()
    # ax.plot(forecast_dow_predictions)
    # ax.legend(['yhat', 'yhat_lower', 'yhat_upper'])
    # st.pyplot(fig)

    # plot 3 not scaled 
    # st.pyplot(figures)

    st.header(f"{dropdown} Prophet Forecast Predictions")
    fig, ax = plt.subplots()
    ax.plot(forecast_dow_predictions)
    ax.legend(['yhat', 'yhat_lower', 'yhat_upper'])


    st.subheader(f"{dropdown} Prophet Forecast")
    st.pyplot(model_dow.plot(forecast_dow_figures))

    st.subheader(f"{dropdown} Prophet Forecast Statistics")
    st.pyplot(fig)

    st.subheader("Prophet Trends")
    st.pyplot(figures)

    st.subheader("21 Day Forecast")
    st.write(forecast_future_month)


    # # Review the last five rows of the DataFrame
    # st.write("The last 5 days",forecast_future_month.tail())

    # # Display the average forecasted price 
    # st.write("Average Forecasted price for the last 20 days", forecast_future_month.mean())


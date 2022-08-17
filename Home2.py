# web development - Dashboard
import streamlit as st 
import os
import json
from web3 import Web3
from pathlib import Path

# Get w3 object
w3 = Web3(Web3.HTTPProvider(st.secrets['WEB3_PROVIDER_URI_OLD']))

# Define and load public rinkeby deployed contract
def load_contract():

    # Load Art Gallery ABI
    with open(Path('./contracts/NFA_abi.json')) as f:
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
    page_title="About",
    page_icon="🇺🇸",
    layout= "wide"    
)

# Test for non-Token Holder test
#0xBe4c620D68ED45cd7b0381eD2FD975dd7946b367 - No NFA Tokens
#0x3Db2D37545C7b89E9A93b8D05c8805a0Ccb4780f - NFA Token exist
NFA_0b = contract.functions.balanceOf('0x3Db2D37545C7b89E9A93b8D05c8805a0Ccb4780f',int(0)).call() 
NFA_1b = contract.functions.balanceOf('0x3Db2D37545C7b89E9A93b8D05c8805a0Ccb4780f',int(1)).call() 
NFA_2b = contract.functions.balanceOf('0x3Db2D37545C7b89E9A93b8D05c8805a0Ccb4780f',int(2)).call()
NFA_allb = NFA_0b + NFA_1b + NFA_2b

if NFA_allb <= 0:
    st.write("# Welcome to NotFinancialAdvice! 👋")
    st.markdown(
    """
    This page is token restricted and content has been redacted
        
    """
    )

# st.set_page_config(
#     page_title="About",
#     page_icon="🇺🇸",
#     layout= "wide"    
# )
else:

    st.write("# Welcome to NotFinancialAdvice! 👋")
    st.image("./Streamlit/Resources/LandingPage.jpg")
    st.markdown(
        """
        This is your one stop shop for all analysis as it relates to the Stock Markets. 
        Whether you are intersted in general information on the company, fundamental analysis, technical analysis 
        or perhaps you want to see what your asset looks like forecasted in the future, we have the tools you are
        looking for!


        **👈 Select a page from the sidebar** to see a variety of financial analysis tools!

        ### Feel Free to connect!
        - [Richie Garafola](https://www.linkedin.com/in/richie-garafola)
        - [Jacob Edelbrock](https://www.linkedin.com/in/jacob-edelbrock-resume/)
        - [Mark Staten](https://www.linkedin.com/in/mark-staten-b9b3885/)

    """
    )


    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(["Agenda", "Executive Summary", "High Level Architechtural Diagram", "NFT Token Gating: Proof of Concept", "Financial Analysis Dashboard", "Oracle Database", "Project Approach",  "Next Steps", "Results and Conclusions"])

    with tab1:
        st.header("Agenda")
        st.image("./Streamlit/Resources/agenda.jpg")

    with tab2:
        st.header("Executive Summary")
        st.image("./Streamlit/Resources/executive_summary.jpg")

    with tab3:
        st.header("High Level Architechtural Diagram")
        st.image("./Streamlit/Resources/high_level_diagram.png")

    with tab4:
        st.header("NFT Token Gating: Proof of Concept")
        st.image("./Streamlit/Resources/nft_token_gating.png")
        st.markdown("""
        [NFA ERC1155 Demonstration](https://www.youtube.com/playlist?list=PLDNke-5WO5QfRG5FaB9-4Ly2WIRSOpuxJ""")

    with tab5:
        st.header("Financial Analysis Dashboard")
        st.image("./Streamlit/Resources/dashboardoverview.png")

    with tab6:
        st.header("Oracle Database")
        st.image("./Streamlit/Resources/oracle_database.png")

    with tab7:
        st.header("Project Approach")
        st.image("./Streamlit/Resources/project_approach.png")    

    with tab8:
        st.header("Next Steps")
        st.image("./Streamlit/Resources/next_steps.png")    

    with tab9:
        st.header("Results and Conclusions")
        st.image("./Streamlit/Resources/results.jpg")

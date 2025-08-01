import streamlit as st

st.set_page_config(layout="wide")

if not st.session_state.get('logged_in'):
    st.error("Please log in to access this page.")
    st.stop()

st.title("💰 Sales Order Management")
st.markdown("---")
st.info("This page will allow you to create sales orders for vendors using refined oil from the inventory.")

# Create a form here to log a new sale
# It should only allow selling 'Refined' oil from the inventory

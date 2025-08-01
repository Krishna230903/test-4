import streamlit as st

st.set_page_config(layout="wide")

if not st.session_state.get('logged_in'):
    st.error("Please log in to access this page.")
    st.stop()

st.title("🏭 Factory Inventory")
st.markdown("---")
st.info("This page will show a summary of all oil in the factory, including its status (Raw, Refining, Refined).")

# Fetch data from the 'inventory' table and display it here
# inventory_df = get_inventory_summary()
# st.dataframe(inventory_df)

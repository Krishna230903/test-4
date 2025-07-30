import streamlit as st
import datetime
from database import get_all_products, log_new_purchase, get_all_purchases
from utils import get_market_prices

st.set_page_config(layout="wide")

if not st.session_state.get('logged_in'):
    st.error("Please log in to access this page.")
    st.stop()

st.title("📦 Purchase Order Management")

# Get current market prices for reference
prices = get_market_prices()
st.info(f"Reference Market Prices: **Yesterday:** ₹{prices['yesterday_price']:,}/Tonne | **Today:** ₹{prices['today_price']:,}/Tonne")

st.markdown("### Log a New Purchase")
products_df = get_all_products()
if not products_df.empty:
    with st.form("new_purchase_form"):
        col1, col2 = st.columns(2)
        with col1:
            product_name = st.selectbox("Select Oil Product", options=products_df['name'])
            supplier_name = st.text_input("Supplier Name", placeholder="e.g., Global Agrochem")
            quantity_tonnes = st.number_input("Quantity (Metric Tonnes)", min_value=1.0, value=20.0, step=0.5)
        with col2:
            purchase_price_per_tonne = st.number_input("Purchase Price per Tonne (INR)", value=prices['yesterday_price'])
            eta_date = st.date_input("Expected Arrival Date (ETA)", min_value=datetime.date.today())

        submitted = st.form_submit_button("Log Purchase Order", use_container_width=True)
        if submitted:
            product_id = products_df.loc[products_df['name'] == product_name, 'id'].iloc[0]
            log_new_purchase(product_id, supplier_name, quantity_tonnes, purchase_price_per_tonne, eta_date)
            st.success(f"Purchase order for {quantity_tonnes} tonnes of {product_name} has been logged!")
            st.rerun()

st.markdown("---")

st.subheader("Current Purchase Orders")
purchases_df = get_all_purchases()
st.dataframe(purchases_df, use_container_width=True)

# Add logic here to select a purchase and update its status

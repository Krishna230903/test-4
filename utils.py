import numpy as np

def get_market_prices():
    """
    Simulates fetching the previous and current day's base crude oil price (INR/Tonne).
    In a real app, this would come from an API.
    """
    yesterday_price = 75000 + np.random.uniform(-500, 500)
    today_price = yesterday_price + np.random.uniform(-800, 1000)
    return {"yesterday_price": round(yesterday_price, 2), "today_price": round(today_price, 2)}

def calculate_sale_price(base_price_per_tonne, quantity_tonnes, density):
    """
    Calculates the final sale price per tonne based on the new model.
    """
    if density == 0 or quantity_tonnes == 0: return base_price_per_tonne

    # 1. Calculate total base price
    total_base_price = base_price_per_tonne * quantity_tonnes

    # 2. Convert tonnes to liters to calculate the extra charge
    liters = (quantity_tonnes / density) * 1000

    # 3. Calculate the total extra charge (₹10 per liter)
    total_extra_charge = liters * 10

    # 4. Calculate the new total price
    new_total_price = total_base_price + total_extra_charge

    # 5. Calculate the final price per tonne
    final_price_per_tonne = new_total_price / quantity_tonnes
    return round(final_price_per_tonne, 2)

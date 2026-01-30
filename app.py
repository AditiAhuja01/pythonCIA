import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(page_title="Silver Analysis", layout="wide")
st.title("Silver Price Calculator & Silver Sales Dashboard")
st.divider()

# --------------------------------------------------
# LOAD DATASETS
# --------------------------------------------------
price_data = pd.read_csv("historical_silver_price.csv")
sales_data = pd.read_csv("state_wise_silver_purchased_kg.csv")

# --------------------------------------------------
# SIDEBAR : SILVER PRICE CALCULATOR
# --------------------------------------------------
with st.sidebar:
    st.subheader("Silver Price Calculator")

    weight = st.number_input("Weight of Silver", min_value=0.0)
    unit = st.selectbox("Unit", ["grams", "kilograms"])
    price = st.number_input("Price per gram (₹)", min_value=0.0)
    currency = st.selectbox("Currency", ["INR (₹)", "USD ($)"])

    rate = 83  # INR to USD

    if st.button("Calculate Total Cost"):
        if unit == "kilograms":
            weight = weight * 1000

        total_cost = weight * price

        if currency == "USD ($)":
            total_cost = total_cost / rate
            symbol = "$"
        else:
            symbol = "₹"

        st.success(f"Total Silver Cost: {symbol}{total_cost:,.2f}")

# --------------------------------------------------
# PART 1 : HISTORICAL SILVER PRICE (BAR CHART)
# --------------------------------------------------
st.subheader("Historical Silver Price Analysis")
st.caption("Average silver price per year (₹ per kg)")

price_filter = st.selectbox(
    "Filter Price Range",
    ["All", "≤ 20,000", "20,000 - 30,000", "≥ 30,000"]
)

filtered_price = price_data.copy()

if price_filter == "≤ 20,000":
    filtered_price = filtered_price[
        filtered_price["Silver_Price_INR_per_kg"] <= 20000
    ]
elif price_filter == "20,000 - 30,000":
    filtered_price = filtered_price[
        (filtered_price["Silver_Price_INR_per_kg"] >= 20000) &
        (filtered_price["Silver_Price_INR_per_kg"] <= 30000)
    ]
elif price_filter == "≥ 30,000":
    filtered_price = filtered_price[
        filtered_price["Silver_Price_INR_per_kg"] >= 30000
    ]

yearly_avg = filtered_price.groupby("Year")["Silver_Price_INR_per_kg"].mean()

fig1, ax1 = plt.subplots(figsize=(6, 4))
ax1.bar(yearly_avg.index, yearly_avg.values, color="brown")
ax1.set_xlabel("Year")
ax1.set_ylabel("Average Silver Price (₹/kg)")
st.pyplot(fig1)

st.divider()

# --------------------------------------------------
# PART 2 : INDIA MAP (GEOPANDAS – WORKING)
# --------------------------------------------------
st.subheader("India Map – Geographical Visualization")
st.caption("GeoPandas map for geographical context")

world_map = gpd.read_file(
    "https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip"
)

india_map = world_map[world_map["ADMIN"] == "India"]

fig2, ax2 = plt.subplots(figsize=(6, 6))
india_map.plot(
    ax=ax2,
    color="#e6c9a8",  # light brown
    edgecolor="black"
)
ax2.set_title("India")
ax2.axis("off")
st.pyplot(fig2)

st.divider()

# --------------------------------------------------
# TOP 5 STATES BY SILVER PURCHASE
# --------------------------------------------------
st.subheader("Top 5 States by Silver Purchase")

top_states = sales_data.sort_values(
    "Silver_Purchased_kg",
    ascending=False
).head(5)

fig3, ax3 = plt.subplots(figsize=(6, 4))
ax3.bar(
    top_states["State"],
    top_states["Silver_Purchased_kg"],
    color="brown"
)
ax3.set_xlabel("State")
ax3.set_ylabel("Silver Purchased (kg)")
ax3.tick_params(axis="x", rotation=30)
st.pyplot(fig3)

st.divider()

# --------------------------------------------------
# JANUARY SILVER PRICE TREND
# --------------------------------------------------
st.subheader("January Silver Price Trend")
st.caption("Silver price trend for January across years")

jan_data = price_data[price_data["Month"] == "Jan"]

fig4, ax4 = plt.subplots(figsize=(6, 4))
ax4.plot(
    jan_data["Year"],
    jan_data["Silver_Price_INR_per_kg"],
    marker="o",
    color="brown"
)
ax4.set_xlabel("Year")
ax4.set_ylabel("Silver Price (₹/kg)")
st.pyplot(fig4)

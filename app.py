import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AI Fisherman Decision Companion",
    page_icon="🐟",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

training_data = pd.read_csv("data/demo_training_data.csv")
fishing_zones = pd.read_csv("data/fishing_zones.csv")
market_prices = pd.read_csv("data/market_prices.csv")


# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.title("🐟 AI Fisherman Decision Companion")

st.write(
    "An AI-based decision-support prototype designed to help "
    "small-scale fishermen make safer and smarter fishing and "
    "livelihood decisions."
)

st.info(
    "⚠️ This prototype does not replace official marine or weather "
    "warnings. Official information should always be treated as "
    "the primary safety source."
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.header("👤 Fisherman Profile")

boat_type = st.sidebar.selectbox(
    "Boat Type",
    [
        "Small Fishing Boat",
        "Motorized Boat",
        "Mechanized Boat"
    ]
)

fishing_method = st.sidebar.selectbox(
    "Fishing Method",
    [
        "Gill Net",
        "Longline",
        "Trawl",
        "Hook and Line"
    ]
)

experience = st.sidebar.slider(
    "Fishing Experience (years)",
    1,
    40,
    10
)

distance = st.sidebar.slider(
    "Usual Distance From Shore (km)",
    1,
    100,
    20
)


# --------------------------------------------------
# OFFICIAL INFORMATION
# --------------------------------------------------

st.header("🌊 Official Marine Information")

col1, col2, col3 = st.columns(3)

with col1:
    sea_condition = st.selectbox(
        "Official Sea Condition",
        [
            "Calm",
            "Moderate",
            "Rough",
            "Very Rough"
        ]
    )

with col2:
    official_warning = st.selectbox(
        "Official Warning",
        [
            "No Warning",
            "Advisory",
            "Warning",
            "Severe Warning"
        ]
    )

with col3:
    wind_speed = st.number_input(
        "Wind Speed (km/h)",
        min_value=0.0,
        max_value=150.0,
        value=20.0
    )


# --------------------------------------------------
# FISHING HISTORY
# --------------------------------------------------

st.header("🎣 Previous Fishing Information")

col1, col2, col3 = st.columns(3)

with col1:
    previous_catch = st.number_input(
        "Average Previous Catch (kg)",
        min_value=0.0,
        value=100.0
    )

with col2:
    success_rate = st.slider(
        "Previous Success Rate (%)",
        0,
        100,
        60
    )

with col3:
    fuel_cost = st.number_input(
        "Estimated Fuel Cost (₹)",
        min_value=0.0,
        value=1500.0
    )


# --------------------------------------------------
# MARKET INFORMATION
# --------------------------------------------------

st.header("💰 Market Information")

col1, col2 = st.columns(2)

with col1:

    fish_type = st.selectbox(
        "Target Fish",
        market_prices["fish_type"].unique()
    )

with col2:

    selected_market = st.selectbox(
        "Market",
        market_prices["market"].unique()
    )


selected_market_data = market_prices[
    (market_prices["fish_type"] == fish_type) &
    (market_prices["market"] == selected_market)
]


if not selected_market_data.empty:

    fish_price = float(
        selected_market_data.iloc[0]["price_per_kg"]
    )

    demand = selected_market_data.iloc[0]["demand_level"]

    trend = selected_market_data.iloc[0]["price_trend"]

else:

    fish_price = 0
    demand = "Unknown"
    trend = "Unknown"


st.write(
    f"**Current Price:** ₹{fish_price:.0f}/kg"
)

st.write(
    f"**Demand:** {demand}"
)

st.write(
    f"**Price Trend:** {trend}"
)


# --------------------------------------------------
# FISHING ZONE
# --------------------------------------------------

st.header("📍 Fishing Zone")

selected_zone = st.selectbox(
    "Select Usual Fishing Zone",
    fishing_zones["zone_name"].unique()
)

zone_data = fishing_zones[
    fishing_zones["zone_name"] == selected_zone
].iloc[0]

zone_distance = float(
    zone_data["distance_from_shore_km"]
)

zone_risk = zone_data["risk_level"]

common_species = zone_data["common_species"]

typical_catch = float(
    zone_data["typical_catch_kg"]
)


st.write(
    f"**Distance:** {zone_distance:.0f} km"
)

st.write(
    f"**Common Species:** {common_species}"
)

st.write(
    f"**Zone Risk:** {zone_risk}"
)

st.write(
    f"**Typical Catch:** {typical_catch:.0f} kg"
)


# --------------------------------------------------
# AI DECISION ENGINE
# --------------------------------------------------

def analyze_decision():

    risk_score = 0
    opportunity_score = 0

    reasons = []

    # Official warning

    if official_warning == "Severe Warning":

        risk_score += 100

        reasons.append(
            "Official severe warning is active."
        )

    elif official_warning == "Warning":

        risk_score += 70

        reasons.append(
            "Official marine warning is active."
        )

    elif official_warning == "Advisory":

        risk_score += 30

        reasons.append(
            "Official advisory is active."
        )


    # Sea condition

    if sea_condition == "Very Rough":

        risk_score += 60

        reasons.append(
            "Sea condition is very rough."
        )

    elif sea_condition == "Rough":

        risk_score += 40

        reasons.append(
            "Sea condition is rough."
        )

    elif sea_condition == "Moderate":

        risk_score += 20


    # Wind

    if wind_speed > 50:

        risk_score += 50

        reasons.append(
            "Wind speed is high."
        )

    elif wind_speed > 35:

        risk_score += 30

        reasons.append(
            "Wind speed is moderately high."
        )

    elif wind_speed > 20:

        risk_score += 10


    # Boat sensitivity

    if (
        boat_type == "Small Fishing Boat"
        and sea_condition in ["Rough", "Very Rough"]
    ):

        risk_score += 25

        reasons.append(
            "Small boats may be more sensitive "
            "to rough sea conditions."
        )


    # Distance

    if zone_distance > 50:

        risk_score += 25

        reasons.append(
            "Selected zone is far from shore."
        )

    elif zone_distance > 30:

        risk_score += 15


    # Zone risk

    if zone_risk == "High":

        risk_score += 25

    elif zone_risk == "Medium":

        risk_score += 10


    # Historical opportunity

    if success_rate >= 70:

        opportunity_score += 30

    elif success_rate >= 50:

        opportunity_score += 20

    else:

        opportunity_score += 10


    # Catch history

    if previous_catch >= 150:

        opportunity_score += 30

    elif previous_catch >= 80:

        opportunity_score += 20

    else:

        opportunity_score += 10


    # Market demand

    if demand == "High":

        opportunity_score += 25

    elif demand == "Medium":

        opportunity_score += 15

    else:

        opportunity_score += 5


    # Market price

    if fish_price >= 400:

        opportunity_score += 20

    elif fish_price >= 250:

        opportunity_score += 10


    # Expected revenue

    expected_catch = min(
        previous_catch,
        typical_catch
    )

    expected_revenue = (
        expected_catch * fish_price
    )

    estimated_profit = (
        expected_revenue - fuel_cost
    )


    # Final decision

    if official_warning == "Severe Warning":

        decision = "🔴 AVOID TRIP"

        explanation = (
            "The official source indicates a severe warning. "
            "Safety should take priority over fishing opportunity."
        )

    elif risk_score >= 100:

        decision = "🔴 HIGH RISK"

        explanation = (
            "Multiple risk factors are currently present. "
            "Recheck official information before making any decision."
        )

    elif risk_score >= 60:

        decision = "🟡 WAIT / REASSESS"

        explanation = (
            "Conditions show elevated risk. "
            "Consider reassessing the trip using updated official information."
        )

    elif opportunity_score >= 60:

        decision = "🟢 RELATIVELY SUITABLE"

        explanation = (
            "The current inputs indicate relatively manageable "
            "conditions and reasonable fishing opportunity."
        )

    else:

        decision = "🟡 LOW OPPORTUNITY"

        explanation = (
            "The estimated fishing and market opportunity is limited."
        )


    return (
        decision,
        risk_score,
        opportunity_score,
        expected_revenue,
        estimated_profit,
        reasons,
        explanation
    )


# --------------------------------------------------
# ANALYSE BUTTON
# --------------------------------------------------

st.divider()

if st.button(
    "🧠 ANALYSE MY FISHING DECISION",
    use_container_width=True
):

    (
        decision,
        risk_score,
        opportunity_score,
        expected_revenue,
        estimated_profit,
        reasons,
        explanation
    ) = analyze_decision()


    # Decision

    st.header("🤖 AI Decision")

    st.success(decision)

    st.write(explanation)


    # Scores

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Risk Score",
            risk_score
        )

    with col2:

        st.metric(
            "Fishing Opportunity Score",
            opportunity_score
        )


    # Financial analysis

    st.header("💰 Livelihood Analysis")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Expected Revenue",
            f"₹{expected_revenue:,.0f}"
        )

    with col2:

        st.metric(
            "Estimated Profit",
            f"₹{estimated_profit:,.0f}"
        )


    # Explanation

    st.header(
        "🔎 Why did the system make this recommendation?"
    )

    if reasons:

        for reason in reasons:

            st.write(
                "• " + reason
            )

    else:

        st.write(
            "No major risk factors detected."
        )


    # Safety

    st.warning(
        "⚠️ Safety Notice: This is a prototype decision-support "
        "system. It does not replace official marine warnings, "
        "government advisories, or professional judgement."
    )


# --------------------------------------------------
# ARCHITECTURE
# --------------------------------------------------

st.divider()

st.header("🏗️ How Our System Works")

st.markdown("""
**Official Marine Information**
↓  
**Fisherman Profile**
↓  
**Boat + Location + Fishing History**
↓  
**Market Information**
↓  
🧠 **Decision Engine**
↓  
**Risk + Opportunity Analysis**
↓  
**Personalized Recommendation**
""")

import streamlit as st

st.set_page_config(page_title="IterationOne Pricing Calculator", layout="wide")

st.title("3D Printing Business Pricing & Profit Calculator")
st.markdown("Calculate costs and profit splits for a bootstrapped, two-person 3D printing business.")

st.header("1. Global Variables")
col1, col2, col3, col4 = st.columns(4)

with col1:
    filament_price = st.number_input("Filament Price per kg (₹)", min_value=0.0, value=1200.0, step=1.0)
with col2:
    electricity_cost = st.number_input("Electricity Cost / kWh (₹)", min_value=0.0, value=8.5, step=0.01)
with col3:
    printer_energy_kwh = st.number_input("Printer Energy Usage (kW/h)", min_value=0.0, value=0.1, step=0.05)
with col4:
    maintenance_cost_per_hour = st.number_input("Maintenance / Print Hour (₹)", min_value=0.0, value=5.0, step=0.10)

st.header("2. Product Specifics")
col_p1, col_p2 = st.columns(2)

with col_p1:
    filament_weight = st.number_input("Filament Weight per Print (g)", min_value=0.0, value=150.0, step=5.0)
with col_p2:
    print_time = st.number_input("Print Time (hours)", min_value=0.0, value=8.0, step=0.5)

st.header("3. Dynamic Team Effort & Ratios")
st.markdown("Determine the total time spent and how the effort is distributed between Person A and Person B.")

col_e1, col_e2 = st.columns(2)

with col_e1:
    st.subheader("Design Time")
    design_time = st.number_input("Total Design Time (hours)", min_value=0.0, value=3.0, step=0.5)
    person_a_design_share = st.slider("Person A Design Contribution (%)", min_value=0, max_value=100, value=50, key="design_share")
    person_b_design_share = 100 - person_a_design_share
    st.write(f"Person B Design Contribution: **{person_b_design_share}%**")

with col_e2:
    st.subheader("Physical Labor Time")
    labor_time = st.number_input("Total Physical Labor Time (hours)", min_value=0.0, value=1.5, step=0.5)
    person_a_labor_share = st.slider("Person A Labor Contribution (%)", min_value=0, max_value=100, value=50, key="labor_share")
    person_b_labor_share = 100 - person_a_labor_share
    st.write(f"Person B Labor Contribution: **{person_b_labor_share}%**")

st.header("4. Pricing Strategy")
col_s1, col_s2 = st.columns(2)
with col_s1:
    hourly_rate = st.number_input("Target Hourly Rate for Labor (₹)", min_value=0.0, value=25.0, step=1.0)
with col_s2:
    profit_margin = st.number_input("Desired Profit Margin (%)", min_value=0.0, value=30.0, step=1.0) / 100.0

st.divider()

# --- Calculations ---

# 1. Cost of Goods Sold (COGS)
material_cost = (filament_price / 1000.0) * filament_weight
energy_kwh = printer_energy_kwh * print_time
energy_cost = energy_kwh * electricity_cost
maintenance_cost = maintenance_cost_per_hour * print_time
total_cogs = material_cost + energy_cost + maintenance_cost

# 2. Time Value (Labor Cost)
total_design_value = design_time * hourly_rate
total_labor_value = labor_time * hourly_rate
total_time_value = total_design_value + total_labor_value

# 3. Final Pricing
base_price = total_cogs + total_time_value
final_price = base_price * (1 + profit_margin)
total_profit = final_price - total_cogs # The amount available to pay for time + margin

# 4. Payout Distribution
# Calculate the monetary value contributed by each person
person_a_contribution_value = (total_design_value * (person_a_design_share / 100.0)) + \
                              (total_labor_value * (person_a_labor_share / 100.0))

person_b_contribution_value = (total_design_value * (person_b_design_share / 100.0)) + \
                              (total_labor_value * (person_b_labor_share / 100.0))

if total_time_value > 0:
    # Split the total profit based on the proportion of time value contributed
    person_a_ratio = person_a_contribution_value / total_time_value
    person_b_ratio = person_b_contribution_value / total_time_value
else:
    # Fallback to 50/50 if no time was logged
    person_a_ratio = 0.5
    person_b_ratio = 0.5

person_a_payout = total_profit * person_a_ratio
person_b_payout = total_profit * person_b_ratio

# --- Results ---

st.header("5. Results & Exact Payout Distribution")

col_r1, col_r2, col_r3 = st.columns(3)

with col_r1:
    st.subheader("Cost Breakdown")
    st.write(f"**Material Cost:** ₹{material_cost:.2f}")
    st.write(f"**Electricity Cost:** ₹{energy_cost:.2f}")
    st.write(f"**Maintenance Cost:** ₹{maintenance_cost:.2f}")
    st.markdown(f"**Total COGS:** **₹{total_cogs:.2f}**")

with col_r2:
    st.subheader("Pricing Summary")
    st.write(f"**Base Price (COGS + Labor):** ₹{base_price:.2f}")
    st.write(f"**Total Profit (Labor + Margin):** ₹{total_profit:.2f}")
    st.markdown(f"### **Final Suggested Price: ₹{final_price:.2f}**")

with col_r3:
    st.subheader("Payout Distribution")
    st.success(f"**Person A Payout:** ₹{person_a_payout:.2f}")
    st.info(f"**Person B Payout:** ₹{person_b_payout:.2f}")

    # Sanity check display
    if round(person_a_payout + person_b_payout, 2) == round(total_profit, 2):
        st.caption("✅ Payouts match total profit exactly.")
    else:
        st.caption("⚠️ Payout mismatch (rounding error).")

import streamlit as st
import pandas as pd

st.title("USER_INPUT Table")

# --- Sample data ---
data = {
    "Market Unit": ["Saudi", "ME", "ME", "ME"],
    "Country": ["Oman", "UAE", "UAE", "UAE"],
    "Risk": ["Low Risk", "Low Risk", "Low Risk", "Low Risk"],
    "Project Code": ["Project#1", "Project#1", "Project#1", "Project#1"],
    "Technology": ["SRAN", "5G", "MW", "CW"],
    "Scope": ["New", "New", "Swap", "Exp"],
    "Project Volume": [789, 999, 790, 555],
    "Project Duration": [10, 12, 5, 10]
}

df = pd.DataFrame(data)

# --- Country mapping for Risk & Market Unit ---
country_data = {
    "UAE": {"Risk": "Low Risk", "Market Unit": "ME"},
    "Qatar": {"Risk": "Low Risk", "Market Unit": "NA"},
    "Oman": {"Risk": "Low Risk", "Market Unit": "NA"},
    "Saudi Bahrain": {"Risk": "Low Risk", "Market Unit": "CEWA"},
    "Rwanda": {"Risk": "Low Risk", "Market Unit": "SAV"},
    "Jordan": {"Risk": "Low Risk", "Market Unit": "NA"},
    "Moroco": {"Risk": "Low Risk", "Market Unit": "NA"},
    "Saudi Arabia": {"Risk": "Low Risk", "Market Unit": "NA"},
    "Maurtitus": {"Risk": "Low Risk", "Market Unit": "NA"},
    "Kuwait": {"Risk": "Low Risk", "Market Unit": "NA"},
    "Senegal": {"Risk": "Low Risk", "Market Unit": "NA"},
    "Egypt": {"Risk": "Low Risk", "Market Unit": "NA"},
    "Namibia": {"Risk": "Low Risk", "Market Unit": "NA"},
    "Tunisia": {"Risk": "Low Risk", "Market Unit": "NA"},
    "Alegria": {"Risk": "Low Risk", "Market Unit": "NA"},
    "Madagascar": {"Risk": "Low Risk", "Market Unit": "NA"},
    "Cyshell": {"Risk": "Low Risk", "Market Unit": "NA"},
    "Comoros": {"Risk": "Low Risk", "Market Unit": "NA"},
    "Cape Verdi": {"Risk": "Low Risk", "Market Unit": "NA"},
    "Kenya": {"Risk": "Medium Risk", "Market Unit": "NA"},
    "Ghana": {"Risk": "Medium Risk", "Market Unit": "NA"},
    "Zambia": {"Risk": "Medium Risk", "Market Unit": "NA"},
    "Uganda": {"Risk": "Medium Risk", "Market Unit": "NA"},
    "Lebanon": {"Risk": "Medium Risk", "Market Unit": "NA"},
    "Tanzania": {"Risk": "Medium Risk", "Market Unit": "NA"},
    "Ethiopia": {"Risk": "Medium Risk", "Market Unit": "NA"},
    "Cameron": {"Risk": "Medium Risk", "Market Unit": "NA"},
    "Pakistan": {"Risk": "Medium Risk", "Market Unit": "NA"},
    "Muaritania": {"Risk": "Medium Risk", "Market Unit": "NA"},
    "Eriteria": {"Risk": "Medium Risk", "Market Unit": "NA"},
    "Dijibouti": {"Risk": "Medium Risk", "Market Unit": "NA"},
    "Congo": {"Risk": "Medium Risk", "Market Unit": "NA"},
    "Gabon": {"Risk": "Medium Risk", "Market Unit": "NA"},
    "Benin": {"Risk": "Medium Risk", "Market Unit": "NA"},
    "Equatorial Guniea": {"Risk": "Medium Risk", "Market Unit": "NA"},
    "Togo": {"Risk": "Medium Risk", "Market Unit": "NA"},
    "Cote D'ivoir": {"Risk": "Medium Risk", "Market Unit": "NA"},
    "Liberia": {"Risk": "Medium Risk", "Market Unit": "NA"},
    "Sierraleone": {"Risk": "Medium Risk", "Market Unit": "NA"},
    "Guniea": {"Risk": "Medium Risk", "Market Unit": "NA"},
    "Guniea Bissau": {"Risk": "Medium Risk", "Market Unit": "NA"},
    "Gambia": {"Risk": "Medium Risk", "Market Unit": "NA"},
    "Malawi": {"Risk": "Medium Risk", "Market Unit": "NA"},
    "Mozambique": {"Risk": "Medium Risk", "Market Unit": "NA"},
    "Zimbabwe": {"Risk": "Medium Risk", "Market Unit": "NA"},
    "Botswana": {"Risk": "Medium Risk", "Market Unit": "NA"},
    "Eswatini": {"Risk": "Medium Risk", "Market Unit": "NA"},
    "Lesoto": {"Risk": "Medium Risk", "Market Unit": "NA"},
    "South Africa": {"Risk": "Medium Risk", "Market Unit": "NA"},
    "Angola": {"Risk": "Medium Risk", "Market Unit": "NA"},
    "Burundi": {"Risk": "Medium Risk", "Market Unit": "NA"},
    "Western Sahara": {"Risk": "Medium Risk", "Market Unit": "NA"},
    "Nigeria": {"Risk": "High Risk", "Market Unit": "NA"},
    "Libya": {"Risk": "High Risk", "Market Unit": "NA"},
    "South Sudan": {"Risk": "High Risk", "Market Unit": "NA"},
    "Somalia": {"Risk": "High Risk", "Market Unit": "NA"},
    "Central Africa": {"Risk": "High Risk", "Market Unit": "NA"},
    "Mali": {"Risk": "High Risk", "Market Unit": "NA"},
    "Burkina Faso": {"Risk": "High Risk", "Market Unit": "NA"},
    "Congo DRC": {"Risk": "High Risk", "Market Unit": "NA"},
    "Chad": {"Risk": "High Risk", "Market Unit": "NA"},
    "Niger": {"Risk": "High Risk", "Market Unit": "NA"},
    "Syria": {"Risk": "Very High", "Market Unit": "NA"},
    "Yamen": {"Risk": "Very High", "Market Unit": "NA"},
    "Sudan": {"Risk": "Very High", "Market Unit": "NA"},
    "Iraq": {"Risk": "Very High", "Market Unit": "NA"},
    "Iran": {"Risk": "Very High", "Market Unit": "NA"},
    "Palestine": {"Risk": "Very High", "Market Unit": "NA"},
}

# --- Columns to show in the editable table ---
editable_columns = ["Country", "Project Code", "Technology", "Project Volume", "Project Duration"]

# --- Dropdown options ---
dropdown_options = {
    "Country": list(country_data.keys()),
    "Project Code": ["Project#1", "Project#2"],
}

# --- Column config ---
column_config_dict = {}
for col in editable_columns:
    if col == "Country":
        column_config_dict[col] = st.column_config.SelectboxColumn(
            label=col,
            options=dropdown_options[col]
        )
    elif col == "Project Code":
        column_config_dict[col] = st.column_config.SelectboxColumn(
            label=col,
            options=dropdown_options[col]
        )
    elif col == "Technology":
        # Show Scope but make it read-only
        column_config_dict[col] = st.column_config.Column(label=col, disabled=True)
    elif col in ["Project Volume", "Project Duration"]:
        column_config_dict[col] = st.column_config.NumberColumn(label=col, step=1)

# --- Editable table ---
edited_df = st.data_editor(df[editable_columns], column_config=column_config_dict, width="stretch")

# --- Sync edited values back to full DataFrame ---
for col in ["Country", "Project Code", "Project Volume", "Project Duration"]:
    df[col] = edited_df[col]

# --- Auto-update Risk & Market Unit in the full DataFrame ---
for idx in df.index:
    country = df.at[idx, "Country"]
    if country in country_data:
        df.at[idx, "Risk"] = country_data[country]["Risk"]
        df.at[idx, "Market Unit"] = country_data[country]["Market Unit"]

# --- Submit button ---
if st.button("Submit USER_INPUT"):
    st.success("✅ USER_INPUT submitted successfully!")
    st.write("Updated Full Table (including Risk & Market Unit):")
    st.dataframe(df)





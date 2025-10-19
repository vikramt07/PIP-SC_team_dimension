import streamlit as st
import pandas as pd

st.title("USER_INPUT Table")

# --- Sample data (from your screenshot) ---
data = {
    "Market Unit": ["Saudi", "ME", "ME", "ME"],
    "Country": ["Oman", "UAE", "UAE", "UAE"],
    "Risk": ["Low Risk", "Low Risk", "Low Risk", "Low Risk"],
    "Project Code": ["Project#1", "Project#1", "Project#1", "Project#1"],
    "Technology": ["SRAN", "5G", "MW", "CW"],
    "Scope": ["New", "Swap", "Exp"],
    "Project Volume": [789, 999, 790, 555],
    "Project Duration": [10, 12, 5, 10]
}

df = pd.DataFrame(data)

# --- Columns that can be edited ---
editable_columns = ["Country", "Project Code", "Scope", "Project Volume", "Project Duration"]

# --- Dropdown options ---
dropdown_options = {
    "Country": ["Oman", "UAE", "KSA"],        # Add all your countries here
    "Project Code": ["Project#1", "Project#2"],  # Add all project codes here
    "Scope": ["New", "Swap", "Exp"]           # Add all scopes here
}

# --- Streamlit column config ---
column_config_dict = {}
for col in df.columns:
    if col in ["Country", "Project Code", "Scope"]:
        column_config_dict[col] = st.column_config.SelectboxColumn(
            label=col,
            options=dropdown_options[col]
        )
    elif col in ["Project Volume", "Project Duration"]:
        column_config_dict[col] = st.column_config.NumberColumn(
            label=col,
            step=1
        )
    else:
        column_config_dict[col] = st.column_config.Column(label=col, disabled=True)

# --- Editable table ---
edited_df = st.data_editor(df, column_config=column_config_dict, width="stretch")

# --- Submit button ---
if st.button("Submit USER_INPUT"):
    st.success("✅ USER_INPUT submitted successfully!")
    st.write("Updated Table:")
    st.dataframe(edited_df)



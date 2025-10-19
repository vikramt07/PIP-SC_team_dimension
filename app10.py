import streamlit as st
import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils import range_boundaries, get_column_letter
import tempfile
import requests
import base64
import json
import os

# --- Repo details ---
REPO = "vikramt07/PIP-SC_team_dimension"
FILE_PATH = "PIP-SC_team_dimension - Copy.xlsx"
BRANCH = "main"

st.title("PIP-SC Team Dimension Calculation — Cloud + GitHub Save")

# --- Editable setup ---
editable_columns = ["Country", "Project Code", "Scope", "Project Volume", "Project Duration"]
dropdown_columns = ["Country", "Project Code", "Scope"]
merge_titles = ["SRAN", "5G", "MW", "CW", "COMMON TEAM"]

# --- GitHub raw file URL ---
RAW_URL = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{FILE_PATH.replace(' ', '%20')}"

# --- Load Excel file into memory ---
@st.cache_data(ttl=60)
def load_excel():
    r = requests.get(RAW_URL)
    if r.status_code != 200:
        st.error("❌ Could not load Excel from GitHub.")
        st.stop()
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
    tmp.write(r.content)
    tmp.flush()
    return tmp.name

excel_path = load_excel()

# --- Dropdown options from Sheet4 ---
sheet4_df = pd.read_excel(excel_path, sheet_name="Sheet4")
dropdown_options = {col: sheet4_df[col].dropna().unique().tolist() for col in dropdown_columns}

# --- Session state ---
if "submitted" not in st.session_state:
    st.session_state.submitted = False


# --- Helper: Load USER_INPUT table ---
def load_user_table():
    wb = load_workbook(excel_path, data_only=False)
    ws = wb["Sheet1"]
    df_user = None
    min_col = min_row = 0
    for t in ws.tables:
        if t == "USER_INPUT":
            tbl_obj = ws.tables[t]
            min_col, min_row, max_col, max_row = range_boundaries(tbl_obj.ref)
            usecols = f"{get_column_letter(min_col)}:{get_column_letter(max_col)}"
            nrows = max_row - min_row + 1
            df_user = pd.read_excel(
                excel_path,
                sheet_name=ws.title,
                header=0,
                usecols=usecols,
                skiprows=min_row - 1,
                nrows=nrows
            )
            df_user.columns = [str(c).strip() for c in df_user.columns]
            df_user = df_user.loc[:, ~df_user.columns.duplicated(keep="first")]
            df_user = df_user.fillna("")
            break
    wb.close()
    return df_user, min_col, min_row


# --- Load other tables (read-only) ---
def load_other_tables():
    wb = load_workbook(excel_path, data_only=False)
    all_tables = {}
    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        for t in ws.tables:
            if t != "USER_INPUT":
                tbl_obj = ws.tables[t]
                ref = getattr(tbl_obj, "ref", None)
                if not ref:
                    continue
                min_col, min_row, max_col, max_row = range_boundaries(ref)
                usecols = f"{get_column_letter(min_col)}:{get_column_letter(max_col)}"
                nrows = max_row - (min_row - 1)
                df = pd.read_excel(
                    excel_path,
                    sheet_name=sheet_name,
                    header=0,
                    usecols=usecols,
                    skiprows=min_row - 1,
                    nrows=nrows
                )
                df.columns = [str(c).strip() for c in df.columns]
                df = df.fillna("")
                all_tables[t] = df
    wb.close()
    return all_tables


# --- Render USER_INPUT ---
df_user, min_col, min_row = load_user_table()

if df_user is None:
    st.warning("USER_INPUT table not found.")
else:
    column_config_dict = {}
    for col in df_user.columns:
        if col in dropdown_columns:
            column_config_dict[col] = st.column_config.SelectboxColumn(label=col, options=dropdown_options[col])
        elif col in ["Project Volume", "Project Duration"]:
            column_config_dict[col] = st.column_config.NumberColumn(label=col, step=1)
        else:
            column_config_dict[col] = st.column_config.Column(label=col, disabled=True)

    edited_df = st.data_editor(df_user, column_config=column_config_dict, width="stretch")

    if st.button("Submit USER_INPUT"):
        changed = False
        wb = load_workbook(excel_path, data_only=False)
        ws = wb["Sheet1"]

        for row_idx in range(len(df_user)):
            for col_name in editable_columns:
                if col_name in df_user.columns:
                    old_val = df_user.at[row_idx, col_name]
                    new_val = edited_df.at[row_idx, col_name]
                    if old_val != new_val:
                        excel_col_idx = df_user.columns.get_loc(col_name) + min_col
                        excel_row_idx = min_row + row_idx + 1
                        ws.cell(row=excel_row_idx, column=excel_col_idx, value=new_val)
                        changed = True

        if changed:
            wb.save(excel_path)
            wb.close()

            # --- Upload back to GitHub ---
            token = os.environ.get("GITHUB_TOKEN")
            if not token:
                st.error("❌ GitHub token missing. Add it in Streamlit secrets.")
                st.stop()

            # Get current file SHA (required for update)
            url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"
            headers = {"Authorization": f"token {token}"}
            get_resp = requests.get(url, headers=headers)
            sha = get_resp.json().get("sha")

            with open(excel_path, "rb") as f:
                content = base64.b64encode(f.read()).decode()

            payload = {
                "message": "Update USER_INPUT from Streamlit app",
                "content": content,
                "branch": BRANCH,
                "sha": sha
            }
            put_resp = requests.put(url, headers=headers, data=json.dumps(payload))

            if put_resp.status_code in [200, 201]:
                st.success("✅ Changes saved back to GitHub!")
            else:
                st.error(f"⚠️ Failed to save: {put_resp.json()}")

        else:
            st.info("ℹ️ No changes detected.")

        st.session_state.submitted = True
        st.rerun()


# --- Render other tables ---
if st.session_state.submitted:
    other_tables = load_other_tables()
    for name, df in other_tables.items():
        st.subheader(f"{name} Table")
        st.dataframe(df, width="stretch")

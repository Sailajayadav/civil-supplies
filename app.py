from flask import Flask, render_template
import pandas as pd
from db_config import get_connection

app = Flask(__name__)

# Correct column names based on actual table
SUMMARY_COLS = [
    "MLS_Point_Code", 
    "MLS_Point_Name", 
    "Mandal_Name", 
    "District_Name",
    "MLS_Point_Incharge_Name", 
    "Storage_Capacity_in"
]

def get_all_summary():
    conn = get_connection()
    df = pd.read_sql(
        f"SELECT {', '.join(SUMMARY_COLS)} FROM dbo.MLS_Master_Data1", conn
    )
    conn.close()
    return df

def get_details(mls_code):
    conn = get_connection()
    df = pd.read_sql(
        "SELECT * FROM dbo.MLS_Master_Data1 WHERE MLS_Point_Code = ?", conn, params=[mls_code]
    )
    conn.close()
    return df.iloc[0].to_dict() if not df.empty else None

@app.route('/')
def index():
    records = get_all_summary().to_dict(orient="records")
    return render_template("index.html", records=records)

@app.route('/details/<int:mls_code>')
def details(mls_code):
    info = get_details(mls_code)
    if not info:
        return "No details found", 404
    return render_template("details.html", info=info)

if __name__ == '__main__':
    app.run(debug=True)

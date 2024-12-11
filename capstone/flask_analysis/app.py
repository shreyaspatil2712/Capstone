from flask import Flask, render_template
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
import pandas as pd
import plotly.express as px
from models import Base, DIMCountry, DIMIndicator, DIMTime, FACTEnrollment

app = Flask(__name__)

# MSSQL Connection
db_url = "mssql+pyodbc://INFA_DOM3:admin123@21BAI1851\\SQLEXPRESS/dev_db?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(db_url, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Function to fetch and prepare data
def fetch_and_prepare_data():
    query = session.query(
        FACTEnrollment.Indicator_Value,
        DIMCountry.Country_Name,
        DIMCountry.Region,
        DIMCountry.IncomeGroup,
        DIMIndicator.Indicator_Name,
        DIMTime.Year
    ).join(DIMCountry).join(DIMIndicator).join(DIMTime)
    
    data = pd.DataFrame(query.all(), columns=[
        "Indicator_Value", "Country_Name", "Region",
        "IncomeGroup", "Indicator_Name", "Year"
    ])
    return data

# Function to generate graphs
def generate_graphs(data):
    graphs = {}
    indicators = data['Indicator_Name'].unique()

    for indicator in indicators:
        indicator_data = data[data['Indicator_Name'] == indicator]

        # 1. Line Graph: Indicator per Country vs Year
        graphs[f"{indicator}_line_country"] = px.line(
            indicator_data,
            x='Year',
            y='Indicator_Value',
            color='Country_Name',
            title=f'{indicator}: Line Graph per Country vs Year'
        ).to_html(full_html=False)

        # 2. Line Graph: Indicator per Region (Averaged) vs Year
        region_avg = indicator_data.groupby(['Region', 'Year'])['Indicator_Value'].mean().reset_index()
        graphs[f"{indicator}_line_region"] = px.line(
            region_avg,
            x='Year',
            y='Indicator_Value',
            color='Region',
            title=f'{indicator}: Line Graph per Region vs Year (Averaged)'
        ).to_html(full_html=False)

        # 3. Bar Graph: Average per Country across All Years
        country_avg = indicator_data.groupby('Country_Name')['Indicator_Value'].mean().reset_index()
        graphs[f"{indicator}_bar_country"] = px.bar(
            country_avg,
            x='Country_Name',
            y='Indicator_Value',
            title=f'{indicator}: Bar Graph of Average per Country Across All Years'
        ).to_html(full_html=False)

        # 4. Line Graph: Average per Year for All Countries
        year_avg = indicator_data.groupby('Year')['Indicator_Value'].mean().reset_index()
        graphs[f"{indicator}_avg_all_countries_line"] = px.line(
            year_avg,
            x='Year',
            y='Indicator_Value',
            title=f'{indicator}: Average Value for All Countries per Year (Line)'
        ).to_html(full_html=False)

        # 5. Bar Graph: Average per Year for All Countries
        graphs[f"{indicator}_avg_all_countries_bar"] = px.bar(
            year_avg,
            x='Year',
            y='Indicator_Value',
            title=f'{indicator}: Average Value for All Countries per Year (Bar)'
        ).to_html(full_html=False)

        # 6. Line Graph: Indicator per Income Class vs Year (Averaged)
        income_avg = indicator_data.groupby(['IncomeGroup', 'Year'])['Indicator_Value'].mean().reset_index()
        graphs[f"{indicator}_line_income"] = px.line(
            income_avg,
            x='Year',
            y='Indicator_Value',
            color='IncomeGroup',
            title=f'{indicator}: Line Graph per Income Class vs Year (Averaged)'
        ).to_html(full_html=False)


    return graphs

# Flask route for the dashboard
@app.route('/')
def index():
    data = fetch_and_prepare_data()
    graphs = generate_graphs(data)
    return render_template('index.html', graphs=graphs)

if __name__ == "__main__":
    app.run(debug=True)

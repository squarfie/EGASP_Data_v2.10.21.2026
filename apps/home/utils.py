# apps/your_app/utils.py


from sqlalchemy import create_engine
import pandas as pd
from django.utils.dateparse import parse_date

#creating a connection to postgresql
try:
    # Create SQLAlchemy engine
    engine = create_engine('postgresql+psycopg2://postgres:admin123@localhost:5432/test_db')

    # SQL query to fetch data
    breakpoints_query = "SELECT * FROM home_breakpointstable"
    antibiotic_query = "SELECT * FROM home_antibioticentry"
    # Use pandas to fetch data via SQLAlchemy engine
    breakpoint_data = pd.read_sql_query(breakpoints_query, engine)
    antibiotic_data = pd.read_sql_query(antibiotic_query, engine)


    # Display the data
    print(breakpoint_data)
    print(antibiotic_data)


    


except Exception as error:
    print("Error while fetching data from PostgreSQL:", error)


# finally:
#     print("Execution completed")

def clean_date(value):
    if not value or value.strip() in ["", "n/a", "NA", None]:
        return None
    
    value = value.strip()

    # Try Django's flexible parser first
    dt = parse_date(value)
    if dt:
        return dt

    # Try multiple fallback formats
    formats = [
        "%m/%d/%Y",
        "%m-%d-%Y",
        "%m %d %Y",
        "%Y-%m-%d",
        "%Y/%m/%d"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(value, fmt).date()
        except:
            pass

    # If still invalid, return None instead of failing
    return None
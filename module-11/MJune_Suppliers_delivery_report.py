import mysql.connector  # type: ignore
import pandas as pd  # type: ignore

try:
    config = {
        "user": "root",
        "password": "MillieBop2020",
        "host": "localhost",
        "database": "bacchus_winery",
        "raise_on_warnings": True
    }

    # Connect to the database
    db_connection = mysql.connector.connect(**config)
    print("Connection to the Bacchus Winery database was successful!")

except mysql.connector.Error as err:
    print(f"Error: {err}")
    exit(1)

cursor = db_connection.cursor()

# Create or replace view
cursor.execute("""
    CREATE OR REPLACE VIEW supplier_delivery AS
    SELECT 
        so.order_num,
        so.order_date,
        sup.supplier_name,
        st.est_delivery_date,
        st.delivery_date,
        st.carrier,
        st.tracking_number
    FROM shipment_tracking AS st
    JOIN supply_orders AS so ON st.shipment_id = so.shipment_id
    JOIN suppliers AS sup ON sup.supplier_id = so.supplier_id
""")

def generate_supplier_delivery_report(cursor):
    # Define the year and months for the report
    year = 2024
    months = ['04', '05', '06']  # April, May, June

    # SQL query to fetch delivery data for April to June 2024
    sql = f"""
    SELECT 
        sup.supplier_name,
        MONTH(st.delivery_date) AS delivery_month,
        COUNT(st.delivery_date) AS total_deliveries,
        SUM(CASE WHEN st.delivery_date <= st.est_delivery_date THEN 1 ELSE 0 END) AS on_time_deliveries,
        AVG(CASE WHEN st.delivery_date > st.est_delivery_date THEN DATEDIFF(st.delivery_date, st.est_delivery_date) ELSE NULL END) AS average_days_late
    FROM 
        shipment_tracking st
    JOIN supply_orders so ON st.shipment_id = so.shipment_id
    JOIN suppliers sup ON sup.supplier_id = so.supplier_id
    WHERE 
        YEAR(st.delivery_date) = %s AND MONTH(st.delivery_date) IN ({','.join(['%s'] * len(months))})
    GROUP BY 
        sup.supplier_name, delivery_month
    ORDER BY 
        delivery_month, sup.supplier_name
    """

    cursor.execute(sql, (year, months[0], months[1], months[2]))
    result = cursor.fetchall()

    # Create a DataFrame to display the results
    df = pd.DataFrame(result, columns=[
        'Supplier Name', 'Delivery Month', 'Total Deliveries', 
        'On-Time Deliveries', 'Average Days Late'
    ])

    # Calculate for on-time deliveries
    df['All On Time'] = df['Total Deliveries'] == df['On-Time Deliveries']

    print("\nSupplier Delivery Report for April to June 2024")
    print(df)

# Generate the report
generate_supplier_delivery_report(cursor)

# Close the cursor and connection
cursor.close()
db_connection.close()
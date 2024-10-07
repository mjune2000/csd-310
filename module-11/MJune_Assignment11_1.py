import mysql.connector  # type: ignore
import pandas as pd  # type: ignore

try:
    config = {
        "user": "root",
        "password": "blahblahblah",
        "host": "localhost",
        "database": "bacchus_winery",
        "raise_on_warnings": True
    }

    # Connect to the database
    db_connection = mysql.connector.connect(**config)
    print("Connection to the Bacchus Winery database was successful!")

    cursor = db_connection.cursor()

    cursor.execute("""
    CREATE OR REPLACE VIEW supplier_delivery AS
    SELECT 
        supplier_id,
        so.shipment_id,
        st.delivery_date,
        st.est_delivery_date
    FROM shipment_tracking AS st
    JOIN supply_orders AS so ON st.tracking_number = so.shipment_id
    JOIN supplier_products AS sp ON sp.supplier_name = sp.supplier_id
    """)

    def generate_supplier_delivery_report():
        year = 2023
        months = [4, 5, 6]  # April, May, June

        sql = """ 
        SELECT 
            s.supplier_name,
            MONTH(sd.delivery_date) AS delivery_month,
            COUNT(sd.delivery_date) AS total_deliveries,
            SUM(CASE WHEN sd.delivery_date <= sd.est_delivery_date THEN 1 ELSE 0 END) AS on_time_deliveries,
            AVG(CASE WHEN sd.delivery_date > sd.est_delivery_date THEN DATEDIFF(sd.delivery_date, sd.est_delivery_date) ELSE NULL END) AS average_days_late
        FROM 
            supplier_delivery AS sd
        JOIN suppliers AS s ON sd.supplier_id = s.supplier_id
        WHERE 
            YEAR(sd.delivery_date) = %s AND MONTH(sd.delivery_date) IN (%s, %s, %s)
        GROUP BY 
            s.supplier_name, delivery_month
        ORDER BY 
            delivery_month, s.supplier_name
        """

        cursor.execute(sql, (year, months[0], months[1], months[2]))
        result = cursor.fetchall()

        df = pd.DataFrame(result, columns=[
            'Supplier Name', 'Delivery Month', 'Total Deliveries', 
            'On-Time Deliveries', 'Average Days Late'
        ])

        # Calculate if all deliveries are on time
        df['All On Time'] = df['Total Deliveries'] == df['On-Time Deliveries']

        print("\nSupplier Delivery Report for April to June 2023")
        print(df)

    # Generate the report
    generate_supplier_delivery_report()

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    # Ensure the cursor and connection are closed
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'db_connection' in locals() and db_connection:
        db_connection.close()

# Hector Lara Mikaela June Robert Minkler Group 3 Milestone 2 Python script 9/27/2024


#  Import package that allows Python to connect to MySQL and execute SQL queries.
import mysql.connector

# Step 2: Establish a connection to MySQL
# We need to specify the host (usually localhost for local development),
# user (username for MySQL), password (your MySQL password).
try:
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="MillieBop2020",
    )

    print("Connection to the Winery database was successful!")

except mysql.connector.Error as err:
    print(f"Error: {err}")
    exit(1)

# Step 3: Create a cursor object to execute SQL queries
cursor = db_connection.cursor()

# Step 4: Create the 'winery' database if it doesn't exist
cursor.execute("CREATE DATABASE IF NOT EXISTS winery;")
print("Database 'winery' created or already existed.")

# Step 5: Connect to the 'winery' database now that it's created
db_connection.database = "winery"

# Step 6: Define SQL queries for creating each table
# These SQL statements will create the tables as per the ERD.
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id INT NOT NULL AUTO_INCREMENT,
    product_name VARCHAR(45) NOT NULL,
    product_description VARCHAR(255),
    wine_type VARCHAR(25),
    sales_price DECIMAL(8,2),
    on_hand_qty INT,
    PRIMARY KEY (product_id)
);
""")

# Step 7: Now we can create the 'suppliers' table
cursor.execute("""
CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id INT NOT NULL AUTO_INCREMENT,
    supplier_name VARCHAR(45) NOT NULL,
    contact_email VARCHAR(45),
    contact_phone VARCHAR(15),
    order_url VARCHAR(45),
    address1 VARCHAR(45),
    address2 VARCHAR(45),
    city VARCHAR(45),
    state CHAR(2),
    zip VARCHAR(10),
    country VARCHAR(45),
    PRIMARY KEY (supplier_id)
);
""")

# Step 8: Create the 'supplier_products' table, which references both 'suppliers' and 'products'
cursor.execute("""
CREATE TABLE IF NOT EXISTS supplier_products (
    supplier_item_id INT NOT NULL AUTO_INCREMENT,
    supplier_id INT NOT NULL,
    item_name VARCHAR(15) NOT NULL,
    item_price DECIMAL(8,2),
    item_description VARCHAR(45),
    inv_on_hand INT,
    product_id INT NOT NULL,
    PRIMARY KEY (supplier_item_id),
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
""")

# Step 9: Create the 'supply_orders' table
cursor.execute("""
CREATE TABLE IF NOT EXISTS supply_orders (
    order_num INT NOT NULL AUTO_INCREMENT,
    order_date DATE NOT NULL,
    shipment_id INT,
    PRIMARY KEY (order_num)
);
""")

# Step 10: Create the 'supply_order_items' table
cursor.execute("""
CREATE TABLE IF NOT EXISTS supply_order_items (
    order_num INT NOT NULL,
    order_item INT NOT NULL,
    supplier_item_id INT NOT NULL,
    quantity INT NOT NULL,
    PRIMARY KEY (order_num, order_item),
    FOREIGN KEY (supplier_item_id) REFERENCES supplier_products(supplier_item_id),
    FOREIGN KEY (order_num) REFERENCES supply_orders(order_num)
);
""")

# Step 11: Create the 'shipment_tracking' table
cursor.execute("""
CREATE TABLE IF NOT EXISTS shipment_tracking (
    shipment_id INT NOT NULL AUTO_INCREMENT,
    ship_date DATE,
    est_delivery_date DATE,
    delivery_date DATE,
    carrier VARCHAR(45),
    tracking_number VARCHAR(128),
    PRIMARY KEY (shipment_id)
);
""")

# Step 12: Create the 'distributors' table
cursor.execute("""
CREATE TABLE IF NOT EXISTS distributors (
    distributor_id INT NOT NULL AUTO_INCREMENT,
    distributor_name VARCHAR(45) NOT NULL,
    contact_email VARCHAR(45),
    contact_phone VARCHAR(15),
    address1 VARCHAR(45),
    address2 VARCHAR(45),
    city VARCHAR(45),
    state CHAR(2),
    zip VARCHAR(10),
    country VARCHAR(45),
    PRIMARY KEY (distributor_id)
);
""")

# Step 13: Create the 'sales_orders' table, which references 'distributors' and 'shipment_tracking'
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales_orders (
    transaction_num INT NOT NULL AUTO_INCREMENT,
    distributor_id INT NOT NULL,
    order_date DATE NOT NULL,
    shipment_id INT,
    PRIMARY KEY (transaction_num),
    FOREIGN KEY (distributor_id) REFERENCES distributors(distributor_id),
    FOREIGN KEY (shipment_id) REFERENCES shipment_tracking(shipment_id)
);
""")

# Step 14: Create the 'employees' table
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    employee_id INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(15) NOT NULL,
    last_name VARCHAR(15) NOT NULL,
    department INT NOT NULL,
    job_title VARCHAR(45),
    PRIMARY KEY (employee_id)
);
""")

# Step 15: Create the 'timekeeping' table
cursor.execute("""
CREATE TABLE IF NOT EXISTS timekeeping (
    punch_id INT NOT NULL AUTO_INCREMENT,
    employee_id INT NOT NULL,
    in_or_out ENUM('IN', 'OUT') NOT NULL,
    punch_datetime TIMESTAMP NOT NULL,
    PRIMARY KEY (punch_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);
""")

# Step 16: Create the 'department' table
cursor.execute("""
CREATE TABLE IF NOT EXISTS department (
    dept_id INT NOT NULL AUTO_INCREMENT,
    depart_name VARCHAR(25) NOT NULL,
    PRIMARY KEY (dept_id)
);
""")

# Step 17: Commit to the database
db_connection.commit()

# Step 18: Close the connection
cursor.close()
db_connection.close()

print("All tables were successfully created.")
/*
    Title: db_init_winery.sql
    Author: Mikaela June
    Date: 27 Sept 2024
    Description: winery database initialization script.
*/

-- drop database user if exists 
DROP USER IF EXISTS 'winery_user'@'localhost';


-- create winery_user and grant them all privileges to the movies database 
CREATE USER 'winery_user_user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Bacchus';

-- grant all privileges to the winery database to user winery_user on localhost 
GRANT ALL PRIVILEGES ON winery.* TO 'winery_user'@'localhost';


-- drop tables if they are present
DROP TABLE IF EXISTS suppliers;
DROP TABLE IF EXISTS supplier_products;
DROP TABLE IF EXISTS supply_order_items;
DROP TABLE IF EXISTS supply_orders;
DROP TABLE IF EXISTS shipment_tracking;
DROP TABLE IF EXISTS sales_orders;
DROP TABLE IF EXISTS items_sold;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS distributors;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS timekeeping;
DROP TABLE IF EXISTS department;

-- create suppliers table --
CREATE TABLE suppliers (
    supplier_id     INT             NOT NULL        AUTO_INCREMENT,
    supplier_name   VARCHAR(45)     NOT NULL,
    contact_email   VARCHAR(45),
    contact_phone   VARCHAR(15),
    order_url       VARCHAR(45),
    address1        VARCHAR(45),
    address2        VARCHAR(45),
    city            VARCHAR(45),
    state_us        CHAR(2),
    zip             VARCHAR(10),
    country         VARCHAR(45),

    PRIMARY KEY(supplier_id)
); 

-- create the film table and set the foreign key --
CREATE TABLE supplier_products (
    supplier_item_id   INT             NOT NULL        AUTO_INCREMENT,
    item_name  VARCHAR(15)     NOT NULL,
    item_price   DECIMAL(8,2),
	item_description VARCHAR(45),
    inv_on_hand     INT NOT NULL,
	supplier_id INT NOT NULL,
	product_id INT,
	
    
    PRIMARY KEY(supplier_item_id),

	CONSTRAINT fk_suppliers
    FOREIGN KEY(supplier_id)
        REFERENCES suppliers(supplier_id),
		
    CONSTRAINT fk_products
    FOREIGN KEY(product_id)
        REFERENCES products(product_id)	
);

-- create supply order items table --
CREATE TABLE supply_order_items (
    order_item     INT      NOT NULL,
    quantity   INT     NOT NULL,
    order_num   INT     NOT NULL,
    supplier_item_id   INT     NOT NULL,


    CONSTRAINT fk_supplier_products
    FOREIGN KEY(supplier_item_id)
        REFERENCES supplier_products(supplier_item_id),

    CONSTRAINT fk_supply_orders
    FOREIGN KEY(order_num)
        REFERENCES supply_orders(order_num),
); 

-- create supply orders table --
CREATE TABLE supply_orders (
    order_num   INT             NOT NULL        AUTO_INCREMENT,
    order_date  DATE    NOT NULL,
    shipment_id INT     NOT NULL,

    PRIMARY KEY(order_num), 

    CONSTRAINT fk_shipment_tracking
    FOREIGN KEY(shipment_id)
        REFERENCES shipment_tracking(shipment_id),
);

-- create shipment tracking table --
CREATE TABLE shipment_tracking (
    shipment_id   INT             NOT NULL        AUTO_INCREMENT,
    ship_date  DATE,
    est_delivery_date  DATE,
    act_delivery_date   DATE, 
    carrier     VARCHAR(45)     NOT NULL,
    tracking_number     VARCHAR(128),

    PRIMARY KEY(shipment_id),

);

-- create a sales orders table --
CREATE TABLE sales_orders (
    transaction_num   INT             NOT NULL        AUTO_INCREMENT,
    distributor_id  INT     NOT NULL,
    order_date      DATE    NOT NULL,
    shipment_id     INT     NOT NULL,

    PRIMARY KEY(transaction_num),

    CONSTRAINT fk_distributors
    FOREIGN KEY(distributor_id)
        REFERENCES distributors(distributor_id),

    CONSTRAINT fk_shipment_tracking
    FOREIGN KEY(shipment_id)
        REFERENCES shipment_tracking(shipment_id),
);

-- create an items sold table --
CREATE TABLE items_sold (
    transaction_num     INT     NOT NULL,
    order_item      INT     NOT NULL,
    product_id      INT     NOT NULL,
    quantity        INT     NOT NULL,

    CONSTRAINT fk_sales_orders
    FOREIGN KEY(transaction_num)
        REFERENCES sales_orders(transaction_num),

    CONSTRAINT fk_products
    FOREIGN KEY(product_id)
        REFERENCES products(product_id),

);

-- create a products table --
CREATE TABLE products(
    product_id      INT     NOT NULL,
    product_name    VARCHAR(45)     NOT NULL,
    product_description     VARCHAR(255),
    wine_type       VARCHAR(25),
    sales_price     DECIMAL(8,2),
    on_hand_qty     INT     NOT NULL,

    PRIMARY KEY(product_id),

);

-- create a distributors table --
CREATE TABLE distributors(
    distributor_id      INT     NOT NULL    AUTO_INCREMENT,
    distributor_name    VARCHAR(45)     NOT NULL,
    contact_email       VARCHAR(45),
    contact_phone       VARCHAR(15),
    address1        VARCHAR(45),
    address2        VARCHAR(45),
    city            VARCHAR(45),
    state_us        CHAR(2),
    zip             VARCHAR(10),
    country         VARCHAR(45),

    PRIMARY KEY(distributor_id),

);

-- create an employees table --
CREATE TABLE employees(
    employee_id     INT     NOT NULL    AUTO_INCREMENT,
    first_name      VARCHAR(45)     NOT NULL,
    last_name       VARCHAR(45)     NOT NULL,
    dept_id      INT     NOT NULL,
    job_title   VARCHAR(45),

    PRIMARY KEY(employee_id),

    CONSTRAINT fk_department
    FOREIGN KEY(dept_id)
        REFERENCES department(dept_id),

);

-- create a timekeeping table --
CREATE TABLE timekeeping(
    punch_id    INT     NOT NULL    AUTO_INCREMENT,
    employee_id     INT     NOT NULL,
    in_or_out   ENUM ('IN','OUT')   NOT NULL, 
    punch_datetime  TIMESTAMP   NOT NULL,

    PRIMARY KEY(punch_id),

    CONSTRAINT fk_employees
    FOREIGN KEY(employee_id)
        REFERENCES employees(employee_id),

); 

-- create department table --
CREATE TABLE department(
    dept_id     INT     NOT NULL    AUTO_INCREMENT,
    depart_name     VARCHAR(15)     NOT NULL,

    PRIMARY KEY(dept_id),

);
-- RetailPulse Phase 2 Database Schema
-- Star-schema architecture: customers (dim), products (dim), transactions (fact)

-- 1. Customers Dimension
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    signup_date DATE NOT NULL,
    city VARCHAR(100) NOT NULL,
    age_group VARCHAR(20) NOT NULL,
    gender VARCHAR(20) NOT NULL,
    acquisition_channel VARCHAR(50) NOT NULL,
    customer_segment_ground_truth VARCHAR(50) NOT NULL
);

-- 2. Products Dimension
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    subcategory VARCHAR(100) NOT NULL,
    price NUMERIC(10, 2) NOT NULL CHECK (price > 0),
    cost NUMERIC(10, 2) NOT NULL CHECK (cost > 0)
);

-- 3. Transactions Fact Table
CREATE TABLE transactions (
    transaction_id INT PRIMARY KEY,
    customer_id INT NOT NULL REFERENCES customers(customer_id),
    transaction_timestamp TIMESTAMP NOT NULL,
    product_id INT NOT NULL REFERENCES products(product_id),
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10, 2) NOT NULL CHECK (unit_price > 0),
    discount NUMERIC(10, 2) NOT NULL CHECK (discount >= 0),
    amount NUMERIC(10, 2) NOT NULL CHECK (amount >= 0),
    payment_method VARCHAR(50) NOT NULL,
    channel VARCHAR(50) NOT NULL,
    -- Ensure monetary consistency according to the Phase 1 generation logic
    -- amount = quantity * unit_price - discount
    -- We allow a small tolerance (0.01) to account for any floating point/numeric precision edge cases in bulk loading
    CONSTRAINT chk_amount_consistency CHECK (
        ABS(amount - (quantity * unit_price - discount)) < 0.02
    )
);

-- 4. Analytical Indexes
-- Note: Further index tuning will happen in Phase 4 (Performance). 
-- These are basic logical indexes supporting the most common access paths/joins.

-- Support time-based revenue and cohort analysis
CREATE INDEX idx_transactions_timestamp ON transactions(transaction_timestamp);

-- Support customer-level aggregation (e.g., RFM)
CREATE INDEX idx_transactions_customer ON transactions(customer_id);

-- Support product/category-level revenue analysis
CREATE INDEX idx_transactions_product ON transactions(product_id);

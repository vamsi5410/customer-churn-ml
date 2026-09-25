CREATE TABLE customers (
    customer_id VARCHAR(80) PRIMARY KEY,
    name VARCHAR(160),
    email VARCHAR(255),
    phone VARCHAR(40),
    tenure INTEGER NOT NULL,
    monthly_charges DOUBLE PRECISION NOT NULL,
    total_charges DOUBLE PRECISION NOT NULL,
    contract VARCHAR(50) NOT NULL,
    internet_service VARCHAR(50) NOT NULL,
    payment_method VARCHAR(80) NOT NULL,
    tech_support VARCHAR(10) NOT NULL,
    online_security VARCHAR(10) NOT NULL,
    churn_probability DOUBLE PRECISION,
    risk_level VARCHAR(20),
    recommendation TEXT,
    updated_at TIMESTAMP
);

CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    customer_id VARCHAR(80) NOT NULL,
    churn_probability DOUBLE PRECISION NOT NULL,
    risk_level VARCHAR(20) NOT NULL,
    recommendation TEXT NOT NULL,
    created_at TIMESTAMP
);

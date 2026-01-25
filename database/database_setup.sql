-- ============================================================================
-- MoMo SMS Analytics Database Setup Script
-- MySQL Database Implementation
-- Date: January 25, 2026
-- Team: David Achibiri, Manuelle Ackun, Rhoda Umutesi
-- ============================================================================

-- Drop existing tables if they exist (for clean setup)
DROP TABLE IF EXISTS TRANSACTION_CATEGORY;
DROP TABLE IF EXISTS LOG;
DROP TABLE IF EXISTS TRANSACTION;
DROP TABLE IF EXISTS CATEGORY;
DROP TABLE IF EXISTS USER;

-- ============================================================================
-- TABLE DEFINITIONS
-- ============================================================================

-- USER Table
-- Stores customer/user information for both senders and receivers
CREATE TABLE USER (
    user_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique identifier for each user',
    phone_number VARCHAR(15) NOT NULL UNIQUE COMMENT 'User phone number in format 0XXXXXXXXX',
    user_name VARCHAR(100) COMMENT 'Full name of the user',
    account_type VARCHAR(30) COMMENT 'Type of MoMo account (personal, merchant, agent)',
    network_provider VARCHAR(30) COMMENT 'Mobile network provider (MTN, Vodafone, AirtelTigo)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Record creation timestamp',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Last update timestamp',
    
    CONSTRAINT chk_phone_format CHECK (phone_number REGEXP '^0[0-9]{9}$'),
    CONSTRAINT chk_account_type CHECK (account_type IN ('personal', 'merchant', 'agent', 'unknown'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='User/Customer information table';

-- CATEGORY Table
-- Stores transaction category definitions
CREATE TABLE CATEGORY (
    category_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique identifier for each category',
    category_name VARCHAR(50) NOT NULL UNIQUE COMMENT 'Category name (airtime, transfer, payment, etc.)',
    description VARCHAR(255) COMMENT 'Detailed description of the category',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Record creation timestamp',
    
    CONSTRAINT chk_category_name CHECK (category_name IN ('airtime', 'transfer', 'received', 'payment', 'withdrawal', 'other'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Transaction category lookup table';

-- TRANSACTION Table
-- Stores main transaction records from MoMo SMS data
CREATE TABLE TRANSACTION (
    transaction_ID VARCHAR(50) PRIMARY KEY COMMENT 'Unique transaction identifier/reference code',
    transaction_date DATETIME NOT NULL COMMENT 'Date and time of transaction',
    amount DECIMAL(12,2) NOT NULL COMMENT 'Transaction amount in local currency',
    transaction_type VARCHAR(50) COMMENT 'Specific type (sent, received, airtime purchase, etc.)',
    sender_ID INT COMMENT 'Foreign key to USER table (sender)',
    receiver_ID INT COMMENT 'Foreign key to USER table (receiver)',
    status VARCHAR(30) DEFAULT 'completed' COMMENT 'Transaction status (completed, pending, failed)',
    reference_code VARCHAR(100) COMMENT 'Additional reference or confirmation code',
    message_body TEXT COMMENT 'Original SMS message text',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Record creation timestamp',
    
    CONSTRAINT fk_sender FOREIGN KEY (sender_ID) REFERENCES USER(user_id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_receiver FOREIGN KEY (receiver_ID) REFERENCES USER(user_id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT chk_amount CHECK (amount >= 0 AND amount <= 10000000),
    CONSTRAINT chk_status CHECK (status IN ('completed', 'pending', 'failed', 'reversed'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Main transaction records table';

-- TRANSACTION_CATEGORY Table (Junction Table)
-- Resolves many-to-many relationship between transactions and categories
CREATE TABLE TRANSACTION_CATEGORY (
    transaction_ID VARCHAR(50) NOT NULL COMMENT 'Foreign key to TRANSACTION table',
    category_ID INT NOT NULL COMMENT 'Foreign key to CATEGORY table',
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'When category was assigned',
    
    PRIMARY KEY (transaction_ID, category_ID),
    CONSTRAINT fk_tc_transaction FOREIGN KEY (transaction_ID) REFERENCES TRANSACTION(transaction_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_tc_category FOREIGN KEY (category_ID) REFERENCES CATEGORY(category_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Junction table linking transactions to categories';

-- LOG Table
-- Stores system logs and processing information for transactions
CREATE TABLE LOG (
    log_ID INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique identifier for each log entry',
    transaction_ID VARCHAR(50) COMMENT 'Foreign key to associated transaction',
    log_message VARCHAR(255) COMMENT 'Log message or error description',
    log_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'When the log entry was created',
    processing_status VARCHAR(30) COMMENT 'Processing status (success, error, warning)',
    
    CONSTRAINT fk_log_transaction FOREIGN KEY (transaction_ID) REFERENCES TRANSACTION(transaction_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT chk_processing_status CHECK (processing_status IN ('success', 'error', 'warning', 'info'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='System logs and processing status table';

-- ============================================================================
-- INDEXES FOR PERFORMANCE OPTIMIZATION
-- ============================================================================

-- USER table indexes
CREATE INDEX idx_user_phone ON USER(phone_number);
CREATE INDEX idx_user_network ON USER(network_provider);

-- TRANSACTION table indexes
CREATE INDEX idx_transaction_date ON TRANSACTION(transaction_date);
CREATE INDEX idx_transaction_amount ON TRANSACTION(amount);
CREATE INDEX idx_transaction_sender ON TRANSACTION(sender_ID);
CREATE INDEX idx_transaction_receiver ON TRANSACTION(receiver_ID);
CREATE INDEX idx_transaction_status ON TRANSACTION(status);
CREATE INDEX idx_transaction_type ON TRANSACTION(transaction_type);

-- CATEGORY table indexes
CREATE INDEX idx_category_name ON CATEGORY(category_name);

-- LOG table indexes
CREATE INDEX idx_log_timestamp ON LOG(log_timestamp);
CREATE INDEX idx_log_status ON LOG(processing_status);

-- ============================================================================
-- SAMPLE DATA INSERTION
-- ============================================================================

-- Insert sample users
INSERT INTO USER (user_id, phone_number, user_name, account_type, network_provider) VALUES
(1, '0241234567', 'Kwame Mensah', 'personal', 'MTN'),
(2, '0554567890', 'Ama Asante', 'merchant', 'Vodafone'),
(3, '0201122334', 'Kofi Adjei', 'personal', 'MTN'),
(4, '0267788990', 'Akua Boateng', 'personal', 'AirtelTigo'),
(5, '0509988776', 'Yaw Osei', 'agent', 'MTN'),
(6, '0244455667', 'Efua Darko', 'personal', 'Vodafone');

-- Insert sample categories
INSERT INTO CATEGORY (category_id, category_name, description) VALUES
(1, 'airtime', 'Mobile airtime and data bundle purchases'),
(2, 'transfer', 'Money transfers sent to other users'),
(3, 'received', 'Money received from other users'),
(4, 'payment', 'Bill payments and merchant payments'),
(5, 'withdrawal', 'Cash withdrawals from agents'),
(6, 'other', 'Other miscellaneous transactions');

-- Insert sample transactions
INSERT INTO TRANSACTION (transaction_ID, transaction_date, amount, transaction_type, sender_ID, receiver_ID, status, reference_code, message_body) VALUES
('TXN20260115001', '2026-01-15 10:30:00', 50.00, 'airtime', 1, NULL, 'completed', 'REF123456', 'You have successfully purchased GHS 50.00 airtime. Your new balance is GHS 200.00'),
('TXN20260115002', '2026-01-15 14:20:00', 150.00, 'transfer', 1, 2, 'completed', 'REF123457', 'You have sent GHS 150.00 to 0554567890. Transaction fee: GHS 0.00'),
('TXN20260116003', '2026-01-16 09:15:00', 150.00, 'received', 2, 1, 'completed', 'REF123457', 'You have received GHS 150.00 from 0241234567'),
('TXN20260116004', '2026-01-16 16:45:00', 200.00, 'payment', 3, 2, 'completed', 'REF123458', 'Payment of GHS 200.00 to Ama Store successful. Balance: GHS 450.00'),
('TXN20260117005', '2026-01-17 11:00:00', 500.00, 'withdrawal', 4, 5, 'completed', 'REF123459', 'You have withdrawn GHS 500.00 from agent 0509988776. Fee: GHS 5.00'),
('TXN20260118006', '2026-01-18 13:30:00', 100.00, 'transfer', 3, 4, 'completed', 'REF123460', 'You have sent GHS 100.00 to 0267788990'),
('TXN20260119007', '2026-01-19 08:20:00', 25.00, 'airtime', 6, NULL, 'completed', 'REF123461', 'Airtime purchase of GHS 25.00 successful');

-- Insert transaction-category mappings (many-to-many relationships)
INSERT INTO TRANSACTION_CATEGORY (transaction_ID, category_ID) VALUES
('TXN20260115001', 1),  -- Airtime purchase
('TXN20260115002', 2),  -- Transfer sent
('TXN20260116003', 3),  -- Money received
('TXN20260116004', 4),  -- Payment
('TXN20260117005', 5),  -- Withdrawal
('TXN20260118006', 2),  -- Transfer sent
('TXN20260119007', 1);  -- Airtime purchase

-- Insert sample logs
INSERT INTO LOG (transaction_ID, log_message, log_timestamp, processing_status) VALUES
('TXN20260115001', 'Transaction parsed successfully from XML', '2026-01-15 10:30:05', 'success'),
('TXN20260115001', 'Transaction cleaned and normalized', '2026-01-15 10:30:06', 'success'),
('TXN20260115002', 'Transaction parsed successfully from XML', '2026-01-15 14:20:05', 'success'),
('TXN20260115002', 'Transaction categorized as transfer', '2026-01-15 14:20:06', 'success'),
('TXN20260116003', 'Transaction parsed successfully from XML', '2026-01-16 09:15:05', 'success'),
('TXN20260116004', 'Transaction parsed successfully from XML', '2026-01-16 16:45:05', 'success'),
('TXN20260117005', 'Transaction parsed successfully from XML', '2026-01-17 11:00:05', 'success'),
('TXN20260117005', 'High-value transaction flagged for review', '2026-01-17 11:00:07', 'warning');

-- ============================================================================
-- SAMPLE CRUD OPERATIONS
-- ============================================================================

-- CREATE: Insert a new transaction
-- INSERT INTO TRANSACTION (transaction_ID, transaction_date, amount, transaction_type, sender_ID, receiver_ID, status, reference_code, message_body)
-- VALUES ('TXN20260120008', '2026-01-20 15:00:00', 75.00, 'airtime', 1, NULL, 'completed', 'REF123462', 'Airtime purchase successful');

-- READ: Get all transactions for a specific user
-- SELECT t.*, u_sender.user_name AS sender_name, u_receiver.user_name AS receiver_name
-- FROM TRANSACTION t
-- LEFT JOIN USER u_sender ON t.sender_ID = u_sender.user_id
-- LEFT JOIN USER u_receiver ON t.receiver_ID = u_receiver.user_id
-- WHERE t.sender_ID = 1 OR t.receiver_ID = 1
-- ORDER BY t.transaction_date DESC;

-- READ: Get transactions with their categories
-- SELECT t.transaction_ID, t.transaction_date, t.amount, t.transaction_type, c.category_name
-- FROM TRANSACTION t
-- INNER JOIN TRANSACTION_CATEGORY tc ON t.transaction_ID = tc.transaction_ID
-- INNER JOIN CATEGORY c ON tc.category_ID = c.category_id
-- WHERE t.transaction_date >= '2026-01-15'
-- ORDER BY t.transaction_date DESC;

-- UPDATE: Update transaction status
-- UPDATE TRANSACTION
-- SET status = 'reversed'
-- WHERE transaction_ID = 'TXN20260115001';

-- DELETE: Remove old logs
-- DELETE FROM LOG
-- WHERE log_timestamp < DATE_SUB(NOW(), INTERVAL 30 DAY);

-- ============================================================================
-- ANALYTICS QUERIES
-- ============================================================================

-- Total transactions per category
-- SELECT c.category_name, COUNT(*) as transaction_count, SUM(t.amount) as total_amount
-- FROM TRANSACTION t
-- INNER JOIN TRANSACTION_CATEGORY tc ON t.transaction_ID = tc.transaction_ID
-- INNER JOIN CATEGORY c ON tc.category_ID = c.category_id
-- GROUP BY c.category_name
-- ORDER BY total_amount DESC;

-- Top users by transaction volume
-- SELECT u.user_name, u.phone_number, COUNT(*) as transaction_count, SUM(t.amount) as total_sent
-- FROM TRANSACTION t
-- INNER JOIN USER u ON t.sender_ID = u.user_id
-- GROUP BY u.user_id, u.user_name, u.phone_number
-- ORDER BY total_sent DESC
-- LIMIT 10;

-- Daily transaction summary
-- SELECT DATE(transaction_date) as transaction_day, 
--        COUNT(*) as daily_transactions,
--        SUM(amount) as daily_total,
--        AVG(amount) as average_amount
-- FROM TRANSACTION
-- GROUP BY DATE(transaction_date)
-- ORDER BY transaction_day DESC;

-- ============================================================================
-- END OF SCRIPT
-- ============================================================================

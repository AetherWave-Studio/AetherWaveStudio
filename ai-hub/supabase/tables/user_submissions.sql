CREATE TABLE user_submissions (
    id SERIAL PRIMARY KEY,
    user_id UUID,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    link VARCHAR(500) NOT NULL,
    category VARCHAR(100) NOT NULL,
    logo_url VARCHAR(500),
    status VARCHAR(50) DEFAULT 'pending',
    admin_notes TEXT,
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    reviewed_at TIMESTAMP WITH TIME ZONE
);
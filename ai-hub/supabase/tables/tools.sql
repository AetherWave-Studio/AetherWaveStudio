CREATE TABLE tools (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    link VARCHAR(500) NOT NULL,
    category VARCHAR(100) NOT NULL,
    logo_url VARCHAR(500),
    screenshot_url VARCHAR(500),
    featured BOOLEAN DEFAULT false,
    popularity_score DECIMAL(3,1) DEFAULT 0.0,
    source VARCHAR(255),
    tags TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
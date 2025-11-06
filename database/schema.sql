
DROP TABLE IF EXISTS search_queries CASCADE;
DROP TABLE IF EXISTS movies CASCADE;


CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    year INTEGER,
    rating DECIMAL(3,1),
    genre VARCHAR(100),
    director VARCHAR(255),
    description TEXT,
    poster_filename VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE INDEX idx_movies_title ON movies(title);
CREATE INDEX idx_movies_year ON movies(year);
CREATE INDEX idx_movies_rating ON movies(rating DESC);


CREATE TABLE search_queries (
    id SERIAL PRIMARY KEY,
    query TEXT NOT NULL,
    results_count INTEGER,
    searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE INDEX idx_search_queries_query ON search_queries(query);
CREATE INDEX idx_search_queries_searched_at ON search_queries(searched_at DESC);

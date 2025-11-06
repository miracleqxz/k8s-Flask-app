"""Analytics database operations"""
import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config


def get_db_connection():
    """Create DB connection"""
    return psycopg2.connect(
        host=Config.POSTGRES_HOST,
        port=Config.POSTGRES_PORT,
        database=Config.POSTGRES_DB,
        user=Config.POSTGRES_USER,
        password=Config.POSTGRES_PASSWORD
    )


def save_search_analytics(query, results_count, cached):
    """Save search analytics to DB"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO search_queries (query, results_count)
        VALUES (%s, %s)
    """, (query, results_count))
    
    conn.commit()
    cursor.close()
    conn.close()


def get_popular_searches(limit=10):
    """Get most popular search queries"""
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    cursor.execute("""
        SELECT 
            query,
            COUNT(*) as search_count,
            AVG(results_count) as avg_results
        FROM search_queries
        WHERE searched_at > NOW() - INTERVAL '7 days'
        GROUP BY query
        ORDER BY search_count DESC
        LIMIT %s
    """, (limit,))
    
    results = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return results


def get_search_stats():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    cursor.execute("""
        SELECT 
            COUNT(*) as total_searches,
            COUNT(DISTINCT query) as unique_queries,
            AVG(results_count) as avg_results_per_search
        FROM search_queries
        WHERE searched_at > NOW() - INTERVAL '7 days'
    """)
    
    stats = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return stats

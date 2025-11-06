"""Index movies to Elasticsearch"""
from database.elasticsearch_sync import (
    create_movies_index,
    index_all_movies,
    get_movies_count_es
)


if __name__ == '__main__':
    print("=" * 50)
    print("🔍 Elasticsearch - Movie Indexing")
    print("=" * 50)
    
    # Create index
    print("\n1️⃣  Creating movies index...")
    create_movies_index()
    
    # Index movies
    print("\n2️⃣  Indexing movies...")
    index_all_movies()
    
    # Verify
    print("\n3️⃣  Verifying...")
    count = get_movies_count_es()
    print(f"✅ Total movies in ES: {count}")
    
    print("\n✅ Done!")

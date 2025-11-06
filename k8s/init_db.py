
import psycopg2
from config import Config


def create_tables():
    
    print("=" * 50)
    print("🗄️  Database Initialization")
    print("=" * 50)
    
    try:
        conn = psycopg2.connect(
            host=Config.POSTGRES_HOST,
            port=Config.POSTGRES_PORT,
            database=Config.POSTGRES_DB,
            user=Config.POSTGRES_USER,
            password=Config.POSTGRES_PASSWORD
        )
        
        cursor = conn.cursor()
        
        print("\nCreating 'movies' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                year INTEGER NOT NULL,
                rating DECIMAL(3, 1) NOT NULL,
                genre VARCHAR(255) NOT NULL,
                director VARCHAR(255) NOT NULL,
                description TEXT NOT NULL,
                poster_filename VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Insert sample movies if table is empty
        cursor.execute("SELECT COUNT(*) FROM movies;")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("Inserting sample movies...")
            
            movies = [
                (1, "The Shawshank Redemption", 1994, 9.3, "Drama", "Frank Darabont", 
                 "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.", "shawshank.jpg"),
                (2, "The Godfather", 1972, 9.2, "Crime, Drama", "Francis Ford Coppola",
                 "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.", "godfather.jpg"),
                (3, "The Dark Knight", 2008, 9.0, "Action, Crime, Drama", "Christopher Nolan",
                 "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests.", "dark_knight.jpg"),
                (4, "Schindler's List", 1993, 8.9, "Biography, Drama, History", "Steven Spielberg",
                 "In German-occupied Poland during World War II, industrialist Oskar Schindler gradually becomes concerned for his Jewish workforce after witnessing their persecution.", "schindlers_list.jpg"),
                (5, "The Lord of the Rings: The Return of the King", 2003, 8.9, "Adventure, Drama, Fantasy", "Peter Jackson",
                 "Gandalf and Aragorn lead the World of Men against Sauron's army to draw his gaze from Frodo and Sam as they approach Mount Doom with the One Ring.", "lotr_return.jpg"),
                (6, "Pulp Fiction", 1994, 8.8, "Crime, Drama", "Quentin Tarantino",
                 "The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.", "pulp_fiction.jpg"),
                (7, "Fight Club", 1999, 8.8, "Drama", "David Fincher",
                 "An insomniac office worker and a devil-may-care soap maker form an underground fight club that evolves into much more.", "fight_club.jpg"),
                (8, "Forrest Gump", 1994, 8.8, "Drama, Romance", "Robert Zemeckis",
                 "The presidencies of Kennedy and Johnson, the Vietnam War, and other historical events unfold from the perspective of an Alabama man.", "forrest_gump.jpg"),
                (9, "Inception", 2010, 8.8, "Action, Sci-Fi, Thriller", "Christopher Nolan",
                 "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea.", "inception.jpg"),
                (10, "Star Wars: Episode V", 1980, 8.7, "Action, Adventure, Fantasy", "Irvin Kershner",
                 "After the Rebels are brutally overpowered by the Empire on the ice planet Hoth, Luke Skywalker begins Jedi training.", "star_wars_v.jpg"),
                (11, "The Matrix", 1999, 8.7, "Action, Sci-Fi", "Lana Wachowski, Lilly Wachowski",
                 "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.", "matrix.jpg"),
                (12, "Goodfellas", 1990, 8.7, "Biography, Crime, Drama", "Martin Scorsese",
                 "The story of Henry Hill and his life in the mob, covering his relationship with his wife Karen Hill and his mob partners.", "goodfellas.jpg"),
                (13, "The Green Mile", 1999, 8.6, "Crime, Drama, Fantasy", "Frank Darabont",
                 "The lives of guards on Death Row are affected by one of their charges: a black man accused of child murder and rape, yet who has a mysterious gift.", "green_mile.jpg"),
                (14, "Interstellar", 2014, 8.6, "Adventure, Drama, Sci-Fi", "Christopher Nolan",
                 "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.", "interstellar.jpg"),
                (15, "The Silence of the Lambs", 1991, 8.6, "Crime, Drama, Thriller", "Jonathan Demme",
                 "A young F.B.I. cadet must receive the help of an incarcerated and manipulative cannibal killer to help catch another serial killer.", "silence_lambs.jpg"),
                (16, "Saving Private Ryan", 1998, 8.6, "Drama, War", "Steven Spielberg",
                 "Following the Normandy Landings, a group of U.S. soldiers go behind enemy lines to retrieve a paratrooper.", "saving_ryan.jpg"),
                (17, "Parasite", 2019, 8.6, "Comedy, Drama, Thriller", "Bong Joon Ho",
                 "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.", "parasite.jpg"),
                (18, "Gladiator", 2000, 8.5, "Action, Adventure, Drama", "Ridley Scott",
                 "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.", "gladiator.jpg"),
                (19, "The Departed", 2006, 8.5, "Crime, Drama, Thriller", "Martin Scorsese",
                 "An undercover cop and a mole in the police attempt to identify each other while infiltrating an Irish gang in South Boston.", "departed.jpg"),
                (20, "Whiplash", 2014, 8.5, "Drama, Music", "Damien Chazelle",
                 "A promising young drummer enrolls at a cut-throat music conservatory where his dreams of greatness are mentored by an instructor who will stop at nothing.", "whiplash.jpg"),
            ]
            
            cursor.executemany("""
                INSERT INTO movies (id, title, year, rating, genre, director, description, poster_filename)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """, movies)
            
            print(f"Inserted {len(movies)} movies")
        else:
            print(f"Movies table already has {count} records")
        
        print("Movies table ready!")
        
        print("\nCreating 'search_queries' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS search_queries (
                id SERIAL PRIMARY KEY,
                query VARCHAR(255) NOT NULL,
                results_count INTEGER NOT NULL,
                searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("Search queries table ready!")
        
        conn.commit()
        
        print("\n" + "=" * 50)
        print("Database initialization complete!")
        print("=" * 50)
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"\nError: {e}")
        raise


if __name__ == '__main__':
    create_tables()
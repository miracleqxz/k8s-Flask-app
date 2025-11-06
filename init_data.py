
from database.movies_db import init_database, insert_movie, count_movies
from database.sample_movies import SAMPLE_MOVIES


def load_sample_data():
    
    existing_count = count_movies()
    
    if existing_count > 0:
        print(f"В базе уже есть {existing_count} фильмов.")
        answer = input("Очистить и загрузить заново? (yes/no): ")
        if answer.lower() != 'yes':
            print("Отменено")
            return
        
        print("🗑️  Очищаю базу...")
        init_database()
    
    print(f"📥 Загружаю {len(SAMPLE_MOVIES)} фильмов...")
    
    for i, movie in enumerate(SAMPLE_MOVIES, 1):
        movie_id = insert_movie(movie)
        print(f"  {i}. ✅ {movie['title']} (ID: {movie_id})")
    
    print(f"\n🎉 Успешно загружено {len(SAMPLE_MOVIES)} фильмов!")


if __name__ == '__main__':
    print("=" * 50)
    print("🎬 Movie Database - Инициализация данных")
    print("=" * 50)
    
    # Создаём таблицы
    print("\n1️⃣  Создаю схему базы данных...")
    init_database()
    
    # Загружаем данные
    print("\n2️⃣  Загружаю тестовые данные...")
    load_sample_data()
    
    print("\n✅ Готово!")

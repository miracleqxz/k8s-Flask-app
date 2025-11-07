
from database.minio_storage import create_poster_bucket, upload_poster
from database.movies_db import get_all_movies
import os


def upload_real_posters(folder_path='posters'):    
    print("=" * 50)
    print("Real Poster Upload to MinIO")
    print("=" * 50)
    
    
    if not os.path.exists(folder_path):
        print(f"\nFolder not found: {folder_path}")
        print("Please create the folder and add poster images.")
        return
    
    
    print("\nChecking MinIO bucket...")
    create_poster_bucket()
    
    
    movies = get_all_movies()
    
    print(f"\nUploading posters from {folder_path}/...")
    print(f"Processing {len(movies)} movies...\n")
    
    success_count = 0
    fail_count = 0
    missing_count = 0
    
    for i, movie in enumerate(movies, 1):
        filename = movie['poster_filename']
        poster_path = os.path.join(folder_path, filename)
        
        # Check if file exists
        if not os.path.exists(poster_path):
            print(f"  {i}. {movie['title']}")
            print(f"      Missing: {filename}")
            missing_count += 1
            continue
        
        
        try:
            with open(poster_path, 'rb') as f:
                image_data = f.read()
            
            # Get file size for display
            file_size_kb = len(image_data) / 1024
            
            # Upload to MinIO
            success = upload_poster(filename, image_data)
            
            if success:
                print(f"  {i}. {movie['title']}")
                print(f"      {filename} ({file_size_kb:.1f} KB)")
                success_count += 1
            else:
                print(f"  {i}. {movie['title']} - Upload failed")
                fail_count += 1
                
        except Exception as e:
            print(f"  {i}. {movie['title']} - Error: {e}")
            fail_count += 1
    
    
    print("\n" + "=" * 50)
    print("Summary:")
    print(f"Uploaded: {success_count}")
    print(f"Failed: {fail_count}")
    print(f"Missing files: {missing_count}")
    print("=" * 50)
    
    if missing_count > 0:
        print("\nMissing files - rename your posters to:")
        print("=" * 50)
        for movie in movies:
            poster_path = os.path.join(folder_path, movie['poster_filename'])
            if not os.path.exists(poster_path):
                print(f"  {movie['poster_filename']:30} <- {movie['title']}")



if __name__ == '__main__':
    import sys   
    upload_real_posters()

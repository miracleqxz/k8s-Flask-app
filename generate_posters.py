
from PIL import Image, ImageDraw, ImageFont
from database.minio_storage import create_poster_bucket, upload_poster
from database.movies_db import get_all_movies
import random


def generate_placeholder_poster(title, year, rating):
    width, height = 300, 450
    
    colors = [
        (25, 25, 112),   # Midnight Blue
        (72, 61, 139),   # Dark Slate Blue
        (106, 90, 205),  # Slate Blue
        (138, 43, 226),  # Blue Violet
        (75, 0, 130),    # Indigo
        (139, 0, 139),   # Dark Magenta
        (128, 0, 0),     # Maroon
        (139, 69, 19),   # Saddle Brown
        (85, 107, 47),   # Dark Olive Green
        (47, 79, 79),    # Dark Slate Gray
    ]
    
    color = random.choice(colors)
    
    img = Image.new('RGB', (width, height), color)
    draw = ImageDraw.Draw(img)
    
    # Try to use system font, fallback to default
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Draw title (wrap text)
    words = title.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font_large)
        if bbox[2] - bbox[0] < width - 40:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    # Draw text
    y_offset = height // 3
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font_large)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        draw.text((x, y_offset), line, fill='white', font=font_large)
        y_offset += 40
    
    # Draw year and rating
    info_text = f"{year}  ⭐ {rating}"
    bbox = draw.textbbox((0, 0), info_text, font=font_small)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    draw.text((x, height - 60), info_text, fill='white', font=font_small)
    
    # Convert to JPEG bytes
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=85)
    return buffer.getvalue()


if __name__ == '__main__':
    import io
    
    print("=" * 50)
    print("🖼️  Movie Poster Generator")
    print("=" * 50)
    
    # Create bucket
    print("\n1️⃣  Creating MinIO bucket...")
    create_poster_bucket()
    
    # Get movies from DB
    print("\n2️⃣  Generating posters...")
    movies = get_all_movies()
    
    print(f"📥 Generating {len(movies)} posters...")
    
    for i, movie in enumerate(movies, 1):
        # Generate placeholder
        poster_data = generate_placeholder_poster(
            movie['title'],
            movie['year'],
            movie['rating']
        )
        
        # Upload to MinIO
        success = upload_poster(movie['poster_filename'], poster_data)
        
        if success:
            print(f"  {i}. ✅ {movie['title']} → {movie['poster_filename']}")
        else:
            print(f"  {i}. ❌ {movie['title']} FAILED")
    
    print(f"\n🎉 Generated {len(movies)} posters!")
    print("\n✅ Done!")

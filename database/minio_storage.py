
from minio import Minio
from minio.error import S3Error
from config import Config
import io


def get_minio_client():
    return Minio(
        f"{Config.MINIO_HOST}:{Config.MINIO_PORT}",
        access_key=Config.MINIO_ACCESS_KEY,
        secret_key=Config.MINIO_SECRET_KEY,
        secure=False
    )


def create_poster_bucket():
    client = get_minio_client()
    bucket_name = "movie-posters"
    
    try:
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
            print(f"Created bucket: {bucket_name}")
        else:
            print(f"Bucket already exists: {bucket_name}")
    except S3Error as e:
        print(f"Error creating bucket: {e}")


def upload_poster(filename, image_data):
    client = get_minio_client()
    bucket_name = "movie-posters"
    
    try:
        client.put_object(
            bucket_name,
            filename,
            io.BytesIO(image_data),
            length=len(image_data),
            content_type='image/jpeg'
        )
        return True
    except S3Error as e:
        print(f"Upload failed for {filename}: {e}")
        return False


def download_poster(filename):
    client = get_minio_client()
    bucket_name = "movie-posters"
    
    try:
        response = client.get_object(bucket_name, filename)
        data = response.read()
        response.close()
        response.release_conn()
        return data
    except S3Error as e:
        print(f"Download failed for {filename}: {e}")
        return None


def poster_exists(filename):
    client = get_minio_client()
    bucket_name = "movie-posters"
    
    try:
        client.stat_object(bucket_name, filename)
        return True
    except S3Error:
        return False


def list_all_posters():
    client = get_minio_client()
    bucket_name = "movie-posters"
    
    try:
        objects = client.list_objects(bucket_name)
        return [obj.object_name for obj in objects]
    except S3Error as e:
        print(f"List failed: {e}")
        return []

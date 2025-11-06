
from minio import Minio
from minio.error import S3Error
from config import Config
import io


def check_minio():
    try:
        client = Minio(
            f"{Config.MINIO_HOST}:{Config.MINIO_PORT}",
            access_key=Config.MINIO_ACCESS_KEY,
            secret_key=Config.MINIO_SECRET_KEY,
            secure=False
        )
        
        
        bucket_name = "health-check-bucket"
        
        
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
        
        
        buckets = client.list_buckets()
        bucket_names = [b.name for b in buckets]
        
        
        test_data = b"Health check test file"
        test_file = "test.txt"
        
        client.put_object(
            bucket_name,
            test_file,
            io.BytesIO(test_data),
            length=len(test_data),
            content_type='text/plain'
        )
        
        
        response = client.get_object(bucket_name, test_file)
        retrieved_data = response.read()
        response.close()
        response.release_conn()
        
        # Verify data integrity
        data_matches = retrieved_data == test_data
        
        # Get objects count in movie-posters bucket
        posters_count = 0
        posters_size = 0
        try:
            objects = client.list_objects('movie-posters')
            for obj in objects:
                posters_count += 1
                posters_size += obj.size
        except:
            pass
        
        
        def bytes_to_human(bytes_val):
            for unit in ['B', 'KB', 'MB', 'GB']:
                if bytes_val < 1024.0:
                    return f"{bytes_val:.2f} {unit}"
                bytes_val /= 1024.0
        
        posters_size_human = bytes_to_human(posters_size)
        
        return {
            'status': 'healthy',
            'service': 'minio',
            'message': 'Successfully connected to MinIO',
            'details': {
                'connection': {
                    'endpoint': f"{Config.MINIO_HOST}:{Config.MINIO_PORT}",
                    'access_key': Config.MINIO_ACCESS_KEY
                },
                'buckets': {
                    'total_buckets': len(buckets),
                    'bucket_names': bucket_names
                },
                'movie_posters': {
                    'bucket': 'movie-posters',
                    'total_objects': posters_count,
                    'total_size': posters_size_human
                },
                'health_test': {
                    'test_bucket': bucket_name,
                    'test_file': test_file,
                    'upload_success': True,
                    'download_success': True,
                    'data_integrity': data_matches
                }
            }
        }
        
    except S3Error as e:
        return {
            'status': 'unhealthy',
            'service': 'minio',
            'message': f'S3 error: {e.message}'
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'service': 'minio',
            'message': f'Unexpected error: {str(e)}'
        }

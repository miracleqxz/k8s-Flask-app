import requests
from config import Config


def check_loki():
    try:
        ready_url = f"http://{Config.LOKI_HOST}:{Config.LOKI_PORT}/ready"
        
        response = requests.get(ready_url, timeout=5)
        
        is_ready = response.status_code == 200
        
        try:
            metrics_url = f"http://{Config.LOKI_HOST}:{Config.LOKI_PORT}/metrics"
            metrics_response = requests.get(metrics_url, timeout=5)
            has_metrics = metrics_response.status_code == 200
        except:
            has_metrics = False
        
        try:
            buildinfo_url = f"http://{Config.LOKI_HOST}:{Config.LOKI_PORT}/loki/api/v1/status/buildinfo"
            buildinfo_response = requests.get(buildinfo_url, timeout=5)
            if buildinfo_response.status_code == 200:
                buildinfo = buildinfo_response.json()
            else:
                buildinfo = {}
        except:
            buildinfo = {}
        
        response_time = response.elapsed.total_seconds()
        
        return {
            'status': 'healthy' if is_ready else 'unhealthy',
            'service': 'loki',
            'message': 'Successfully connected to Loki',
            'details': {
                'connection': {
                    'host': Config.LOKI_HOST,
                    'port': Config.LOKI_PORT,
                    'ready_endpoint': ready_url
                },
                'ready': {
                    'status': 'ready' if is_ready else 'not ready',
                    'metrics_available': has_metrics
                },
                'buildinfo': {
                    'version': buildinfo.get('version', 'N/A'),
                    'revision': buildinfo.get('revision', 'N/A'),
                    'branch': buildinfo.get('branch', 'N/A'),
                    'buildDate': buildinfo.get('buildDate', 'N/A')
                },
                'response': {
                    'status_code': response.status_code,
                    'response_time_seconds': round(response_time, 3),
                    'response_text': response.text[:100] if response.text else 'N/A'
                }
            }
        }
        
    except requests.ConnectionError as e:
        return {
            'status': 'unhealthy',
            'service': 'loki',
            'message': f'Connection error: {str(e)}'
        }
    except requests.Timeout as e:
        return {
            'status': 'unhealthy',
            'service': 'loki',
            'message': f'Timeout error: {str(e)}'
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'service': 'loki',
            'message': f'Unexpected error: {str(e)}'
        }
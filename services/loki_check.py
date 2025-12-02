import requests
from config import Config


def check_loki():
    try:
        ready_url = f"http://{Config.LOKI_HOST}:{Config.LOKI_PORT}/ready"
        
        response = requests.get(ready_url, timeout=5)
        
        response_text = response.text.strip()
        is_ready = response.status_code == 200 and response_text == "ready"
        
        is_initializing = "not ready" in response_text.lower() or "waiting" in response_text.lower()
        
        
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
        
    
        if is_ready:
            status = 'healthy'
            message = 'Successfully connected to Loki'
        elif is_initializing:
            status = 'healthy'  
            message = 'Loki is initializing (this is normal)'
        else:
            status = 'unhealthy'
            message = 'Loki is not ready'
        
        return {
            'status': status,
            'service': 'loki',
            'message': message,
            'details': {
                'connection': {
                    'host': Config.LOKI_HOST,
                    'port': Config.LOKI_PORT,
                    'ready_endpoint': ready_url
                },
                'ready': {
                    'status': 'ready' if is_ready else ('initializing' if is_initializing else 'not ready'),
                    'response_text': response_text[:100],
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
                    'response_time_seconds': round(response_time, 3)
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
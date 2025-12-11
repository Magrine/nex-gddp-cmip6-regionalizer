import requests
import os
import sys

def download_file(url, global_path, current, total):
    try:
        filename = os.path.basename(global_path)
        
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            total_size = int(response.headers.get('content-length', 0))
            
            with open(global_path, 'wb') as f:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=1024*1024):
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = int(50 * downloaded / total_size)
                        actual_percent = int(100 * downloaded / total_size)
                        
                        bar = '=' * percent
                        spaces = ' ' * (50 - percent)
                        
                        sys.stdout.write(
                            f"\rProgress ({current}/{total}): [{bar}{spaces}] {actual_percent}% (1/3 Downloading)"
                        )
                        sys.stdout.flush()
            
            return True
        else:
            print(f"\nStatus error {response.status_code} on file {filename}")
            return False
            
    except Exception as e:
        print(f"\nConnection error: {e}")
        return False

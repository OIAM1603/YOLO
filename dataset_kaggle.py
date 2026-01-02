import os
import urllib3
import requests.sessions
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
old_request = requests.sessions.Session.request

def unsafe_request(self, *args, **kwargs):
 kwargs['verify'] = False
 return old_request(self, *args, **kwargs)
requests.sessions.Session.request = unsafe_request
    
from requests.sessions import Session as OriginalSession
class UnsafeSession(OriginalSession):

 def request(self, *args, **kwargs):
  kwargs['verify'] = False
  return super().request(*args, **kwargs)

requests.Session = UnsafeSession
import kagglehub
import shutil
from pathlib import Path

# Download (vẫn tải vào cache)
cache_path = Path(kagglehub.dataset_download("oiam2010/vehicles-vl-augmented"))
print("Cache path:", cache_path)

# Thư mục hiện tại
target_dir = Path.cwd() / "dataset"
target_dir.mkdir(parents=True, exist_ok=True)

# Copy toàn bộ dataset
if not any(target_dir.iterdir()):
    shutil.move(cache_path, target_dir)
    print("Dataset copied to:", target_dir)
else:
    print("Target directory already exists, skip copying")

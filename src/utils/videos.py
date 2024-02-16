import hashlib
from pathlib import Path
from src.config import PROJECT_ROOT


class VideoUtils:
    @staticmethod
    def save(contents):
        video_checksum = hashlib.md5(contents).hexdigest()
        video_path = f"{PROJECT_ROOT}/cache/{video_checksum[:2]}/{video_checksum[2:]}"
        Path(video_path).mkdir(parents=True, exist_ok=True)
        with open(Path(video_path, "video"), 'wb') as _obj:
            _obj.write(contents)

        return video_checksum

import hashlib
from pathlib import Path
import ffmpeg

from src.config import PROJECT_ROOT


class VideoUtils:
    @staticmethod
    def save(contents):
        video_checksum = hashlib.md5(contents).hexdigest()
        video_dir = f"{PROJECT_ROOT}/cache/{video_checksum[:2]}/{video_checksum[2:]}"
        Path(video_dir).mkdir(parents=True, exist_ok=True)
        with open(Path(video_dir, "video"), "wb") as _obj:
            _obj.write(contents)

        return video_checksum

    @staticmethod
    def extract_audio(checksum):
        video_dir = f"{PROJECT_ROOT}/cache/{checksum[:2]}/{checksum[2:]}"
        video_path = Path(video_dir, "video").absolute().as_posix()
        audio_path = Path(video_dir, "audio.wav").absolute().as_posix()
        ffmpeg.input(video_path).output(audio_path).run(overwrite_output=True)

    @staticmethod
    def extract_frame(checksum):
        video_dir = f"{PROJECT_ROOT}/cache/{checksum[:2]}/{checksum[2:]}"
        video_path = Path(video_dir, "video").absolute().as_posix()
        frame_path = Path(video_dir, "frame-%d.png").absolute().as_posix()
        ffmpeg.input(video_path).output(frame_path, vf="fps=1").run(
            overwrite_output=True
        )

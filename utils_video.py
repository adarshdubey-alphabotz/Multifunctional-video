#!/usr/bin/env python3
"""
Multifunctional Video Utility Script (lazy imports)
- Avoids raising ModuleNotFoundError at import time
- Prints actionable install instructions when modules are missing
- Safe resource cleanup
Compatible with Python 3.8+
"""

import sys
import os
import traceback
from typing import List, Optional, Any


def _install_instructions():
    return ("Missing required Python packages.\n"
            "Install them in your environment, e.g.:\n"
            "  python3 -m pip install -r requirements.txt\n"
            "or:\n"
            "  python3 -m pip install moviepy Pillow numpy imageio imageio-ffmpeg\n")


def _safe_close(obj: Any):
    """Call close() if available without raising."""
    try:
        if hasattr(obj, "close") and callable(obj.close):
            obj.close()
    except Exception:
        # Best-effort; ignore exceptions during close
        pass


# ====================================================
#  Split a video into smaller parts
# ====================================================
def split_video(file_path: str, split_points: List[int]) -> List[str]:
    try:
        from moviepy.editor import VideoFileClip
    except ModuleNotFoundError:
        print("[ERROR] moviepy is not installed.")
        print(_install_instructions())
        return []

    try:
        clip = VideoFileClip(file_path)
        prev = 0
        output_files: List[str] = []

        for sec in split_points:
            outpath = f"{os.path.splitext(file_path)[0]}_{prev}_{sec}.mp4"
            print(f"[INFO] Creating part: {outpath}")
            part = clip.subclip(prev, sec)
            part.write_videofile(outpath, codec="libx264", audio_codec="aac", verbose=False, logger=None)
            _safe_close(part)
            output_files.append(outpath)
            prev = sec

        _safe_close(clip)
        return output_files
    except Exception as e:
        print("[ERROR] Failed to split video:", e)
        traceback.print_exc()
        return []


# ====================================================
#  Merge two videos
# ====================================================
def merge_videos(v1: str, v2: str) -> Optional[str]:
    try:
        from moviepy.editor import VideoFileClip, concatenate_videoclips
    except ModuleNotFoundError:
        print("[ERROR] moviepy is not installed.")
        print(_install_instructions())
        return None

    try:
        print(f"[INFO] Merging: {v1} + {v2}")
        clip1 = VideoFileClip(v1)
        clip2 = VideoFileClip(v2)
        final = concatenate_videoclips([clip1, clip2])
        outpath = f"merged_{os.path.basename(v1)}_{os.path.basename(v2)}.mp4"
        final.write_videofile(outpath, codec="libx264", audio_codec="aac", verbose=False, logger=None)

        _safe_close(clip1)
        _safe_close(clip2)
        _safe_close(final)
        return outpath
    except Exception as e:
        print("[ERROR] Failed to merge videos:", e)
        traceback.print_exc()
        return None


# ====================================================
#  Take screenshots from a video
# ====================================================
def take_screenshots(video_path: str, times: List[str]) -> List[str]:
    try:
        from moviepy.editor import VideoFileClip
    except ModuleNotFoundError:
        print("[ERROR] moviepy is not installed.")
        print(_install_instructions())
        return []

    try:
        # Pillow is used to convert array to image file
        try:
            from PIL import Image
        except ModuleNotFoundError:
            print("[ERROR] Pillow is not installed.")
            print(_install_instructions())
            return []

        clip = VideoFileClip(video_path)
        imgs: List[str] = []

        for tstr in times:
            mm_ss = tstr.strip().split(":")
            if len(mm_ss) == 1:
                sec = int(mm_ss[0])
            else:
                sec = int(mm_ss[0]) * 60 + int(mm_ss[1])
            print(f"[INFO] Capturing frame at {sec} seconds")
            frame = clip.get_frame(sec)
            img = Image.fromarray(frame)
            fname = f"{os.path.splitext(video_path)[0]}_{sec}.png"
            img.save(fname)
            imgs.append(fname)

        _safe_close(clip)
        return imgs
    except Exception as e:
        print("[ERROR] Failed to take screenshots:", e)
        traceback.print_exc()
        return []


# ====================================================
#  Add watermark to a video
# ====================================================
def add_watermark(video_path: str, img_path: str, pos: str = "bottom-right") -> Optional[str]:
    try:
        from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
    except ModuleNotFoundError:
        print("[ERROR] moviepy is not installed.")
        print(_install_instructions())
        return None

    try:
        # Pillow used only to validate image exists
        try:
            from PIL import Image
        except ModuleNotFoundError:
            print("[ERROR] Pillow is not installed.")
            print(_install_instructions())
            return None

        print(f"[INFO] Adding watermark at '{pos}' position")

        clip = VideoFileClip(video_path)
        # Validate the watermark image can be opened
        Image.open(img_path).close()

        water_clip = ImageClip(img_path).set_duration(clip.duration)

        # Resize watermark relative to video size
        video_w, video_h = clip.w, clip.h
        wm_w, wm_h = int(video_w * 0.2), int(video_h * 0.2)
        # Avoid zero-size resize
        if wm_w <= 0 or wm_h <= 0:
            wm_w, wm_h = min(video_w, 100), min(video_h, 100)
        water_clip = water_clip.resize((wm_w, wm_h))

        # Position options
        position_map = {
            "top-left": (5, 5),
            "top-right": (video_w - wm_w - 5, 5),
            "bottom-left": (5, video_h - wm_h - 5),
            "bottom-right": (video_w - wm_w - 5, video_h - wm_h - 5),
            "center": ((video_w - wm_w) // 2, (video_h - wm_h) // 2)
        }

        water_clip = water_clip.set_pos(position_map.get(pos, (5, 5)))
        final = CompositeVideoClip([clip, water_clip])

        outpath = f"{os.path.splitext(video_path)[0]}_wm_{pos}.mp4"
        final.write_videofile(outpath, codec="libx264", audio_codec="aac", verbose=False, logger=None)

        _safe_close(clip)
        _safe_close(water_clip)
        _safe_close(final)
        return outpath
    except Exception as e:
        print("[ERROR] Failed to add watermark:", e)
        traceback.print_exc()
        return None


# ====================================================
#  Self-test (optional)
# ====================================================
if __name__ == "__main__":
    print("[INFO] utils_video.py loaded as script.")
    print("[INFO] Python Executable:", sys.executable)
    print("[INFO] Python Version:", sys.version)
    print("[INFO] Current Working Dir:", os.getcwd())
    # Example usage for testing:
    # split_video("sample.mp4", [5, 10])
    # merge_videos("part1.mp4", "part2.mp4")
    # take_screenshots("sample.mp4", ["0:05", "0:10"])
    # add_watermark("sample.mp4", "logo.png", "center")

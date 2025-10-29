# utils_video.py
"""
Updated Multifunctional Video Utility Script
Compatible with Python 3.8+
Includes improved imports, safe handling, and debug logs.
"""

import sys
import os
import traceback

# Debug info: helps confirm environment issues
print(f"[INFO] Python Executable: {sys.executable}")
print(f"[INFO] Python Version: {sys.version}")
print(f"[INFO] Current Working Dir: {os.getcwd()}")

try:
    from moviepy.editor import (
        VideoFileClip,
        concatenate_videoclips,
        CompositeVideoClip,
        ImageClip
    )
    from PIL import Image
except ModuleNotFoundError as e:
    print("[ERROR] Missing required modules.")
    print("Try installing them using:")
    print("  pip install moviepy Pillow numpy imageio imageio-ffmpeg")
    traceback.print_exc()
    sys.exit(1)


# ====================================================
#  Split a video into smaller parts
# ====================================================
def split_video(file_path, split_points):
    try:
        clip = VideoFileClip(file_path)
        prev = 0
        output_files = []

        for sec in split_points:
            outpath = f"{os.path.splitext(file_path)[0]}_{prev}_{sec}.mp4"
            print(f"[INFO] Creating part: {outpath}")
            part = clip.subclip(prev, sec)
            part.write_videofile(outpath, codec="libx264", audio_codec="aac", verbose=False, logger=None)
            output_files.append(outpath)
            prev = sec

        clip.close()
        return output_files
    except Exception as e:
        print("[ERROR] Failed to split video:", e)
        traceback.print_exc()
        return []


# ====================================================
#  Merge two videos
# ====================================================
def merge_videos(v1, v2):
    try:
        print(f"[INFO] Merging: {v1} + {v2}")
        clip1, clip2 = VideoFileClip(v1), VideoFileClip(v2)
        final = concatenate_videoclips([clip1, clip2])
        outpath = f"merged_{os.path.basename(v1)}_{os.path.basename(v2)}.mp4"
        final.write_videofile(outpath, codec="libx264", audio_codec="aac", verbose=False, logger=None)

        clip1.close()
        clip2.close()
        final.close()
        return outpath
    except Exception as e:
        print("[ERROR] Failed to merge videos:", e)
        traceback.print_exc()
        return None


# ====================================================
#  Take screenshots from a video
# ====================================================
def take_screenshots(video_path, times):
    try:
        clip = VideoFileClip(video_path)
        imgs = []

        for tstr in times:
            mm_ss = tstr.strip().split(":")
            sec = int(mm_ss[0]) * 60 + int(mm_ss[1])
            print(f"[INFO] Capturing frame at {sec} seconds")
            frame = clip.get_frame(sec)
            img = Image.fromarray(frame)
            fname = f"{os.path.splitext(video_path)[0]}_{sec}.png"
            img.save(fname)
            imgs.append(fname)

        clip.close()
        return imgs
    except Exception as e:
        print("[ERROR] Failed to take screenshots:", e)
        traceback.print_exc()
        return []


# ====================================================
#  Add watermark to a video
# ====================================================
def add_watermark(video_path, img_path, pos="bottom-right"):
    try:
        print(f"[INFO] Adding watermark at '{pos}' position")

        clip = VideoFileClip(video_path)
        water_img = Image.open(img_path)
        water_clip = ImageClip(img_path).set_duration(clip.duration)

        # Resize watermark relative to video size
        video_w, video_h = clip.w, clip.h
        wm_w, wm_h = int(video_w * 0.2), int(video_h * 0.2)
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

        clip.close()
        water_clip.close()
        final.close()
        return outpath
    except Exception as e:
        print("[ERROR] Failed to add watermark:", e)
        traceback.print_exc()
        return None


# ====================================================
#  Self-test (optional)
# ====================================================
if __name__ == "__main__":
    print("[INFO] utils_video.py loaded successfully.")
    # Example usage for testing:
    # split_video("sample.mp4", [5, 10])
    # merge_videos("part1.mp4", "part2.mp4")
    # take_screenshots("sample.mp4", ["0:05", "0:10"])
    # add_watermark("sample.mp4", "logo.png", "center")

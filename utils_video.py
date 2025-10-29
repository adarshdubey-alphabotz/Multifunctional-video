# utils_video.py
from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, ImageClip
from PIL import Image
import os

def split_video(file_path, split_points):
    clip = VideoFileClip(file_path)
    prev = 0
    files = []
    for sec in split_points:
        outpath = f"{file_path}_{prev}_{sec}.mp4"
        part = clip.subclip(prev, sec)
        part.write_videofile(outpath, codec="libx264")
        files.append(outpath)
        prev = sec
    return files

def merge_videos(v1, v2):
    c1, c2 = VideoFileClip(v1), VideoFileClip(v2)
    outpath = f"merged_{v1}_{v2}.mp4"
    final = concatenate_videoclips([c1, c2])
    final.write_videofile(outpath, codec="libx264")
    return outpath

def take_screenshots(video_path, times):
    clip = VideoFileClip(video_path)
    imgs = []
    for tstr in times:
        ms = tstr.strip().split(":")
        sec = int(ms[0]) * 60 + int(ms[1])
        frame = clip.get_frame(sec)
        img = Image.fromarray(frame)
        fname = f"{video_path}_{sec}.png"
        img.save(fname)
        imgs.append(fname)
    return imgs

def add_watermark(video_path, img_path, pos):
    clip = VideoFileClip(video_path)
    water_img = Image.open(img_path)
    water_clip = ImageClip(img_path).set_duration(clip.duration)
    video_w, video_h = clip.w, clip.h
    wm_w, wm_h = water_img.size
    wm_w, wm_h = int(video_w*0.2), int(video_h*0.2)
    water_clip = water_clip.resize((wm_w, wm_h))
    position_map = {
        "top-left": (5, 5),
        "top-right": (video_w - wm_w - 5, 5),
        "bottom-left": (5, video_h - wm_h - 5),
        "bottom-right": (video_w - wm_w - 5, video_h - wm_h - 5),
        "center": ((video_w - wm_w)//2, (video_h - wm_h)//2)
    }
    water_clip = water_clip.set_pos(position_map.get(pos, (5,5)))
    final = CompositeVideoClip([clip, water_clip])
    outpath = f"{video_path}_wm_{pos}.mp4"
    final.write_videofile(outpath, codec="libx264")
    return outpath

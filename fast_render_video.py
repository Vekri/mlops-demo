import os
import subprocess
import imageio_ffmpeg

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
base = os.path.abspath(".")
vis = os.path.join(base, "visuals")

scenes = [
    "scene1_intro",
    "scene2_scikit",
    "scene3_mlflow",
    "scene4_fastapi",
    "scene5_docker",
    "scene6_github",
    "scene7_monitoring",
    "scene8_outro"
]

concat_list = []
for name in scenes:
    img = os.path.join(vis, f"{name}.png")
    aud = os.path.join(vis, f"{name}.mp3")
    part_mp4 = os.path.join(vis, f"{name}.mp4")
    
    cmd = [
        ffmpeg, "-y",
        "-loop", "1",
        "-i", img,
        "-i", aud,
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest",
        part_mp4
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    concat_list.append(f"file '{part_mp4.replace(os.sep, '/')}'")
    print(f"Rendered segment: {name}.mp4")

# Write concat list file
concat_txt = os.path.join(vis, "concat_list.txt")
with open(concat_txt, "w") as f:
    f.write("\n".join(concat_list))

# Final output
final_mp4 = os.path.join(base, "mlops_end_to_end_tutorial.mp4")
concat_cmd = [
    ffmpeg, "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", concat_txt,
    "-c", "copy",
    final_mp4
]
subprocess.run(concat_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(f"SUCCESS: Final tutorial video rendered in full HD at {final_mp4}")
print(f"Size: {os.path.getsize(final_mp4)} bytes")

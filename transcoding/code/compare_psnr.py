import os
import sys

from utils import compare_psnr, get_bitrate, get_video_size, get_videos

"""
Compare generated video quality of different codec:
(1) libx264 CPU
(2) h264_nvenc GPU
(3) libx264 SoC-CPU
(4) h264_mediacodec SoC-HW

Codec | Target bitrate | PSNR (to original video) | File size
------+----------------+--------------------------+----------
"""


def compare_tr_output(folder: str, annotation: str):
    video_path = os.path.join("videos", folder)
    origin_video_path = "videos/"
    for v in get_videos():
        ref_video = os.path.join(origin_video_path, v)
        target_video = os.path.join(video_path, v)

        bitrate = float(get_bitrate("ffprobe", target_video)) / 10**3
        psnr = compare_psnr("ffmpeg", target_video, ref_video)
        file_size = get_video_size(target_video)
        print(annotation, target_video, bitrate, psnr, file_size)


if __name__ == "__main__":
    if sys.argv[1] == "cpu":
        compare_tr_output("cpu_output_online", "cpu_libx264")

    elif sys.argv[1] == "gpu":
        compare_tr_output("gpu_output_online", "gpu-a40_nvenc")

    elif sys.argv[1] == "soc-cpu":
        compare_tr_output("soc-cpu_output_online", "soc-cpu_libx264")

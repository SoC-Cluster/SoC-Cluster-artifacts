import re
import subprocess


def get_videos():
    videos = [
        "presentation_1920x1080_25.mkv",
        "desktop_1280x720_30.mkv",
        "chicken_3840x2160_30.mkv",
        "hall_1920x1080_29.mkv",
        "game3_1280x720_59.mkv",
        "holi_854x480_30.mkv",
    ]
    return videos


def compare_psnr(ffmpeg, video, ref):
    """Returns PSNR (dB)"""

    cmd = [ffmpeg, "-i", video, "-i", ref, "-filter_complex", "psnr", "-f", "null", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, _ = p.communicate()
    avg_psnr = re.search(".+ average:(\d+\.\d+|inf) .+", out.decode("utf-8"))
    assert avg_psnr is not None
    return float(avg_psnr.group(1))


def get_bitrate(ffprobe, video):
    """Returns bitrate (bit/s)"""

    cmd = [ffprobe, "-i", video]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()

    m = re.search("bitrate: ([0-9]+) kb/s", err.decode("utf-8"))
    assert m is not None
    return int(m.group(1)) * 1000  # report in b/s


def get_video_stats(ffprobe, video):
    """Returns resolution (pixels/frame), and framerate (fps) of a video"""

    # run ffprobe
    cmd = [ffprobe, "-show_entries", "stream=width,height", video]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()

    # grep resolution
    width = re.search("width=([0-9]+)", out.decode("utf-8"))
    assert width is not None, "Problem in fetching video width with {} on {}".format(
        ffprobe, video
    )
    height = re.search("height=([0-9]+)", out.decode("utf-8"))
    assert height is not None, "Problem in fetching video height with {} on {}".format(
        ffprobe, video
    )
    resolution = int(width.group(1)) * int(height.group(1))

    # grep framerate
    frame = re.search("([0-9\.]+) fps", err.decode("utf-8"))
    assert frame is not None, "Problem in fetching framerate with {} on {}".format(
        ffprobe, video
    )
    framerate = float(frame.group(1))

    return resolution, framerate


def get_video_size(video):
    """Returns video size"""

    cmd = f"ls -lh {video}"
    out = subprocess.check_output(cmd, shell=True)
    video_size = out.decode("utf-8").split()[4]
    return video_size

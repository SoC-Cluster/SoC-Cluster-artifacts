"""
Video metadata.
"""

video_fps = [30, 30, 59, 25, 29, 30]

"""
Live streaming transcoding.
[fps, per frame power consumption, max_stream_num]
"""
online_soc_libx264 = [
    [132.9787234, 0.01920161538, 13],
    [166.2971175, 0.01705555556, 15],
    [83.1220062, 0.03056898305, 4],
    [92.11495947, 0.03133333333, 9],
    [56.53021442, 0.08237471264, 3],
    [28.99671371, 0.2130434667, 1],
]
online_soc_mediacodec = [
    [238.8535032, 0.007860444333, 16],  # bounded by mediacodec instance num
    [240.3846154, 0.007754, 16],  # bounded by mediacodec instance num
    [254.3103448, 0.006475702985, 12],  # bounded by computation
    [167.1122995, 0.0108058, 16],  # same
    [139.4230769, 0.01496705172, 7],  # bounded by computation
    [62.34413965, 0.03906760417, 2],  # bounded by computation
]

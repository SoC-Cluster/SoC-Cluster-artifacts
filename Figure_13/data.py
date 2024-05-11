resnet50_latency = {
    "SoC-CPU": {
        "Snapdragon 835": 197.592,
        "Snapdragon 845": 86.125,
        "Snapdragon 855": 77.337,
        "Snapdragon 865": 74.3005,
        "Snapdragon 888": 60.0395,
        "Snapdragon 8+Gen1": 41.5662,
    },
    "SoC-GPU": {
        "Snapdragon 835": 70.50825,
        "Snapdragon 845": 36.8,
        "Snapdragon 855": 36.5481,
        "Snapdragon 865": 32.7,
        "Snapdragon 888": 30.0795,
        "Snapdragon 8+Gen1": 21.978,
    },
    "SoC-DSP": {
        # "Snapdragon 835": None,
        "Snapdragon 845": 8.4,
        "Snapdragon 855": 8.52475,
        "Snapdragon 865": 8.454125,
        # "Snapdragon 888": None,
        "Snapdragon 8+Gen1": 0.97853,
    },
}

yolov5x_latency = {
    "SoC-CPU": {
        "Snapdragon 835": 5278.725,
        "Snapdragon 845": 2835.479,
        "Snapdragon 855": 2229.403,
        "Snapdragon 865": 2268.369,
        "Snapdragon 888": 2096.809,
        "Snapdragon 8+Gen1": 1009.595,
    },
    "SoC-GPU": {
        "Snapdragon 835": 2129.341,
        "Snapdragon 845": 1282.042,
        "Snapdragon 855": 1209.805,
        "Snapdragon 865": 739.468,
        "Snapdragon 888": 654.713,
        "Snapdragon 8+Gen1": 511.983,
    },
}

#######################
####################### Pre; Arhive transcoding
#######################
pre_offline_throughput = {
    "SoC-CPU": {
        "Snapdragon 835": 11.35847342,
        "Snapdragon 845": 13.60026113,
        "Snapdragon 855": 21.08992745,
        "Snapdragon 865": 24.68891961,
        "Snapdragon 888": 28.14681378,
        "Snapdragon 8+Gen1": 29.99760019,
    }
}

#######################
####################### Hall; Archive transcoding
#######################
hall_offline_throughput = {
    "SoC-CPU": {
        "Snapdragon 835": 0.8669345195,
        "Snapdragon 845": 1.307165974,
        "Snapdragon 855": 1.578128231,
        "Snapdragon 865": 1.860309966,
        "Snapdragon 888": 2.210466942,
        "Snapdragon 8+Gen1": 2.35149117,
    }
}

#######################
####################### Pre; Live streaming transcoding
#######################
pre_online_throughput = {
    "SoC-CPU": {
        "Snapdragon 835": 39.93610224,
        "Snapdragon 845": 50.48465267,
        "Snapdragon 855": 64.5994832,
        "Snapdragon 865": 91.70946442,
        "Snapdragon 888": 115.5268022,
        "Snapdragon 8+Gen1": 162.5487646,
    },
    "SoC-HW": {
        "Snapdragon 835": 44.43654461,
        "Snapdragon 845": 58.87894489,
        "Snapdragon 855": 91.24087591,
        "Snapdragon 865": 168.6909582,
        "Snapdragon 888": 163.3986928,
        "Snapdragon 8+Gen1": 168.9189189,
    },
}

#######################
####################### Hall; Live streaming transcoding
#######################
hall_online_throughput = {
    "SoC-CPU": {
        "Snapdragon 835": 16.56764168,
        "Snapdragon 845": 20.24008934,
        "Snapdragon 855": 31.13592441,
        "Snapdragon 865": 37.41935484,
        "Snapdragon 888": 44.75308642,
        "Snapdragon 8+Gen1": 67.34788667,
    },
    "SoC-HW": {
        "Snapdragon 835": 43.20619785,
        "Snapdragon 845": 54.1651102,
        "Snapdragon 855": 85.69739953,
        "Snapdragon 865": 139.8264224,
        "Snapdragon 888": 135.3874883,
        "Snapdragon 8+Gen1": 139.5572666,
    },
}

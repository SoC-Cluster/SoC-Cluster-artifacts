import sys


def read_data(data_file: str):
    """Return two list which is timestamp and power"""
    prepare_phase_power_list = []
    work_phase_power_list = []
    prepare_flag = True
    work_flag = False

    with open(data_file) as f:
        lines = f.readlines()
    for line in lines:
        if line.startswith("timestamp"):
            data = line.split(" ")
            power = data[1].split(":")[-1]
            # print(power)
            if prepare_flag:
                prepare_phase_power_list.append(float(power))
            elif work_flag:
                work_phase_power_list.append(float(power))
        else:
            if prepare_flag:
                prepare_flag = False
            else:
                work_flag = True
    return prepare_phase_power_list, work_phase_power_list


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("Should pass energy log file as param")
    else:
        energy_log = sys.argv[1]
        prepare_phase_power_list, work_phase_power_list = read_data(energy_log)

        prepare_phase = 0.0
        work_phase = 0.0
        for i in range(0, len(prepare_phase_power_list)):
            prepare_phase += prepare_phase_power_list[i]
        prepare_phase /= len(prepare_phase_power_list)
        for j in range(0, len(work_phase_power_list)):
            work_phase += work_phase_power_list[j]
        work_phase /= len(work_phase_power_list)

        print(work_phase - prepare_phase)

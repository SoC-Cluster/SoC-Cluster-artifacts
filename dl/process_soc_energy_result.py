import sys


def deal(data_file: str):
    with open(data_file) as f:
        lines = f.readlines()
    power_list = []
    other_list = []
    for line in lines:
        if line.startswith("9)"):
            power = line.split(":")[-1]
            power = power.split()[0]
            if float(power) > 159:
                power_list.append(float(power))
            else:
                other_list.append(float(power))
    print(sum(power_list) / len(power_list) - sum(other_list) / len(other_list))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("Should pass energy log file as param")
    else:
        deal(sys.argv[1])

# value = "b"
# values = ("a", "b", "c")


def check_same_value(value, values):
    count = 0
    for v in values:
        if v == value:
            count += 1

    if (count == 1) | (count == 0):
        return True
    else:
        return False


def nic_available(nic, citizen_nic):
    h = 0
    for n in range(len(nic)):
        if citizen_nic == nic[n][0]:
            h = 1

    if h == 1:
        return 0
    else:
        return 1
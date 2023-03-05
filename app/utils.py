
def formatValue(value):
    if abs(value) >= 1e-3:
        suffix = "mA"
        factor = 1e3
    else:
        suffix = "uA"
        factor = 1e6
    return "{:.2f}{}".format(value * factor, suffix)
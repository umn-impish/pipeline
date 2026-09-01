def pprint(
    iteration: int,
    total: int,
    prefix: str = "",
    suffix: str = "",
    decimals: int = 1,
    length: int = 50,
    fill: str = "█",
    print_end: str = "\r",
):
    """Call in a loop to create terminal progress bar.
    iteration: current iteration
    total    : total iterations
    prefix   : prefix string
    suffix   : suffix string
    decimals : positive number of decimals in percent complete
    length   : character length of bar
    fill     : bar fill character
    print_end : end character (e.g. "\r", "\r\n")

    From: https://stackoverflow.com/a/34325723
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + "-" * (length - filled_length)
    print(f"\r{prefix} |{bar}| {percent}% {suffix}", end=print_end)
    if iteration == total:
        print()

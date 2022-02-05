# progress.py
"""Helper function to display the progress
of the program to the terminal.
"""


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', print_end="\r"):
    """
    Call in a loop to create terminal progress bar.
    Acknowledgement to Greenstick on stackoverflow.com for
    offering the function:
    https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters

    Parameters
    ----------
    iteration (Required) : 'int'
        current iteration
    total (Required) : 'int'
        total iterations
    prefix (Optional) : 'str'
        prefix string
    suffix (Optional) : 'str'
        suffix string
    decimals (Optional) : 'int'
        positive number of decimals in percent complete
    length (Optional) : 'int'
        character length of bar
    fill (Optional) : 'str'
        bar fill character
    print_end (Optional) : 'str'
        end character (e.g. "\r", "\r\n")


    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)
    # Print New Line on Complete
    if iteration == total:
        print()

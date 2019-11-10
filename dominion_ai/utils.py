import subprocess


def speak_str(s, is_silent=False):
    """Utility function to have macOS use Text to Speech to speak a string"""

    torun = 'say "'
    torun += s
    torun += '"'

    prefix = 'MUTED' if is_silent else 'Speaking'
    print(f'({prefix}: {s})')
    if not is_silent:
        subprocess.call(torun, shell=True)

# io_.py
# Input Output
# Author: Tim Schlottmann


def write_file(path: str, s: str = "") -> str:
  """ Save a string to a file """
  with open(path, "w") as f:
    f.write(s)
    f.flush()
  return path


def read_file(path: str) -> str:
  """ Get the content of a file """
  try:
    return open(path, "r").read()
  except FileNotFoundError:
    return ""

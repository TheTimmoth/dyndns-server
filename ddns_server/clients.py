# clients.py
# Clients
# Author: Tim Schlottmann

from .dicts import JsonDict


class Clients(JsonDict):
  """ Settings of the app """
  def __getitem__(self, client_name: str) -> dict:
    return super().__getitem__(client_name)

  def __setitem__(self, client_name: str, values: dict):
    super().__setitem__(client_name, values)

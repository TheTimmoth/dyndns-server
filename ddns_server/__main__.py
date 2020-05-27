#!/usr/bin/python3

from contextlib import redirect_stdout
from time import strftime

from .ddns_server import DDNSServer
from .io_ import read_file
from .io_ import write_file
from .settings import Settings

_DEFAULT_SETTINGS = {
    "clientsPath": "./clients.json",
    "logToFile": False,
    "logPath": "/var/log/ddns",
    "address": "127.0.0.1",
    "port": 21001,
    "domains": [""],
    "tlsCert": "",
    "tlsKey": "",
    "dnsServerIP": "",
    "nsupdatePath": "nsupdate",
    "nsupdateKey": "",
    "dry_run": False,
}

_SETTINGS_PATH = "./settings.json"


def start_server(settings: Settings):
  s = DDNSServer(
      address=settings["address"],
      port=settings["port"],
      domains=settings["domains"],
      dns_server_ip=settings["dnsServerIP"],
      nsupdate_path=settings["nsupdatePath"],
      nsupdate_key=settings["nsupdateKey"],
      clients_path=settings["clientsPath"],
      tls_cert=settings["tlsCert"],
      tls_key=settings["tlsKey"],
      dry_run=settings["dryRun"])
  s.listen()


def main():
  settingsFile = read_file(_SETTINGS_PATH)
  settings = Settings(settingsFile, _DEFAULT_SETTINGS)

  # Write settings file if it does not exist and exit
  if not settingsFile:
    write_file(_SETTINGS_PATH, str(settings))
    print(
        strftime("%Y-%m-%d %H:%M:%S ") +
        f"Settings file created at {_SETTINGS_PATH}. Please edit settings first."
    )
    print(strftime("%Y-%m-%d %H:%M:%S ") + "Bye")
    exit()

  if settings["logToFile"]:
    f = open(settings["logPath"], mode="a", buffering=1)
    with redirect_stdout(f):
      start_server(settings)
  else:
    start_server(settings)


if __name__ == "__main__":
  main()

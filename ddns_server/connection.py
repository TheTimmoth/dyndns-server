# connection.py
# Connection
# Author: Tim Schlottmann

from time import strftime

from ipaddress import ip_address
from ipaddress import IPv4Address
from ipaddress import IPv6Address
from os import remove
from shlex import split
from socket import AF_INET
from subprocess import run
from threading import Thread

from .clients import Clients
from .io_ import read_file
from .settings import Settings


class Connection(Thread):
  def __init__(
      self,
      conn_id: int,
      conn,
      domains: list,
      dns_server_ip: str,
      nsupdate_path: str,
      nsupdate_key: str,
      clients_path: str,
      dry_run: bool,
  ):
    super().__init__(name=f"connection{conn_id}")
    self.conn_id = conn_id
    self.conn = conn

    if self.conn.family == AF_INET:
      self.addr = IPv4Address(conn.getpeername()[0])
    elif IPv6Address(conn.getpeername()[0]).ipv4_mapped:
      self.addr = IPv6Address(conn.getpeername()[0]).ipv4_mapped
    else:
      self.addr = IPv6Address(conn.getpeername()[0])

    self.domains = domains
    self.dns_server_ip = dns_server_ip
    self.nsupdate_path = nsupdate_path
    self.nsupdate_key = nsupdate_key
    self.clients_path = clients_path
    self.dry_run = dry_run

    self.client_ip = self.conn.getpeername()[0]

  def run(self):
    #Identify client
    psk = None
    try:
      psk = self.conn.recv(1024)
    except ConnectionResetError as e:
      print(
          strftime("%Y-%m-%d %H:%M:%S ") +
          f"[{self.conn_id}] Received connection reset from {client_ip}")
    if not psk:
      self.conn.close()
      return
    self.psk = psk.decode("utf-8").rstrip()

    updateDomains = self.identifyClient(self.psk)

    for d in self.domains:
      if d in updateDomains:
        for l in updateDomains[d]["subdomains"]:
          self.updateDNS(l, d)
    self.conn.sendall(str(self.addr).encode("utf-8"))
    self.conn.close()

  def updateDNS(self, label, domain):
    nsupdateInput = f"./nsupdateInput_{self.conn_id}.txt"

    server = self.dns_server_ip
    zone = label + "." + domain
    ttl = 60  #TODO: modifiable per domain basis
    exe = self.nsupdate_path
    key = self.nsupdate_key

    # Update DNS Server
    if ip_address(self.addr).version == 4:
      rrType = "A"
    else:
      rrType = "AAAA"
    print(
        strftime("%Y-%m-%d %H:%M:%S ") +
        f"[{self.conn_id}] Updating DNS: {zone} {ttl} {rrType} {self.addr}")

    file = open(nsupdateInput, "w")
    file.write(f"server {server}\n")
    if not self.dry_run:
      file.write(f"update delete {zone} {rrType}\n")
      file.write(f"update add {zone} {ttl} {rrType} {self.addr}\n")
    file.write("send\n")
    file.close()

    run(split(f"{exe} -k {key} {nsupdateInput}"))

    remove(nsupdateInput)

  def identifyClient(self, psk: str):
    clients = Clients(read_file(self.clients_path))

    for c in clients:
      if clients[c]["psk"] == psk:
        print(
            strftime("%Y-%m-%d %H:%M:%S ") +
            f"[{self.conn_id}] Client {c} connected from {self.client_ip}")
        return clients[c]["domains"]
    return None

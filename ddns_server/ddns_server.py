# ddns_server.py
# DDNSServer
# Author: Tim Schlottmann

from ipaddress import ip_address
from time import strftime
from typing import NamedTuple

import atexit
import socket
import ssl

from .connection import Connection
from .io_ import read_file
from .settings import Settings


class DDNSServer:
  """ The server component """

  def __init__(
      self,
      address,
      port,
      domains: list,
      tls_cert: str,
      tls_key: str,
      dns_server_ip: str,
      nsupdate_path: str,
      nsupdate_key: str,
      clients_path: str,
      dry_run: bool,
  ):

    self.address = address
    self.port = port
    self.domains = domains
    self.tls_cert = tls_cert
    self.tls_key = tls_key
    self.dns_server_ip = dns_server_ip
    self.nsupdate_path = nsupdate_path
    self.nsupdate_key = nsupdate_key
    self.clients_path = clients_path
    self.conn_id = 0
    self.dry_run = dry_run
    atexit.register(self.shutdown)

  def listen(self):
    print(strftime("%Y-%m-%d %H:%M:%S ") + "Listening...")
    # if socket.has_dualstack_ipv6():
    #   # Python 3.8
    #   s = socket.create_server((self.address, self.port),
    #                            family=socket.AF_INET6,
    #                            dualstack_ipv6=True)

    if self.address:
      if ip_address(self.address).version == 4:
        self.s = socket.socket(
            socket.AF_INET, type=socket.SOCK_STREAM, proto=0, fileno=None)
    else:
      self.s = socket.socket(
          socket.AF_INET6, type=socket.SOCK_STREAM, proto=0, fileno=None)
    self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.s.bind((self.address, self.port))
    self.s.listen()
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(self.tls_cert, self.tls_key)
    context.options |= ssl.OP_NO_SSLv2
    context.options |= ssl.OP_NO_SSLv3
    context.options |= ssl.OP_NO_TLSv1
    context.options |= ssl.OP_NO_TLSv1_1
    context.options |= ssl.OP_NO_TLSv1_2
    self.ss = context.wrap_socket(self.s, server_side=True)
    while 1:
      conn = self.ss.accept()[0]
      Connection(
          conn_id=self.conn_id,
          conn=conn,
          domains=self.domains,
          dns_server_ip=self.dns_server_ip,
          nsupdate_path=self.nsupdate_path,
          nsupdate_key=self.nsupdate_key,
          clients_path=self.clients_path,
          dry_run=self.dry_run,
      ).start()
      self.conn_id += 1

  def shutdown(self):
    print(strftime("%Y-%m-%d %H:%M:%S ") + "Server is shutting down...")
    if self.ss:
      self.ss.close()
    if self.s:
      self.s.close()
    print(strftime("%Y-%m-%d %H:%M:%S ") + "Bye")

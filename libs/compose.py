import signal
import subprocess
import socket
import struct


def get_default_gateway_linux():
    """
    Read the default gateway directly from /proc.
    """
    with open("/proc/net/route") as fh:
        for line in fh:
            fields = line.strip().split()
            if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                continue

            return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))


class DelayedSignalHandler(object):
    """
    Allows docker-compose to gracefully exit when sending Ctrl+C

    See https://stackoverflow.com/a/10492061
    """

    def __init__(self, managed_signals):
        self.managed_signals = managed_signals
        self.managed_signals_queue = list()
        self.old_handlers = dict()

    def _handle_signal(self, caught_signal, frame):
        self.managed_signals_queue.append((caught_signal, frame))

    def __enter__(self):
        for managed_signal in self.managed_signals:
            old_handler = signal.signal(managed_signal, self._handle_signal)
            self.old_handlers[managed_signal] = old_handler

    def __exit__(self, *_):
        for managed_signal, old_handler in self.old_handlers.items():
            signal.signal(managed_signal, old_handler)

        for managed_signal, frame in self.managed_signals_queue:
            self.old_handlers[managed_signal](managed_signal, frame)


def call_compose(*args):
    with DelayedSignalHandler((signal.SIGINT, signal.SIGTERM)):
        return subprocess.call(' '.join(['docker-compose'] + list(args)), shell=True)

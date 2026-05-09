"""Provides a raw console to test module and demonstrate usage."""
import argparse
import asyncio
import logging

import anthemav

__all__ = ("console", "monitor")


async def console(log):
    """Connect to receiver and show events as they occur.

    Pulls the following arguments from the command line (not method arguments):

    :param host:
        Hostname or IP Address of the device.
    :param port:
        TCP port number of the device.
    :param verbose:
        Show debug logging.
    """
    parser = argparse.ArgumentParser(description=console.__doc__)
    parser.add_argument("--host", default="127.0.0.1", help="IP or FQDN of AVR")
    parser.add_argument("--port", default="14999", help="Port of AVR")
    parser.add_argument("--verbose", "-v", action="count")

    args = parser.parse_args()

    if args.verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(level=level)

    def log_callback(message):
        """Receives event callback from Anthem Protocol class."""
        log.info("Callback invoked: %s" % message)

    host = args.host
    port = int(args.port)

    log.info("Connecting to Anthem AVR at %s:%i" % (host, port))

    conn = await anthemav.Connection.create(
        host=host, port=port, update_callback=log_callback
    )

    log.info("Power state is " + str(conn.protocol.power))
    conn.protocol.power = True
    await asyncio.sleep(5)
    log.info("Power state is " + str(conn.protocol.power))
    log.info("Model is %s", conn.protocol.model)
    log.info("Number of zone is %s", len(conn.protocol.zones))
    log.info("Volume is " + str(conn.protocol.zones[1].volume))

    await asyncio.get_event_loop().create_future()  # run forever until Ctrl+C


def monitor():
    """Wrapper to call console with a loop."""
    log = logging.getLogger(__name__)
    try:
        asyncio.run(console(log))
    except KeyboardInterrupt:
        pass

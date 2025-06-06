# SPDX-FileCopyrightText: © 2024 Tenstorrent AI ULC

# SPDX-License-Identifier: Apache-2.0
import sys

from ttexalens.tt_exalens_ifc import ttexalens_client, ttexalens_server_not_supported
from typing import Callable

server_port = 0
server = None


def check_not_implemented_response(server_command: Callable[[], any]):
    try:
        server_command()
        print("fail")
    except ttexalens_server_not_supported:
        print("pass")


def empty_get_cluster_description():
    global server
    check_not_implemented_response(lambda: server.get_cluster_description())


def empty_convert_from_noc0():
    global server
    check_not_implemented_response(lambda: server.convert_from_noc0(1, 2, 3, "core_type", "coord_type"))


def empty_pci_read32():
    global server
    check_not_implemented_response(lambda: server.pci_read32(0, 1, 2, 3, 123456))


def empty_pci_write32():
    global server
    check_not_implemented_response(lambda: server.pci_write32(0, 1, 2, 3, 123456, 987654))


def empty_pci_read():
    global server
    check_not_implemented_response(lambda: server.pci_read(0, 1, 2, 3, 123456, 1024))


def empty_pci_read32_raw():
    global server
    check_not_implemented_response(lambda: server.pci_read32_raw(111, 123456))


def empty_pci_write32_raw():
    global server
    check_not_implemented_response(lambda: server.pci_write32_raw(1, 123456, 987654))


def empty_dma_buffer_read32():
    global server
    check_not_implemented_response(lambda: server.dma_buffer_read32(1, 123456, 456))


def empty_pci_read_tile():
    global server
    check_not_implemented_response(lambda: server.pci_read_tile(0, 1, 2, 3, 123456, 1024, 14))


def empty_pci_write():
    global server
    check_not_implemented_response(
        lambda: server.pci_write(0, 1, 2, 3, 123456, bytes([10, 11, 12, 13, 14, 15, 16, 17]))
    )


def empty_jtag_read32():
    global server
    check_not_implemented_response(lambda: server.jtag_read32(0, 1, 2, 3, 123456))


def empty_jtag_write32():
    global server
    check_not_implemented_response(lambda: server.jtag_write32(0, 1, 2, 3, 123456, 987654))


def empty_jtag_read32_axi():
    global server
    check_not_implemented_response(lambda: server.jtag_read32_axi(1, 123456))


def empty_jtag_write32_axi():
    global server
    check_not_implemented_response(lambda: server.jtag_write32_axi(1, 123456, 987654))


def empty_get_file():
    global server
    check_not_implemented_response(lambda: server.get_file("file_name"))


def pci_write32_pci_read32():
    global server
    server.pci_write32(0, 1, 2, 3, 123456, 987654)
    read = server.pci_read32(0, 1, 2, 3, 123456)
    print("pass" if read == 987654 else "fail")


def pci_write_pci_read():
    global server
    server.pci_write(0, 1, 2, 3, 123456, b"987654")
    read = server.pci_read(0, 1, 2, 3, 123456, 6)
    print("pass" if read == b"987654" else "fail")


def pci_write32_raw_pci_read32_raw():
    global server
    server.pci_write32_raw(1, 123456, 987654)
    read = server.pci_read32_raw(1, 123456)
    print("pass" if read == 987654 else "fail")


def dma_buffer_read32():
    global server
    server.pci_write32_raw(1, 123456, 987654)
    read = server.dma_buffer_read32(1, 123456, 753)
    print("pass" if read == 987654 + 753 else "fail")


def pci_read_tile():
    global server
    read = server.pci_read_tile(0, 1, 2, 3, 123456, 1024, 14)
    print("pass" if read == "pci_read_tile(0, 1, 2, 3, 123456, 1024, 14)" else "fail")


def jtag_write32_jtag_read32():
    global server
    server.jtag_write32(0, 1, 2, 3, 123456, 987654)
    read = server.jtag_read32(0, 1, 2, 3, 123456)
    print("pass" if read == 987654 else "fail")


def jtag_write32_axi_jtag_read32_axi():
    global server
    server.jtag_write32_axi(1, 123456, 987654)
    read = server.jtag_read32_axi(1, 123456)
    print("pass" if read == 987654 else "fail")


def get_cluster_description():
    global server
    read = server.get_cluster_description()
    print("pass" if read == "get_cluster_description()" else "fail")


def convert_from_noc0():
    global server
    read = server.convert_from_noc0(1, 2, 3, "core_type", "coord_type")
    print("pass" if read == (3, 4) else "fail")


def get_device_ids():
    global server
    read = server.get_device_ids()
    print("pass" if read == b"\x00\x01" else "fail")


def get_device_arch():
    global server
    read = server.get_device_arch(1)
    print("pass" if read == "get_device_arch(1)" else "fail")


def get_device_soc_description():
    global server
    read = server.get_device_soc_description(1)
    print("pass" if read == "get_device_soc_description(1)" else "fail")


def get_file():
    global server
    read = server.get_file("file_name")
    print("pass" if read == "get_file(file_name)" else "fail")


def main():
    # Check if at least two arguments are provided (script name + function name)
    if len(sys.argv) < 3:
        print("Usage: python test_server.py <server_port> <function_name> [args...]")
        sys.exit(1)

    # Get server port and remove it from the arguments list
    port = sys.argv[1]
    del sys.argv[1]
    try:
        global server_port
        server_port = int(port)
    except ValueError:
        print(f"Couldn't parse port '{port}' as an int")
        sys.exit(1)

    # Try to connect to server
    try:
        global server
        # connect_to_server won't work here because it prints to stdout
        server = ttexalens_client("localhost", port)
    except:
        print(f"Couldn't connect to TTExaLens server on port '{port}'")
        sys.exit(1)

    # Get the function name and remove it from the arguments list
    function_name = sys.argv[1]
    del sys.argv[1]

    # Check if the specified function exists
    if function_name not in globals() or not callable(globals()[function_name]):
        print(f"Error: Function '{function_name}' not found.")
        sys.exit(1)

    # Call the specified function with the remaining arguments
    globals()[function_name](*sys.argv[1:])


if __name__ == "__main__":
    main()

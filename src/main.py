import argparse
from pymodbus.client import ModbusTcpClient

def main():
    parser = argparse.ArgumentParser(description='Modbus TCP communication script.')
    parser.add_argument('-host', type=str, default='192.168.0.1', help='The IP address to connect to.')
    parser.add_argument('-port', type=int, default=1502, help='The port number to connect to.')
    parser.add_argument('-slave', type=int, default=1, help='The slave address.')
    parser.add_argument('-address', type=int, required=True, help='The register address.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-w', '--write', type=str, help='Data to write to the register.')
    group.add_argument('-r', '--read', action='store_true', help='Read the register.')

    args = parser.parse_args()

    modbus_comm = ModbusTcpClient(host=args.host,
                                  port=args.port)
    modbus_comm.connect()
    if args.read:
        # Perform read operation
        data = modbus_comm.read_holding_registers(address=args.address,
                                                  slave=int(args.slave))
        print(f"Data read from register {args.address}: {data.registers[0]}")
    else:
        # Perform write operation
        modbus_comm.write_register(address=args.address,
                                   slave=int(args.slave),
                                   value=int(args.write))
        print(f"Data written to register {args.address}: {args.write}")
    modbus_comm.close()

if __name__ == "__main__":
    main()

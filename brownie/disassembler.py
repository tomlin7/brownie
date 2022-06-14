from pathlib import Path

from .decoder import Decoder


def disassemble(decoder: Decoder, address: int, count: int):
    for _ in range(count):
        try:
            new_address, instruction = decoder.decode(address)
            pp = instruction.print()
            print(f'{address:>04X} {pp}')
            address = new_address
        except IndexError as e:
            print(f'ERROR - {e!s}')
            break

if __name__ == '__main__':
    dec = Decoder.create(opcode_file='brownie/etc/opcodes.json', data=Path('examples/snake.gb').read_bytes(), address=0)
    _, instruction = dec.decode(0x201)
    print(instruction.print())
    disassemble(dec, 0x150, 16)

from pathlib import Path

import pytest
from brownie import Decoder, Instruction, Operand


@pytest.fixture
def make_decoder(request):
    def make(data: bytes, address: int=0):
        opcode_file = Path(request.config.rootdir) / "brownie/etc/opcodes.json"
        return Decoder.create(opcode_file=opcode_file, data=data, address=address)
    return make


def test_decoder_nop_instruction(make_decoder):
    decoder = make_decoder(data=bytes.fromhex("00"))
    new_address, instruction = decoder.decode(0x0)
    assert new_address == 0x1
    assert instruction == Instruction(
        opcode=0x0,
        immediate=True,
        operands=[],
        cycles=[4],
        bytes=1,
        mnemonic="NOP",
        comment=""
    )

def test_decoder_idk():
    dec = Decoder.create(opcode_file='brownie/etc/opcodes.json', data=Path('examples/snake.gb').read_bytes(), address=0)
    _, instruction = dec.decode(0x201)
    assert instruction == Instruction(opcode=224, immediate=False, operands=[
            Operand(immediate=False, name='a8', bytes=1, value=139, adjust=None),
            Operand(immediate=True, name='A', bytes=None, value=None, adjust=None)
        ], cycles=[12], bytes=2, mnemonic='LDH', comment='')
    assert instruction.print() == 'LDH      (0x8b), A'

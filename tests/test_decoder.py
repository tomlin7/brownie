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

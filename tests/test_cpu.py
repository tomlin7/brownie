from pathlib import Path

import hypothesis.strategies as st
import pytest
from brownie import CPU, Decoder, Registers
from hypothesis import given


@pytest.fixture(scope="session")
def make_cpu(request):
    def make(data, PC=0):
        registers = Registers(PC=PC)
        decoder = Decoder.create(opcode_file="brownie/etc/opcodes.json", data=data, address=0)
        cpu = CPU(registers=registers, decoder=decoder)
        return cpu

    return make

@given(count=st.integers(min_value=0, max_value=100))
def test_cpu_execute_nop_and_advance(make_cpu, count):
    cpu = make_cpu(b"\x00" * count)
    assert cpu.registers["PC"] == 0
    cpu.run()
    assert cpu.registers["PC"] == count

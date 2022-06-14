import hypothesis.strategies as st
import pytest
from brownie import FLAGS, REGISTERS_HIGH, Registers
from hypothesis import given


@pytest.fixture(scope="session")
def make_registers():
    def make():
        return Registers()
    return make

@given(
    value=st.integers(min_value=0, max_value=0xFF),
    field=st.sampled_from(sorted(REGISTERS_HIGH.items())),
)
def test_registers_high(make_registers, field, value):
    registers = make_registers()
    high_register, full_register = field
    registers[high_register] = value
    assert registers[full_register] == value << 8

@given(
    starting_value=st.integers(min_value=0, max_value=0xFF),
    field=st.sampled_from(sorted(FLAGS.items())),
)
def test_flags(make_registers, starting_value, field):
    flag, bit = field
    registers = make_registers()
    outcome = []
    for value in (0, 1):
        # set attribute directly
        registers.AF = starting_value
        registers[flag] = value
        outcome.append(registers["F"])
        assert registers["F"] >> bit & 1 == value
    assert outcome.pop() != outcome.pop()

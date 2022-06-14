import sys
import hypothesis.strategies as st
from hypothesis import given
from brownie import read_cartridge_metadata


HEADER_START = 0x100
HEADER_END = 0x14F
# heade rsize as measured from the last element to the first + 1
HEADER_SIZE = (HEADER_END - HEADER_START) + 1

@given(data=st.binary(
    min_size=HEADER_SIZE + HEADER_START,
    max_size=HEADER_SIZE + HEADER_START))
def test_read_cartridge_metadata_smoketest(data):
    def read(offset, count=1):
        return data[offset: offset + count + 1]

    metadata = read_cartridge_metadata(data)
    assert metadata.title == read(0x134, 14)
    
    checksum = read(0x14E, 2)
    # the checksum is in _big endian_ -- so we need to tell Python to
    # read it back in properly!
    assert metadata.global_checksum == int.from_bytes(checksum, sys.byteorder)

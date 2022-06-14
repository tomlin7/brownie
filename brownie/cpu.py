from dataclasses import dataclass

from .instruction import Instruction
from .decoder import Decoder
from .registers import Registers


class InstructionError(Exception):
    pass


@dataclass
class CPU:
    registers: Registers
    decoder: Decoder

    def execute(self, instruction: Instruction):
        match instruction:
            case Instruction(mnemonic='NOP'):
                pass
            case _:
                raise InstructionError(f'Cannot execute {instruction}')

    def run(self):
        while True:
            address = self.registers["PC"]
            try:
                next_address, instruction = self.decoder.decode(address)
            except IndexError:
                break
            self.registers["PC"] = next_address
            self.execute(instruction)

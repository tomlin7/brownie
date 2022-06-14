from dataclasses import dataclass

from .operand import Operand


@dataclass
class Instruction:
    opcode: int
    immediate: bool
    operands: list[Operand]
    cycles: list[int]
    bytes: int
    mnemonic: str
    comment: str = ""

    def copy(self, operands):
        return Instruction(opcode=self.opcode, immediate=self.immediate,
            operands=operands, cycles=self.cycles, bytes=self.bytes,
            mnemonic=self.mnemonic, comment=self.comment)
    
    def print(self):
        ops = ', '.join(op.print() for op in self.operands)
        s = f"{self.mnemonic:<8} {ops}"
        if self.comment:
            s += f" ; {self.comment:<10}"
        
        return s

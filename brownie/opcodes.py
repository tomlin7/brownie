import json
from dataclasses import dataclass
from typing import Literal


@dataclass
class Operand:
    immediate: bool
    name: str
    bytes: int = None
    value: int = None
    adjust: Literal["+", "-"] = None

    def copy(self, value):
        return Operand(immediate=self.immediate, name=self.name,
            bytes=self.bytes, value=value, adjust=self.adjust)
    
    def print(self):
        adjust = self.adjust or ""
        v = (hex(self.value) if self.bytes else self.value) if self.value else self.name
        v = v + adjust
        
        if self.immediate:
            return v
        return f"({v})"


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


def load_opcodes(opcode_file):
    instructions = []
    with open(opcode_file) as f:
        opcodes = json.load(f)
        
        for kind in opcodes.values():
            codes = []
            for opcode, details in kind.items():
                details.pop('flags', None)

                operands = []
                for op in details['operands']:
                    if incr := op.pop('increment', False):
                        op['adjust'] = '+' if incr else '-'
                    if decr := op.pop('decrement', False):
                        op['adjust'] = '-' if decr else '+'
                    operands.append(Operand(**op))
                details['operands'] = operands
                
                instruction = Instruction(int(opcode, base=16), **details)
                codes.append(instruction)
            instructions.append(codes)
    
    return instructions

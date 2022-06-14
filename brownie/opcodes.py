import json

from .instruction import Instruction
from .operand import Operand


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

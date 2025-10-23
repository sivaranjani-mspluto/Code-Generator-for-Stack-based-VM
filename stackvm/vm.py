from typing import List, Any, Tuple, Optional, Dict, Union
from .opcodes import OpCode

class VM:
    """
    A simple stack-based virtual machine.
    
    This VM executes bytecode instructions on a stack. Each operation
    manipulates the stack in some way, making it easy to implement
    and understand.
    """
    
    def __init__(self, memory_size: int = 1024):
        """Initialize the VM with empty stack, memory, and program counter."""
        self.stack: List[Any] = []
        self.memory: Dict[int, Any] = {}
        self.pc: int = 0  # Program counter
        self.running: bool = False
        self.memory_size = memory_size
        
        # Store return addresses for function calls
        self.call_stack: List[int] = []
        
        # Instruction handlers mapped to opcodes
        self.handlers = {
            OpCode.PUSH: self._push,
            OpCode.POP: self._pop,
            OpCode.ADD: self._add,
            OpCode.SUB: self._sub,
            OpCode.MUL: self._mul,
            OpCode.DIV: self._div,
            OpCode.PRINT: self._print,
            OpCode.HALT: self._halt,
            OpCode.JMP: self._jump,
            OpCode.JZ: self._jump_if_zero,
            OpCode.JNZ: self._jump_if_not_zero,
            OpCode.CALL: self._call,
            OpCode.RET: self._ret,
            OpCode.LOAD: self._load,
            OpCode.STORE: self._store,
            OpCode.DUP: self._dup,
            OpCode.SWAP: self._swap,
            OpCode.EQ: self._eq,
            OpCode.NEQ: self._neq,
            OpCode.LT: self._lt,
            OpCode.GT: self._gt,
            OpCode.AND: self._and,
            OpCode.OR: self._or,
            OpCode.NOT: self._not,
        }
    
    def reset(self) -> None:
        """Reset the VM to its initial state."""
        self.stack.clear()
        self.memory.clear()
        self.pc = 0
        self.running = False
        self.call_stack.clear()
    
    def execute(self, bytecode: List[Union[OpCode, Any]]) -> Any:
        """
        Execute the given bytecode.
        
        Args:
            bytecode: List of instructions and their operands
            
        Returns:
            The top value on the stack after execution, or None if the stack is empty
        """
        self.reset()
        self.bytecode = bytecode
        self.running = True
        
        while self.running and self.pc < len(self.bytecode):
            instruction = self.bytecode[self.pc]
            
            if isinstance(instruction, OpCode):
                # Simple operation with no operand
                handler = self.handlers.get(instruction)
                if handler is None:
                    raise RuntimeError(f"Unknown opcode: {instruction}")
                handler()
                self.pc += 1
            else:
                # Operation with operand
                opcode = instruction[0]
                operand = instruction[1] if len(instruction) > 1 else None
                
                if opcode not in self.handlers:
                    raise RuntimeError(f"Unknown opcode: {opcode}")
                    
                if opcode == OpCode.PUSH:
                    self._push(operand)
                elif opcode == OpCode.JMP:
                    self._jump(operand)
                    continue  # Don't increment PC, jump sets it
                elif opcode == OpCode.JZ:
                    if self._jump_if_zero(operand):
                        continue  # Jump happened, don't increment PC
                elif opcode == OpCode.JNZ:
                    if self._jump_if_not_zero(operand):
                        continue  # Jump happened, don't increment PC
                elif opcode == OpCode.CALL:
                    self._call(operand)
                    continue  # Don't increment PC, call sets it
                elif opcode == OpCode.LOAD:
                    self._load(operand)
                elif opcode == OpCode.STORE:
                    self._store(operand)
                else:
                    raise RuntimeError(f"Unhandled opcode with operand: {opcode}")
                
                self.pc += 1
        
        return self.stack[-1] if self.stack else None
    
    # Stack operations
    def _push(self, value: Any) -> None:
        """Push a value onto the stack."""
        self.stack.append(value)
    
    def _pop(self) -> Any:
        """Pop a value from the stack."""
        if not self.stack:
            raise RuntimeError("Stack underflow")
        return self.stack.pop()
    
    def _dup(self) -> None:
        """Duplicate the top value on the stack."""
        if not self.stack:
            raise RuntimeError("Stack underflow")
        self.stack.append(self.stack[-1])
    
    def _swap(self) -> None:
        """Swap the top two values on the stack."""
        if len(self.stack) < 2:
            raise RuntimeError("Not enough values on stack to swap")
        self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]
    
    # Arithmetic operations
    def _add(self) -> None:
        """Add the top two values on the stack."""
        b = self._pop()
        a = self._pop()
        self.stack.append(a + b)
    
    def _sub(self) -> None:
        """Subtract the top value from the second value on the stack."""
        b = self._pop()
        a = self._pop()
        self.stack.append(a - b)
    
    def _mul(self) -> None:
        """Multiply the top two values on the stack."""
        b = self._pop()
        a = self._pop()
        self.stack.append(a * b)
    
    def _div(self) -> None:
        """Divide the second value by the top value on the stack."""
        b = self._pop()
        a = self._pop()
        if b == 0:
            raise ZeroDivisionError("Division by zero")
        self.stack.append(a // b)  # Integer division
    
    # Comparison operations
    def _eq(self) -> None:
        """Check if the top two values are equal."""
        b = self._pop()
        a = self._pop()
        self.stack.append(1 if a == b else 0)
    
    def _neq(self) -> None:
        """Check if the top two values are not equal."""
        b = self._pop()
        a = self._pop()
        self.stack.append(1 if a != b else 0)
    
    def _lt(self) -> None:
        """Check if the second value is less than the top value."""
        b = self._pop()
        a = self._pop()
        self.stack.append(1 if a < b else 0)
    
    def _gt(self) -> None:
        """Check if the second value is greater than the top value."""
        b = self._pop()
        a = self._pop()
        self.stack.append(1 if a > b else 0)
    
    # Logical operations
    def _and(self) -> None:
        """Logical AND of the top two values on the stack."""
        b = self._pop()
        a = self._pop()
        self.stack.append(1 if a and b else 0)
    
    def _or(self) -> None:
        """Logical OR of the top two values on the stack."""
        b = self._pop()
        a = self._pop()
        self.stack.append(1 if a or b else 0)
    
    def _not(self) -> None:
        """Logical NOT of the top value on the stack."""
        a = self._pop()
        self.stack.append(0 if a else 1)
    
    # Control flow
    def _jump(self, target: int) -> None:
        """Jump to the specified instruction."""
        self.pc = target
    
    def _jump_if_zero(self, target: int) -> bool:
        """Jump to the specified instruction if the top of the stack is zero."""
        if not self.stack:
            raise RuntimeError("Stack underflow")
        if self.stack[-1] == 0:
            self.pc = target
            return True
        return False
    
    def _jump_if_not_zero(self, target: int) -> bool:
        """Jump to the specified instruction if the top of the stack is not zero."""
        if not self.stack:
            raise RuntimeError("Stack underflow")
        if self.stack[-1] != 0:
            self.pc = target
            return True
        return False
    
    def _call(self, target: int) -> None:
        """Call a subroutine at the specified address."""
        self.call_stack.append(self.pc + 1)  # Save return address (next instruction)
        self.pc = target
    
    def _ret(self) -> None:
        """Return from a subroutine."""
        if not self.call_stack:
            raise RuntimeError("Call stack underflow")
        self.pc = self.call_stack.pop()
    
    # Memory operations
    def _load(self, address: int) -> None:
        """Load a value from memory onto the stack."""
        if address < 0 or address >= self.memory_size:
            raise IndexError(f"Memory address out of bounds: {address}")
        self.stack.append(self.memory.get(address, 0))
    
    def _store(self, address: int) -> None:
        """Store the top value from the stack into memory."""
        if address < 0 or address >= self.memory_size:
            raise IndexError(f"Memory address out of bounds: {address}")
        if not self.stack:
            raise RuntimeError("Stack underflow")
        self.memory[address] = self._pop()
    
    # I/O operations
    def _print(self) -> None:
        """Print the top value on the stack."""
        if not self.stack:
            raise RuntimeError("Stack underflow")
        print(f"Output: {self.stack[-1]}")
    
    def _halt(self) -> None:
        """Stop execution."""
        self.running = False

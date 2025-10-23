from typing import List, Union, Tuple, Any, Dict, Optional
from .opcodes import OpCode, OPCODE_MAP

class CodeGenerator:
    """
    A code generator that converts high-level operations into bytecode
    for the stack-based VM.
    
    This class provides methods to generate bytecode for common operations
    and control structures, making it easier to write programs for the VM.
    """
    
    def __init__(self):
        """Initialize the code generator with an empty program."""
        self.program: List[Union[OpCode, Tuple[OpCode, Any]]] = []
        self.labels: Dict[str, int] = {}
        self.forward_refs: Dict[str, List[int]] = {}
    
    def reset(self) -> None:
        """Reset the code generator to its initial state."""
        self.program.clear()
        self.labels.clear()
        self.forward_refs.clear()
    
    def emit(self, opcode: Union[OpCode, str], operand: Any = None) -> 'CodeGenerator':
        """
        Emit a single instruction to the program.
        
        Args:
            opcode: The operation code or its string representation
            operand: Optional operand for the instruction
            
        Returns:
            self for method chaining
        """
        if isinstance(opcode, str):
            opcode = OPCODE_MAP[opcode.lower()]
        
        if operand is not None:
            self.program.append((opcode, operand))
        else:
            self.program.append(opcode)
            
        return self
    
    def label(self, name: str) -> 'CodeGenerator':
        """
        Define a label at the current position.
        
        Args:
            name: The name of the label
            
        Returns:
            self for method chaining
        """
        # Check if there are any forward references to this label
        if name in self.forward_refs:
            # Update all forward references with the current position
            for addr in self.forward_refs[name]:
                # Replace the placeholder with the actual address
                op, _ = self.program[addr]
                self.program[addr] = (op, len(self.program))
            # Remove the forward reference
            del self.forward_refs[name]
        
        # Record the label's position
        self.labels[name] = len(self.program)
        return self
    
    def jump(self, target: str) -> 'CodeGenerator':
        """
        Emit an unconditional jump to a label.
        
        Args:
            target: The name of the target label
            
        Returns:
            self for method chaining
        """
        return self.emit(OpCode.JMP, target)
    
    def jump_if_zero(self, target: str) -> 'CodeGenerator':
        """
        Emit a conditional jump that jumps if the top of the stack is zero.
        
        Args:
            target: The name of the target label
            
        Returns:
            self for method chaining
        """
        return self.emit(OpCode.JZ, target)
    
    def jump_if_not_zero(self, target: str) -> 'CodeGenerator':
        """
        Emit a conditional jump that jumps if the top of the stack is not zero.
        
        Args:
            target: The name of the target label
            
        Returns:
            self for method chaining
        """
        return self.emit(OpCode.JNZ, target)
    
    def call(self, target: str) -> 'CodeGenerator':
        """
        Emit a subroutine call to a label.
        
        Args:
            target: The name of the target label
            
        Returns:
            self for method chaining
        """
        return self.emit(OpCode.CALL, target)
    
    def ret(self) -> 'CodeGenerator':
        """
        Emit a return from subroutine instruction.
        
        Returns:
            self for method chaining
        """
        return self.emit(OpCode.RET)
    
    def push(self, value: Any) -> 'CodeGenerator':
        """
        Emit a push instruction with the given value.
        
        Args:
            value: The value to push onto the stack
            
        Returns:
            self for method chaining
        """
        return self.emit(OpCode.PUSH, value)
    
    def pop(self) -> 'CodeGenerator':
        """
        Emit a pop instruction.
        
        Returns:
            self for method chaining
        """
        return self.emit(OpCode.POP)
    
    def add(self) -> 'CodeGenerator':
        """Emit an add instruction."""
        return self.emit(OpCode.ADD)
    
    def sub(self) -> 'CodeGenerator':
        """Emit a subtract instruction."""
        return self.emit(OpCode.SUB)
    
    def mul(self) -> 'CodeGenerator':
        """Emit a multiply instruction."""
        return self.emit(OpCode.MUL)
    
    def div(self) -> 'CodeGenerator':
        """Emit a divide instruction."""
        return self.emit(OpCode.DIV)
    
    def eq(self) -> 'CodeGenerator':
        """Emit an equality comparison instruction."""
        return self.emit(OpCode.EQ)
    
    def neq(self) -> 'CodeGenerator':
        """Emit a not-equal comparison instruction."""
        return self.emit(OpCode.NEQ)
    
    def lt(self) -> 'CodeGenerator':
        """Emit a less-than comparison instruction."""
        return self.emit(OpCode.LT)
    
    def gt(self) -> 'CodeGenerator':
        """Emit a greater-than comparison instruction."""
        return self.emit(OpCode.GT)
    
    def and_(self) -> 'CodeGenerator':
        """Emit a logical AND instruction."""
        return self.emit(OpCode.AND)
    
    def or_(self) -> 'CodeGenerator':
        """Emit a logical OR instruction."""
        return self.emit(OpCode.OR)
    
    def not_(self) -> 'CodeGenerator':
        """Emit a logical NOT instruction."""
        return self.emit(OpCode.NOT)
    
    def dup(self) -> 'CodeGenerator':
        """Emit a duplicate top of stack instruction."""
        return self.emit(OpCode.DUP)
    
    def swap(self) -> 'CodeGenerator':
        """Emit a swap top two stack elements instruction."""
        return self.emit(OpCode.SWAP)
    
    def load(self, address: int) -> 'CodeGenerator':
        """
        Emit a load from memory instruction.
        
        Args:
            address: Memory address to load from
            
        Returns:
            self for method chaining
        """
        return self.emit(OpCode.LOAD, address)
    
    def store(self, address: int) -> 'CodeGenerator':
        """
        Emit a store to memory instruction.
        
        Args:
            address: Memory address to store to
            
        Returns:
            self for method chaining
        """
        return self.emit(OpCode.STORE, address)
    
    def print_(self) -> 'CodeGenerator':
        """Emit a print instruction."""
        return self.emit(OpCode.PRINT)
    
    def halt(self) -> 'CodeGenerator':
        """Emit a halt instruction."""
        return self.emit(OpCode.HALT)
    
    def generate(self) -> List[Union[OpCode, Tuple[OpCode, Any]]]:
        """
        Generate the final bytecode with all labels resolved.
        
        Returns:
            The generated bytecode
            
        Raises:
            ValueError: If there are unresolved forward references
        """
        # Check for unresolved forward references
        if self.forward_refs:
            raise ValueError(f"Unresolved forward references: {', '.join(self.forward_refs.keys())}")
        
        # Process the program to resolve labels
        resolved_program = []
        
        for instruction in self.program:
            if isinstance(instruction, tuple):
                opcode, operand = instruction
                
                # Check if the operand is a label reference
                if isinstance(operand, str):
                    if operand in self.labels:
                        # Replace label with its address
                        resolved_program.append((opcode, self.labels[operand]))
                    else:
                        # This should not happen if we've processed all forward refs
                        raise ValueError(f"Unknown label: {operand}")
                else:
                    resolved_program.append(instruction)
            else:
                resolved_program.append(instruction)
        
        return resolved_program
    
    def assemble(self, source: str) -> List[Union[OpCode, Tuple[OpCode, Any]]]:
        """
        Assemble source code into bytecode.
        
        This is a simple assembler that parses a text representation
        of the program into bytecode.
        
        Args:
            source: The source code to assemble
            
        Returns:
            The generated bytecode
        """
        self.reset()
        
        # First pass: collect labels
        for line_num, line in enumerate(source.split('\n'), 1):
            line = line.strip()
            if not line or line.startswith(';'):
                continue  # Skip empty lines and comments
                
            if line.endswith(':'):
                # This is a label definition
                label = line[:-1].strip()
                self.label(label)
            else:
                # This is an instruction
                parts = line.split()
                opcode = parts[0].upper()
                
                # Handle instructions that take a label as an operand
                if opcode in ('JMP', 'JZ', 'JNZ', 'CALL') and len(parts) > 1:
                    # This is a label reference, we'll resolve it later
                    pass
                
                # Add the instruction to the program
                if len(parts) > 1:
                    # Try to convert the operand to an integer if possible
                    try:
                        operand = int(parts[1])
                        self.emit(opcode, operand)
                    except ValueError:
                        # If it's not an integer, treat it as a string (label)
                        self.emit(opcode, parts[1])
                else:
                    self.emit(opcode)
        
        # Second pass: resolve labels and generate bytecode
        return self.generate()
    
    def dump(self) -> str:
        """
        Generate a human-readable disassembly of the program.
        
        Returns:
            A string containing the disassembled program
        """
        result = []
        
        # Create a reverse mapping of addresses to labels
        addr_to_label = {addr: name for name, addr in self.labels.items()}
        
        for i, instruction in enumerate(self.program):
            # Add label if this address has one
            if i in addr_to_label:
                result.append(f"{addr_to_label[i]}:")
            
            if isinstance(instruction, tuple):
                opcode, operand = instruction
                result.append(f"  {i:04d}: {opcode.name:<8} {operand}")
            else:
                result.append(f"  {i:04d}: {instruction.name}")
        
        return '\n'.join(result)

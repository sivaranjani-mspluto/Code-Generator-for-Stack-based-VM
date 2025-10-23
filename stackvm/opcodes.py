from enum import Enum, auto

class OpCode(Enum):
    """Operation codes for the stack-based VM."""
    # Stack operations
    PUSH = auto()    # Push value onto stack
    POP = auto()     # Remove top value from stack
    DUP = auto()     # Duplicate top stack value
    SWAP = auto()    # Swap top two stack values
    
    # Arithmetic operations
    ADD = auto()     # Add top two values
    SUB = auto()     # Subtract top value from second value
    MUL = auto()     # Multiply top two values
    DIV = auto()     # Divide second value by top value
    MOD = auto()     # Modulo of second value by top value
    
    # Comparison operations
    EQ = auto()      # Equal to
    NEQ = auto()     # Not equal to
    LT = auto()      # Less than
    GT = auto()      # Greater than
    LTE = auto()     # Less than or equal to
    GTE = auto()     # Greater than or equal to
    
    # Control flow
    JMP = auto()     # Unconditional jump
    JZ = auto()      # Jump if zero
    JNZ = auto()     # Jump if not zero
    CALL = auto()    # Call subroutine
    RET = auto()     # Return from subroutine
    HALT = auto()    # Stop execution
    
    # I/O operations
    PRINT = auto()   # Print top of stack
    READ = auto()    # Read input to stack
    
    # Memory operations
    LOAD = auto()    # Load from memory
    STORE = auto()   # Store to memory
    
    # Logical operations
    AND = auto()     # Logical AND
    OR = auto()      # Logical OR
    NOT = auto()     # Logical NOT
    
    def __str__(self):
        return self.name

# Map operation names to their corresponding opcodes
OPCODE_MAP = {opcode.name.lower(): opcode for opcode in OpCode}

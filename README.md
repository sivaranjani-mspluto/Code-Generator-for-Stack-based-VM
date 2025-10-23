# StackVM Code Generator

A minimal stack-based virtual machine with a code generator, demonstrating how efficient code generation can contribute to SDG 8: Decent Work and Economic Growth.

## Overview

This project implements a simple stack-based virtual machine (VM) with a code generator that can convert high-level operations into efficient bytecode. The VM demonstrates how optimized code generation can lead to better performance and resource utilization, contributing to economic growth through more efficient computing.

## Features

- Simple stack-based VM implementation
- Bytecode generator
- Example programs
- Test suite
- Clear documentation

## How it Relates to SDG 8

SDG 8 aims to promote sustained, inclusive, and sustainable economic growth. This project contributes by:
- Demonstrating efficient computing techniques that reduce computational costs
- Providing educational value in compiler and VM design
- Enabling more efficient software that can run on resource-constrained devices
- Potentially reducing energy consumption through optimized code execution

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/stackvm-generator.git
cd stackvm-generator

# Install dependencies
pip install -r requirements.txt
```

## Usage

```python
from stackvm import VM, CodeGenerator

# Create a new VM instance
vm = VM()

# Create a code generator
gen = CodeGenerator()

# Generate some bytecode
bytecode = gen.generate([
    ('PUSH', 10),
    ('PUSH', 20),
    ('ADD',),
])

# Run the bytecode
result = vm.execute(bytecode)
print(f"Result: {result}")
```

## Project Structure

- `stackvm/` - Main package
  - `__init__.py` - Package initialization
  - `vm.py` - Virtual machine implementation
  - `codegen.py` - Code generator implementation
  - `opcodes.py` - Bytecode operation codes
- `examples/` - Example programs
- `tests/` - Unit tests
- `requirements.txt` - Python dependencies


## EXECUTING
# Arithmetic example 
```bash
python -m examples.arithmetic.py
```
#OUTPUT
```bash
Generated program:
  0000: PUSH     10
  0001: PUSH     20
  0002: ADD
  0003: PUSH     3
  0004: MUL
  0005: PUSH     5
  0006: SUB
  0007: PRINT
  0008: HALT

Executing program...
Output: 85
Final result: 85
```
# Fibonacci example
```bash
python -m examples.fibonacci
```
#OUTPUT
```bash
Generated program:
  0000: PUSH     10
  0001: STORE    0
  0002: PUSH     0
  0003: STORE    1
  0004: PUSH     1
  0005: STORE    2
  0006: PUSH     0
  0007: STORE    3
  0008: PUSH     10
  0009: PRINT
  0010: PUSH     70
  0011: PRINT
  0012: PUSH     105
  0013: PRINT
  0014: PUSH     98
  0015: PRINT
  0016: PUSH     111
  0017: PRINT
  0018: PUSH     110
  0019: PRINT
  0020: PUSH     97
  0021: PRINT
  0022: PUSH     99
  0023: PRINT
  0024: PUSH     99
  0025: PRINT
  0026: PUSH     105
  0027: PRINT
  0028: PUSH     32
  0029: PRINT
  0030: PUSH     83
  0031: PRINT
  0032: PUSH     101
  0033: PRINT
  0034: PUSH     113
  0035: PRINT
  0036: PUSH     117
  0037: PRINT
  0038: PUSH     101
  0039: PRINT
  0040: PUSH     110
  0041: PRINT
  0042: PUSH     99
  0043: PRINT
  0044: PUSH     101
  0045: PRINT
  0046: PUSH     58
  0047: PRINT
  0048: PUSH     10
  0049: PRINT
  0050: LOAD     1
  0051: PRINT
  0052: PUSH     32
  0053: PRINT
  0054: LOAD     2
  0055: PRINT
  0056: PUSH     32
  0057: PRINT
loop:
  0058: LOAD     3
  0059: LOAD     0
  0060: PUSH     2
  0061: SUB
  0062: LT
  0063: JZ       end
  0064: LOAD     1
  0065: LOAD     2
  0066: ADD
  0067: STORE    4
  0068: LOAD     4
  0069: PRINT
  0070: PUSH     32
  0071: PRINT
  0072: LOAD     2
  0073: STORE    1
  0074: LOAD     4
  0075: STORE    2
  0076: LOAD     3
  0077: PUSH     1
  0078: ADD
  0079: STORE    3
  0080: JMP      loop
end:
  0081: PUSH     10
  0082: PRINT
  0083: HALT

Executing program...

Output: 10
Output: 70
Output: 105
Output: 98
Output: 111
Output: 110
Output: 97
Output: 99
Output: 99
Output: 105
Output: 32
Output: 83
Output: 101
Output: 113
Output: 117
Output: 101
Output: 110
Output: 99
Output: 101
Output: 58
Output: 10
Output: 0
Output: 32
Output: 1
Output: 32
Output: 1
Output: 32
Output: 2
Output: 32
Output: 3
Output: 32
Output: 5
Output: 32
Output: 8
Output: 32
Output: 13
Output: 32
Output: 21
Output: 32
Output: 34
Output: 32
Output: 10
```
## License

MIT

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

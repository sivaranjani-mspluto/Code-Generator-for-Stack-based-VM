"""
StackVM - A simple stack-based virtual machine with code generation.

This module provides a stack-based virtual machine and code generator
designed to demonstrate efficient code execution and its impact on
sustainable economic growth (SDG 8).
"""

from .vm import VM
from .codegen import CodeGenerator
from .opcodes import OpCode

__version__ = '0.1.0'
__all__ = ['VM', 'CodeGenerator', 'OpCode']

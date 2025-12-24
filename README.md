# Useful links

Site (Sandbox, Docs and Blog): https://rr-roadmap.onrender.com/#/

# RR — R Interpreter on RPython / PyPy Toolchain

RR is an interpreter for a dialect of R, implemented using the RPython framework (the same toolchain behind PyPy).  
The main goal of RR is to enable **native integration of Python calls from within R code**, allowing a seamless bridge between R and Python environments.

## Motivation

While there are tools that connect R and Python at the process or inter‑language binding level, RR aims to go one step further: by compiling a custom R interpreter via RPython, we get a unified runtime where:

- R code executes under a VM that we fully control;  
- Python calls can be embedded directly in R code and executed natively;  
- data types and control flow can be handled in a unified fashion, enabling powerful interop and optimizations.

## Features (planned / partial)

- Bytecode-based interpreter for R-like language structure (variables, arithmetic, control flow, etc.).  
- Support for Python interop: ability to call Python functions and integrate results seamlessly.   
- Written in RPython, so can be translated into a native executable using the PyPy toolchain — trading implementation productivity for performance.

## Use Cases

- Experimentation: writing R code that leverages Python libraries without leaving the R-like syntax.  
- Prototyping language features, embedding Python logic inside R scripts.  
- Learning: understanding interpreter internals, bytecode, bridging two languages in a single runtime.

## Status & Limitations

RR is currently **work-in-progress**, and not intended yet for production usage. Some opcodes and language features might be missing or unstable.  
Since RR is built on RPython, the implementation must respect its restrictions (e.g. limited dynamic features, static typing constraints).  
Nevertheless, RR offers an interesting platform for experimenting with mixed R/Python execution semantics.


# TUSCA Simulator
## Introduction
This is the final project made for the subject "Organization and Architecture of Computers", a simple game written in assembly (described below) from scratch by:

- Gabriel Cazinni Cardoso
- Gabriel Franceschi Libardi
- Lucas Eduardo Gulka Pulcinelli
- Matheus Pereira Dias

## The assembly language used
The whole project is written in an assembly language made entirely by the Institute of Mathematical and Computer Sciences from the University of São Paulo. The source is in [this repository](https://github.com/simoesusp/Processador-ICMC).

## How to compile and run the program
You should have a bin/ directory with two programs: "montador" and "sim", one is the assembler for the architecture and the other is an emulator. Both should be compiled from the above repository (you can also change the variables MONTADOR and SIM via command line during the invocation of "make")

The program can be compiled by using "make" and run by using "make run". The full assembly source code is concatenated in a single file in build/full.asm (because the assembler only supports a single input file.

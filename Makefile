MONTADOR ?= bin/montador
SIM ?= bin/sim

ASMFILES = $(shell find src -type f)

CHARMAP = charmap.mif
BOOTSTRAPPER = bootstrapper.asm
FULL_ASM = build/full.asm
MIF_OUT = build/game.mif


.PHONY: all clean run

all: $(MIF_OUT)

clean:
	@rm -rf build

run: $(MIF_OUT) $(CHARMAP)
	@$(SIM) $(MIF_OUT) $(CHARMAP)


$(MIF_OUT): $(FULL_ASM)
	@mkdir -p build
	@$(MONTADOR) $< $@

$(FULL_ASM): $(BOOTSTRAPPER) $(ASMFILES)
	@mkdir -p build
	@cat $^ > $@


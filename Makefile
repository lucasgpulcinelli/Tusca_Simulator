MONTADOR ?= bin/montador
SIM ?= bin/sim


CHARMAP = res/charmap/charmap.mif
BOOTSTRAPPER = src/bootstrapper.asm
FULL_ASM = build/full.asm
MIF_OUT = build/game.mif

ASMFILES = $(filter-out $(BOOTSTRAPPER),$(shell find src -type f))


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


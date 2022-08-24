MONTADOR ?= bin/montador
SIM ?= bin/sim
PREPROCESSOR ?= bin/preprocessor.py


CHARMAP = res/charmap/charmap.mif
USER_DEFS = res/user_defs.json
CHARMAP_JSON = res/charmap/charmap.json
BOOTSTRAPPER = src/bootstrapper.asm
FULL_ASM = build/full.asm
FULL_PREP = build/fullprep.asm
MIF_OUT = build/game.mif

ASMFILES = $(filter-out $(BOOTSTRAPPER),$(shell find src -type f))


.PHONY: all clean run

all: $(MIF_OUT)

clean:
	@rm -rf build

run: $(MIF_OUT) $(CHARMAP)
	@$(SIM) $(MIF_OUT) $(CHARMAP)


$(MIF_OUT): $(FULL_PREP)
	@mkdir -p build
	@$(MONTADOR) $< $@

$(FULL_PREP): $(FULL_ASM) $(CHARMAP_JSON) $(USER_DEFS)
	@$(PREPROCESSOR) $(CHARMAP_JSON) $(USER_DEFS) $< $@

$(FULL_ASM): $(BOOTSTRAPPER) $(ASMFILES)
	@mkdir -p build
	@cat $^ > $@


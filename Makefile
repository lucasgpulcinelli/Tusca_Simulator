MONTADOR ?= bin/montador
SIM ?= bin/sim
PREPROCESSOR ?= bin/preprocessor.py
VARS_PROCESSOR ?= bin/variaveis.py


CHARMAP = res/charmap/charmap.mif
CHARMAP_JSON = res/charmap/charmap.json
BOOTSTRAPPER = src/bootstrapper.asm
FULL_ASM = build/full.asm
FULL_PREP = build/fullprep.asm
MIF_OUT = build/game.mif
VARS_ASM = build/all_vars.asm
VARS_ALL = build/all_vars.vars

VARS_FILES = $(shell find src -type f | grep "\.vars")
ASMFILES = $(filter-out $(BOOTSTRAPPER),$(shell find src -type f | grep "\.asm"))


.PHONY: all clean run

all: $(MIF_OUT)

clean:
	@rm -rf build

run: $(MIF_OUT) $(CHARMAP)
	$(SIM) $(MIF_OUT) $(CHARMAP)


$(MIF_OUT): $(FULL_PREP)
	@mkdir -p build
	$(MONTADOR) $< $@

$(FULL_PREP): $(FULL_ASM) $(CHARMAP_JSON)
	$(PREPROCESSOR) $(CHARMAP_JSON) $< $@

$(VARS_ALL): $(VARS_FILES)
	@mkdir -p build
	cat $^ > $@

$(VARS_ASM): $(VARS_ALL)
	@mkdir -p build
	$(VARS_PROCESSOR) $< $@


$(FULL_ASM): $(BOOTSTRAPPER) $(VARS_ASM) $(ASMFILES)
	@mkdir -p build
	cat $^ > $@


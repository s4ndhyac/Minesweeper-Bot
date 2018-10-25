# ==============================CS-199==================================
# FILE:			Makefile
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains useful commands for this project. You
#				may use the following commands:
#				
#				- "make" 			- compiles the project and places the
#									  python bytecode files in the bin
#									  folder
#			
#				- "make submission" - creates the zip file that you will
#									  submit
#
# NOTES: 		- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

RAW_SOURCES = \
	Action.py\
	AI.py\
	Main.py\
	ManualAI.py\
	MyAI.py\
	RandomAI.py\
	World.py


SOURCE_DIR = src
BIN_DIR = bin
DOC_DIR = doc
SOURCES = $(foreach s, $(RAW_SOURCES), $(SOURCE_DIR)/$(s))

all: $(SOURCES)
	@-eval `'/usr/bin/tclsh' '/pkg/modules/modulecmd.tcl' 'bash' load python/3.5.2` ; \
	 if hash python3 &> /dev/null ; \
	 then \
		python3 -m compileall -q src ; \
	 else \
		python -m compileall -q src ; \
	 fi
	@rm -rf $(BIN_DIR)
	@mkdir -p $(BIN_DIR)
	@mkdir -p $(DOC_DIR)
	@cp -a src/__pycache__/. bin
	@for file in bin/* ; \
	do \
		mv -f $$file $${file%%.*}.pyc; \
	done
	@rm -rf src/__pycache__/

submission: all
	@rm -f *.zip
	@echo ""
	@read -p "Enter Team Name (No spaces, '_', '/', '*'): " teamName; \
	 echo ""; \
	 zip -rqq s_$${teamName}.zip $(SOURCE_DIR) $(BIN_DIR) $(DOC_DIR)

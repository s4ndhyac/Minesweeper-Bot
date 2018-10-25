# ======================================================================
# FILE:        Makefile
#
# AUTHOR:      John Lu
#
# DESCRIPTION: This file contains useful commands for this project. You
#              may use the following commands:
#
#              - make            - compiles the code the src/ folder and
#								   creates executable jar file, mine.jar
#
#              - make submission - creates the the submission zip, you will
#                                  submit.
#			   
#			   - make clean      - removes .class files from src/ and 
#								   mine.jar executable
#
#              - DO NOT change this file.
# ======================================================================


compile:
	@echo "cleaning directory.."
	@make clean
	@echo "compiling src.."
	@javac -classpath ".:jars/*" -Xlint:unchecked src/*.java 
	@echo "creating executable jar file.."
	@jar cvfm mine.jar manifest.txt src/*.class > /dev/null
	@mkdir bin doc
	@mv src/*.class bin
	@mv mine.jar bin
	@cp -r jars bin
	@echo 'complete.'

submission:
	@echo "cleaning..."; make clean
	@echo "recompiling..."; make compile
	@rm -f *.zip
	@echo ""
	@read -p "Enter Last Name: " lastName; \
	 echo ""; \
	 read -p "Enter Student ID Number: " idNumber; \
	 echo ""; \
	 read -p "Enter Team Name: " teamName; \
	 echo "zipping src/ and mine.jar"; \
	 zip -rqq $${lastName}_$${idNumber}_$${teamName}.zip src mine.jar
	@echo "Done."

clean:
	rm -rf bin doc *.zip

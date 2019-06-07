test: new_test.mdl lex.py main.py matrix.py mdl.py display.py draw.py gmath.py yacc.py
	python main.py new_test.mdl

clean:
	rm *pyc *out parsetab.py

clear:
	rm *pyc *out parsetab.py *ppm

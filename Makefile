.PHONY: verifica libro clean pulisci

verifica:
	python3 scripts/verifica_cantiere.py

libro: verifica
	mkdir -p build
	cd latex && latex -interaction=nonstopmode -halt-on-error -output-directory=../build SA_Book.tex
	cd latex && latex -interaction=nonstopmode -halt-on-error -output-directory=../build SA_Book.tex
	dvips -o build/SA_Book.ps build/SA_Book.dvi
	ps2pdf -dALLOWPSTRANSPARENCY build/SA_Book.ps build/SA_Book.pdf

clean pulisci:
	rm -rf build


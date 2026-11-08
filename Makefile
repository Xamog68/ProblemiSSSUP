.PHONY: verifica libro clean pulisci sito-check sito-aggiorna sito-ricostruisci

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

# Controlla l'allineamento senza modificare nulla.
sito-check:
	python3 scripts/sito_check.py

# Aggiorna solo le conversioni obsolete o mancanti.
sito-aggiorna: verifica
	python3 scripts/genera_dati_sito.py

# Ricostruisce tutte le conversioni.
sito-ricostruisci: verifica
	python3 scripts/genera_dati_sito.py --force

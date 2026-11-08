# Makefile alternativo, senza toccare il Makefile storico del progetto.
# Dalla radice del repository:
#   make -f scripts/libro.mk libro
#   make -f scripts/libro.mk libro CAMPI=Testo,Aiutino ANNI=1996-2000,2025
#   make -f scripts/libro.mk libro CAMPI=Testo SITO=https://example.org/index.html
CAMPI ?= tutti
ANNI ?= tutti
SITO ?=
.PHONY: libro
libro:
	python3 scripts/compila_libro.py --campi "$(CAMPI)" --anni "$(ANNI)" $(if $(SITO),--sito "$(SITO)")

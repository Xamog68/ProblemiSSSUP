# Problemi di Matematica alla SSSUP

Cantiere per il recupero, la revisione e la futura pubblicazione dei problemi
di matematica delle prove di ammissione alla Scuola Superiore Sant'Anna.

Il materiale attualmente censito comprende 78 problemi dal 1996 al 2013:

- sei problemi per anno dal 1996 al 1998;
- quattro problemi per anno dal 1999 al 2013.

## Principio fondamentale

I file LaTeX in `contenuti/problemi/` sono la fonte canonica dei contenuti.
Libro, sito e altri prodotti futuri dovranno essere generati da questi file,
senza mantenere copie divergenti dei testi.

Ogni problema può contenere i campi:

- testo;
- risposta breve;
- aiutino;
- soluzione ufficiale;
- soluzioni alternative;
- osservazioni;
- commenti.

## Stato iniziale

Il cantiere nasce dalla fotografia storica `SA_Libro.zip`. Il suo checksum e
le regole di conservazione sono documentati in `fonti/README.md`.

I sorgenti, quasi interamente ASCII ma con ritorni di riga del vecchio Mac,
sono stati normalizzati in UTF-8 con terminatori LF. Non sono state effettuate
correzioni matematiche.

Il vecchio libro rimane riproducibile, per quanto possibile, tramite il master
in `latex/`. Usa PSTricks e la filiera LaTeX -> DVI -> PostScript -> PDF.

## Comandi

```sh
make verifica
make libro
```

`make verifica` richiede soltanto Python 3. `make libro` richiede una
distribuzione TeX dotata di PSTricks, `dvips` e `ps2pdf`.

## Avvertenza editoriale

La paternità complessiva del materiale e le condizioni di pubblicazione non
sono ancora documentate. Per questo motivo il cantiere non contiene per ora
una licenza di distribuzione.


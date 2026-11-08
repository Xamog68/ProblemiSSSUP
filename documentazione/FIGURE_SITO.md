# Figure del sito SSSUP: conversione SVG e lavori aperti

**Stato all'8 novembre 2026 (dopo il commit `e519325`):** i **156 disegni
PSTricks** individuati nei sorgenti sono stati convertiti con successo in
**156 SVG vettoriali** e inseriti nei punti corrispondenti del sito. La
conversione massiva sul Mac ha concluso con **156 SVG OK, zero errori e zero
figure non provate**. Il collaudo del sito ha contato 156 immagini collegate,
nessun segnaposto PSTricks residuo e 96 problemi tecnicamente allineati.

**Restano due figure esterne da ricostruire** nei problemi **2024.2**
(`squares.pdf`) e **2026.1**. Restano inoltre interventi estetici e verifiche
visive: una conversione riuscita non garantisce che le etichette siano ben
posizionate o che ogni figura sia matematicamente fedele all'originale.

La vecchia segnalazione di **31 problemi con figure incomplete** risale a prima
della conversione: comprendeva **29 problemi con PSTricks** e **2 problemi
con figure esterne mancanti**. Non descrive più la situazione attuale.

## Architettura

- **Fonte canonica:** `contenuti/problemi/SA_AAAA_N.tex`. I file canonici non
  sono stati modificati per la conversione web; PSTricks continua a essere
  usato dal libro PDF.
- **Generazione:** `scripts/genera_figure_svg_massivo.py` estrae le figure,
  conserva il contesto LaTeX necessario e usa `latex` e `dvisvgm` con supporto
  agli special `ps` (Ghostscript). Ogni figura viene elaborata separatamente,
  con timeout e log: il fallimento di una non interrompe le altre.
- **Area di lavoro locale:** `build/figure-svg/` contiene `inventario.json`,
  `inventario.csv`, `catalogo.html`, i log e le immagini sotto `svg/`.
  Questa directory non va versionata.
- **Installazione:** `scripts/installa_figure_svg.py` controlla completezza,
  corrispondenza degli identificativi, impronte del sorgente, XML SVG e assenza
  di immagini raster incorporate. Se il preflight non passa, non avvia la
  copia. Gli SVG installati e il loro `manifest.json` sono in
  `sito/assets/figure/` e sono versionati.
- **Collocazione nel sito:** `scripts/genera_dati_sito.py` associa ogni figura
  al proprio **problema, campo e numero progressivo**, inserendo nel dato web
  un riferimento al file SVG. Gli identificativi hanno la forma
  `SA_2004_4__SoluzioneUfficiale__03.svg`. La modifica di un sorgente
  invalida la sua impronta: non si deve usare silenziosamente un'immagine
  obsoleta.

Gli SVG sono realmente vettoriali: con `dvisvgm --no-fonts` anche i glifi
vengono convertiti in tracciati, evitando dipendenze dai font del lettore.
Non sono perciò necessariamente selezionabili come testo. Sul sito possono
essere aperti in una scheda per ingrandirli.

## Rigenerazione dopo una correzione LaTeX

Dalla radice di `ProblemiSSSUP/` (su un sistema con TeX, `dvisvgm` e supporto
Ghostscript attivo):

```sh
python3 scripts/genera_figure_svg_massivo.py
python3 scripts/installa_figure_svg.py
python3 scripts/installa_figure_svg.py --applica
python3 scripts/genera_dati_sito.py --sito sito
make sito-check
python3 scripts/installa_figure_svg.py --verifica-sito
git diff --check
```

Il primo comando riprende i risultati validi e rigenera le figure che
necessitano di aggiornamento; `--forza` permette di ripetere anche le
conversioni già riuscite. Per un caso circoscritto si possono usare
`--anno` e `--problema`; prima di una nuova installazione completa serve
comunque un inventario che copra **tutto** l'archivio. Il controllo
`--verifica-sito` richiede che l'inventario locale sia ancora disponibile.

Per ispezionare il catalogo:

```sh
open -a Firefox build/figure-svg/catalogo.html
```

Per provare la resa web senza pubblicare:

```sh
python3 -m http.server 8000 --directory sito
```

Il caricamento web e il libro derivano sempre dagli stessi sorgenti, ma
seguono filiere diverse: eventuali correzioni delle etichette nei disegni
vanno fatte e documentate nel LaTeX, non direttamente nell'SVG generato.

## Tabelle HTML, Sudoku e domino

Un primo inventario euristico ha individuato, fra i 156 PSTricks convertiti,
**20 possibili tabelle** e **5 possibili griglie HTML**. Per ora sono tutti
pubblicati come SVG: la classificazione **non** autorizza sostituzioni
automatiche. Esempi da valutare in futuro: scacchiere (1997.3), aule
(2002.2), torneo (2004.3), caselle numerate (2007.2).

Sono distinti dai 156 SVG i **31 Sudoku** e le **53 tessere del domino** che
il convertitore rappresenta già in HTML/MathJax.

## Figure esterne da ricostruire

Quando manca una figura esterna originale, conservare nel LaTeX il commento
sulla propria riga, nel punto previsto:

```latex
% SSSUP-FIGURA-DA-RICOSTRUIRE: squares.pdf
```

Il marcatore non altera la compilazione TeX e il convertitore web lo rende
come avviso; questo caso **non** viene risolto dal generatore PSTricks.
Gli originali restano documentati in `fonti-locali/`, fuori da Git. Quando
la figura verrà ricostruita nel sorgente canonico, rimuovere il marcatore,
rigenerare il sito ed eseguire i controlli.

## Controlli e limiti

- `make sito-check` verifica l'allineamento **tecnico** LaTeX/web.
- `python3 scripts/installa_figure_svg.py --verifica-sito` verifica
  separatamente la presenza e la collocazione delle **156 immagini**, se il
  catalogo locale esiste.
- Le etichette geometriche mal posizionate si osservano talvolta già nel PDF
  storico o ricompilato; non vanno attribuite automaticamente a SVG.
  Un possibile cambiamento di comportamento di `pst-eucl` è un'ipotesi da
  verificare, non una causa accertata.
- Il collaudo matematico, l'accessibilità e il confronto visivo esaustivo
  restano indipendenti dalla riuscita della conversione.

Vedere anche `SITO.md`, `SITO_CHECK.md` e `TODO.md`.

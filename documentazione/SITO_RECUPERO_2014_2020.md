# Sito: recupero dei problemi 2014–2020

## Obiettivo

Integrare nel sito i 20 testi canonici recuperati e già registrati in Git
(commit `f9417ed`), passando da 96 a 116 problemi. Gli anni 2014–2020
compaiono nell'indice con 3, 2, 3, 3, 3, 3 e 3 problemi.

Il progetto contiene già il convertitore LaTeX -> HTML e il generatore
PSTricks -> SVG. Questa integrazione aggiunge 20 titoli descrittivi a
`sito/dati/titoli.json`, senza riscrivere le pagine o i sorgenti canonici.

## Rigenerazione sul Mac

Dalla radice del repository, con `pandoc`, `latex`, `dvisvgm`, `dvips`
e `ps2pdf` già disponibili:

```sh
git status -sb
python3 scripts/genera_figure_svg_massivo.py
python3 scripts/installa_figure_svg.py
python3 scripts/installa_figure_svg.py --applica
python3 scripts/genera_dati_sito.py --sito sito
make sito-check
python3 scripts/installa_figure_svg.py --verifica-sito
git diff --check
```

Importante: eseguire **l'inventario SVG completo**, non una selezione con
`--anno`, perché l'installatore richiede il catalogo di *tutte* le figure.
Il generatore riutilizza le conversioni precedenti che sono ancora valide.

Sono attesi:

- 116 problemi canonici e 116 dati web allineati;
- 164 SVG, ossia i precedenti 160 piu' le quattro nuove figure;
- nessun PSTricks irrisolto e nessuna figura esterna pendente;
- 20 nuovi file web `sito/dati/problemi/201[4-9]_*.js` e `2020_*.js`;
- i sette anni 2014–2020 tutti disponibili nell'indice;
- nei nuovi problemi e' presente soltanto il campo Testo: non inventare
  Risposta, Aiutino, Soluzione o un'indicazione di provenienza AI.

Le quattro figure nuove, tutte nel campo `Testo`, sono:

- `SA_2015_2__Testo__01.svg` (simboli elettrici);
- `SA_2016_1__Testo__01.svg` (rastrelliere);
- `SA_2017_3__Testo__01.svg` (scacchiera);
- `SA_2020_1__Testo__01.svg` (albero).

## Controllo visivo locale

```sh
python3 -m http.server 8000 --directory sito
```

Aprire in Firefox `http://localhost:8000/` e verificare soprattutto gli anni
2015, 2016, 2017, 2020. I punti (a), (b), (c) devono essere numerati come
nel libro; le condizioni devono apparire come elenchi puntati.
Verificare le quattro immagini con zoom, il comportamento della navigazione,
le formule MathJax e l'assenza di messaggi «Disegno PSTricks non ancora
convertito».

## Consolidamento

Solo dopo i controlli visivi:

```sh
git add sito/dati/titoli.json sito/dati/manifest.js sito/dati/problemi/
git add sito/assets/figure/ documentazione/SITO_RECUPERO_2014_2020.md
git diff --cached --check
git diff --cached --stat
git commit -m "Pubblica sul sito i problemi Sant'Anna 2014-2020"
git push origin main
```

## Verifiche di questa preparazione

- I 20 sorgenti riprodotti dalla revisione editoriale sono stati convertiti
  correttamente con Pandoc; tutte le loro pagine web contengono il testo.
- Le quattro figure PSTricks hanno superato la compilazione LaTeX isolata.
- Un test tecnico dell'intero catalogo ha verificato 116 problemi, 164
  riferimenti a figure e nessuna figura pendente **usando SVG fittizi**:
  serve esclusivamente a provare il meccanismo di indicizzazione e controllo;
  **nessuno di questi SVG fittizi e' incluso nel pacchetto**.
- Gli SVG vettoriali autentici sono da produrre sul Mac e controllare
  visivamente prima del commit.

Il numero di problemi allineati verifica la coerenza tecnica, **non**
certifica la correttezza matematica o l'accuratezza filologica del testo.

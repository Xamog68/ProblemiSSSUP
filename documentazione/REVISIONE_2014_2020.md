# Revisione editoriale 2014--2020 (10 novembre 2026)

Aggiorna i 20 file canonici `contenuti/problemi/SA_2014_1.tex` -- `SA_2020_3.tex`, **a partire dalla versione già recuperata** nel pacchetto `ProblemiSSSUP_recupero_2014_2020_completo.zip`.

Criteri applicati:
- vere domande: `enumerate` con `\item[(a)]`, `\item[(b)]`, ecc.;
- dati, ipotesi e regole: `itemize` non numerati, anche annidati;
- accenti uniformati in UTF-8, come nel resto dell'archivio (è, é, à, ù, ì; perché, sì, ecc.);
- eliminate le ridefinizioni di `\labelenumii` obsolete;
- corretti i due refusi manifesti «stategia» e «quadrilareri».

Invariati: i contenuti matematici delle formule, i disegni PSTricks, l'ordine delle richieste e tutti i campi Risposta/Aiutino/Soluzioni/Osservazioni. Nessuna riscrittura sostanziale del testo storico.

Installazione consigliata dalla radice del repository (già contenente i 20 file del recupero):

    git status -sb
    git apply --check ~/Downloads/ProblemiSSSUP_revisione_testi_accenti_2014_2020.patch
    git apply ~/Downloads/ProblemiSSSUP_revisione_testi_accenti_2014_2020.patch
    make -f scripts/libro.mk libro SITO=https://xamog68.github.io/ProblemiSSSUP/index.html
    open build/SA_Book.pdf
    git diff --check

In alternativa alla patch, nello ZIP ci sono i 20 file revisionati da copiare nella cartella `contenuti/problemi/`.

Verifica effettuata: compilazione LaTeX/DVI/PS/PDF dei 20 testi e del libro con 116 problemi, rispettivamente 19 e 264 pagine; formule inline identiche alle precedenti. I controlli del sito restano da fare nel repository locale dopo la rigenerazione dei dati web e degli SVG delle nuove figure.

# Decisioni

## 2026-11-07 — Apertura del cantiere

1. Il progetto è distinto da ArchivioEureka.
2. I 78 file LaTeX modulari costituiscono la fonte canonica iniziale.
3. La fotografia storica integrale resta immutabile e fuori da Git.
4. I sorgenti sono normalizzati tecnicamente in UTF-8/LF, senza modifiche di
   contenuto.
5. Non si importano prodotti di compilazione, copie precedenti o ZIP annidati.
6. Libro e futuro sito dovranno derivare dalla stessa fonte LaTeX.
7. Non si assegna ancora una licenza: paternità e condizioni di pubblicazione
   devono essere chiarite.

## Correzioni certe nella fotografia iniziale

Sono stati corretti due metadati interni manifestamente incoerenti con il nome
del file e con la sequenza usata dal master:

- `SA_2012_4.tex`: `Anno` da 2011 a 2012;
- `SA_2013_3.tex`: `NumeroProblema` da 4 a 3.
- `SA_2011_4.tex`: rimosso il byte MacRoman spurio nella parola `possessore`.

Per compatibilità con `pst-eucl` moderno, le 16 occorrenze storiche di
`MarkAngleRadius=0pt` sono state trasformate in `MarkAngleRadius=0`: il
parametro è numerico nelle unità del disegno, mentre il suffisso `pt` finiva
nel PostScript come operatore inesistente.

Per lo stesso motivo sono stati rimossi i quattro suffissi `\psunit` dai
valori di `MarkAngleRadius` in `SA_2004_4.tex`. I valori numerici restano
invariati. Gli usi di `\psunit` in parametri dimensionali diversi sono stati
conservati.

Non è stato modificato il contenuto matematico.

## 2026-11-07 - Importazione dei problemi 2021-2026

1. I 18 problemi del periodo 2021-2026 sono importati in file
   LaTeX canonici separati, mantenendo intatti gli originali.
2. I testi matematici vengono conservati senza interventi editoriali.
3. Le parti commentate delle bozze non vengono importate nei file
   canonici, ma restano disponibili nelle fonti originali.
4. Le figure esterne non vengono importate: saranno ricostruite
   direttamente nel sorgente LaTeX.
5. I problemi 2024.2 e 2026.1 contengono promemoria per le figure
   ancora da realizzare.
6. I campi non disponibili (risposte, aiutini, soluzioni) restano vuoti.
7. Il libro storico di 205 pagine rimane indipendente dai nuovi problemi.

## 2026-11-07 - Obiettivo finale e architettura editoriale

Il progetto ha come obiettivo la raccolta, conservazione,
revisione e pubblicazione dei problemi di matematica delle prove
di ammissione alla Scuola Superiore Sant'Anna.

### Unica fonte canonica

Ogni problema è rappresentato da un unico sorgente LaTeX,
contenente testo e, quando disponibili, risposta breve, aiutino,
soluzioni, osservazioni e commenti.

Non devono esistere copie editoriali indipendenti dello stesso
contenuto destinate ai diversi prodotti.

### Primo prodotto: libro PDF

Il libro sarà generato automaticamente dai sorgenti canonici.

Dovrà essere possibile scegliere:
- tutti i problemi oppure una selezione;
- gli anni da includere;
- quali campi pubblicare: testi, risposte, aiutini, soluzioni,
  osservazioni e commenti.

Il master storico rimane conservato e riproducibile separatamente.

### Secondo prodotto: sito GitHub Pages

Il sito statico sarà organizzato principalmente per anno.

Per ciascun anno presenterà i problemi della prova e permetterà
di consultare, con un clic, gli altri contenuti disponibili
per ciascun problema: risposte, aiutini, soluzioni, osservazioni
e commenti.

I contenuti mancanti non genereranno collegamenti vuoti.
Il sito dovrà poter essere aggiornato automaticamente quando
viene completato un campo del sorgente canonico.

### Principio tecnico

Libro e sito saranno due prodotti generati dalla medesima
fonte LaTeX, eventualmente attraverso strumenti differenti.
Non si manterrà una seconda versione HTML dei testi matematici.

Le figure dovranno essere ricostruite direttamente nei sorgenti
LaTeX, per quanto possibile, senza dipendere da PDF esterni.

### Materiale non ancora validato

Bozze, appunti e soluzioni non verificate rimangono distinti
dai contenuti canonici pubblicabili.

In particolare, i materiali di soluzione del 2024-2026 sono
attualmente considerati appunti, da trascrivere e controllare.

Prima della pubblicazione dovranno essere chiarite paternità,
autorizzazioni e condizioni di distribuzione del materiale.

## 2026-11-07 - Architettura e interfaccia del sito

Il sito web utilizza gli stessi sorgenti LaTeX canonici del libro.

La conversione dei contenuti matematici e l'infrastruttura
grafica sono indipendenti.

Ogni pagina annuale mostra immediatamente tutti i testi.
Per ciascun problema sono disponibili due modalita:
- B: pulsante che rivela le fisarmoniche dei materiali aggiuntivi;
- C: nuova scheda con testo e materiali gia aperti.

I pulsanti relativi ai contenuti mancanti non vengono mostrati.
La navigazione rapida rimane accessibile durante lo scorrimento.

I dati web gia convertiti possono essere aggiornati singolarmente,
senza rigenerare l'interfaccia.

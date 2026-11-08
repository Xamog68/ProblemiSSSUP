# Stato del progetto ProblemiSSSUP

**Fotografia corrente: 8 novembre 2026.** Le fotografie del 7 novembre,
riportate in fondo, sono conservate come cronologia: **non descrivono più
lo stato attuale**.

## Archivio canonico

- **96 problemi in 24 annate**: 78 dal 1996 al 2013 e 18 dal 2021 al 2026.
- Mancano i testi delle prove 2014–2020.
- Tutti i 96 problemi hanno `Testo`, `Risposta` e `Aiutino` con contenuto.
- Sono presenti **56 soluzioni preesistenti** nel campo tecnico
  `SoluzioneUfficiale` (denominazione storica, non certificazione di ufficialità)
  e **40 soluzioni redazionali AI** nel campo `SoluzioneRedazionale`.
- L'8 novembre sono state aggiunte **82 bozze AI in 43 sorgenti**: 24 risposte,
  18 aiutini, 40 soluzioni; altri 53 sorgenti sono rimasti byte-identici
  alla fotografia precedente all'integrazione.
- Le bozze AI sono marcate nei sorgenti e nel sito; non sono ancora verificate
  matematicamente in maniera sistematica.

La scelta di iniziare nel 1996 è complementare alla raccolta di Torrigiani,
Francaviglia e Franzoni (Zanichelli, 1995), che copre le prove fino al 1995.

## Prodotti editoriali

### Sito pubblico

- **Online**: https://xamog68.github.io/ProblemiSSSUP/
- Repository GitHub reso pubblico, distribuzione tramite GitHub Actions dalla
  directory `sito/` (`.github/workflows/pages.yml`).
- 96 problemi convertiti e allineati ai sorgenti, con 96 titoli redazionali
  memorizzati separatamente in `sito/dati/titoli.json`.
- Navigazione per anno e problema, vista separata dei materiali, fisarmoniche
  con le bozze AI segnalate dalle stelline prima dell'apertura.
- È presente una direttiva `noindex` per scoraggiare i motori di ricerca;
  il sito resta pubblicamente accessibile.
- Il test `make sito-check` ha restituito **ALLINEATO 96, OBSOLETO 0,
  MANCANTE 0, ERRORE 0** l'8 novembre 2026.

**Figure web:** i **156 disegni PSTricks** sono stati convertiti in
SVG vettoriali e integrati nel sito con commit `e519325` (8 novembre 2026).
Il lotto sul Mac ha prodotto 156 SVG OK, zero errori e zero figure non
provate; il collaudo dei dati web ha trovato 156 SVG inseriti e nessun
PSTricks pendente. La vecchia segnalazione di 31 problemi incompleti
riguardava lo stato anteriore a questo intervento. Restano **due figure
esterne da ricostruire** (2024.2 e 2026.1) e possibili correzioni
visive delle figure già prodotte. La riuscita tecnica non attesta fedeltà
grafica o validità matematica.

### Libro

- Libro storico conservato, compilato sul Mac il 7 novembre 2026: **205
  pagine**, tramite la filiera LaTeX → DVI → PostScript → PDF.
- Libro modulare **v2.1**, già integrato: inventario automatico, selezione
  di annate e campi, indice con collegamenti, soluzioni su pagine distinte.
- Collaudo completo della v2.1 l'8 novembre 2026: **263 pagine**, 7 capitoli,
  24 annate, 96 testi, 96 risposte, 96 aiutini e 96 soluzioni.
- Compilazione: `make -f scripts/libro.mk libro`; manuale: `LEGGIMI.md`.

## Provenienza e diritti

Le fonti locali originali rimangono in `fonti-locali/`, fuori da Git.
Il manifesto `dati/integrazioni_ai/20261108.json` registra i contributi AI
e la loro provenienza. La distinzione fra testi d'esame, soluzioni
preesistenti, lavoro editoriale originale e contributi AI è mantenuta;
**non è stata decisa una licenza generale del repository**. Occorre
completare la ricognizione delle attribuzioni e dei diritti.

## Cantieri ancora aperti

1. Verifica matematica delle bozze AI e delle parti preesistenti problematiche
   (priorità documentate in `INTEGRAZIONE_AI_20261108.md`).
2. Completare le due figure esterne (2024.2 e 2026.1) e rifinire
   progressivamente le etichette dei disegni PSTricks già convertiti;
   valutare le figure che potrebbero essere tabelle HTML.
3. Recupero delle prove 2014–2020 e verifica filologica dei testi moderni.
4. Autori, attribuzioni, condizioni di riutilizzo e licenze.
5. Ulteriore collaudo su browser/dispositivi e perfezionamento editoriale.

Per la lista operativa: `TODO.md`.

---

## Fotografie storiche del 7 novembre 2026 (conservate)

Le sezioni seguenti riportano lo stato del progetto **prima**
dell'integrazione AI, del libro modulare v2.1 e della pubblicazione web.
Frasi come «sito non realizzato» e «campi vuoti» vanno lette esclusivamente
nel loro contesto temporale: la fotografia corrente è riportata sopra.

### Stato del cantiere

Data della fotografia iniziale: 7 novembre 2026.

#### Contenuti

| Campo | Problemi con contenuto |
|---|---:|
| Testo | 78 |
| Risposta breve | 72 |
| Aiutino | 78 |
| Soluzione ufficiale | 56 |
| Soluzioni alternative | 21 |
| Osservazioni | 33 |
| Commenti | 2 |

Le sei risposte non compilate sono 1996.1, 1997.4, 1997.5, 1998.3,
1999.4 e 2001.3.

Le 22 soluzioni ufficiali non compilate sono tutti i problemi degli anni
1998, 1999, 2000, 2001 e 2003.

#### Materiale editoriale

- Il master storico costruisce testi, risposte, aiutini, soluzioni e commenti.
- La classificazione storica copre soltanto gli anni 1996–1998 e non è ancora
  stata importata come dato canonico.
- Il titolo storico è `Problemi di Matematica alla SSSUP`.
- Nel master l'autore è ancora indicato come `Authors to be decided`.

#### Tecnologia

- Sorgenti originari: quasi interamente ASCII, terminatori CR e un byte
  MacRoman spurio.
- Sorgenti del cantiere: UTF-8 e terminatori LF.
- Grafica usata dal libro: prevalentemente PSTricks incorporato nei problemi.
- Filiera storica: LaTeX, DVI, dvips, ps2pdf.

#### Verifica di compilazione

Il 7 novembre 2026 il libro è stato compilato con successo su macOS mediante
MacTeX 2025 e Ghostscript 10.04.0. Il PDF risultante contiene 205 pagine, come
il PDF storico del 2013, e occupa 967157 byte.

Per la compatibilità con gli strumenti attuali sono stati necessari soltanto
adattamenti sintattici documentati in `DECISIONI.md`; PSTricks e i disegni
incorporati sono stati conservati.

#### Ampliamento del 7 novembre 2026

L'archivio contiene ora 96 problemi canonici:

- 78 problemi storici, dal 1996 al 2013;
- 9 problemi del periodo 2021-2023;
- 9 problemi del periodo 2024-2026.

Tutti i 96 problemi hanno il campo Testo compilato.
I 18 nuovi problemi hanno per ora vuoti gli altri campi.

Il verificatore controlla separatamente le statistiche del nucleo
storico e la struttura dell'archivio ampliato.

Restano da recuperare i problemi degli anni 2014-2020.

Figure da ricostruire:
- 2024.2: nove quadrati incernierati;
- 2026.1: quadrilatero con i quattro lati assegnati.

Le fonti originali e i materiali recuperati sono conservati in
fonti-locali/, esclusa dal repository Git.

#### Appunti di soluzione 2024-2026

Per gli anni 2024, 2025 e 2026 esistono tracce di soluzioni,
manoscritte o in altri formati, corrispondenti ai problemi delle prove.

Questi materiali sono classificati come APPUNTI DI SOLUZIONE:
- non sono ancora trascritti sistematicamente in LaTeX;
- non sono stati sottoposti a verifica matematica completa;
- non si presume che coprano tutti i problemi;
- non vanno ancora considerati soluzioni definitive o ufficiali.

Le macro canoniche delle soluzioni rimangono vuote fino alla
trascrizione e alla successiva verifica.

#### Obiettivo editoriale e situazione al 7 novembre 2026

##### Archivio canonico

Sono disponibili 96 problemi in file LaTeX individuali:
- 78 problemi del periodo 1996-2013;
- 18 problemi del periodo 2021-2026.

Mancano i problemi degli anni 2014-2020.

Tutti i problemi canonici hanno il testo compilato.
I problemi del 2021-2026 non hanno ancora contenuti aggiuntivi
importati nei campi di risposta, aiutino e soluzione.

Per il 2024-2026 esistono appunti di soluzione pertinenti
alle prove, da trascrivere in LaTeX e verificare accuratamente.
Non si presume che siano completi per tutti i problemi.

##### Inventario delle fonti

È disponibile un generatore automatico dell'inventario generale.

La fotografia del 7 novembre 2026 comprende 408 voci di fonte,
tra file locali e membri degli archivi ZIP.

Le fonti originali rimangono in fonti-locali/, fuori da Git.
L'inventario distingue prove scritte, test a risposta multipla,
materiali di soluzione e altre fonti.

##### Prodotti editoriali

Libro storico:
- compilazione riuscita sul Mac;
- 205 pagine;
- ancora basato sui problemi del 1996-2013.

Nuovo libro:
- generatore configurabile non ancora realizzato.

Sito GitHub Pages:
- non ancora realizzato;
- prevista navigazione per anno e per problema;
- contenuti aggiuntivi consultabili su richiesta.

La preparazione dei prodotti editoriali potrà procedere
anche prima del completamento di tutti i problemi e soluzioni.

#### 2026-11-07 - Prototipo modulare del sito

Prima versione dell'infrastruttura B+C inserita nel repository.

L'indice comprende tutti gli anni dal 1996 al 2026.
Sono gia disponibili in formato web:
- i quattro problemi del 2013, con 18 sezioni aggiuntive;
- i 18 problemi del 2021-2026, con i testi.

Gli anni 1996-2012 attendono la conversione web.
Le prove scritte del 2014-2020 sono ancora da recuperare.

La documentazione tecnica si trova in documentazione/SITO.md.
Il sito e sperimentale e non e ancora pubblicato su GitHub Pages.

# ProblemiSSSUP — Libro modulare v2.1

**Stato all'8 novembre 2026:** versione integrata nel repository e collaudata
per struttura e impaginazione; restano aperte la revisione matematica dei
contenuti e la verifica completa delle figure. Questo file documenta il libro
**già installato**, non più un pacchetto ZIP da estrarre.

## Componenti

- `latex/SA_Book.tex`: caricatore e impaginazione dei capitoli;
- `latex/SA_Book.sty`: stile storico mantenuto;
- `scripts/compila_libro.py`: ricognizione automatica dei sorgenti e generazione
  del catalogo dei contenuti richiesti;
- `scripts/libro.mk`: ricetta Make modulare, senza cambiare il Makefile storico;
- `contenuti/problemi/SA_AAAA_N.tex`: sorgenti matematici canonici.

Il libro è organizzato **per campo** (testi, risposte, aiutini, soluzioni,
soluzioni alternative, osservazioni, commenti), non per singolo problema.
Le annate e i problemi presenti sono scoperti automaticamente dal generatore.

## Impaginazione

- **Testi:** ogni anno comincia su nuova pagina, con titolo non numerato e
  righe orizzontali; numero del problema a sinistra e testo sulla stessa riga.
  Le domande interne sono indicate con (a), (b), (c).
- **Risposte:** identificatore `AAAA.N` a sinistra, testo sulla medesima riga.
- **Aiutini:** intestazioni brevi `\paragraph` *run-in*.
- **Soluzioni:** ogni problema comincia su una pagina nuova, anche nel capitolo
  delle soluzioni alternative.
- **Intestazioni e footer:** riprendono lo stile di `SA_Book.sty` e `\Fondo`,
  mostrando anno nei testi e capitolo negli altri campi.
- **Indice:** rimandi interni al PDF; i collegamenti al sito web sono facoltativi.
- **Bozze AI:** identificate esplicitamente come da verificare; il nome
  `SoluzioneUfficiale` è un dettaglio ereditato dello schema e non una garanzia.

## Compilazione

Dalla radice del repository:

```sh
make -f scripts/libro.mk libro
make -f scripts/libro.mk libro CAMPI=Testo,Risposta,Aiutino ANNI=2024-2026
make -f scripts/libro.mk libro CAMPI=Testo ANNI=1996-1998,2025
make -f scripts/libro.mk libro CAMPI=Soluzioni ANNI=2025
```

Campi disponibili: `Testo`, `Risposta`, `Aiutino`, `Soluzioni`,
`SoluzioniAlternative`, `Osservazioni`, `Commenti`; predefinito: tutti.
Gli intervalli possono comprendere anni non presenti, che vengono saltati.

Il risultato è `build/SA_Book.pdf`. Il procedimento utilizza tre passaggi
`latex`, poi `dvips` e `ps2pdf`, per mantenere compatibilità con PSTricks,
indice e rimandi. **Non usare `make libro` come sinonimo:** è la ricetta
storica, diversa dal generatore modulare.

## Collegamenti dal libro al sito

Si può fornire l'indirizzo pubblico, con il file `index.html`:

```sh
make -f scripts/libro.mk libro CAMPI=Testo ANNI=2025 \
    SITO=https://xamog68.github.io/ProblemiSSSUP/index.html
```

Il titolo dell'anno apre `?anno=2025`, e il numero del problema
`?anno=2025&problema=3`. Se `SITO` non viene passato, non vengono creati
link esterni. Il PDF mantiene comunque i collegamenti interni.

## Collaudo e limiti

Il collaudo completo della v2.1, eseguito l'8 novembre 2026 sui 96 sorgenti
con le integrazioni AI, ha prodotto un PDF di **263 pagine**, 7 capitoli,
24 annate, 96 testi, 96 risposte, 96 aiutini e 96 soluzioni (56 preesistenti
e 40 redazionali AI). Sono state controllate le pagine iniziali delle 96
soluzioni, tutte distinte, e campioni delle altre sezioni. È stata provata
anche la compilazione selettiva del 2025 con collegamenti web.

**Questi sono controlli tipografici e strutturali:** non certificano le prove,
la provenienza di tutti i contenuti, né la completezza delle figure.
Per i lavori aperti vedi `documentazione/TODO.md`.

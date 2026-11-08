# ProblemiSSSUP - Book v2.1 (revisione tipografica)

**Stato:** proposta da collaudare sul Mac; nessun sorgente canonico viene modificato.

La versione 2.1 conserva il caricatore modulare della v2 e ripristina la
presentazione storica delle sezioni principali.

## Contenuto dello ZIP

- `latex/SA_Book.tex`: nuovo caricatore + impaginazione ripristinata;
- `scripts/compila_libro.py`: inventario automatico e generatore catalogo;
- `scripts/libro.mk`: ricetta Make alternativa, senza toccare il Makefile storico;
- `LEGGIMI.md`: queste istruzioni.

Il pacchetto **non** contiene e **non** modifica i file `SA_YYYY_N.tex`,
`latex/SA_Book.sty`, `sito/` o il Makefile principale.

## Che cosa cambia rispetto alla v2

- **Testi**: ciascun anno inizia su nuova pagina, con titolo senza numerazione
  e righe orizzontali sopra e sotto; i problemi sono voci di `enumerate`,
  numero a sinistra e testo sulla stessa riga; gli elenchi interni usano
  `(a)`, `(b)`, `(c)` attraverso `\labelenumii`.
- **Risposte**: `enumerate` con l'identificatore `1996.1` nel margine
  sinistro, come nel libro storico. Testo e numero sulla stessa riga.
- **Aiutini**: `\paragraph` *run-in*, cioe' numero e testo nello stesso
  paragrafo, senza titoli isolati.
- **Footer**: ripristinato lo stile storico `\Fondo`, con anno nelle pagine
  dei testi e nome del capitolo nelle altre sezioni; restano le intestazioni
  pari/dispari di `SA_Book.sty`.
- **Soluzioni**: ogni problema inizia da pagina nuova. Anche le soluzioni
  alternative sono presentate un problema per pagina.
- **Contenuti AI**: risposte, aiutini e soluzioni nuove restano segnalati
  come bozze da verificare; le soluzioni preesistenti non sono chiamate
  "ufficiali" nel testo visibile.
- **Indice**: capitoli e anni sono collegamenti interni al PDF. La comparsa
  dei link web e' facoltativa (vedi sotto).

## Installazione controllata

Dal repository, verificare prima `git status -sb` e salvare in un commit
l'eventuale lavoro non consolidato. Estrarre il pacchetto nella radice del
repository (sostituisce soltanto i tre file tecnici elencati sopra):

```sh
unzip -o ~/Downloads/SSSUP_Book_v2_1.zip -d .
git diff --check
```

Conviene evitare di creare copie provvisorie dentro il progetto: Git conserva
le versioni precedenti.

## Compilazione

Dalla radice del progetto:

```sh
make -f scripts/libro.mk libro
make -f scripts/libro.mk libro CAMPI=Testo,Risposta,Aiutino ANNI=2024-2026
make -f scripts/libro.mk libro CAMPI=Testo ANNI=1996-1998,2025
make -f scripts/libro.mk libro CAMPI=Soluzioni ANNI=2025
```

Campi disponibili: `Testo`, `Risposta`, `Aiutino`, `Soluzioni`,
`SoluzioniAlternative`, `Osservazioni`, `Commenti`. Predefinito: tutti.
Gli anni vengono scoperti automaticamente dai nomi dei file; gli intervalli
possono comprendere anni privi di sorgenti (questi vengono saltati).

Il libro viene prodotto in `build/SA_Book.pdf` tramite tre passaggi `latex`,
poi `dvips` e `ps2pdf` (compatibilita' PSTricks, indice e rimandi).
**Non** usare ancora il vecchio `make libro`: il Makefile storico non e' stato
modificato.

## Collegamenti al sito

L'indice del PDF funziona sempre. Con una URL web di base *reale*:

```sh
make -f scripts/libro.mk libro CAMPI=Testo ANNI=2025 \
    SITO=https://example.org/sssup/index.html
```

L'indirizzo dell'esempio e' illustrativo. Il titolo dell'anno rimanda a
`?anno=2025`; il numero del problema rimanda a
`?anno=2025&problema=3`.
Senza `SITO` i link esterni non sono creati.

## Collaudo della v2.1

Con 96 file canonici e le bozze AI integrate, la compilazione completa ha
prodotto **263 pagine**, con 7 capitoli, 24 annate, 96 testi, 96 risposte,
96 aiutini e 96 soluzioni. Ho controllato che tutte e 96 le soluzioni
abbiano una pagina iniziale distinta e ho ispezionato le pagine dei testi,
delle risposte, degli aiutini, delle soluzioni e dell'indice.

La compilazione selettiva del 2025 con `SITO=...` ha creato correttamente
link interni e URL esterne distinte per anno e per problema.

**I controlli sono tipografici e strutturali, non verifiche delle dimostrazioni.**

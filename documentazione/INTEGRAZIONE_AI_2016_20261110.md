# ProblemiSSSUP - Bozze AI dei problemi 2016

Data: 10 novembre 2026.
Autore dei nuovi campi: ChatGPT (OpenAI).
Stato: **DA VERIFICARE**. Nessuna approvazione matematica umana e nessuna
attribuzione di ufficialita alle soluzioni.

## Contenuto e provenienza

Sono aggiunti esclusivamente i campi `Risposta`, `Aiutino` e
`SoluzioneRedazionale` dei tre sorgenti canonici del 2016.
Ogni campo contiene i marcatori `SSSUP-BOZZA-AI` e `SSSUP-PROVENIENZA`
previsti dal generatore del progetto. I marcatori consentono al libro e
al sito di segnalare la natura AI senza duplicare l'avviso nel testo.

I sorgenti sono stati recuperati dal ramo pubblico `main` del repository:

- https://raw.githubusercontent.com/Xamog68/ProblemiSSSUP/main/contenuti/problemi/SA_2016_1.tex
- https://raw.githubusercontent.com/Xamog68/ProblemiSSSUP/main/contenuti/problemi/SA_2016_2.tex
- https://raw.githubusercontent.com/Xamog68/ProblemiSSSUP/main/contenuti/problemi/SA_2016_3.tex

Le copie originali sono state verificate tramite SHA-256 contro le impronte
`_build.latex_sha256` pubblicate nei corrispondenti dati web `2016_N.js`.
E' stato inoltre verificato che, svuotando i tre nuovi campi, si riottiene
esattamente il sorgente originale. Testi, figura PSTricks, altri campi e
spaziatura esterna ai nuovi campi sono quindi invariati byte per byte.

## Stato matematico

### 2016.1 - Rastrelliere

- Distanza orizzontale interpretata come distanza fra gli assi, pari a `l`
  secondo il testo. Le prese diverse di P non sono collegate in parallelo:
  ogni presa alimenta uno o due carichi.
- Determinazione esatta del minimo per n pari, compresa la soglia esplicita.
- Per n dispari: regione di ottimalita dei collegamenti singoli,
  costruzioni alternative, intervallo rigoroso sul costo minimo e limite
  dell'errore della costruzione. NON si afferma di avere determinato tutte
  le soglie o la traslazione globalmente ottimale.
- **Nota redazionale futura:** il testo misura l fra gli assi dei binari,
  mentre la quota nella figura ricostruita e' fra i bordi interni delle
  rastrelliere. La discrepanza va confrontata con la fonte storica.
  Nessun intervento e' stato fatto sul Testo o sulla figura.

### 2016.2 - Copertura del disco

- Limite inferiore per area e due limiti superiori, uno elementare e uno
  ottenuto mediando sulle traslazioni di una griglia.
- Un quadrato: raggio massimo esatto l/2.
- Due quadrati: costruzione garantita con raggio l/(2*cos(pi/8)).
- Tre quadrati: costruzione garantita con raggio 5*l/8.
- Gli ultimi due raggi sono soltanto stime per difetto: NON si afferma
  l'ottimalita delle costruzioni. Nessuna ricerca numerica non certificata
  e' usata come dimostrazione.

### 2016.3 - Lotteria

- Prezzi teorici di pareggio: 81/4 e 121/6 euro.
- Prezzi minimi espressi in centesimi: 20.25 e 20.17 euro.
- Nel secondo caso la media comprende anche la scelta casuale della
  pallina trasferita. Per una pallina k nota, la formula condizionata e'
  (2025-k*k)/99. L'indipendenza e' usata solo condizionatamente a k.

## Controlli effettuati

Le dimostrazioni sono nei campi SoluzioneRedazionale; i controlli numerici
seguenti sono soltanto riscontri aggiuntivi e non le sostituiscono.

- 2016.1: minimo della lunghezza ramificata: 225 coppie (l,h), confronto con minimizzazione numerica, inclusi estremi.
- 2016.1: soglia esplicita: 300 valori di l; uguaglianza e segno ai due lati della soglia.
- 2016.1: intervallo dispari: 400 terne (l,h,m); coerenza dei limiti e ampiezza non superiore a delta.
- 2016.2: due quadrati: 200001 punti della circonferenza; il disco interno segue dalla convessita di ogni quadrato e dal centro comune.
- 2016.2: tre quadrati: identita della calotta esatta; controllo aggiuntivo su griglia 801 per 801.
- 2016.3: medie esatte: 100 esiti iniziali e 990 esiti dopo il trasferimento, in aritmetica razionale; 81/4 e 121/6.
- Conversione web dei nuovi campi: 9 frammenti convertiti con Pandoc/MathJax senza errori o avvisi; non e una build completa del sito.
- Compilazione locale con LaTeX, includendo la figura originale e tutti
  i nuovi campi: completata, 9 pagine DVI, nessun errore, nessun avviso di
  compilazione e nessuna scatola overfull/underfull segnalata.
- Non e' stata eseguita in questo ambiente una build integrale del libro
  o del sito del repository. I comandi sottostanti eseguono questi
  aggiornamenti sul clone locale.

## Applicazione e pubblicazione

Dalla radice del clone locale, dopo aver estratto lo ZIP:

```bash
git diff --check
git diff -- contenuti/problemi/SA_2016_*.tex
make verifica
python3 scripts/genera_figure_svg_massivo.py
python3 scripts/installa_figure_svg.py --applica
python3 scripts/genera_dati_sito.py --sito sito
make sito-check
```

La rigenerazione delle figure serve anche se il disegno non e' cambiato:
il catalogo SVG controlla l'impronta dell'intero sorgente. Il generatore
riprende i risultati validi; la generazione completa mantiene l'inventario
necessario all'installatore. La successiva generazione dei dati web deve
essere completa per riallineare l'impronta globale del catalogo SVG.

Per ricompilare il libro usando il generatore modulare del progetto:

```bash
make -f scripts/libro.mk libro
```

Il workflow Pages pubblica la cartella `sito/` e si attiva sui cambiamenti
in quella cartella: il solo commit dei sorgenti .tex non aggiorna il sito.

Riferimenti operativi consultati:

- https://github.com/Xamog68/ProblemiSSSUP/blob/main/documentazione/FIGURE_SITO.md
- https://github.com/Xamog68/ProblemiSSSUP/blob/main/.github/workflows/pages.yml
- https://github.com/Xamog68/ProblemiSSSUP/blob/main/scripts/libro.mk

## Impronte dei sorgenti

### SA_2016_1.tex

Originale verificato:

```text
0a7cedb81f12936efb10e2822ec68c1a98f25e55378077a14aff8ef9d95af40d
```

Bozza consegnata:

```text
d991abe2a4c7b466889c00fdac11ad7ee9deb8bdd478f377b18f5856a8903ee9
```

### SA_2016_2.tex

Originale verificato:

```text
7361ccfdc3006262a209979fe7fef290184b91c824af3b53d625041fb040898e
```

Bozza consegnata:

```text
4a4795b08036f8b00efb38d4b11ac50a26b823076c81ae9e0db85d2c2a05b149
```

### SA_2016_3.tex

Originale verificato:

```text
1480b395c6a5fb7e4598773029045c420c3391c8f098715ac6100c341f65a021
```

Bozza consegnata:

```text
2196e46725e5062727c2972a1bf68ae630218763ecac3d062a4c19e455eace65
```


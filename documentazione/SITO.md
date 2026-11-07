# Sito web SSSUP — infrastruttura sperimentale B+C

*Stato: prototipo locale, 7 novembre 2026. Non pubblicato su GitHub Pages.*

## Scopo e separazione delle responsabilita

I file `contenuti/problemi/SA_AAAA_N.tex` sono l'unica fonte canonica
per testi e materiali matematici. Il sito ne mostra una copia derivata per
il web, ma non introduce una seconda fonte editoriale modificata a mano.

- `sito/index.html`: struttura HTML, intestazione e caricamento risorse.
- `sito/assets/site.css`: aspetto grafico e impaginazione.
- `sito/assets/site.js`: interazione, navigazione e presentazione dei dati.
- `sito/dati/manifest.js`: elenco anni 1996–2026 e disponibilita dei problemi.
- `sito/dati/problemi/AAAA_N.js`: contenuti matematici gia convertiti,
  registrati con `window.SSSUP.registerProblem(...)`.
- `sito/dati/titoli.json`: etichette descrittive sperimentali; non sono
  necessariamente titoli originali della prova.
- `scripts/genera_dati_sito.py`: convertitore incrementale dei contenuti,
  separato dal codice di interfaccia; richiede Pandoc.

Le due viste del medesimo problema usano gli stessi file di dati:

1. **Vista anno (B)**: tutti i testi visibili subito; un pulsante
   "Mostra materiali aggiuntivi" per problema, che apre le fisarmoniche
   delle sole sezioni realmente presenti.
2. **Vista separata (C)**: nuova scheda con testo del problema e materiali
   tutti aperti inizialmente, richiudibili singolarmente.

Nella pagina dell'anno una navigazione fissa per i problemi rimane
accessibile durante lo scorrimento. I controlli globali di apertura,
filtraggio e misura della lunghezza sono raccolti sotto "Strumenti" e
sono soprattutto ausili di prova, non una scelta editoriale definitiva.

## Contenuti del prototipo

- Anni indicizzati: 1996–2026 (31 anni).
- Dati web disponibili: 2013 (4 problemi con 18 sezioni aggiuntive)
  e 2021–2026 (18 problemi con soli testi canonici).
- Anni 1996–2012: i 74 file LaTeX canonici esistono ma non sono ancora
  convertiti per questa anteprima.
- Anni 2014–2020: testi delle prove scritte non ancora recuperati.

Le conversioni di questa anteprima **non sono un'edizione verificata**.
In particolare PSTricks, le figure mancanti, le macro non standard e i
riferimenti LaTeX devono essere controllati prima della pubblicazione.
Il sito utilizza MathJax da CDN per le formule: una connessione Internet
puo essere necessaria anche usando l'anteprima locale.

## Prova locale (senza Pandoc)

Dalla radice del repository:

```sh
open sito/index.html
```

Se Firefox limita il caricamento dei file locali, usare un server statico:

```sh
cd sito
python3 -m http.server 8765
```

Aprire `http://localhost:8765/` e fermare il server con `Ctrl+C`.

Esempi di collegamento diretto:

```text
sito/index.html?anno=2013
sito/index.html?anno=2013&problema=2
sito/index.html?anno=2013&problema=2&vista=materiali
sito/index.html?anno=2013&problema=2&sezione=SoluzioneUfficiale
```

## Aggiornamento incrementale dei dati

Quando Pandoc sara disponibile, dalla radice del repository:

```sh
python3 scripts/genera_dati_sito.py --anno 2013 --problema 2
```

Per convertire tutti i problemi disponibili:

```sh
python3 scripts/genera_dati_sito.py
```

Il generatore scrive/aggiorna i file in `sito/dati/` e
`sito/dati/manifest.js`, senza toccare `sito/assets/` o i sorgenti `.tex`.
La cache locale `sito/dati/build_cache.json` non si versiona.
I file `AAAA_N.js` sono prodotti derivati e possono essere versionati
per rendere il sito consultabile senza dover installare Pandoc.

**Attenzione:** la conversione e sperimentale. Il generatore può perdere
macro LaTeX speciali, sostituire disegni PSTricks con segnaposto e non
riprodurre fedelmente tutte le formule. Controllare i risultati prima di
pubblicare il sito. Per ora non e configurato alcun deploy automatico
su GitHub Pages.

## Decisioni editoriali e lavoro futuro

- Unica fonte LaTeX per libro PDF e sito; presentazione e dati separati.
- Un aggiornamento solo CSS/JS non richiede conversioni matematiche.
- Risposta, aiutino, soluzioni, alternative e osservazioni appaiono solo
  se realmente disponibili.
- In futuro potranno essere aggiunti contenuti AI provvisori, etichettati
  esplicitamente e distinti dalle soluzioni storiche o verificate.
- Verificare il convertitore su tutti i 96 problemi; gestire robustamente
  disegni, conversioni mancanti e la presenza di sottoinsiemi sparsi.
- Prima del sito pubblico: verifica matematica e grafica, provenienza,
  diritti di distribuzione, accessibilita, mobile e deploy GitHub Pages.

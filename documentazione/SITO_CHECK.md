# Controllo di allineamento dei problemi web

## Scopo

L'infrastruttura HTML/CSS/JavaScript del sito e separata dai suoi contenuti matematici.
Il comando `python3 scripts/sito_check.py` confronta ogni problema LaTeX canonico
con il corrispondente file web `sito/dati/problemi/AAAA_N.js`, **senza modificarlo**.

La conversione registra direttamente dentro ciascun file web quattro impronte:

- SHA-256 dei byte del sorgente LaTeX;
- SHA-256 dello script `scripts/genera_dati_sito.py` (regole di conversione);
- stringa di versione di Pandoc;
- SHA-256 dei frammenti HTML registrati per il problema (controllo di integrita).

Il confronto controlla anche anno, numero, nome del file sorgente e titolo.
Non serve la vecchia cache locale `build_cache.json`: puo rimanere sul disco,
ma il generatore nuovo non la legge piu. I metadati viaggiano insieme ai file web
versionati su GitHub e sono quindi utilizzabili su altre macchine.

## Comandi

Dalla radice del repository:

```sh
python3 scripts/sito_check.py
python3 scripts/sito_check.py --anno 2013 --problema 1
python3 scripts/sito_check.py --dettagli

# Conversione incrementale di tutti i problemi NON allineati:
python3 scripts/genera_dati_sito.py

# Conversione isolata per prova, senza toccare il sito versionato:
python3 scripts/genera_dati_sito.py --anno 2013 --problema 1 \
  --sito build/prova-sito-check --force
python3 scripts/sito_check.py --anno 2013 --problema 1 \
  --sito build/prova-sito-check
```

Esiti: `ALLINEATO`, `OBSOLETO`, `MANCANTE`, `ERRORE`.
Le conversioni del prototipo precedenti a questa modifica sono inizialmente
`OBSOLETO` perche non contengono impronte verificabili: e normale.
Anche una modifica soltanto al generatore rende obsoleti i vecchi dati.
Le modifiche a `sito/assets/site.css` e `sito/assets/site.js` non influiscono.

Il controllo restituisce codice 0 soltanto se tutti i problemi esaminati
sono allineati, altrimenti 1. Quindi puo essere usato in CI o in Make.

## Limiti

- L'allineamento tecnico **non** equivale a revisione matematica o editoriale.
- Disegni PSTricks segnalati con segnaposto devono essere risolti prima della pubblicazione.
- L'hash attualmente include il file LaTeX e lo script di conversione: se si
  introdurranno in futuro input LaTeX esterni, macro condivise, filtri Pandoc o
  altre dipendenze, occorrera includerli nel calcolo delle impronte.
- Non pubblicare automaticamente materiali non verificati soltanto perche
  il controllo produce `ALLINEATO`.

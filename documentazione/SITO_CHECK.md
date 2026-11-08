# Controllo di allineamento dei problemi web

**Stato all'8 novembre 2026:** sito distribuito pubblicamente; ultimo
controllo noto `make sito-check`:

```text
Problemi canonici esaminati: 96
ALLINEATO : 96
OBSOLETO  : 0
MANCANTE  : 0
ERRORE    : 0

INCOMPLETO (figure segnalate): 31 problemi
Disegni PSTricks non convertiti: 156
Figure da ricostruire: 2
```

## Che cosa viene controllato

L'infrastruttura HTML/CSS/JavaScript del sito è separata dai suoi contenuti.
Il comando `python3 scripts/sito_check.py` confronta ogni problema LaTeX
canonico con il corrispondente `sito/dati/problemi/AAAA_N.js`, **senza
modificarlo**.

Il generatore registra dentro ciascun file web quattro impronte o metadati:

- SHA-256 dei byte del sorgente LaTeX;
- SHA-256 di `scripts/genera_dati_sito.py` (regole di conversione);
- stringa di versione di Pandoc;
- SHA-256 dei frammenti HTML del problema (integrità).

Si controllano inoltre anno, numero, nome sorgente e titolo. La vecchia
cache `build_cache.json` non è necessaria al controllo: le impronte viaggiano
con i file derivati versionati. Il controllo di allineamento va eseguito
**dopo** ogni rigenerazione con Pandoc.

## Comandi

```sh
make sito-check
python3 scripts/sito_check.py
python3 scripts/sito_check.py --anno 2013 --problema 1
python3 scripts/sito_check.py --dettagli

# Rigenerazione dei problemi non allineati:
python3 scripts/genera_dati_sito.py --sito sito

# Conversione isolata, senza modificare il sito versionato:
python3 scripts/genera_dati_sito.py --anno 2013 --problema 1 \
  --sito build/prova-sito-check --force
python3 scripts/sito_check.py --anno 2013 --problema 1 \
  --sito build/prova-sito-check
```

Esiti: `ALLINEATO`, `OBSOLETO`, `MANCANTE`, `ERRORE`. Un cambio del
convertitore rende obsoleti i dati precedenti anche quando il sorgente
LaTeX è identico. Le modifiche all'interfaccia CSS/JS non influiscono
sull'impronta della conversione. Il controllo restituisce codice 0 se i
problemi selezionati sono tutti allineati; altrimenti 1.

## Controlli indipendenti e limiti

- **ALLINEATO** significa che il file web corrisponde al sorgente e alle
  regole di conversione attuali: non implica revisione matematica,
  correttezza delle formule, delle figure o delle attribuzioni.
- **INCOMPLETO** segnala i problemi con figure da ricostruire o disegni
  PSTricks ancora sostituiti da segnaposto. Un problema può risultare
  contemporaneamente ALLINEATO e INCOMPLETO.
- Anche in assenza di segnaposto una conversione richiede controllo visivo.
  Le figure segnalate sono documentate in `FIGURE_SITO.md`.
- Le nuove sezioni AI possono comparire sul sito in stato **DA VERIFICARE**;
  non diventano corrette perché superano il test tecnico.
- Se in futuro il convertitore dipenderà da risorse LaTeX esterne, macro
  condivise o filtri Pandoc, le impronte andranno estese a tali dipendenze.

Il sito è stato pubblicato con queste limitazioni dichiarate, non perché
siano state risolte tutte le verifiche editoriali.

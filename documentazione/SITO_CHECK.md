# Controllo di allineamento dei problemi web

**Stato all'8 novembre 2026, dopo l'integrazione SVG:** sito pubblico,
con tutti i 96 problemi tecnicamente allineati e le 156 figure PSTricks
presenti come SVG. Restano 2 figure esterne da ricostruire.

```text
Problemi canonici esaminati: 96
ALLINEATO : 96
OBSOLETO  : 0
MANCANTE  : 0
ERRORE    : 0

Verifica SVG dedicata: 156 SVG inseriti, 0 PSTricks pendenti,
                      2 figure esterne da ricostruire.
```

I vecchi conteggi «31 problemi incompleti» e «156 PSTricks non convertiti»
sono **antecedenti** al commit `e519325` e non vanno più usati per
fotografare lo stato corrente.

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

# Controllo specifico della collocazione dei 156 SVG
# (richiede l'inventario locale build/figure-svg/inventario.json):
python3 scripts/installa_figure_svg.py --verifica-sito

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
- **INCOMPLETO** segnala figure esterne ancora da ricostruire (o eventuali
  segnaposto PSTricks in caso di future conversioni mancanti/obsolete).
  Un problema può risultare contemporaneamente ALLINEATO e INCOMPLETO.
- La correttezza del **lotto SVG** richiede anche il controllo dedicato
  `installa_figure_svg.py --verifica-sito`: legge inventario e impronte
  locali, quindi non è eseguibile soltanto dal sito pubblicato.
- Anche in assenza di segnaposto una conversione richiede controllo visivo.
  Le figure segnalate sono documentate in `FIGURE_SITO.md`.
- Le nuove sezioni AI possono comparire sul sito in stato **DA VERIFICARE**;
  non diventano corrette perché superano il test tecnico.
- Le impronte dei sorgenti vengono utilizzate anche dal manifesto SVG;
  un cambiamento al LaTeX richiede rigenerazione delle figure interessate,
  reinstallazione e nuova generazione dei dati web. Altre dipendenze esterne
  dovranno essere considerate qualora vengano introdotte.

Il sito è stato pubblicato con queste limitazioni dichiarate, non perché
siano state risolte tutte le verifiche editoriali.

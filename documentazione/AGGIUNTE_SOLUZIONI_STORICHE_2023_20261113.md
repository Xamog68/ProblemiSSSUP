# ProblemiSSSUP — aggiunte redazionali ai problemi 2023

**Data:** 13 novembre 2026. **Stato:** bozze AI da verificare; nessun risultato preesistente modificato.

## Materiali selezionati

- `SA_2023_1.tex`: in `Osservazioni`, esempi più brevi per gli estremi 751 e 1250 del punto (b).
- `SA_2023_2.tex`: in `SoluzioniAlternative`, ricorrenze di un anno per (b) e (c), in luogo delle serie geometriche.
- `SA_2023_3.tex`: in `SoluzioniAlternative`, ottimizzazione del raggio tramite il discriminante di un trinomio in `a^2`.

I contenuti sono **rielaborazioni AI** di spunti matematici contenuti in manoscritti storici presenti nell'archivio privato `Concorsi/SSSUP_2023/Soluzioni/`. Non vengono spacciati per soluzioni ufficiali. I file storici non sono compresi in questo pacchetto e non devono essere pubblicati indiscriminatamente.

Sono invariati (anche nei byte) i Testi, le Risposte, gli Aiutini, la SoluzioneRedazionale, le figure e tutti gli altri campi preesistenti; viene popolato soltanto un campo prima vuoto in ciascun problema.

## Installazione

Eseguire nella radice del repository, dopo aver decompresso lo ZIP in una cartella temporanea:

```
python3 /percorso/allo/zip/installa_aggiunte_2023.py --root .
python3 /percorso/allo/zip/installa_aggiunte_2023.py --root . --apply
```

La modalità predefinita simula l'installazione; quella `--apply` controlla gli SHA-256 dei tre sorgenti di partenza, per evitare sovrascritture involontarie. Non installa nulla se non combaciano tutti e tre.

Per libro e sito, dopo l'installazione:

```
make verifica
python3 scripts/genera_dati_sito.py --sito sito
make sito-check
make -f scripts/libro.mk libro
```

I tre problemi non contengono figure PSTricks, quindi l'operazione non richiede rigenerazione di SVG.

Per la pubblicazione controllare prima le differenze:

```
git diff -- contenuti/problemi/SA_2023_*.tex
git diff --check
git add contenuti/problemi/SA_2023_*.tex documentazione/AGGIUNTE_SOLUZIONI_STORICHE_2023_20261113.md sito/dati
git diff --cached --stat
git commit -m "Aggiunte soluzioni alternative storiche ai problemi 2023"
git push
```

## Verifiche specifiche

- (2023.1) `499 * 0.5 + 750.5 = 1000`, arrotondamenti `499 + 751 = 1250`; con `0 < eps < 1/499` i primi 499 arrotondano a 0, l'ultimo a 751.
- (2023.2) Le due ricorrenze forniscono gli stessi risultati delle serie della soluzione redazionale; il caso `p=1` va trattato a parte nel punto (b).
- (2023.3) `2 r (a^2)^2 - 3V a^2 + 12V r^2=0`; discriminante `9V^2-96Vr^3`; l'uguaglianza si ha per `h=sqrt(2)*a`.

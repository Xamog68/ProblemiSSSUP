# Sito web ProblemiSSSUP

**Stato all'8 novembre 2026:** sito pubblico su GitHub Pages, con 96 problemi
in 24 annate. URL: https://xamog68.github.io/ProblemiSSSUP/

## Fonte canonica e componenti

I file `contenuti/problemi/SA_AAAA_N.tex` sono l'unica fonte canonica
per testi e materiali matematici. La versione HTML è un **derivato**,
non una seconda redazione indipendente.

| Elemento | Ruolo |
|---|---|
| `sito/index.html` | Contenitore HTML e caricamento delle risorse. |
| `sito/assets/site.css` | Grafica, fisarmoniche, numerazione delle domande e responsive. |
| `sito/assets/site.js` | Navigazione, viste anno/problema, materiali e metadati. |
| `sito/dati/manifest.js` | Elenco degli anni e dei problemi disponibili. |
| `sito/dati/problemi/AAAA_N.js` | Contenuti convertiti, registrati con `window.SSSUP.registerProblem(...)`. |
| `sito/dati/titoli.json` | 96 titoli descrittivi redazionali, distinti dai testi canonici. |
| `scripts/genera_dati_sito.py` | Generazione dei dati LaTeX → HTML con Pandoc. |
| `scripts/sito_check.py` | Verifica di allineamento tecnico dei file web. |
| `scripts/genera_figure_svg_massivo.py` | Conversione isolata PSTricks → SVG con log e timeout per figura. |
| `scripts/installa_figure_svg.py` | Preflight, installazione degli SVG e verifica della loro collocazione. |
| `sito/assets/figure/` | 156 SVG vettoriali e `manifest.json` delle impronte; risorse versionate. |
| `.github/workflows/pages.yml` | Distribuzione di `sito/` su GitHub Pages. |

Il sito usa MathJax per la matematica; le formule sono caricate da CDN.
La resa in assenza di connessione non è garantita.

## Interfaccia e contenuti

L'indice mostra le annate dal 1996 al 2026, distinguendo quelle mancanti.
Sono consultabili i 96 problemi degli anni 1996–2013 e 2021–2026;
le prove 2014–2020 restano da recuperare.

- **Vista anno (B):** tutti i testi visibili; un pulsante per ciascun problema
  mostra i materiali aggiuntivi nelle fisarmoniche corrispondenti ai soli
  campi presenti. La navigazione fissa resta disponibile durante lo scroll.
- **Vista problema/materiali (C):** scheda dedicata al problema con materiali
  consultabili individualmente, inizialmente aperti quando previsto.
- È disponibile un comando evidente per tornare all'elenco degli anni.
- Le domande dei testi sono visualizzate come (a), (b), (c), coerentemente
  con il livello `enumii` del libro; risposte e soluzioni non sono forzate
  alla stessa numerazione.

I campi aggiunti dall'AI conservano metadati di provenienza e appaiono con
l'icona delle stelline e la dicitura **«Bozza AI · Da verificare» già
nelle fisarmoniche chiuse**. Questo riguarda 24 risposte, 18 aiutini e
40 soluzioni redazionali. I materiali preesistenti non vengono chiamati
«ufficiali» soltanto per il nome tecnico della macro LaTeX.

I titoli sono etichette editoriali e non modificano `\Testo`.
I **156 disegni PSTricks** sono mostrati come SVG vettoriali, ottenuti senza
modificare il codice LaTeX dei problemi. Il convertitore li associa a
problema, campo e numero progressivo; le impronte impediscono l'uso
silenzioso di SVG obsoleti. Restano segnalate due figure esterne da
ricostruire (2024.2 e 2026.1); si veda `FIGURE_SITO.md`.

## Prova locale

Dalla radice del repository:

```sh
python3 -m http.server 8000 --directory sito
```

Aprire `http://localhost:8000/` in Firefox e arrestare il server con `Ctrl+C`.
Non servono Node.js né un server applicativo per consultare il sito.

Esempi di URL pubblici:

```text
https://xamog68.github.io/ProblemiSSSUP/?anno=2025
https://xamog68.github.io/ProblemiSSSUP/?anno=2025&problema=3
```

## Rigenerazione e controllo

Quando si modifica un file LaTeX canonico, una regola del convertitore o il
file dei titoli, rigenerare i dati web interessati. Se la modifica coinvolge
una figura PSTricks, seguire prima la procedura SVG riportata sotto.
Dalla radice:

```sh
python3 scripts/genera_dati_sito.py --sito sito
make sito-check
git diff --check
```

Per un solo problema:

```sh
python3 scripts/genera_dati_sito.py --anno 2013 --problema 2 --sito sito
python3 scripts/sito_check.py --anno 2013 --problema 2
```

Il generatore aggiorna `sito/dati/`; non modifica i sorgenti canonici.
I dati derivati sono versionati affinché il sito funzioni senza Pandoc
sul server. La produzione degli SVG è un passaggio **separato**, necessario
quando si modificano sorgenti che contengono figure PSTricks:

```sh
python3 scripts/genera_figure_svg_massivo.py
python3 scripts/installa_figure_svg.py --applica
python3 scripts/genera_dati_sito.py --sito sito
make sito-check
python3 scripts/installa_figure_svg.py --verifica-sito
```

Gli SVG si generano **localmente** con TeX, `dvisvgm` e Ghostscript;
GitHub Pages distribuisce soltanto i file già convertiti. L'installatore
richiede il catalogo completo in `build/figure-svg/` e blocca l'operazione
se qualche figura manca o ha un'impronta obsoleta. Le istruzioni dettagliate
sono in `FIGURE_SITO.md`. Un aggiornamento soltanto di CSS o JS non richiede riconversione
matematica. Si raccomanda un controllo visivo dei problemi modificati.

Il test `make sito-check` dell'8 novembre 2026 ha restituito 96 problemi
`ALLINEATO`, 0 `OBSOLETO`, 0 `MANCANTE`, 0 `ERRORE`. Dopo l'integrazione
sono presenti 156 SVG e nessun segnaposto PSTricks residuo; rimangono
2 figure esterne mancanti. **Allineato non significa matematicamente o
graficamente verificato**: servono anche controlli visivi.

## Pubblicazione tramite GitHub Pages

Il repository GitHub è pubblico; il sito viene pubblicato dalla **sola
cartella `sito/`**, tramite il workflow `.github/workflows/pages.yml`.
In **Settings → Pages → Build and deployment**, la sorgente deve essere
**GitHub Actions**, non *Deploy from a branch*. In caso contrario potrebbe
essere mostrato l'`index.html` della radice del repository, cioè la roadmap,
anziché il sito dei problemi.

Per aggiornare il sito: rigenerare i dati se necessario, eseguire i controlli,
creare un commit e fare `git push origin main`. Seguire l'esecuzione nella
scheda **Actions** di GitHub. Il primo deploy corretto è stato ottenuto
rilanciando il workflow dedicato dopo la configurazione di Pages.

La pagina contiene una direttiva `noindex` per scoraggiare la comparsa del
sito nei risultati di ricerca; **non è un controllo d'accesso**. Il repository
pubblico, gli URL conosciuti e le pagine accessibili restano consultabili.
Non creare sitemap a fini promozionali senza una nuova decisione editoriale.

## Provenienza, licenze e limiti

- I titoli e le integrazioni redazionali sono distinti dai testi d'esame.
- Non esiste una licenza unica adottata per tutto il materiale.
- I testi e le soluzioni preesistenti non diventano opera del curatore
  perché sono ospitati sul sito.
- Il footer segnala il lavoro editoriale originale; non risolve da solo
  attribuzioni o diritti sui materiali di terzi.
- Due figure esterne da ricostruire, 82 integrazioni AI ancora da
  verificare e differenze filologiche restano lavori aperti. La revisione
  tipografica dei 156 SVG è distinta dalla loro conversione tecnica.

Si vedano `DECISIONI.md`, `TODO.md`, `SITO_CHECK.md` e
`INTEGRAZIONE_AI_20261108.md`.

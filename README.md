# Problemi di Matematica alla SSSUP

Archivio dei problemi di matematica delle prove di ammissione alla Scuola
Superiore Sant'Anna di Pisa, con sorgenti LaTeX, libro PDF e sito web.

**Sito pubblico:** https://xamog68.github.io/ProblemiSSSUP/

Il progetto raccoglie **96 problemi di 24 annate**: 78 del periodo
1996–2013 e 18 del periodo 2021–2026 (tre per anno negli ultimi sei anni).
Le prove del 2014–2020 non sono ancora state recuperate. La raccolta parte dal
1996 perché il volume di Guido Torrigiani, Sebastiano Francaviglia e Tullio
Franzoni, *Problemi di matematica della Scuola superiore S. Anna* (Zanichelli,
1995), copre il periodo precedente, fino al 1995. Il nostro progetto è
indipendente da quella pubblicazione.

## Materiali e stato di revisione

I file in `contenuti/problemi/SA_AAAA_N.tex` sono **la fonte canonica**.
Libro e sito sono derivati da questi file: non si modificano separatamente
le copie HTML dei contenuti matematici.

Ogni sorgente comprende il testo e può contenere risposta breve, aiutino,
soluzione preesistente, soluzione redazionale, soluzioni alternative,
osservazioni e commenti. Il nome tecnico ereditato `SoluzioneUfficiale`
**non certifica** che una soluzione sia ufficiale o verificata.

L'8 novembre 2026 sono state integrate **82 bozze AI in 43 problemi**:
24 risposte, 18 aiutini e 40 soluzioni redazionali. I nuovi contributi
sono marcati `SSSUP-BOZZA-AI` nei sorgenti e sono presentati nel sito
con l'icona delle stelline e la dicitura **«Bozza AI · Da verificare»**, anche
a fisarmonica chiusa. **Non sono stati sottoposti a revisione matematica
completa.** Si vedano `documentazione/INTEGRAZIONE_AI_20261108.md` e
`documentazione/TODO.md` per provenienza e punti critici.

I **96 titoli descrittivi** del sito sono etichette redazionali, non titoli
ufficiali delle prove: si conservano in `sito/dati/titoli.json`, senza
alterare i testi canonici.

## Il sito

La pagina principale mostra gli anni disponibili. Le pagine delle annate
presentano tutti i testi e consentono di aprire, per ciascun problema,
risposte, aiutini, soluzioni e gli altri contenuti presenti. È disponibile
anche una vista dedicata al singolo problema. Le domande nei testi sono
visualizzate con (a), (b), (c), come nel libro.

Il sito è statico, ospitato da **GitHub Pages** e distribuito dalla cartella
`sito/` tramite `.github/workflows/pages.yml`. È pubblico, ma contiene
l'indicazione `noindex` per scoraggiare l'indicizzazione: **non è una misura
di riservatezza**. È possibile che il repository GitHub o singoli URL siano
comunque reperibili nei motori di ricerca.

**Limite noto:** 31 problemi hanno figure segnalate come incomplete nel web;
il controllo rileva 156 disegni PSTricks non convertiti e due figure esterne
da ricostruire. I segnaposto sono dichiarazioni di incompletezza, non
disegni equivalenti. Cfr. `documentazione/FIGURE_SITO.md`.

## Comandi essenziali

Dalla radice del repository:

```sh
make verifica
make sito-check
python3 scripts/genera_dati_sito.py --sito sito
make -f scripts/libro.mk libro
```

La conversione web richiede Python 3 e Pandoc; il sito distribuito richiede
soltanto un browser e, per MathJax da CDN, una connessione Internet.
Il libro v2.1 richiede inoltre una distribuzione TeX con PSTricks, `dvips`
e `ps2pdf`. La compilazione modulare genera `build/SA_Book.pdf`; la ricetta
storica `make libro` è distinta. Istruzioni: `LEGGIMI.md`,
`documentazione/SITO.md` e `documentazione/SITO_CHECK.md`.

Il controllo `sito-check` verifica **l'allineamento tecnico** fra i sorgenti
e i dati web; non verifica correttezza matematica, fedeltà delle figure o
diritto di riutilizzo.

## Fonti, attribuzioni e diritti

Il progetto nasce dalla fotografia storica `SA_Libro.zip`; checksum e
conservazione sono documentati in `fonti/README.md`. Le fonti originali
locali sono mantenute in `fonti-locali/`, esclusa dal repository Git.

I testi delle prove, i materiali preesistenti, il codice del sito e i nuovi
contributi redazionali possono avere titolarità differenti. Il copyright
sul lavoro editoriale originale **non attribuisce automaticamente** al
curatore i diritti sui testi d'esame o sulle soluzioni di altri autori.
La disponibilità pubblica del repository **non equivale a una licenza
generale di riutilizzo**. La ricognizione su paternità, licenze e
attribuzioni resta aperta: si veda `documentazione/DECISIONI.md`.

## Documentazione

- `documentazione/STATO.md`: fotografia corrente e cronologia delle fasi.
- `documentazione/DECISIONI.md`: decisioni editoriali e tecniche.
- `documentazione/TODO.md`: lavori aperti e priorità.
- `documentazione/SITO.md`: architettura, sviluppo e pubblicazione web.
- `documentazione/SITO_CHECK.md`: controlli e limiti del convertitore.
- `documentazione/INTEGRAZIONE_AI_20261108.md`: provenienza e criticità delle bozze.
- `LEGGIMI.md`: manuale operativo del libro v2.1.

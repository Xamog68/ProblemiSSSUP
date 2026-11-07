# Recupero dei testi 2024-2026

Data: 7 novembre 2026.

## Stato

In `fonti-locali/2024/SA_2024_testi_chat.tex`,
`fonti-locali/2025/SA_2025_testi_chat.tex` e
`fonti-locali/2026/SA_2026_testi_chat.tex` sono stati conservati i testi
LaTeX incollati dall'utente nella conversazione ChatGPT del 7 novembre 2026.
Sono 3 esercizi per ciascun anno (9 in tutto), comprendenti anche le varianti
e le annotazioni editoriali che erano commentate nel codice.

I testi **non sono ancora canonici**, non hanno avuto revisione editoriale e
non sono stati inseriti in `contenuti/problemi/`. Nessuna soluzione e' stata
importata insieme a questi testi.

## Dipendenze

Il testo 2024.2 usa `fonti-locali/2024/squares.pdf`.
Il testo 2026.1 usa `fonti-locali/2026/es1.pdf` e l'ambiente `wrapfigure`.
Le due figure erano presenti nella cartella locale prima del recupero,
ma non sono incluse nel pacchetto dei testi della chat.

Il testo 2025.2 contiene la parola `quest'anno`: il riferimento e' al 2025.

## Altri anni

I testi 2021-2023 sono gia' presenti in `fonti-locali/2021/SA_21.tex`,
`fonti-locali/2022/SA_22.tex`, `fonti-locali/2023/SA_23.tex`.
Le rispettive prove contengono tre esercizi per anno, inseriti direttamente
nel corpo dei sorgenti. Nei sorgenti 2022 `\\AnnoTest` e' rimasto `2021`:
non alterare gli originali per correggerlo.

## Prossimi passi

1. Leggere `dati/schema-problema.yml` ed esaminare un esempio storico in
   `contenuti/problemi/` prima di decidere la conversione.
2. Separare in file canonici i problemi recuperati, senza cancellare o
   sovrascrivere le fonti locali.
3. Verificare testi, immagini, soluzioni e varianti editoriali.

Le fonti locali restano fuori Git come deciso all'apertura del cantiere.
Questo documento, invece, puo' essere tracciato nel repository come
promemoria stabile del loro recupero.

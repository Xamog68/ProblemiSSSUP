# Integrazione AI dei problemi 2017 — ProblemiSSSUP

Data: 10 novembre 2026.

Fonte: `contenuti/problemi/SA_2017_1.tex`, `_2.tex`, `_3.tex`,
verificati contro il repository pubblico `Xamog68/ProblemiSSSUP`.
Lavoro svolto sui sorgenti canonici, mediante inserimento dei soli campi
`Risposta`, `Aiutino`, `SoluzioneRedazionale` (bozze AI da verificare).
`Testo`, figure e altri campi sono rimasti identici byte per byte.

## Risultati matematici

- **2017.1.** 55 bianche; per il caso generale N >= 2,
  soluzioni se e solo se N e un quadrato, con bianche (N+sqrt(N))/2.
- **2017.2.** Indicando con x il numero di giri con segno della lancetta lunga
  e assumendo solo quanto scritto nel testo, x in (-3,0) oppure (5,8).
  La lancetta non puo essere ferma. In un minuto la lancetta piu veloce
  percorre un angolo in (12,18) oppure (30,48) gradi.
  Se si aggiunge l'ipotesi di rotazione oraria anche per la lancetta lunga,
  resta x in (5,8) e l'intervallo (30,48) gradi.
- **2017.3.** 20 mosse con il vuoto iniziale in (2,1), 18 con il vuoto in (1,2);
  per b=(r,c) il minimo e 18+|r-1|+|c-2|; la media aritmetica delle
  14 configurazioni e 41/2.

## Osservazioni redazionali per futura revisione (non apportate)

1. **2017.2:** il testo non specifica il verso di rotazione della lancetta
   lunga. Per una lettura letterale bisogna includere anche i giri antiorari.
   Chiarire se tutte le lancette devono ruotare in senso orario.
2. **2017.3:** il testo parla di «Valor Medio» senza dire esplicitamente
   che le 14 posizioni iniziali del vuoto siano equiprobabili.
   La risposta 41/2 interpreta quindi «Valor Medio» come media aritmetica.
3. **2017.1:** l'estrazione contemporanea di due palline comporta N >= 2,
   da ricordare nella discussione del caso generale.

## Provenienza e controlli

Tutti i campi integrati recano marcatura `SSSUP-BOZZA-AI` e
`SSSUP-PROVENIENZA`; **non sono soluzioni ufficiali**.
L'integrita dei sorgenti e stata controllata ripristinando i tre
campi vuoti e confrontando i file ottenuti byte per byte con le copie
canoniche iniziali. Verifiche matematiche indipendenti incluse: ricerca
esatta sul grafo dei 210 stati (posizione piastrella speciale,
posizione spazio vuoto), che riproduce il risultato per 2017.3.
Le bozze vanno sottoposte a revisione umana prima della certificazione.

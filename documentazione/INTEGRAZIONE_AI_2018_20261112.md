# ProblemiSSSUP - Integrazione AI 2018

Data: 12 novembre 2026. **Bozze AI da verificare, non soluzioni ufficiali.**

## Fonti e integrita

Sono stati letti i tre sorgenti canonici pubblici del ramo `main`:

```text
https://raw.githubusercontent.com/Xamog68/ProblemiSSSUP/main/contenuti/problemi/SA_2018_1.tex
https://raw.githubusercontent.com/Xamog68/ProblemiSSSUP/main/contenuti/problemi/SA_2018_2.tex
https://raw.githubusercontent.com/Xamog68/ProblemiSSSUP/main/contenuti/problemi/SA_2018_3.tex
```

Per conservare i byte dei sorgenti, la lavorazione usa le copie del pacchetto
`ProblemiSSSUP_testi_2014_2020_revisionati.zip`, gia approvato dall'utente.
Il loro contenuto e stato confrontato con i sorgenti pubblici sopra indicati.
Non si dichiara una verifica del commit remoto o dell'identita binaria di un
download GitHub: l'accesso pubblico ha fornito il contenuto testuale.

Sono stati riempiti soltanto `Risposta`, `Aiutino` e
`SoluzioneRedazionale`. Ripristinando questi tre campi vuoti si ottiene,
per ciascun problema, il file iniziale identico byte per byte.
`Testo`, gli altri campi e l'eventuale materiale grafico non sono stati
modificati. Nei tre problemi 2018 non sono presenti figure.
Ogni campo aggiunto reca i marcatori `SSSUP-BOZZA-AI` e `SSSUP-PROVENIENZA`.

## Stato matematico dei tre problemi

### SA_2018_1 - Banconote

**Soluzione completa nell'interpretazione con tagli interi positivi.**

- Per N=100, tagli 1 e 10 oppure 1 e 11; media minima 9,1.
- Il confronto globale non si limita a cercare vicino a una radice:
  due stime escludono d <= 5 e d >= 21, poi si controllano esattamente
  i quindici valori rimasti.
- Per ogni N >= 2, formula esplicita della media e minimizzazione finita
  su d=2,...,N, con conservazione di tutti gli eventuali ex aequo.
- Il caso N=1 viene trattato separatamente.

L'integralita dei tagli non e scritta espressamente nel Testo:
la soluzione la dichiara, senza modificarlo.

### SA_2018_2 - Patente a punti

**Risultati esatti e limiti con modello temporale dichiarato.**

Ogni persona commette infrazioni periodiche di periodo T, con prima
infrazione in (0,T]. Il recupero viene applicato prima della decurtazione
se coincidono temporalmente. Le fasi non sono specificate dal Testo.

- Due amici: condizione necessaria e sufficiente T >= L/10,
  indipendente dalle fasi nel modello dichiarato.
- n amici, fasi arbitrarie: T >= L/(20-ceil(19/n)) e necessario;
  T >= L/(19-ceil(18/n)) e sufficiente.
- Con infrazioni complessive equidistanti a passo T/n:
  condizione necessaria e sufficiente T >= nL/(19n-18).
- Le dimostrazioni di necessita considerano il primo aumento di punti;
  le strategie sufficienti attribuiscono ciclicamente blocchi di
  19 infrazioni. Non e necessario sfruttare i bonus di due punti.
- Controesempio alla possibilita di ignorare le fasi: n=19 e L=18,5T.
  Infrazioni simultanee: strategia possibile con 19 infrazioni a un amico
  per volta e riposo di 19T. Infrazioni equidistanti: impossibile,
  perche 343T/19 < 18,5T.

La formula del modello equidistante NON va presentata come risposta
incondizionata alla traccia. Le convenzioni alle uguaglianze vanno mantenute.

### SA_2018_3 - Mattonelle

**Soluzione parziale, esplicitamente marcata come tale anche nella Risposta.**
La traccia chiede minimi: non si afferma che bastassero stime ne che i
limiti trovati risolvano integralmente la richiesta.

Modello dichiarato: tagli rettilinei su un pezzo alla volta, niente
impilamento, spessore nullo, riuso dei ritagli, prezzi non negativi.
Le costruzioni sono reticoli paralleli alle pareti senza giunzioni a T.

| Lato | Posa | Mattonelle acquistate | Tagli |
|---|---|---:|---:|
| 9 cm | A: da un angolo | 4489 | 134 |
| 9 cm | B: due fasce opposte da 3 cm | 4467 | 157 |
| 9 cm | C: quattro fasce da 3 cm | 4445 | 181 |
| 9,5 cm | Da un angolo, riuso delle strisce | 3991 | 128 |

I limiti inferiori per area sono 4445 e 3989 mattonelle acquistate.
La posa C dimostra che 4445 e il numero minimo di mattonelle da 9 cm,
ma questo NON dimostra il minimo del costo che comprende anche i tagli.
La posa A e ottima soltanto per la sua specifica disposizione geometrica.

Per i costi globali C9 e C95 si ottiene:

```text
4445*k1 <= C9 <= min(4489*k1+134*k3,
                    4467*k1+157*k3,
                    4445*k1+181*k3)
3989*k2 <= C95 <= 3991*k2+128*k3
```

Le condizioni di convenienza date confrontano un costo realizzabile
con un limite inferiore per la scelta opposta: sono sufficienti,
non una classificazione completa dei parametri.

Per le rotture si dichiara una procedura: tagli indipendenti con
successo p=0,99; pagamento anche dei tagli falliti; tutti i tagli su
una mattonella vengono terminati prima della posa; una rottura provoca
lo scarto dell'intero lotto di quella mattonella. Il costo atteso
per m successi consecutivi e

```text
A_m = [k1 + k3*(1+p+...+p^(m-1))] / p^m.
```

Seguono attese esatte per le tre pose da 9 cm. Non si dichiara ottimale
la procedura di scarto o di taglio. Restano da dimostrare il minimo
globale di costo, il confronto completo fra formati e l'eventuale
minimo atteso. Anche questo limite e scritto nei campi canonici,
non soltanto in questa nota.

## Questioni per una futura revisione redazionale

Nessuna delle modifiche seguenti e stata applicata al Testo.

1. **2018.1:** precisare che i tagli sono interi positivi di Piso.
2. **2018.2:** precisare sincronizzazione o fasi delle infrazioni,
   istante iniziale e ordine fra recupero e decurtazione coincidenti;
   rendere piu trasparenti le regole dei bonus e correggere `decurtarti`.
3. **2018.3:** precisare cosa conta come taglio, l'eventuale impilamento,
   lo spessore di taglio, il riuso dei pezzi, e che cosa viene scartato
   quando una mattonella gia parzialmente tagliata si rompe.
   Per la parte probabilistica, esplicitare indipendenza e costo dei
   tentativi falliti, e distinguere attesa di una posa da minimo atteso.

## Verifiche effettuate

- Compilazione di prova dei tre sorgenti con pdfLaTeX: riuscita,
  8 pagine, nessun `Overfull` segnalato.
- Anteprima PDF renderizzata e controllata visivamente sulle otto pagine.
- Conversione Pandoc dei nove campi aggiunti: riuscita senza avvisi.
- 31.125 confronti esatti fra formula delle banconote e somma diretta.
- 5.490 controlli esatti degli intervalli di riposo, con fasi simultanee,
  uniformi e non uniformi; verifica del controesempio n=19.
- Controllo razionale delle quattro griglie: area, pezzi, acquisti e tagli.
- Controllo esatto delle identita di rinnovo per i costi attesi e
  restituzione dei costi deterministici quando p=1.
- Verifica SHA-256 dell'integrita dei sorgenti al di fuori dei campi aggiunti.

I test sono riproducibili con:

```bash
python3 documentazione/CONTROLLI_AI_2018_20261112.py
```

Il controllo delle impronte si riferisce esattamente a questa versione:
fallira intenzionalmente se i sorgenti vengono successivamente revisionati.
I test aritmetici non sostituiscono la revisione umana delle dimostrazioni.
Non sono stati eseguiti qui il build completo del repository o la
rigenerazione integrale del sito. Il repository remoto non e stato modificato.

## Installazione e rigenerazione

Dalla radice del repository, controllare prima che i sorgenti 2018
non abbiano modifiche locali da conservare, quindi estrarre lo ZIP.
Il pacchetto contiene tre sorgenti completi e questa documentazione.

```bash
cd ~/Projects/ProblemiSSSUP &&
git diff --exit-code HEAD -- contenuti/problemi/SA_2018_*.tex &&
unzip -o ~/Downloads/ProblemiSSSUP_2018_sorgenti_completi_AI.zip &&
git diff --check &&
python3 documentazione/CONTROLLI_AI_2018_20261112.py
```

```bash
make verifica &&
python3 scripts/genera_dati_sito.py --sito sito &&
make sito-check &&
make -f scripts/libro.mk libro
```

I tre sorgenti 2018 non hanno figure: questa integrazione non richiede
la rigenerazione degli SVG. Controllare il diff prima del commit.

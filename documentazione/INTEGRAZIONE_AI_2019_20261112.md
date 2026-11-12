# ProblemiSSSUP - bozze matematiche 2019

**Data:** 12 novembre 2026. **Autore:** ChatGPT (OpenAI).
**Stato:** BOZZE AI DA VERIFICARE. Non sono soluzioni ufficiali ne' contenuti approvati.

## Ambito e fonti

Sono stati letti integralmente i sorgenti canonici pubblicati sul ramo `main`:

- `https://raw.githubusercontent.com/Xamog68/ProblemiSSSUP/main/contenuti/problemi/SA_2019_1.tex`
- `https://raw.githubusercontent.com/Xamog68/ProblemiSSSUP/main/contenuti/problemi/SA_2019_2.tex`
- `https://raw.githubusercontent.com/Xamog68/ProblemiSSSUP/main/contenuti/problemi/SA_2019_3.tex`

La base materiale dei tre file proviene dalla copia gia' disponibile nella
conversazione di `ProblemiSSSUP_testi_2014_2020_revisionati.zip`. Il testo dei
file e' stato confrontato con i sorgenti canonici letti online: non sono
state rilevate differenze di contenuto. Non e' stato acquisito un hash
remoto o un identificativo di commit: le impronte nel JSON riguardano
esclusivamente i file di base e i file prodotti nel pacchetto.

Sono stati riempiti soltanto `Risposta`, `Aiutino`, `SoluzioneRedazionale`.
Ognuno dei nove campi ha i marcatori `SSSUP-BOZZA-AI` e
`SSSUP-PROVENIENZA` riconosciuti dal progetto.
Testo, figure (assenti nei tre sorgenti), SoluzioneUfficiale,
SoluzioniAlternative, Osservazioni, Commenti e tutto il resto sono rimasti
identici byte per byte alla base. Questo e' verificato ripristinando a
vuoto i soli tre campi aggiunti e confrontando l'impronta dell'intero file.

Non sono stati modificati il repository online, i generatori, il sito
o il libro canonico. Il PDF di anteprima e' una compilazione autonoma.

## Risultati e ipotesi

### SA_2019_1 - Guasti dei computer

Modello dichiarato: vita discreta geometrica con probabilita' annua p,
condizionata alla sopravvivenza, e durate indipendenti tra computer.
Per 0 < p <= 1:

- (a) p(1-p)^N/(2-p);
- (b) (1-p)^(N+1)/(2-p);
- (c) p^2(1-p)^3/(3-3p+p^2).

Per p=0 tutti gli eventi hanno probabilita' zero; il limite della formula
(b) per p -> 0 positivo non coincide con il caso p=0. Il caso p=1 e'
trattato esplicitamente, compresa l'esponente zero nel punto (a).

La soluzione segnala che senza indipendenza il Testo non determina le
risposte. Come controesempio, per N=0 durate geometriche identiche
producono guasti simultanei con probabilita' 1.

### SA_2019_2 - Gioco a squadre

(a) Vince A,C quando N non e' multiplo di n+1; altrimenti vince B,D.

(b) Vince B,D. All'inizio di un giro con residuo 22k+16, k>=1:
A dice a, B dice max(1,11-a); dopo la mossa c di C, D dice
22-a-b-c. Ogni giro aggiunge 22. Dopo 22 giri il residuo e' 16.
Se A dice a>=6, B chiude con 16-a; se a<=5, B dice 6-a,
lasciando 10 a C, e D chiude con 10-c.

Il Testo non regola il superamento di N, ma la soluzione NON aggiunge
silenziosamente il divieto: dimostra che, seguendo la strategia vincente,
nessun avversario ha la possibilita' di oltrepassare N. Il risultato vale
anche con una lettura letterale che lasci ammesse quelle mosse.

### SA_2019_3 - Incollamenti

Preliminare: triangolo equilatero, C=1/sqrt(12 sqrt(3)).

(a) Sono classificati entrambi gli incollamenti. La rotazione di 180 gradi
intorno al punto medio del lato comune produce sempre un parallelogramma.
Nell'incollamento speculare si ottiene un triangolo esattamente per un
triangolo rettangolo incollato lungo un cateto; si ottiene un
parallelogramma esattamente per un isoscele incollato lungo la base.

(b) Triangolo rettangolo isoscele, incollato lungo l'ipotenusa;
unione quadrata e P_min=4 sqrt(2A), con A area del singolo pezzo.

(c) Trapezio isoscele che e' meta' di un esagono regolare, tagliato
lungo una diagonale fra vertici opposti: basi 2a,a, lati obliqui a.
Unione esagonale regolare e P_min=4*3^(1/4)*sqrt(A).

Le costanti per sqrt(A)<=C P sono 1/(4 sqrt(2)) e 1/(4*3^(1/4)).
Le costanti per l'area TOTALE S=2A, cioe' sqrt(S)<=C P, sono invece
1/4 e 1/sqrt(8 sqrt(3)). Entrambe le convenzioni sono dichiarate.

La minimalita' nel punto (c) e' dimostrata con l'inviluppo convesso
(al piu' sei vertici) e la disuguaglianza isoperimetrica poligonale.
La soluzione comprende una giustificazione autonoma di tale disuguaglianza:
esistenza di un massimo, esclusione dei vertici degeneri, uguaglianza dei
lati, conciclicita', regolarita'. La dimostrazione include quadrilateri
concavi e non si limita a esibire una configurazione.

## Questioni per una futura revisione dei Testi

Nessuna di queste proposte e' stata applicata ai Testi.

1. 2019.1: esplicitare il carattere condizionato della probabilita' annua,
   il modello discreto e l'indipendenza delle durate dei diversi computer.
2. 2019.2: precisare la regola in caso di superamento di N; la lacuna non
   cambia le strategie vincenti qui dimostrate.
3. 2019.3: distinguere l'area A del singolo pezzo dall'area totale S=2A
   nelle disuguaglianze finali; chiarire che si considerano poligoni semplici.

## Controlli eseguiti

- Integrita' dei sorgenti e marcatori di tutti i nove campi.
- 360 casi razionali per le formule (a),(b) del 2019.1, con code di serie
  geometriche esatte; formula (c) e partizione degli eventi controllate.
- Programmazione dinamica esatta del gioco uniforme per n=2,...,20 e
  N fino a 500; gioco asimmetrico fino a 1000. Questo controllo usa la
  regola standard senza superamento; separatamente viene verificata la
  strategia esplicita, che impedisce materialmente il superamento.
- Verificate tutte le 1650 scelte avversarie nei 22 possibili livelli
  della fase ripetitiva e tutte le chiusure finali.
- Controllate le costanti geometriche e le configurazioni di uguaglianza.
  Controllo algebrico indipendente del limite del quadrilatero su 28822
  quadruple di lati razionali, con 12 casi di uguaglianza.
- Compilazione pdflatex dell'anteprima riuscita, 7 pagine, nessun
  `Overfull`, `Underfull` o avviso nella compilazione finale.
- Rendering e ispezione visiva dell'anteprima.
- Conversione Pandoc dei nove nuovi campi riuscita, senza avvisi.

I controlli finiti non sostituiscono le dimostrazioni o la revisione umana.
La compilazione dell'intero libro e la rigenerazione del sito devono
essere eseguite nella copia locale completa del repository.

## Installazione prudente sul Mac

Lo script non richiede pacchetti Python aggiuntivi. L'opzione
`--verifica-base` controlla l'intero contenuto dei tre file PRIMA
che siano sostituiti, anche in presenza di modifiche gia' committate.
Se il controllo si ferma, non forzare la sostituzione: confrontare le versioni.

```bash
cd ~/Projects/ProblemiSSSUP &&
git diff --exit-code HEAD -- contenuti/problemi/SA_2019_*.tex &&
tmp2019="$(mktemp -d)" &&
unzip -q ~/Downloads/ProblemiSSSUP_2019_sorgenti_completi_AI.zip -d "$tmp2019" &&
python3 "$tmp2019/documentazione/CONTROLLI_AI_2019_20261112.py" --verifica-base . &&
cp "$tmp2019"/contenuti/problemi/SA_2019_*.tex contenuti/problemi/ &&
cp "$tmp2019"/documentazione/* documentazione/ &&
python3 documentazione/CONTROLLI_AI_2019_20261112.py &&
git diff --check
```

```bash
git diff -- contenuti/problemi/SA_2019_*.tex
```

Non ci sono figure in questi tre sorgenti: non e' necessario rigenerare
SVG per questa sola integrazione.

```bash
make verifica &&
python3 scripts/genera_dati_sito.py --sito sito &&
make sito-check &&
make -f scripts/libro.mk libro
```

```bash
git add contenuti/problemi/SA_2019_*.tex \
  documentazione/INTEGRAZIONE_AI_2019_20261112.md \
  documentazione/CONTROLLI_AI_2019_20261112.py \
  documentazione/IMPRONTE_AI_2019_20261112.json \
  sito/dati

git diff --cached --check &&
git diff --cached --stat
```

Dopo il controllo:

```bash
git commit -m "Aggiunte bozze AI per i tre problemi del 2019" &&
git push
```

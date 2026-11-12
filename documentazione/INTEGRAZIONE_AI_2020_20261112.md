# ProblemiSSSUP - Integrazione AI 2020

Data: 12 novembre 2026. Autore dei nuovi campi: ChatGPT (OpenAI).  
Stato: **bozze redazionali AI da verificare, non approvate**.

## Contenuto del pacchetto

- Tre sorgenti completi `contenuti/problemi/SA_2020_1.tex`, `SA_2020_2.tex`, `SA_2020_3.tex`.
- Questa nota, il manifesto SHA-256 e lo script di controllo.
- Il registro cumulativo `documentazione/CAHIER_DOLEANCES_2014_2020.md`.

Sono stati riempiti soltanto `Risposta`, `Aiutino` e `SoluzioneRedazionale`. I marcatori `% SSSUP-BOZZA-AI` e `% SSSUP-PROVENIENZA` sono dentro ciascun campo. Ripristinando a vuoto questi tre campi si recuperano byte per byte i sorgenti di partenza, inclusi Testo, figura PSTricks e altri campi. Nessun file di un'altra annata è incluso come sostituzione.

## Provenienza e limiti della verifica delle basi

Le basi binarie sono quelle del precedente pacchetto `ProblemiSSSUP_testi_2014_2020_revisionati.zip`, già fornito nel progetto. I tre sorgenti canonici effettivi sono stati letti sul ramo `main` del repository pubblico e confrontati nel contenuto con queste basi. Non è disponibile un hash binario scaricato dal remoto: le impronte nel manifesto riguardano i file locali del pacchetto, non un commit GitHub dichiarato come verificato.

Fonti canoniche lette:

- `https://raw.githubusercontent.com/Xamog68/ProblemiSSSUP/main/contenuti/problemi/SA_2020_1.tex`
- `https://raw.githubusercontent.com/Xamog68/ProblemiSSSUP/main/contenuti/problemi/SA_2020_2.tex`
- `https://raw.githubusercontent.com/Xamog68/ProblemiSSSUP/main/contenuti/problemi/SA_2020_3.tex`

Confronto aggiuntivo con le prime due pagine del fascicolo ufficiale `prove_matematica-fisica_a.a._20-21.pdf` caricato dall'utente. Il confronto filologico precedente resta in `ProblemiSSSUP_confronto_ufficiali_2016_2020.md` e non è stato sovrascritto.

## Stato matematico

### 2020.1 - Albero

Risultati dimostrati distinguendo l'unione dei rami finiti dalla sua chiusura. Con alpha=pi, il contatto con il terreno fuori dal tronco avviene per rho>1/sqrt(2) nel primo modello e per rho>=1/sqrt(2) nel secondo. Con alpha=pi/2, H=(1+rho/sqrt(2))/(1-rho^2) per rho<1; per 0<rho<1 è un supremo sul modello non chiuso e un massimo sulla chiusura. Per rho=1 l'altezza è illimitata.

Il punto (c) è trattato in entrambi i modelli. Per la chiusura si usa una formula esplicita con alpha=pi, basata su serie geometriche con segni che riempiono un rettangolo. Per i rami finiti si dà una costruzione separata mediante valori intermedi e un numero finito di passi; la maggiore lunghezza di questo complemento evita di confondere appartenenza e approssimabilità. Nessuna affermazione di minimalità della profondità.

### 2020.2 - Polinomi

Soluzione completa nel modello dichiarato di coefficienti indipendenti e uniformi in [0,1]. Per n pari p_n=0; per n dispari p_n=(n-1)^2/[(2n-1)n^(n/(n-1))]. In particolare p_3=4/(15sqrt(3)), e il limite lungo i gradi dispari è 1/2. La distribuzione congiunta è un'ipotesi esplicitata nella soluzione, non aggiunta al Testo.

### 2020.3 - Aula: bozza dichiaratamente parziale

(a) No per n=1,2; sì per ogni n>=7, con costruzione sfalsata. **Non risolti n=3,4,5,6.**

(b) Costruzione esatta da 13 studenti nell'aula 4x9 m e fascia libera di 2 m; limite superiore elementare 16; miglioramento a 14 mediante un teorema esterno. Quindi **13<=M_*<=14**, senza decisione fra i due valori e senza determinazione dell'aula ottimale. La larghezza 9-4sqrt(3) riguarda solo la costruzione proposta e richiede di chiarire la convenzione sul bordo della fascia; 2 m sono comunque realizzati senza studenti sul bordo.

Il Testo chiede qui ottimi e classificazioni esatti: non si afferma di avere soddisfatto interamente tali richieste. Le lacune sono dichiarate nella Risposta e nella Soluzione, non soltanto in questa nota.

### Risultato esterno usato

J. H. Folkman e R. L. Graham, *A Packing Inequality for Compact Convex Subsets of the Plane*, Canadian Mathematical Bulletin 12 (1969), 745-752, DOI `10.4153/CMB-1969-096-7`.

La disuguaglianza di Oler, per punti con distanze almeno 2 in un convesso di area A e perimetro P, dà m<=A/(2sqrt(3))+P/4+1. È citata e applicata, **non dimostrata nel pacchetto**. L'enunciato della fonte, per distanza 1, è stato controllato anche sulla pagina PDF renderizzata. Non vengono usati record numerici di packing come prove di impossibilità.

Fonte primaria: `https://www.cambridge.org/core/services/aop-cambridge-core/content/view/S000843950005428X`.

## Cahier cumulativo

Il nuovo registro copre tutti i venti problemi 2014-2020 e distingue ambiguità delle fonti, convenzioni, refusi ed errori nostri. Non applica nessuno degli interventi proposti. Include, tra l'altro, la perdita della puntata del 2015.1, la figura errata da noi ricostruita nel 2016.1, i versi dell'orologio, il valor medio delle piastrelle, i modelli temporali delle patenti, i tagli delle mattonelle, l'indipendenza dei guasti, l'area degli incollamenti e le nuove questioni del 2020.

Aggiunge una verifica importante sul 2014.1: nel modello con consumo istantaneo e intervalli chiusi, cinque consumi da 1 kg agli istanti 1,3,5,7,9 soddisfano dieci osservazioni [j,j+1]. La bozza precedente con minimo 6 richiede quindi una convenzione che escluda tale modello. Questa è un'annotazione per la revisione, non una modifica ai campi matematici del 2014.

## Controlli effettuati in questa sessione

1. Verifica delle tre impronte iniziali e delle tre impronte finali.
2. Ricostruzione esatta delle basi eliminando soltanto i contenuti dei tre campi aggiunti; nessuna differenza fuori da essi.
3. Controlli delle serie e soglie del problema 1; programmazione dinamica numerica sulle otto direzioni fino a profondità 16; otto esempi della costruzione finita (c) con aritmetica Decimal a 65 cifre. Sono controlli, non una certificazione automatica delle dimostrazioni.
4. Valori critici dei polinomi verificati con frazioni esatte; integrazione numerica indipendente per sette gradi dispari.
5. Verifica esatta delle distanze nelle configurazioni sfalsate e dei 13 posti nell'aula; controlli algebrici dei limiti superiori. Lo script non dimostra il teorema di Oler.
6. Controllo esatto dell'esempio atomico aggiunto al cahier per il 2014.1.
7. Conversione dei nove campi con Pandoc verso HTML/MathJax, senza errori o messaggi di avviso.
8. Compilazione dell'anteprima autonoma con LaTeX, dvips e Ghostscript: 8 pagine. Controllo visivo delle pagine renderizzate; nessun errore LaTeX o box sovrapposto rilevato.

**Non eseguiti qui:** compilazione dell'intero libro del repository, ricostruzione completa dei dati del sito, aggiornamento del catalogo SVG e push. Il repository online non è stato modificato.

## Installazione e pubblicazione

Il controllo `--verifica-base` va eseguito prima della sostituzione: se le impronte non coincidono, fermarsi e confrontare i file. Controlla anche che un documento omonimo già presente non venga sostituito con contenuto diverso. Non eliminare eventuali note locali per forzare il controllo.

```bash
cd ~/Projects/ProblemiSSSUP &&
git diff --exit-code HEAD -- contenuti/problemi/SA_2020_*.tex &&
tmp2020="$(mktemp -d)" &&
unzip -q ~/Downloads/ProblemiSSSUP_2020_sorgenti_completi_AI.zip -d "$tmp2020" &&
python3 "$tmp2020/documentazione/CONTROLLI_AI_2020_20261112.py" --verifica-base . &&
cp "$tmp2020"/contenuti/problemi/SA_2020_*.tex contenuti/problemi/ &&
cp "$tmp2020"/documentazione/* documentazione/ &&
python3 documentazione/CONTROLLI_AI_2020_20261112.py &&
git diff --check
```

Controllare le differenze con `git diff -- contenuti/problemi/SA_2020_*.tex` e leggere il cahier. In questa annata c'è una figura: anche se il disegno è invariato, il catalogo del progetto usa l'impronta dell'intero sorgente. Va quindi aggiornato con il flusso completo prima di rigenerare il sito.

```bash
make verifica &&
python3 scripts/genera_figure_svg_massivo.py &&
python3 scripts/installa_figure_svg.py --applica &&
python3 scripts/genera_dati_sito.py --sito sito &&
make sito-check &&
make -f scripts/libro.mk libro
```

Infine, dopo la revisione delle differenze:

```bash
git add contenuti/problemi/SA_2020_*.tex \
  documentazione/INTEGRAZIONE_AI_2020_20261112.md \
  documentazione/CONTROLLI_AI_2020_20261112.py \
  documentazione/IMPRONTE_AI_2020_20261112.json \
  documentazione/CAHIER_DOLEANCES_2014_2020.md \
  sito/dati sito/assets/figure

git diff --cached --check &&
git diff --cached --stat
```

```bash
git commit -m "Aggiunte bozze AI 2020 e cahier redazionale 2014-2020" &&
git push
```

Questo conclude la disponibilità di una prima bozza per i venti problemi recuperati, **non la verifica matematica definitiva né il completamento di tutte le parti rimaste aperte nelle bozze**.

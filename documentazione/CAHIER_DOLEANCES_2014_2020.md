# ProblemiSSSUP - Cahier de doléances 2014-2020

**Aggiornamento:** 12 novembre 2026.  
**Stato:** registro redazionale cumulativo, preparato con assistenza AI; da discutere e verificare.  
**Ambito:** i 20 problemi recuperati dal 2014 al 2020. Nessuna annotazione in questo documento autorizza una modifica automatica del Testo o delle figure.

## Come leggere questo registro

Distinguiamo quattro tipi di annotazione:

- **A - Ambiguità sostanziale:** letture diverse possono cambiare la risposta matematica.
- **C - Convenzione da esplicitare:** modello usuale o precisazione utile, non necessariamente un errore dell'autore.
- **R - Refuso della fonte:** questione testuale o tipografica, con provenienza distinta.
- **N - Errore nostro:** introdotto nella trascrizione o nella ricostruzione grafica; non va attribuito all'originale.

Un problema non diventa ben posto semplicemente perché si adotta tacitamente una delle interpretazioni. Le bozze devono dichiarare le ipotesi aggiuntive; eventuali versioni redazionali dei Testi saranno approvate separatamente. Al contrario, non ogni convenzione scolastica implicita costituisce un difetto grave: le voci C sono anche promemoria prudenziali.

**Fonti:** Testi canonici in `contenuti/problemi/`; archivio storico `2014-2020.zip`; confronto del 10 novembre in `documentazione/ProblemiSSSUP_confronto_ufficiali_2016_2020.md`; note di integrazione AI delle singole annate; fascicoli ufficiali 2016-2020 forniti dall'utente. Per il 2014 e 2015 non è stato completato il confronto con un nuovo download ufficiale. Il PDF storico del 2015 è invece disponibile. Questo registro non sostituisce la conservazione delle fonti.

## Copertura dei venti problemi

| Problema | Tema | Esito della ricognizione redazionale |
|---|---|---|
| 2014.1 | Mangiatore e giudici | A: consumo istantaneo ed estremi degli intervalli; C: osservazione continuativa |
| 2014.2 | Biglietto ferroviario | Nessuna lacuna sostanziale rilevata; C: prezzi reali o in centesimi |
| 2014.3 | Uomo nero | C: struttura del mazzo e uniformità delle pescate |
| 2015.1 | Scommesse | A: guadagno/perdita e capitale; C: moneta equa e indipendente |
| 2015.2 | Cablaggio | A/C: prese libere, alimentazione e modello dei collegamenti; N: virgolette finali |
| 2016.1 | Rastrelliere | N: figura ricostruita non fedele; C: modello elettrico |
| 2016.2 | Quadrati sul cerchio | Nessuna lacuna sostanziale rilevata: sono richieste stime |
| 2016.3 | Lotteria | C: prezzo prima o dopo aver osservato il trasferimento |
| 2017.1 | Urna | C: dominio di N e campionamento uniforme senza reinserimento |
| 2017.2 | Orologio | A: verso della lancetta lunga |
| 2017.3 | Piastrelle scorrevoli | A/C: significato del valor medio |
| 2018.1 | Banconote | A/C: tagli interi positivi |
| 2018.2 | Patenti | A: fasi temporali, eventi simultanei e recuperi; R: decurtarti |
| 2018.3 | Mattonelle | A: tagli, riutilizzo, rotture e costi attesi |
| 2019.1 | Computer | A: modello dei guasti e indipendenza |
| 2019.2 | Gioco a squadre | A: superamento del traguardo, non decisivo per le strategie proposte |
| 2019.3 | Incollamenti | A: area del pezzo o dell'unione; R: refuso già corretto |
| 2020.1 | Albero | A: rami finiti o chiusura, massimo o supremo; R: cui omesso nell'ufficiale |
| 2020.2 | Polinomi | A: distribuzione congiunta dei coefficienti |
| 2020.3 | Distanziamento | C/A: dominio di n e significato della striscia; ottimizzazione non ristretta alle griglie |

## 2014

### SA_2014_1 - Mangiatore

**A, priorità alta.** Il testo consente di mangiare quanto si vuole in quanto tempo si vuole. Occorre distinguere una funzione cumulativa continua da un modello che ammetta quantità positive concentrate in un istante. Con masse istantanee diventa decisiva anche l'inclusione degli estremi degli intervalli di osservazione.

**Esempio concreto:** dieci giudici osservano rispettivamente gli intervalli chiusi [0,1], [1,2], ..., [9,10]. Il concorrente consuma istantaneamente 1 kg agli istanti 1, 3, 5, 7, 9. Ogni giudice vede esattamente 1 kg e la copertura è completa, ma il totale è 5 kg. Questo basta a mostrare che il minimo di 6 kg della bozza precedente non può essere presentato senza una convenzione che escluda tale modello. Non si sta qui dichiarando il minimo globale del modello atomico.

**C.** Precisare inoltre che ciascun giudice osserva per un intervallo continuo di un'ora, interamente contenuto nelle dieci ore della gara, non per un insieme di tempi di misura totale un'ora.

**Proposta:** fissare una funzione cumulativa continua non decrescente, intervalli di osservazione di lunghezza 1 contenuti in [0,10], e consumo nullo nei singoli istanti. Rivedere la formulazione delle ipotesi prima di approvare definitivamente la bozza matematica. Nessuna modifica applicata ora.

### SA_2014_2 - Toscolandia

La preferenza per il treno a parità di costo è già esplicita: **non va inserita fra le omissioni**.

**C, secondaria.** Dichiarare eventualmente p>0 e il dominio della distanza d. Separare il modello con prezzo reale dall'eventuale variante con centesimi interi. La scelta di arrotondare al centesimo è una variante applicativa, non un vincolo presente nel testo. Nessuna altra ambiguità sostanziale identificata in questa ricognizione.

### SA_2014_3 - Uomo nero

**C.** La riduzione a coppie residue più un jolly usa un mazzo con molteplicità pari per ogni valore e un solo jolly. Rendere esplicita l'equiprobabilità delle carte pescate, condizionatamente alla mano corrente. Per la generalizzazione in n si può descrivere direttamente lo stato con n coppie residue e il jolly, evitando dipendenze dalla dimensione di un particolare mazzo commerciale. Sono precisazioni del modello usuale, non errori di trascrizione accertati.

## 2015

### SA_2015_1 - Testa o croce

**A, priorità alta, segnalazione esplicita dell'utente.** Non è detto chiaramente che con croce si perde la stessa cifra puntata. La locuzione scommettere su testa non sostituisce la definizione del saldo. Il difetto è già nel PDF storico, non è stato introdotto nella trascrizione.

**Proposta di frase:** prima di ogni lancio si sceglie una puntata di 1 oppure 2 euro; con testa il saldo aumenta della puntata, con croce diminuisce della stessa quantità.

**A/C collegate:** saldo netto iniziale zero; ammissibilità delle perdite intermedie e assenza di vincoli di capitale; moneta equa e lanci indipendenti. La condizione di effettuare esattamente n lanci è invece già presente: non inventare un'opzione di arresto.

**R:** il refuso storico stategia è già stato corretto in strategia nel canonico. Conservare tale correzione. Il chiarimento del modello resta da approvare e applicare.

### SA_2015_2 - Cablaggio

**A/C.** Contano le prese effettivamente alimentate e libere, non quelle occupate dalle spine dei collegamenti. Precisare il ruolo delle triple in cascata, le connessioni consentite e il fatto che i cavi non sono essi stessi prese. Le lunghezze sono non negative, non numeri reali arbitrari anche negativi.

**N, da correggere.** Le virgolette di chiusura dell'esempio finale sono presenti nel PDF storico e sono state perse nella nostra trascrizione. Non attribuire il difetto alla fonte.

Il commento finale **ammette espressamente costruzioni approssimate con copertura garantita** e apprezza una stima della distanza dall'ottimo. Non trasformare questa richiesta in un obbligo di determinare ogni ottimo esatto.

## 2016

### SA_2016_1 - Rastrelliere

**N, priorità alta.** La figura PSTricks ricostruita ha introdotto una separazione fra le basi e una quota l fra i bordi interni. La figura ufficiale mostra invece le basi affiancate: l è sia la larghezza delle basi sia la distanza fra gli assi, coerentemente con il testo. La precedente attribuzione della discrepanza all'originale era sbagliata: **l'errore è nostro**.

**Intervento futuro:** correggere la ricostruzione grafica, non adattare il Testo alla figura sbagliata. Mantenere la distanza fra gli assi usata dalla bozza matematica. Questo pacchetto 2020 non modifica la figura del 2016.

**C.** Rendere esplicito, se necessario, il modello delle connessioni: ciascun carico alimentato da una presa, al massimo due carichi per presa; nessuna combinazione di alimentazioni diverse per aggirare la capacità. Per n dispari il testo consente già un'analisi qualitativa: non confondere tale concessione con un'omissione.

### SA_2016_2 - Copertura del cerchio

Non è emersa una lacuna sostanziale. I quesiti chiedono stime, anche per i raggi copribili con pochi quadrati. Le costruzioni non devono essere chiamate ottime senza una prova, ma non è necessario dimostrarne l'ottimalità per soddisfare quelle richieste. Le sovrapposizioni sono espressamente ammesse.

### SA_2016_3 - Lotteria

**C.** Nel secondo punto chiarire che il prezzo è stabilito prima di conoscere la pallina trasferita e che la media comprende anche tale scelta casuale. Se il numero trasferito fosse osservato prima di stabilire il prezzo, si avrebbe invece un prezzo condizionato a quel numero. L'eventuale arrotondamento ai centesimi va distinto dal prezzo reale di pareggio. Nessun cambiamento applicato.

## 2017

### SA_2017_1 - Urna

**C.** Nel caso generale occorre N intero e N>=2, altrimenti non si possono estrarre due palline. La lettura usuale è una scelta uniforme di due palline distinte, senza reinserimento. Precisazioni minori di ammissibilità, non una nuova soluzione del problema.

### SA_2017_2 - Orologio

**A.** Il verso orario è specificato per la lancetta corta; quello della lunga non è fissato. La lettura letterale permette anche il moto antiorario. La bozza tratta entrambe le interpretazioni: una revisione deve dichiarare se si ammettono velocità angolari con entrambi i segni oppure solo il verso orario. Non restringere il modello silenziosamente.

### SA_2017_3 - Piastrelle scorrevoli

**A/C.** Il Valor Medio richiesto deve essere definito come media aritmetica sui 14 possibili posti iniziali del vuoto, diversi da (1,1), oppure mediante l'ipotesi che tali posti siano equiprobabili. La semplice possibilità di trovarsi in ogni casella non assegna una distribuzione. La bozza usa la media aritmetica. Eventualmente precisare che l'adiacenza è per un lato, non per un vertice.

## 2018

### SA_2018_1 - Banconote

**A/C.** I prezzi sono interi, ma non è dichiarato altrettanto esplicitamente che i tagli siano interi positivi. La bozza lavora in questo modello e ne trae che uno dei due tagli deve essere 1. La convenzione va esplicitata prima di trasformare quell'argomento in un'affermazione non qualificata. Per N=1 trattare separatamente la banalità del problema e l'eventuale inutilità del secondo taglio.

### SA_2018_2 - Patenti a punti

**A, priorità alta.** Un'infrazione ogni T per ciascuna persona non specifica le fasi delle successioni temporali: simultanee, equidistanti complessivamente, oppure sfalsate in altro modo. Vanno inoltre precisati il primo evento e l'ordine fra recupero, bonus e decurtazione quando cadono nello stesso istante. Chiarire anche se e come si ripetono i bonus dopo intervalli successivi senza infrazioni.

La formula della bozza per n amici, T>=nL/(19n-18), è dichiarata nel modello delle infrazioni complessive equidistanti, **non come risposta incondizionata**. Il caso n=19, L=18,5T discusso nella nota 2018 mostra che sincronizzare gli eventi può cambiare la possibilità di evitare le sospensioni. La soglia di uguaglianza richiede una convenzione sugli eventi coincidenti.

**R.** Decurtarti al posto di decurtati compare anche nel fascicolo ufficiale: refuso della fonte, da correggere nella futura revisione.

### SA_2018_3 - Mattonelle

**A, priorità alta.** Definire un taglio: rettilineo o arbitrario, su un pezzo alla volta o su mattonelle sovrapposte, con spessore trascurabile o perdita di materiale. Precisare quali ritagli siano riutilizzabili e come le condizioni di contatto per un lato intero si applichino ai ritagli lungo i bordi. Non introdurre tacitamente un vincolo di posa a griglia parallela alle pareti se non è dimostrato o dichiarato.

Nel punto probabilistico occorre dire se le rotture dei tagli sono indipendenti, se un tentativo fallito costa comunque k3, e cosa si butta quando una mattonella già tagliata si rompe: solo il pezzo in lavorazione oppure anche ritagli precedentemente prodotti. Specificare quando si può decidere di cambiare procedimento dopo una rottura.

**Distinzione matematica, non refuso:** minimo numero di mattonelle acquistate, minimo costo con i tagli, costo atteso di una procedura e minimo costo atteso sono quattro quantità diverse. La bozza 2018 resta parziale sull'ottimizzazione globale; le attese calcolate riguardano procedure dichiarate. Nessuna delle convenzioni aggiuntive è stata inserita nel Testo.

## 2019

### SA_2019_1 - Guasti dei computer

**A.** Il modello usato è discreto: p è la probabilità di guasto in un anno condizionata al fatto che il computer funzioni ancora all'inizio di quell'anno. Le durate dei computer sono indipendenti. Il testo non esplicita queste ipotesi, indispensabili per le formule proposte. Allineare la convenzione sugli anni di installazione e di primo possibile guasto; N è un intero non negativo. Il caso p=0 va trattato separatamente, senza sostituirlo in formule ottenute dopo divisioni per p.

### SA_2019_2 - Gioco a squadre

**A.** Non è detto cosa accada se la somma supera N. Dichiarare una regola per rendere il gioco definito anche fuori dalle strategie vincenti. Le strategie proposte nella bozza impediscono tuttavia il superamento anche agli avversari: questa omissione non modifica quei risultati. Non attribuire al Testo un divieto di superamento che esso non contiene.

### SA_2019_3 - Incollamenti

**A, priorità alta.** Distinguere l'area A del singolo triangolo o quadrilatero dall'area totale S=2A dopo l'incollamento. Le costanti nella disuguaglianza fra radice dell'area e perimetro cambiano di un fattore sqrt(2) se si scambiano le convenzioni. La bozza riporta entrambe, senza riscrivere il Testo.

**C.** Specificare figure semplici, non degeneri, con interni disgiunti dopo l'incollamento, e perimetro della figura unione. Parte di queste condizioni è già nel Testo: la revisione deve chiarire, non duplicare inutilmente.

**R, già risolto nel canonico.** Quadrilareri era nel sorgente storico; quadrilateri compare nel PDF ufficiale e nel canonico. Conservare la correzione, non reintrodurre il refuso in nome della fedeltà a una bozza.

## 2020

### SA_2020_1 - Albero infinito

**A, priorità alta.** Distinguere l'unione T di tutti i segmenti di profondità finita dalla sua chiusura. Per alpha=pi e rho=1/sqrt(2), T non incontra il terreno fuori dal tronco, mentre la chiusura contiene, per esempio, (sqrt(2),0). L'estremo critico della risposta (a) cambia quindi a seconda della definizione.

Nel punto (b), per 0<rho<1 l'altezza indicata dalla bozza è un supremo non raggiunto su T, ma un massimo sulla chiusura. Per rho=1 l'altezza non è limitata. Il termine altezza massima non deve nascondere queste distinzioni.

Nel punto (c) la bozza 2020 prova che ogni punto appartiene a qualche albero **in entrambe le interpretazioni**: la formula semplice con alpha=pi e rho=sqrt(M/(M+1)) garantisce l'appartenenza alla chiusura; una costruzione separata, generalmente con un altro rho, raggiunge il punto su un ramo finito. Non identificare una prova di approssimabilità con una prova di appartenenza.

**C.** Fissare origine del tronco e terreno; definire le svolte come rotazioni di +/-alpha/2; chiarire il significato degli angoli per alpha>pi. Dichiarare che i rami non si arrestano a terra o alle intersezioni e che la profondità è genealogica, non una distanza minima nella figura con intersezioni. Queste sono convenzioni di modello, non modifiche eseguite.

**R, da non importare.** Il PDF ufficiale omette cui nella frase sul ramo da cui si origina un altro ramo. Il sorgente storico e il canonico sono corretti: conservarli, documentando la variante.

### SA_2020_2 - Polinomi casuali

**A.** Scelti a caso non determina una distribuzione congiunta. La bozza assume a,b uniformi e indipendenti in [0,1]. Anche marginali entrambe uniformi non bastano: scegliendo b=a si ottiene probabilità zero, diversa dalla formula del modello indipendente. Esplicitare la scelta uniforme nel quadrato unitario. Nessuna modifica del Testo.

### SA_2020_3 - Distanziamento nell'aula

**C/A.** Specificare n intero positivo. Nel punto (b), definire la striscia come fascia lungo l'intera lunghezza di uno dei lati e precisare se il bordo che la separa dai banchi può ospitare studenti. La bozza da 13 studenti lascia libera anche la striscia chiusa larga 2 m, quindi non dipende da quest'ultima convenzione per la sua fattibilità.

La domanda sulla larghezza della striscia può avere più risposte se si ottimizza solo il numero di studenti. Un eventuale secondo criterio di massimizzazione della larghezza va dichiarato, non aggiunto tacitamente. Analogamente, non è dato alcun vincolo a usare griglie regolari: un'ottimalità dimostrata solo fra griglie non sarebbe un'ottimalità globale.

**Non è un'autorizzazione a sostituire l'ottimo con una stima:** il Testo chiede qui una classificazione e un massimo. La bozza dichiara esplicitamente ciò che non risolve; vedere il registro matematico sotto.

## Questioni matematiche separate dalla revisione del Testo

Questa sezione evita di confondere un enunciato ambiguo con una dimostrazione ancora mancante.

| Problema | Stato da tenere visibile |
|---|---|
| Tutte le annate | I contributi AI sono bozze da verificare, non soluzioni certificate o approvate per il solo fatto di essere pubblicate. |
| 2014.1 | La convenzione sul consumo istantaneo va definita prima di approvare il minimo 6 della bozza. |
| 2015.2 e 2016.2 | Le stime dichiarate sono compatibili con le richieste; non pretendere ottimi non richiesti. |
| 2016.1, n dispari | Il testo ammette un'analisi qualitativa; restano distinti risultati esatti e limiti. |
| 2018.2 | Risultati subordinati alle convenzioni temporali dichiarate. |
| 2018.3 | Non dimostrati gli ottimi globali di costo e costo atteso; procedure e limiti sono espliciti. |
| 2020.3(a) | Dimostrato no per n=1,2 e sì per n>=7. Non risolti nella bozza n=3,4,5,6. |
| 2020.3(b) | 13 studenti realizzabili; al più 14 mediante il teorema esterno di Oler. Non deciso fra 13 e 14, né individuate tutte le aule ottimali. |

## Interventi da approvare

Prima separare gli errori nostri (figura 2016.1 e virgolette 2015.2) dalle riscritture dei testi originali. Poi discutere le ambiguità sostanziali ad alta priorità, conservando una traccia delle ipotesi usate nelle soluzioni. Ogni intervento futuro dovrebbe registrare formulazione precedente, nuova formulazione, motivo, eventuale effetto sulla soluzione e stato di approvazione.

**Nessun Testo e nessuna figura sono stati modificati per produrre questo registro.** La ricognizione copre tutti i venti problemi, ma non pretende di escludere che una revisione successiva ne individui altre ambiguità.

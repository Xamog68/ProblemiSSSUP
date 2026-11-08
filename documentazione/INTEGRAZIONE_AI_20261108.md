# ProblemiSSSUP - Integrazione dei campi mancanti

**Data:** 8 novembre 2026. **Autore delle nuove redazioni:** ChatGPT. **Stato di tutte le aggiunte:** bozze AI da verificare.

## 1. Risultato

Sono stati esaminati i 96 sorgenti canonici dello ZIP ricevuto. Sono stati aggiunti **82 blocchi di contenuto** in **43 file**; gli altri **53 file sono identici byte per byte** alla fotografia in ingresso.

| Campo | Aggiunte | Regola applicata |
|---|---:|---|
| `Risposta` | 24 | Riempito solo se assente, vuoto o composto da un segnaposto senza contenuto. |
| `Aiutino` | 18 | Stessa regola. |
| `SoluzioneRedazionale` | 40 | Aggiunta solo quando `SoluzioneUfficiale` non contiene una soluzione. |
| `Testo`, `SoluzioneUfficiale`, `SoluzioniAlternative`, `Osservazioni`, `Commenti` | 0 modifiche | Conservati integralmente, inclusi i commenti e la formattazione. |

Non sono stati riscritti campi parzialmente compilati: un campo contenente qualcosa oltre ai segnaposto è stato conservato tutto. La copertura per campi non certifica quindi la completezza di ogni sottodomanda dei materiali preesistenti.

Dopo l'integrazione tutte le 96 macro `Risposta` e tutte le 96 macro `Aiutino` contengono materiale. Restano 56 campi storici `SoluzioneUfficiale` con contenuto; i 40 problemi senza tale contenuto hanno ora una `SoluzioneRedazionale`. Questo è un censimento editoriale, **non una certificazione matematica**.

Non sono stati prodotti nuovi testi di prove mancanti, nuove soluzioni alternative, osservazioni o disegni. Le figure esistenti e i due promemoria di ricostruzione restano esattamente com'erano. Gli anni 2014-2020 non sono stati ricostruiti.

## 2. Provenienza e convenzioni

Ogni nuovo campo contiene un commento nella forma:

```latex
% SSSUP-BOZZA-AI: Risposta; autore=ChatGPT; data=2026-11-08; stato=DA-VERIFICARE
% SSSUP-PROVENIENZA: AI: elaborazione nuova dal testo
```

Il nome del campo cambia in `Aiutino` o `SoluzioneRedazionale` dove necessario. Nei contributi basati su appunti o su materiale preesistente cambia anche la descrizione della provenienza. Questi marcatori sono visibili nel sorgente; non vengono automaticamente stampati o mostrati dal sito attuale.

Le soluzioni nuove sono aggiunte in coda mediante:

```latex
\providecommand{\SoluzioneRedazionale}{}
\renewcommand{\SoluzioneRedazionale}{
% SSSUP-BOZZA-AI: SoluzioneRedazionale; ...
...
}
```

Non è stato cambiato il nome tecnico `SoluzioneUfficiale`: esso resta una convenzione ereditata e **non significa che il materiale preesistente sia ufficiale o certificato**.

Il manifesto `dati/integrazioni_ai/20261108.json` registra, per tutti i 96 problemi, le impronte SHA-256 prima e dopo, i campi aggiunti, le fonti e le note. Permette di distinguere i contributi senza dedurne la provenienza dalla formulazione matematica.

### Appunti e figure ricevuti

| Problema | Fonte utilizzata | Tipo di lavoro nuovo |
|---|---|---|
| 1997.4, 1997.5 | Soluzione già presente nel sorgente canonico | Sintesi per il solo campo Risposta mancante. |
| 2024.1 | `2024/SSSUP_2024-P1.pdf` | Rielaborazione degli appunti; esplicitata la convenzione sui raggi tangenti. |
| 2024.2 | `2024/squares.pdf` | Soluzione elaborata ex novo, utilizzando la geometria della figura. |
| 2024.3 | `2024/SSSUP_2024-P3.pdf` | Trascrizione ragionata e sviluppo degli appunti. |
| 2025.1 | `2025/Soluzione_P1.tex` | Rielaborazione della soluzione fornita. |
| 2025.2 | `2025/Soluzione_P2.pdf` | Rielaborazione degli appunti e verifica enumerativa del calendario. |
| 2025.3 | `2025/Soluzione_P3.pdf` | Rielaborazione dei punti (a)-(c); costruzione AI nuova per (d). |
| 2026.1 | `2026/PI_ChatGPT_umana.pdf` | Rielaborazione e controllo dei casi di uguaglianza. |
| 2026.2 | `2026/P2_ChatGPT.pdf` | Rielaborazione, precisazione delle ipotesi e del limite inferiore. |
| 2026.3 | `2026/P3_ChatGPT-1.pdf` | Rielaborazione, correzione di conti nella nuova stesura e distinzione tra modelli di strategia. |

I file originali degli appunti non sono stati modificati. I DOCX/RTF e il foglio di correzione del 2025 non sono stati usati come soluzioni matematiche e non sono inclusi nel pacchetto. Non sono allegati documenti amministrativi o dati di candidati.

Le integrazioni non elencate in questa tabella sono elaborazioni AI a partire dall'enunciato canonico. Non sono state importate soluzioni dal web.

## 3. Inventario delle aggiunte per problema

Una voce `conservato` significa che il campo non è stato modificato; non implica che sia stato riesaminato o approvato.

| Problema | Risposta | Aiutino | Soluzione redazionale | Base delle nuove aggiunte |
|---|---|---|---|---|
| 1996.1 | Bozza AI | Conservato | Non aggiunta: soluzione preesistente | Elaborazione AI dal testo |
| 1997.4 | Bozza AI | Conservato | Non aggiunta: soluzione preesistente | Sintesi del materiale preesistente |
| 1997.5 | Bozza AI | Conservato | Non aggiunta: soluzione preesistente | Sintesi del materiale preesistente |
| 1998.1 | Conservato | Conservato | Aggiunta | Elaborazione AI dal testo |
| 1998.2 | Conservato | Conservato | Aggiunta | Elaborazione AI dal testo |
| 1998.3 | Bozza AI | Conservato | Aggiunta | Elaborazione AI dal testo |
| 1998.4 | Conservato | Conservato | Aggiunta | Elaborazione AI dal testo |
| 1998.5 | Conservato | Conservato | Aggiunta | Elaborazione AI dal testo |
| 1998.6 | Conservato | Conservato | Aggiunta | Elaborazione AI dal testo |
| 1999.1 | Conservato | Conservato | Aggiunta | Elaborazione AI dal testo |
| 1999.2 | Conservato | Conservato | Aggiunta | Elaborazione AI dal testo |
| 1999.3 | Conservato | Conservato | Aggiunta | Elaborazione AI dal testo |
| 1999.4 | Bozza AI | Conservato | Aggiunta | Elaborazione AI dal testo |
| 2000.1 | Conservato | Conservato | Aggiunta | Elaborazione AI dal testo |
| 2000.2 | Conservato | Conservato | Aggiunta | Elaborazione AI dal testo |
| 2000.3 | Conservato | Conservato | Aggiunta | Elaborazione AI dal testo |
| 2000.4 | Conservato | Conservato | Aggiunta | Elaborazione AI dal testo |
| 2001.1 | Conservato | Conservato | Aggiunta | Elaborazione AI dal testo |
| 2001.2 | Conservato | Conservato | Aggiunta | Elaborazione AI dal testo |
| 2001.3 | Bozza AI | Conservato | Aggiunta | Elaborazione AI dal testo |
| 2001.4 | Conservato | Conservato | Aggiunta | Elaborazione AI dal testo |
| 2003.1 | Conservato | Conservato | Aggiunta | Elaborazione AI dal testo |
| 2003.2 | Conservato | Conservato | Aggiunta | Elaborazione AI dal testo |
| 2003.3 | Conservato | Conservato | Aggiunta | Elaborazione AI dal testo |
| 2003.4 | Conservato | Conservato | Aggiunta | Elaborazione AI dal testo |
| 2021.1 | Bozza AI | Bozza AI | Aggiunta | Elaborazione AI dal testo |
| 2021.2 | Bozza AI | Bozza AI | Aggiunta | Elaborazione AI dal testo |
| 2021.3 | Bozza AI | Bozza AI | Aggiunta | Elaborazione AI dal testo |
| 2022.1 | Bozza AI | Bozza AI | Aggiunta | Elaborazione AI dal testo |
| 2022.2 | Bozza AI | Bozza AI | Aggiunta | Elaborazione AI dal testo |
| 2022.3 | Bozza AI | Bozza AI | Aggiunta | Elaborazione AI dal testo |
| 2023.1 | Bozza AI | Bozza AI | Aggiunta | Elaborazione AI dal testo |
| 2023.2 | Bozza AI | Bozza AI | Aggiunta | Elaborazione AI dal testo |
| 2023.3 | Bozza AI | Bozza AI | Aggiunta | Elaborazione AI dal testo |
| 2024.1 | Bozza AI | Bozza AI | Aggiunta | Appunti forniti e sviluppo AI |
| 2024.2 | Bozza AI | Bozza AI | Aggiunta | Enunciato e figura; soluzione nuova |
| 2024.3 | Bozza AI | Bozza AI | Aggiunta | Appunti forniti e sviluppo AI |
| 2025.1 | Bozza AI | Bozza AI | Aggiunta | Appunti forniti e sviluppo AI |
| 2025.2 | Bozza AI | Bozza AI | Aggiunta | Appunti forniti e sviluppo AI |
| 2025.3 | Bozza AI | Bozza AI | Aggiunta | Appunti forniti e sviluppo AI |
| 2026.1 | Bozza AI | Bozza AI | Aggiunta | Appunti forniti e sviluppo AI |
| 2026.2 | Bozza AI | Bozza AI | Aggiunta | Appunti forniti e sviluppo AI |
| 2026.3 | Bozza AI | Bozza AI | Aggiunta | Appunti forniti e sviluppo AI |

## 4. Punti da sottoporre prioritariamente a revisione

### Conflitti con campi preesistenti, lasciati intatti

**1998.6.** La risposta ricevuta contiene nel tratto intermedio `1+q^3/3`, mentre il costo marittimo dell'enunciato porta a `1+q^2/3`. La nuova soluzione espone il secondo risultato. Il vecchio campo Risposta non è stato corretto.

**2000.2.** Le formule della risposta ricevuta non coincidono con quelle ricavate nella nuova soluzione mediante le tangenti comuni ai due cerchi. Per l'ombra totale interviene `R-r`; per il bordo esterno della penombra interviene `R+r`, con i rispettivi denominatori. La nuova derivazione è esplicita e le vecchie formule sono rimaste intatte. Prima di pubblicare insieme risposta e soluzione occorre risolvere questo conflitto.

Queste segnalazioni sono emerse durante la scrittura dei campi mancanti: non costituiscono una revisione sistematica dei contenuti già presenti.

### Risultati nuovi o interpretazioni particolarmente sensibili

**2022.3.** La soluzione propone una riduzione rigorosa dei percorsi a tratti esterni, archi e corde, con una distanza concava sul cerchio. Il risultato è stato confrontato anche con una ricerca numerica sugli ingressi e sulle uscite, ma il lemma geometrico va riesaminato indipendentemente.

**2024.1.** La bozza ricevuta considera illuminati anche i punti raggiunti da una tangente. La soglia del punto (a) è allora `h >= 1`; con illuminazione stretta diventa `h > 1`. La convenzione è dichiarata nella nuova risposta e nella soluzione, senza modificare il testo.

**2024.2.** La soluzione usa il meccanismo di aperture sincrone rappresentato in `squares.pdf`. Va verificato che questa sia esattamente la famiglia di configurazioni intesa dall'enunciato. Si ottengono `P=4+8s`, `A=8s^2+1`, con `s=cos(theta)+sin(theta)`, e raggio massimo `sqrt(7/2+sqrt(10))`.

**2025.2(a).** Il rapporto `221/365` è una percentuale attesa sotto l'ipotesi di date di nascita uniformi; la percentuale empirica dei candidati non è determinata dal solo testo. Il riferimento a "quest'anno" resta il 2025.

**2025.3(d).** Gli appunti ricevuti non sviluppavano questo punto. La nuova bozza propone il pentagono `0 <= y <= 1`, `0 <= x <= 19/10`, `x+y <= 2`, di area `299/200 < 3/2`, con una verifica separata per rettangoli sottili e non sottili. È un contributo AI nuovo, non una trascrizione del manoscritto.

**2026.3(d).** Per una strategia deterministica di B, o interpretando B come giocatore ottimale, la probabilità di vittoria non può essere `1/2`. Permettendo una randomizzazione deliberatamente non ottimale, invece, si può ottenere esattamente `1/2`. La risposta espone entrambe le letture.

### Registro completo delle precisazioni

**1998.2**

La conclusione presuppone due corde distinte, come normalmente inteso; due copie della stessa corda non la implicano.

**1998.5**

Ipotesi da precisare: n=-1 e un controesempio se il dominio comprende gli interi negativi; la formula vale per ogni dispari diverso da -1.

**1998.6**

Conflitto segnalato, non corretto: la Risposta preesistente contiene 1+q^3/3 nel tratto intermedio; dal testo e dal calcolo deriva 1+q^2/3.

**2000.2**

Conflitto con le formule preesistenti di Risposta, lasciate intatte: il bordo dell'ombra totale usa R-r e sqrt(d^2-(R-r)^2); il bordo esterno della penombra usa R+r. Le aree nella nuova bozza sono ricavate dalle due famiglie di tangenti.

**2000.3**

La soluzione usa indipendenza delle risposte, non enunciata esplicitamente nel testo.

**2001.3**

Esplicitata l'ipotesi implicita di almeno quattro studenti.

**2021.1**

Esplicitate partenza da fermo e convenzione sugli istanti di cambio del semaforo. Il caso verde residuo=40 dipende dalla convenzione.

**2021.3**

Il moto richiesto nel punto (b) ha un limite temporale: con obelisco fermo non si attraversa la sua base con un riflettore finito sulla parete.

**2022.1**

I conteggi includono l'incrocio iniziale. Nei punti (b) e (c) si usano le orientazioni appropriate ai due tipi di vertice, non lo stesso orientamento di bordo di una griglia pari.

**2022.3**

Prova geometrica nuova, da riesaminare in particolare nel lemma di riduzione dei percorsi a corde e archi; verificato anche numericamente il minimo per ingressi/uscite sul cerchio.

**2023.2**

Indipendenza dei dischi e modello geometrico di sopravvivenza annuale sono assunzioni esplicite della nuova bozza, non dati completamente specificati dal testo.

**2024.1**

Convenzione di illuminazione tangente esplicitata seguendo la bozza: h>=1. Con archi aperti la soglia e h>1.

**2024.2**

Soluzione nuova basata sulla famiglia di aperture sincrone rappresentata da squares.pdf; verificare che il testo intenda esattamente questa famiglia e non ulteriori montaggi delle cerniere.

**2024.3**

Il punto (c) mantiene esplicitamente l'indipendenza delle risposte; senza di essa le marginali a,b,c non bastano.

**2025.1**

Esplicitata l'ipotesi di dadi equi e indipendenti, adottata dalla bozza ricevuta.

**2025.2**

Nel punto (a) la bozza assume uniformita delle date: restituita una percentuale attesa, non una percentuale empirica determinata dai soli dati del testo. Quest'anno=2025.

**2025.3**

Il pentagono di area 299/200 nel punto (d) e un contributo AI nuovo rispetto alla bozza manoscritta, verificato per inclusione dei vertici.

**2026.1**

Corretto nella rielaborazione, non nel PDF originale, il verso dell'asse perpendicolare: AC e l'asse della corda BD, non viceversa. Assunti quadrilateri semplici non degeneri.

**2026.2**

Esplicitati scorta iniziale illimitata e numero finito di viaggi. Rafforzata la necessita della soglia C/2: non basta presumerla per ogni tratto di una strategia arbitraria.

**2026.3**

Corretti nella nuova rielaborazione due conti del PDF: la differenza nel punto (b) e N-2499, non N-2500; 101*99*97=969903. Nel punto (d) distinta strategia ottima/deterministica da randomizzazione arbitraria.


## 5. Controlli eseguiti

### Conservazione dell'esistente

Per ogni file è stato confrontato il contenuto di tutte le macro preesistenti. Inoltre, togliendo in memoria le nuove aggiunte e ripristinando soltanto i precedenti corpi vuoti di Risposta/Aiutino, si ricostruisce **esattamente la sequenza di byte originale**. Questo controllo verifica anche ciò che sta fuori dalle macro: commenti, spazi, ordine e figure.

Sono risultati identici tutti i campi non vuoti; sono identici tutti i Testo, SoluzioneUfficiale, SoluzioniAlternative, Osservazioni, Commenti e i metadati originari. Cinquantatrè file non hanno alcuna modifica.

### Compilazione

Sono stati compilati con pdfLaTeX tutti gli 82 nuovi blocchi. È stato anche eseguito un test che carica i 43 sorgenti aggiornati, azzera il campo redazionale tra problemi e stampa soltanto le integrazioni: compilazione riuscita, 57 pagine di prova. Sono state ispezionate alcune pagine rappresentative.

Non è stata eseguita qui la compilazione del master storico completo `SA_Book.tex`, che dipende dal progetto locale e dalle sue macro. Non è stato collaudato il sito con la nuova macro. I PDF e i sorgenti di prova non sono inclusi: nessuna copia di lavorazione da portare nel repository.

### Controlli matematici mirati

Sono stati effettuati controlli simbolici, enumerativi e numerici su 22 aspetti: conteggi dei dadi; arresto dell'algoritmo sui dispari positivi fino a 9999; congruenza del cubo; completamenti dei quadrati e fattorizzazioni; confronto delle strategie probabilistiche; classifica del torneo; strategie del gioco per `k=1,...,30`; somme delle cifre; probabilità dei corridori; cammini sulla griglia; costi dei percorsi attorno al disco; geometria dei quadrati incernierati; calendario; inclusione del rettangolo nel pentagono capiente; conti dell'urna; raggi delle ombre.

Il dettaglio dei controlli e dei loro limiti è in `dati/integrazioni_ai/controlli_20261108.json`. Le enumerazioni finite e i campionamenti numerici non sostituiscono le prove; la compilazione non certifica la matematica. Tutte le aggiunte conservano lo stato **DA VERIFICARE**.

## 6. Integrazione nel progetto: non ancora automatica

Questo ZIP è un pacchetto di contenuti da confrontare, non un aggiornamento da estrarre alla cieca sopra il repository.

1. Confrontare l'archivio corrente con la fotografia di partenza. Le impronte prima/dopo sono nel manifesto. Se un sorgente è stato modificato dopo la preparazione dello ZIP, non sovrascriverlo automaticamente.
2. Aggiungere `SoluzioneRedazionale` allo schema, al caricatore del libro e al convertitore del sito. Il caricatore deve azzerarla a ogni problema, anche quando il file successivo non la definisce.
3. Propagare i marcatori AI ai dati web e alla stampa. Il convertitore attuale elimina i commenti: aggiungere soltanto il nuovo campo alla lista non basta a rendere visibile la provenienza delle risposte e degli aiutini.
4. Adeguare il verificatore ai nuovi contenuti storici: per esempio le sei risposte storiche prima vuote sono ora riempite. Il vecchio conteggio fisso delle risposte non deve essere confuso con un controllo di integrità; il confronto con la fotografia resta invece verificabile.
5. Risolvere o segnalare pubblicamente i conflitti elencati, poi compilare il libro e rigenerare selettivamente il sito. Non pubblicare le bozze come materiale verificato.

Il nome `SoluzioneRedazionale` distingue il nuovo strato dal materiale preesistente, ma non impone una scelta definitiva di interfaccia. Non è stata modificata alcuna infrastruttura del progetto.

## 7. Verifica riproducibile del pacchetto

Dalla radice del pacchetto estratto, il seguente comando legge lo ZIP originale senza estrarlo e controlla tutte le impronte e la conservazione dell'esistente:

```bash
python3 scripts/verifica_integrazione_ai.py --originale /percorso/contenuti.zip
```

Non scrive alcun file e non modifica il repository. Il risultato atteso è `VERIFICA SUPERATA`, con 43 file integrati, 53 identici e 82 nuovi campi.

`SHA256SUMS.txt` contiene le impronte dei file del pacchetto, escluso il manifesto dei checksum stesso. Non è una firma digitale: serve per controllare l'integrità della copia.

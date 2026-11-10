# ProblemiSSSUP — confronto con le prove ufficiali 2016–2020

**Data:** 10 novembre 2026. **Stato:** ricognizione redazionale, nessuna modifica ai sorgenti canonici.

## Materiali verificati

- I cinque fascicoli ufficiali `prove_matematica-fisica_a.a._16-17.pdf` fino a `_20-21.pdf`, forniti dall'utente: le pagine di **matematica** sono le prime due nel 2016 e nel 2018–2020, la prima nel 2017. Le altre pagine riguardano prove di fisica e problem solving, non questa raccolta.
- I 15 sorgenti canonici `contenuti/problemi/SA_2016_1.tex` … `SA_2020_3.tex`, consultati sul repository pubblico `Xamog68/ProblemiSSSUP` (ramo `main`, 10/11/2026).
- I sorgenti storici `2016.tex` … `2020.tex` dell'archivio `2014-2020.zip` già acquisito.

## Risultato generale

**Non emerge una revisione linguistica sistematica negli ufficiali:** per i 15 esercizi le richieste, le ipotesi e i dati matematici rimangono sostanzialmente quelli dei nostri testi canonici. Nel 2018–2020 il confronto testuale delle copie PDF con la ricompilazione degli originali `.tex` rileva, oltre alle istruzioni amministrative aggiunte all'intestazione, soltanto le varianti minute descritte sotto. Le pagine 2016–2017 sono scansioni: il confronto è stato visivo, non un diff testuale automatico.

| Codice | Confronto del testo con il PDF ufficiale | Osservazioni |
|---|---|---|
| SA_2016_1 | Corrisponde | **Figura PSTricks da correggere**: il PDF rappresenta due basi di larghezza `l` con gli assi distanti `l`; la nostra ricostruzione mostra invece basi distanziate e quota `l` fra bordi. |
| SA_2016_2 | Corrisponde | L'ufficiale chiede esplicitamente stime, non ottimi esatti. Numerazione originale 1–5, canonica (a)–(e). |
| SA_2016_3 | Corrisponde | Numerazione originale 1–2, canonica (a)–(b). |
| SA_2017_1 | Corrisponde | Nell'ufficiale la lista delle ipotesi è (a),(b) e quella delle domande è 1,2; la canonica usa `itemize` per le ipotesi e (a),(b) per le domande. |
| SA_2017_2 | Corrisponde | Le condizioni dei rintocchi e i tre quesiti corrispondono. |
| SA_2017_3 | Corrisponde | Scacchiera 3 × 5, vuoto nella casella (2,3) in convenzione riga/colonna; la ricostruzione rende graficamente lo stesso caso. |
| SA_2018_1 | Corrisponde | Ridondanza nella frase su prezzi uniformemente ripartiti/equiprobabili già nell'ufficiale. |
| SA_2018_2 | Corrisponde | Il refuso «decurtarti» e le formulazioni potenzialmente ambigue sul recupero dei punti sono presenti nel PDF ufficiale. |
| SA_2018_3 | Corrisponde | Le regole dei tagli e l'1% di rottura sono quelle ufficiali. Possibili precisazioni redazionali sul significato dei «tagli» e sul modello probabilistico. |
| SA_2019_1 | Corrisponde | Manca anche nell'ufficiale l'esplicitazione dell'indipendenza dei guasti fra computer/anni: utile da annotare come interpretazione, non come differenza. |
| SA_2019_2 | Corrisponde | Non è precisato nell'ufficiale il comportamento in caso di superamento di `N` nel gioco. |
| SA_2019_3 | **Refuso corretto nell'ufficiale** | Il sorgente storico 2019 contiene «quadrilareri», il PDF ufficiale reca «quadrilateri»; il sorgente canonico è già corretto. |
| SA_2020_1 | **Variante in senso peggiorativo nel PDF** | L'originale `.tex` storico e il canonico hanno «con il ramo da cui è stato originato»; nel PDF ufficiale si legge «con il ramo da è stato originato», senza «cui». La figura dell'albero è ricostruita, non una riproduzione identica. |
| SA_2020_2 | Corrisponde | Identiche le tre richieste sui polinomi. |
| SA_2020_3 | Corrisponde | Identiche le ipotesi sul distanziamento e sulle forme delle aule. |

## Priorità redazionali proposte, senza modifiche immediate

1. **Correggere la figura di SA_2016_1**, riallineando distanza degli assi e larghezza delle rastrelliere come nel PDF ufficiale; preservare il Testo e verificare che la soluzione matematica usi la medesima distanza.
2. **Mantenere la correzione già presente** in SA_2019_3: «quadrilateri».
3. **Mantenere «da cui»** in SA_2020_1: la fonte storica è grammaticalmente corretta, il PDF ufficiale no. Annotare se si decide di distinguere fonte storica e versione definitiva.
4. Mettere in un elenco separato i problemi con possibili chiarimenti interpretativi: **2017.2** (versi/velocità delle lancette), **2018.2** (recupero punti), **2018.3** (ritagli, tagli e rotture), **2019.1** (indipendenza dei guasti), **2019.2** (somme maggiori di N), **2020.1** (punti dell'albero infinito). Sono proposte di lettura critica, non differenze dimostrate fra le due fonti.

## Distinzione importante

Le prove ufficiali 2016–2020 non mostrano una «seconda redazione ben rifinita» degli enunciati. Sarebbe scorretto sostituire silenziosamente i Testi canonici con riscritture interpretative: conviene conservare fedelmente l'originale e lavorare con note esplicative/versioni redazionali approvate.

**Non esaminati con questo confronto ufficiale:** 2014 e 2015, perché non erano inclusi nei cinque PDF ricevuti.

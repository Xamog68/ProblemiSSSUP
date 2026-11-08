# Da fare — ProblemiSSSUP

**Aggiornato l'8 novembre 2026.** Le attività completate non devono essere
confuse con le verifiche matematiche ancora aperte.

## Prossime priorità

- [ ] Revisionare matematicamente le 82 integrazioni AI (24 risposte,
      18 aiutini, 40 soluzioni redazionali) e registrare l'esito per campo.
- [ ] Riesaminare i conflitti con le risposte preesistenti nei problemi
      **1998.6** e **2000.2** prima di considerarle concordanti con le nuove
      soluzioni. Altri casi sensibili sono elencati in
      `INTEGRAZIONE_AI_20261108.md`.
- [x] Convertire e inserire sul sito **156 SVG vettoriali** da PSTricks,
      con zero errori di generazione e verifica dell'associazione per campo.
- [ ] Ricostruire le **due figure esterne** ancora mancanti (2024.2 e 2026.1).
- [ ] Correggere gradualmente le etichette geometriche mal posizionate
      (spesso già nel PDF), senza alterare le immagini generate a mano.
- [ ] Valutare i **25 disegni candidati a tabelle/griglie HTML**, senza
      sostituire automaticamente gli SVG approvati.
- [ ] Controllare visivamente formule, riferimenti, figure e impaginazione
      del sito su Firefox, altri browser e dispositivi mobili.
- [ ] Chiarire paternità e attribuzioni dei materiali preesistenti,
      condizioni di riutilizzo e scelta di eventuali licenze distinte per
      codice, testi d'esame e contributi originali.

## Archivio e contenuti

- [x] Importare 78 problemi storici 1996–2013 e 18 problemi 2021–2026.
- [x] Normalizzare UTF-8, accenti e paragrafi nei sorgenti LaTeX.
- [x] Integrare le 82 bozze AI senza sovrascrivere i campi preesistenti.
- [ ] Recuperare i problemi mancanti del 2014–2020.
- [ ] Verificare editorialmente i 18 testi 2021–2026 contro le prove originali.
- [ ] Importare la classificazione storica 1996–1998 e classificare gli altri
      problemi per area, argomento e difficoltà.
- [ ] Associare in modo sistematico gli autori e le fonti delle soluzioni
      preesistenti e degli appunti moderni ai singoli problemi.
- [ ] Valutare le trascrizioni degli appunti 2024–2026 in rapporto alle bozze
      già integrate, prima di considerarli materiale definitivo.
- [ ] Valutare se introdurre i 96 titoli redazionali nei sorgenti canonici;
      per ora restano separati in `sito/dati/titoli.json`.

## Test a risposta multipla (cantiere distinto)

- [ ] Catalogare le prove a risposta multipla del Sant'Anna, a partire
      dall'archivio locale `fonti-locali/originali/compiti_20261107_completo.zip`
      e dall'inventario
      `fonti-locali/inventari/INVENTARIO_COMPITI_CORRETTO_20261107.md`.
- [ ] Ricostruire per ogni annata sessioni, testi, versioni e risposte,
      verificando in particolare il materiale del periodo 2014–2016.
- [ ] Valutare una sezione autonoma del sito e, eventualmente, un fascicolo
      separato per i quiz. Conservare gli originali e documentare le fonti.
- [ ] Non confondere il recupero dei quiz con quello delle prove a risposta
      aperta mancanti del 2014–2020: sono due obiettivi distinti.

## Libro PDF

- [x] Compilare il libro storico sul Mac (205 pagine, 7 novembre 2026).
- [x] Creare e collaudare il libro modulare v2.1, con selezione di annate
      e campi, collegamenti e 96 soluzioni su pagine iniziali distinte.
- [ ] Confrontare sistematicamente il PDF storico e il libro modulare,
      verificando impaginazione, formule e figure (il collaudo finora non
      è una revisione esaustiva).
- [ ] Decidere nome definitivo, frontespizio e attribuzioni del libro.

## Sito web

- [x] Convertire i 96 problemi e introdurre controllo di allineamento
      LaTeX/web tramite impronte.
- [x] Implementare navigazione per anno e problema, vista materiali e
      fisarmoniche per i contenuti presenti.
- [x] Mostrare le bozze AI con diciture e icona delle stelline prima
      dell'apertura delle fisarmoniche.
- [x] Introdurre 96 titoli redazionali e domande (a), (b), (c) nei testi.
- [x] Pubblicare tramite GitHub Pages dalla cartella `sito/` usando
      GitHub Actions, senza pubblicare la roadmap al posto del sito.
- [x] Aggiungere ritorno visibile agli anni, footer di provenienza e `noindex`.
- [ ] Sviluppare una procedura più semplice per la conversione periodica dei
      dati e il controllo visivo prima del push; il **deployment** da GitHub
      è automatico, la rigenerazione dei dati non lo è.
- [x] Integrare gli SVG mediante manifesto e impronte dei sorgenti,
      mantenendo le figure nella sezione corretta di ogni problema.
- [ ] Verificare progressivamente ritagli, etichette e ingrandimento degli
      SVG su browser e dispositivi diversi; gli avvisi devono riguardare
      soltanto i campi realmente incompleti.

## Manutenzione e documentazione

- [x] Versionare le regole di conversione e i controlli di integrità.
- [x] Documentare l'architettura e il procedimento di aggiornamento.
- [ ] Aggiungere controlli automatici in CI oltre al workflow di deployment,
      se utili, senza confondere l'allineamento con la verifica matematica.
- [ ] Registrare formalmente gli esiti della revisione matematica mano a mano
      che le bozze vengono approvate o corrette.
- [ ] Conservare il materiale originale e gli inventari locali fuori da Git
      finché non ne sia definita l'eventuale pubblicabilità.

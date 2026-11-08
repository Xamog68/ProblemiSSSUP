# Figure da completare nel sito SSSUP

## Marcatori nei sorgenti canonici

Quando una figura esterna presente negli originali non e ancora stata
ricostruita nel sorgente LaTeX canonico, usare un commento sulla propria riga
nel punto in cui il disegno dovra comparire:

```latex
% SSSUP-FIGURA-DA-RICOSTRUIRE: squares.pdf
```

Il commento non modifica l'impaginazione TeX; la conversione web lo
trasforma in un segnaposto visibile. Conservare separatamente il riferimento
agli originali conservati in `fonti-locali/`, senza incorporare questi file
nel repository pubblico. Quando il disegno sara ricostruito nel LaTeX,
rimuovere il marcatore e rigenerare il problema.

## Controlli indipendenti

- **ALLINEATO** riguarda esclusivamente le impronte di conversione
  (sorgente, generatore, Pandoc, contenuto web).
- **INCOMPLETO (figure segnalate)** indica la presenza, nel sorgente,
  di marcatori `SSSUP-FIGURA-DA-RICOSTRUIRE` e/o di disegni PSTricks che
  il convertitore sostituisce ancora con segnaposto.
- Un problema puo essere **ALLINEATO** e **INCOMPLETO** allo stesso tempo.
- L'assenza di marcatori **non dimostra** che un problema sia completo:
  restano necessari controlli editoriali e confronto con le prove originali.

## Verifica e rigenerazione

Da `ProblemiSSSUP/`:

```bash
python3 scripts/sito_check.py --anno 2024 --problema 2
python3 scripts/genera_dati_sito.py --anno 2024 --problema 2
python3 scripts/sito_check.py --anno 2024 --problema 2
```

Il controllo e di sola lettura, il generatore modifica solo i dati web;
non riscrive HTML/CSS/JavaScript dell'interfaccia o i sorgenti LaTeX.

### Limitazioni

Il convertitore non disegna i PSTricks e non ricostruisce le figure
esterne. I segnaposto sono segnali di incompletezza, non sostituti
matematici dei disegni. La conversione va sempre verificata visivamente.
La verifica riguarda i problemi effettivamente selezionati dal comando.

/* Interfaccia indipendente dai sorgenti LaTeX e dai dati convertiti. */
(() => {
  'use strict';
  const catalog = window.SSSUP_CATALOG;
  const main = document.getElementById('main');
  const heading = document.getElementById('page-title');
  const subtitle = document.getElementById('page-subtitle');
  const parameter = new URLSearchParams(location.search);
  const year = Number(parameter.get('anno'));
  const problemTarget = Number(parameter.get('problema'));
  const sectionTarget = parameter.get('sezione');
  const view = parameter.get('vista');
  const registered = new Map();
  const pending = new Map();
  const sections = [
    ['Risposta','Risposta breve'], ['Aiutino','Aiutino'],
    ['SoluzioneUfficiale','Soluzione'],
    ['SoluzioneRedazionale','Soluzione'],
    ['SoluzioniAlternative','Soluzioni alternative'],
    ['Osservazioni','Osservazioni'], ['Commenti','Commenti']
  ];
  window.SSSUP = window.SSSUP || {};
  window.SSSUP.registerProblem = (problem) => {
    const key = `${problem.year}_${problem.number}`;
    registered.set(key,problem);
    if (pending.has(key)) { pending.get(key).resolve(problem);pending.delete(key); }
  };
  if (Array.isArray(window.SSSUP_PRELOADED)) {
    window.SSSUP_PRELOADED.forEach(window.SSSUP.registerProblem);
  }
  function el(tag,className,text) {
    const n=document.createElement(tag);
    if(className)n.className=className;
    if(text!==undefined)n.textContent=text;
    return n;
  }
  function link(text,href,className) { const a=el('a',className,text);a.href=href;return a; }
  function entry(year) { return catalog.years.find(y=>y.year===year); }
  function linkFor(year,number,section) {
    const p = new URLSearchParams({anno:String(year)});
    if(number)p.set('problema',String(number));
    if(section)p.set('sezione',section);
    return 'index.html?'+p.toString()+(number?'#problema-'+number:'');
  }
  function showIndex() {
    heading.textContent='Un archivio, trentun anni di problemi.';
    subtitle.textContent='I testi sono conservati in LaTeX. Il sito è un modo diverso di consultarli.';
    main.replaceChildren();
    main.append(el('p','intro','Una pagina per ogni anno dal 1996 al 2026. Le caselle verdi indicano prove consultabili; quelle grigie le prove ancora da recuperare.'));
    main.append(el('p','intro','Questa raccolta inizia nel 1996. Le prove precedenti sono coperte dal volume di Guido Torrigiani, Sebastiano Francaviglia e Tullio Franzoni, pubblicato da Zanichelli nel 1995.'));
    const grid=el('div','year-grid');
    for (const y of catalog.years) {
      const cls=y.missing?'missing':y.preview?'ready':'source-only';
      const a=link('',linkFor(y.year),`year-link ${cls}`);
      a.append(el('strong','',String(y.year)));
      a.append(el('span','',y.missing?'Prova da recuperare':y.preview?`${y.preview} problemi consultabili`:`${y.count} problemi nei sorgenti`));
      grid.append(a);
    }
    main.append(grid);
    const legend=el('div','legend');
    for(const [cls,text] of [['is-ready','Problemi consultabili'],['is-source','Materiali in preparazione'],['is-missing','Prova da recuperare']])legend.append(el('span',cls,text));
    main.append(legend);
    const note=el('div','notice');
    note.textContent='Archivio indipendente e non ufficiale, in revisione. I contenuti generati dall’AI sono segnalati con le stelline e l’indicazione «Bozza AI · Da verificare». Alcune figure e soluzioni preesistenti richiedono ulteriori controlli.';
    main.append(note);
    main.append(el('p','intro','Apri un anno per consultare i problemi. La barra di navigazione in basso a destra consente di spostarsi fra i problemi e tornare all’elenco degli anni.'));
  }
  function loadProblem(year,number) {
    const key=`${year}_${number}`;
    if(registered.has(key))return Promise.resolve(registered.get(key));
    if(pending.has(key))return pending.get(key).promise;
    const script=document.createElement('script');
    script.src=`dati/problemi/${key}.js`;
    script.async=true;
    const item={};
    item.promise=new Promise((resolve,reject)=>{item.resolve=resolve;item.reject=reject;});
    pending.set(key,item);
    script.onerror=()=>{pending.delete(key);item.reject(new Error(`Dati non trovati: ${key}`));};
    script.onload=()=>{if(!registered.has(key)){pending.delete(key);item.reject(new Error(`Dati non validi: ${key}`));}};
    document.head.append(script);
    return item.promise;
  }
  function allDetails() {return Array.from(main.querySelectorAll('details.extra'));}
  function allPanels() {return Array.from(main.querySelectorAll('.materials-panel'));}
  function setPanel(panel,open) {
    panel.hidden=!open;
    const button=panel.parentElement.querySelector('button.materials-trigger');
    const count=panel.querySelectorAll('details.extra').length;
    button.setAttribute('aria-expanded',String(open));
    button.querySelector('.materials-trigger-label').textContent=`${open?'Nascondi':'Mostra'} materiali aggiuntivi (${count})`;
  }
  function revealPanels() {for(const d of allPanels())setPanel(d,true);}
  function collapsePanels() {for(const d of allPanels())setPanel(d,false);}
  function setAll(open) {
    if(open)revealPanels();
    for(const d of allDetails())d.open=open;
    if(!open)collapsePanels();
    updateStats();
  }
  function onlyField(field) {
    const wanted = field === 'Soluzioni'
      ? new Set(['SoluzioneUfficiale','SoluzioneRedazionale'])
      : new Set([field]);
    for(const panel of allPanels()) {
      setPanel(panel,Array.from(panel.querySelectorAll('details.extra'))
        .some(d=>wanted.has(d.dataset.field)));
    }
    for(const d of allDetails())d.open=wanted.has(d.dataset.field);
    updateStats();
  }
  function height() {void document.body.offsetHeight;return document.documentElement.scrollHeight;}
  function updateStats() {
    const stats=document.getElementById('stats');
    if(!stats)return;
    const ds=allDetails();const count=ds.filter(d=>d.open && (!d.closest('.materials-panel') || !d.closest('.materials-panel').hidden)).length;
    const h=height();const screens=(h/Math.max(1,window.innerHeight)).toFixed(1).replace('.',',');
    stats.textContent=`${count}/${ds.length} sezioni visibili · ${h.toLocaleString('it-IT')} px · ${screens} schermate`;
  }
  function compareLengths() {
    const ds=allDetails(),panels=allPanels(),prior=ds.map(d=>d.open),priorPanels=panels.map(d=>!d.hidden),y=window.scrollY;
    for(const d of ds)d.open=false;
    collapsePanels();
    const closed=height();
    revealPanels();
    for(const d of ds)d.open=true;
    const opened=height();
    ds.forEach((d,i)=>{d.open=prior[i]});
    panels.forEach((d,i)=>setPanel(d,priorPanels[i]));
    const ratio=(opened/Math.max(1,closed)).toFixed(2).replace('.',',');
    const info=document.getElementById('compare-info');
    info.textContent=`Tutto chiuso: ${closed.toLocaleString('it-IT')} px · Tutto aperto: ${opened.toLocaleString('it-IT')} px · La pagina diventa circa ${ratio} volte più lunga (misura riferita a questa finestra).`;
    info.hidden=false;
    window.scrollTo(0,y);
    updateStats();
  }
  // Pannello di navigazione sempre accessibile, non legato allo scorrimento della prova.
  // Gli strumenti globali sono secondari: servono soprattutto per provare l'interfaccia.
  function createDock(y=null) {
    const dock=el('nav','nav-dock');
    dock.setAttribute('aria-label','Navigazione rapida e strumenti');
    const row=el('div','nav-dock-row');
    const toYears=link('← Anni','index.html','dock-index');
    toYears.setAttribute('aria-label','Torna all’elenco di tutti gli anni');
    row.append(toYears);
    if(y && y.preview>1){
      row.append(el('span','dock-caption','Vai al problema'));
      for(let n=1;n<=y.preview;n++) {
        const a=link(String(n),`#problema-${n}`,'dock-problem');
        a.setAttribute('aria-label',`Vai al problema ${n}`);
        row.append(a);
      }
    }
    const controls=el('details','dock-tools');
    controls.append(el('summary','', 'Strumenti'));
    const body=el('div','dock-tools-body');
    body.append(el('p','dock-tools-heading','Comandi per questa prova'));
    const actions=[
      ['Apri tutte le sezioni',()=>setAll(true)],
      ['Chiudi tutte le sezioni',()=>setAll(false)],
      ['Solo risposte',()=>onlyField('Risposta')],
      ['Solo aiutini',()=>onlyField('Aiutino')],
      ['Solo soluzioni',()=>onlyField('Soluzioni')],
      ['Confronta lunghezze',compareLengths]
    ];
    for(const [label,handler] of actions){
      const b=el('button','dock-action',label);b.type='button';b.addEventListener('click',handler);body.append(b);
    }
    const stats=el('div','stats','Calcolo lunghezza…');stats.id='stats';body.append(stats);
    const result=el('div','compare-result');result.id='compare-info';result.hidden=true;body.append(result);
    controls.append(body);row.append(controls);dock.append(row);
    return dock;
  }
  // Icona Sparkles inline: non richiede font, librerie o servizi esterni.
  function aiSparkles() {
    const ns='http://www.w3.org/2000/svg';
    const svg=document.createElementNS(ns,'svg');
    svg.setAttribute('viewBox','0 0 24 24');
    svg.setAttribute('class','extra-ai-icon');
    svg.setAttribute('aria-hidden','true');
    svg.setAttribute('focusable','false');
    for(const d of [
      'M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9L12 3Z',
      'M19 16l.8 2.2L22 19l-2.2.8L19 22l-.8-2.2L16 19l2.2-.8L19 16Z',
      'M4 2l.55 1.45L6 4l-1.45.55L4 6l-.55-1.45L2 4l1.45-.55L4 2Z'
    ]) {
      const path=document.createElementNS(ns,'path');
      path.setAttribute('d',d);
      svg.append(path);
    }
    return svg;
  }
  function makeDetails(data) {
    const extras=el('div','extra-zone');
    let count=0;
    for(const [key,label] of sections) {
      const html=data.sections?.[key];if(!html||!html.trim())continue;
      const provenance=data.provenance?.[key];
      const isAI=provenance?.tipo==='ai';
      if(key==='SoluzioneRedazionale' && !isAI) {
        throw new Error('Soluzione redazionale priva di provenienza AI');
      }
      const provenanceLabel=isAI?'Bozza AI · Da verificare':
        provenance?.tipo==='preesistente'?'Contenuto preesistente':
        'Provenienza non disponibile';
      const d=el('details','extra');d.dataset.field=key;
      const summary=el('summary');
      const summaryMain=el('span','extra-summary-main');
      summaryMain.append(el('span','extra-summary-name',label));
      if(isAI)summaryMain.append(aiSparkles());
      summaryMain.append(el('span',isAI?'extra-provenance ai':'extra-provenance',
        provenanceLabel));
      summary.append(summaryMain);d.append(summary);
      const inner=el('div','extra-body');inner.innerHTML=html;d.append(inner);
      d.addEventListener('toggle',()=>requestAnimationFrame(updateStats));
      extras.append(d);count++;
    }
    return {extras,count};
  }
  function materialsLink(data) {
    // Put all query parameters ahead of the optional hash, for URLs to work on file:// too.
    const url=new URLSearchParams({anno:String(data.year),problema:String(data.number),vista:'materiali'});
    const a=link('Apri problema completo in nuova scheda', 'index.html?'+url.toString(), 'materials-new-tab');
    a.target='_blank';a.rel='noopener noreferrer';
    a.setAttribute('aria-label',`Apri testo e materiali del problema ${data.year}.${data.number} in una nuova scheda`);
    return a;
  }
  function renderProblem(data,standalone=false) {
    const article=el('article','problem');article.id=`problema-${data.number}`;
    const head=el('div','problem-header');
    const left=el('div');left.append(el('span','number',`Problema ${data.year}.${data.number}`));
    left.append(el('h2','',data.title || `Problema ${data.number}`));
    head.append(left);
    const source=`https://github.com/Xamog68/ProblemiSSSUP/blob/main/contenuti/problemi/${encodeURIComponent(data.source)}`;
    const a=link('Sorgente LaTeX',source,'source');a.target='_blank';a.rel='noopener noreferrer';head.append(a);
    article.append(head);
    const body=el('div','math-body');body.innerHTML=data.sections?.Testo||'';article.append(body);
    if(data.warning)article.append(el('div','problem-alert',data.warning));
    const {extras,count}=makeDetails(data);
    if(standalone){
      article.classList.add('standalone-problem');
      if(count){
        const title=el('div','standalone-materials-head');
        title.append(el('h3','',`Materiali aggiuntivi (${count})`));
        title.append(el('p','', 'Tutte le sezioni sono aperte inizialmente; puoi richiuderle singolarmente.'));
        article.append(title);
        article.append(extras);
      }
    } else if(count) {
      const actions=el('div','materials-actions');
      const trigger=el('button','materials-trigger');trigger.type='button';
      const text=el('span','materials-trigger-label',`Mostra materiali aggiuntivi (${count})`);
      trigger.append(text);
      trigger.append(el('span','chevron',''));
      trigger.setAttribute('aria-expanded','false');
      const panel=el('div','materials-panel');panel.id=`materiali-${data.year}-${data.number}`;
      panel.hidden=true;panel.append(extras);
      trigger.setAttribute('aria-controls',panel.id);
      trigger.addEventListener('click',()=>{setPanel(panel,panel.hidden);requestAnimationFrame(updateStats);});
      actions.append(trigger);
      actions.append(materialsLink(data));
      actions.append(panel);
      article.append(actions);
    }
    return article;
  }
  function typeset() {
    if(window.MathJax?.typesetPromise)return window.MathJax.typesetPromise([main]).then(updateStats).catch(console.warn);
    return Promise.resolve();
  }
  function ensureDeepLink() {
    if(problemTarget) {
      const target=document.getElementById('problema-'+problemTarget);
      if(target){
        if(sectionTarget){
          const d=Array.from(target.querySelectorAll('details')).find(x=>x.dataset.field===sectionTarget);
          if(d){ const p=d.closest('.materials-panel');if(p)setPanel(p,true); d.open=true; }
        }
        target.scrollIntoView({block:'start',behavior:'instant'});
      }
    }
  }
  async function showMaterialsTab(y) {
    heading.textContent=`Problema ${y.year}.${problemTarget}: testo e materiali.`;
    subtitle.textContent='Il problema completo in una scheda separata, con tutti i materiali inizialmente aperti.';
    main.replaceChildren();
    main.append(link('← Torna alla prova del '+y.year,linkFor(y.year,problemTarget),'back-years'));
    if(y.missing || !y.preview || problemTarget < 1 || problemTarget > y.preview) {
      main.append(el('p','notice','Problema non disponibile nell’archivio online.'));
      return;
    }
    const data=await loadProblem(y.year,problemTarget);
    main.append(createDock());
    main.append(renderProblem(data,true));
    // In questa vista "Apri tutto" significa davvero testo + materiali subito visibili.
    for(const d of allDetails())d.open=true;
    updateStats();
    await typeset();
    if(sectionTarget){
      const d=allDetails().find(x=>x.dataset.field===sectionTarget);
      if(d)d.scrollIntoView({block:'start',behavior:'instant'});
    }
    if(window.ResizeObserver)new ResizeObserver(()=>requestAnimationFrame(updateStats)).observe(main.querySelector('article.problem'));
    window.addEventListener('resize',updateStats);
  }
  async function showYear(y) {
    heading.textContent=`La prova del ${y.year}.`;
    subtitle.textContent=y.missing?'Testi ancora da recuperare.':`${y.count} problemi nell’archivio canonico · testi sempre visibili, materiali aggiuntivi a richiesta.`;
    main.replaceChildren();
    main.append(link('← Torna a tutti gli anni','index.html','back-years'));
    if(y.missing){
      const area=el('div','no-content');area.append(el('h2','','Prova non ancora reperita'));
      area.append(el('p','','La pagina dell’anno esiste già. Quando recupereremo i testi, i problemi appariranno qui automaticamente.'));
      main.append(area);return;
    }
    if(!y.preview){
      const area=el('div','no-content');area.append(el('h2','','Sorgenti LaTeX già presenti'));
      area.append(el('p','',`I ${y.count} problemi del ${y.year} sono nell’archivio canonico, ma non risultano ancora disponibili sul sito.`));
      area.append(el('p','','Una volta installato Pandoc, il generatore potrà produrre i dati web dei singoli problemi. L’interfaccia resterà invariata.'));
      main.append(area);return;
    }
    const intro=el('p','intro',`Questa prova comprende ${y.preview} problemi consultabili. I testi sono sempre visibili; i materiali si aprono sotto ciascun problema oppure in una nuova scheda. La navigazione rapida rimane nell’angolo in basso a destra.`);
    main.append(intro);
    const region=el('div','problems');main.append(region);
    main.append(createDock(y));
    const slots=new Map();
    for(let n=1;n<=y.preview;n++){const slot=el('div');slot.id=`slot-${n}`;slot.append(el('p','loading',`Caricamento problema ${n}…`));region.append(slot);slots.set(n,slot);}
    const settled=await Promise.allSettled(Array.from({length:y.preview},(_,i)=>loadProblem(y.year,i+1)));
    for(let i=0;i<settled.length;i++){
      const s=settled[i],slot=slots.get(i+1);slot.replaceChildren();
      if(s.status==='fulfilled')slot.append(renderProblem(s.value));
      else slot.append(el('p','notice',`Non riesco a leggere il problema ${y.year}.${i+1}: ${s.reason.message}`));
    }
    main.append(link('← Torna a tutti gli anni','index.html','back-years back-years-bottom'));
    main.append(el('p','jump-top',''));
    main.lastChild.append(link('↑ Torna in cima','#'));
    updateStats();
    ensureDeepLink();
    await typeset();
    ensureDeepLink();
    if(window.ResizeObserver)new ResizeObserver(()=>requestAnimationFrame(updateStats)).observe(region);
    window.addEventListener('resize',updateStats);
  }
  window.addEventListener('load',() => {
    if (window.MathJax?.typesetPromise) {
      window.MathJax.typesetPromise([main]).then(updateStats).catch(console.warn);
    }
  });
  if(!catalog||!Array.isArray(catalog.years)){
    main.replaceChildren(el('p','notice','Manifest dei contenuti non trovato. Verifica che la cartella dati sia stata estratta dallo ZIP.'));
  } else if(year && entry(year) && view==='materiali' && problemTarget){
    showMaterialsTab(entry(year)).catch(err=>{main.append(el('p','notice',String(err)));console.error(err)});
  } else if(year && entry(year)){
    showYear(entry(year)).catch(err=>{main.append(el('p','notice',String(err)));console.error(err)});
  } else showIndex();
})();

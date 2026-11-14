/* ProblemiSSSUP: statistics are a separate, optional layer; no LaTeX/site.js rewriting. */
(() => {
  'use strict';
  const PREFIX = 'dati/statistiche/';
  const NS = 'http://www.w3.org/2000/svg';
  const main = document.getElementById('main');
  if (!main || !window.fetch) return;
  const pageYear = Number(new URLSearchParams(location.search).get('anno'));
  const problemFiles = new Set();
  const loaded = new Map();

  const E = (tag, className = '', text) => {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = String(text);
    return node;
  };
  const S = (tag, attrs = {}, text) => {
    const node = document.createElementNS(NS, tag);
    for (const [key,value] of Object.entries(attrs)) node.setAttribute(key,String(value));
    if (text !== undefined) node.textContent = String(text);
    return node;
  };
  const text = (p, content, className = '') => p.append(E('p', className, content));

  function makeChart(stats) {
    const wrapper = E('div','sssup-a-graph');
    const n = stats.elaborati;
    const subs = stats.sottodomande;
    const maxValue = Math.max(10, Math.ceil(n / 20) * 20);
    const left=51, right=672, top=32, bottom=235;
    const svg=S('svg',{viewBox:'0 0 720 285',role:'img',preserveAspectRatio:'xMidYMid meet'});
    const description = `Su ${n} elaborati: `+subs.map(p => `punto ${p.id}: ${p.contributo} con contributo riconosciuto e ${p.sostanzialmente_completo} sostanzialmente completi`).join('; ');
    svg.setAttribute('aria-label',description);
    for (let i=0;i<=4;i++) {
      const value=Math.round(maxValue*i/4);
      const y=bottom-(bottom-top)*i/4;
      svg.append(S('line',{class:'sssup-a-axis',x1:left,y1:y,x2:right,y2:y}));
      svg.append(S('text',{x:left-12,y:y+4,'text-anchor':'end'},value));
    }
    svg.append(S('text',{x:left,y:17},'Candidati'));
    const width=(right-left)/subs.length;
    subs.forEach((item,i) => {
      const cx=left+(i+0.5)*width;
      const pairs=[['contributo','#75b7ad',-17],['sostanzialmente_completo','#0e6b65',17]];
      for (const [field,fill,dx] of pairs) {
        const count=item[field];
        const barHeight=(count/maxValue)*(bottom-top);
        const x=cx+dx-14;
        const y=bottom-barHeight;
        svg.append(S('rect',{x,y,width:28,height:Math.max(0,barHeight),fill,rx:3}));
        svg.append(S('text',{class:'sssup-a-count',x:x+14,y:Math.max(26,y-6),'text-anchor':'middle'},count));
      }
      svg.append(S('text',{class:'sssup-a-id',x:cx,y:262,'text-anchor':'middle'},`(${item.id})`));
    });
    wrapper.append(svg);
    return wrapper;
  }

  function makeTopTable(stats) {
    const container=E('div');
    const chooser=E('div','sssup-a-switch');
    chooser.setAttribute('role','group');
    chooser.setAttribute('aria-label','Gruppo nella prova di matematica');
    const tableBox=E('div','sssup-a-table');
    const table=E('table');
    const thead=E('thead');
    const trh=E('tr');
    const headline=E('th','','Fra i primi 10 della matematica');
    headline.setAttribute('scope','col');
    const nh=E('th','','Quanti');nh.setAttribute('scope','col');
    trh.append(headline,nh);thead.append(trh);
    const tbody=E('tbody'); table.append(thead,tbody);tableBox.append(table);
    const footnote=E('p','sssup-a-note');
    const buttons=[];

    function show(key) {
      const group=stats.top_matematica[key];
      if(!group) return;
      for (const b of buttons) b.setAttribute('aria-pressed',String(b.dataset.top===key));
      headline.textContent=`Fra i primi ${key} della prova di matematica`;
      tbody.replaceChildren();
      const rows=[];
      if (group.completi_sostanziali) {
        for (const sub of stats.sottodomande) {
          const item = group.completi_sostanziali[sub.id];
          if (!item || item.stato === 'non_ricostruibile') continue;
          const partial = item.da_verificare > 0;
          const label = `Hanno sostanzialmente completato (${sub.id})${partial ? ' — minimo documentato' : ''}`;
          rows.push([label, `${item.documentati} su ${group.effettivi}`]);
        }
      } else if(group.completi_stretti) {
        for (const sub of stats.sottodomande) {
          if(Object.hasOwn(group.completi_stretti,sub.id))
            rows.push([`Hanno completato (${sub.id}) senza penalizzazioni`,`${group.completi_stretti[sub.id]} su ${group.effettivi}`]);
        }
      } else {
        rows.push(['Hanno ottenuto un contributo utile nel problema',`${group.contributo_problema} su ${group.effettivi}`]);
        rows.push(['Hanno raggiunto almeno metà del problema',`${group.almeno_meta} su ${group.effettivi}`]);
        rows.push(['Hanno raggiunto almeno quattro quinti del problema',`${group.almeno_quattro_quinti} su ${group.effettivi}`]);
      }
      rows.push([`Sono anche tra i primi ${key} del singolo problema`,`${group.anche_top_problema} su ${group.effettivi}`]);
      for(const [label,value] of rows) {
        const tr=E('tr');tr.append(E('td','',label),E('td','',value));
        tbody.append(tr);
      }
      const toReview = group.completi_sostanziali && Object.values(group.completi_sostanziali)
        .some(row => row.stato === 'ricostruzione_da_verificare' && row.da_verificare > 0);
      footnote.textContent=`Il gruppo comprende ${group.effettivi} elaborati${group.effettivi>Number(key)?', inclusi gli ex aequo alla soglia':''}. La classifica usa tutti e tre i problemi di matematica, non la graduatoria finale di ammissione.${toReview?' Nei conteggi segnalati come minimi documentati restano casi da verificare.':''}`;
    }
    for(const key of ['5','10','20']) {
      const b=E('button','',`Top ${key}`);
      b.type='button';b.dataset.top=key;b.setAttribute('aria-pressed','false');
      b.addEventListener('click',()=>show(key));
      chooser.append(b);buttons.push(b);
    }
    container.append(chooser,tableBox,footnote);
    show('10');
    return container;
  }

  function nativeAISummary(article) {
    const title = 'Come è andata al concorso?';
    // Prima il problema corrente; poi le altre sezioni gia' disegnate.
    const selector = 'details.extra:not(.sssup-analytics) > summary';
    const candidates = [
      ...article.querySelectorAll(selector),
      ...document.querySelectorAll(selector)
    ];
    const labels = [
      'Risposta breve', 'Soluzione redazionale', 'Soluzioni alternative',
      'Soluzione preesistente', 'Soluzione ufficiale', 'Osservazioni',
      'Commenti', 'Risposta', 'Aiutino', 'Soluzione'
    ];
    for (const original of candidates) {
      const text = original.textContent || '';
      const containsAI = /bozza\s*AI|da\s*verificare/i.test(text) ||
        !!original.querySelector('[class*="ai-"], [class*="AI"], [aria-label*="AI"]');
      if (!containsAI) continue;
      const copy = original.cloneNode(true);
      // Le eventuali etichette id non vanno duplicate nel documento.
      for (const node of [copy, ...copy.querySelectorAll('[id]')]) node.removeAttribute('id');
      const walker = document.createTreeWalker(copy, NodeFilter.SHOW_TEXT);
      let node;
      let renamed = false;
      while ((node = walker.nextNode())) {
        const value = node.nodeValue || '';
        const label = labels.find(s => value.includes(s));
        if (label && !/bozza\s*AI|da\s*verificare/i.test(value)) {
          node.nodeValue = value.replace(label, title);
          renamed = true;
          break;
        }
      }
      if (renamed) {
        copy.removeAttribute('aria-label');
        return copy;
      }
    }
    // Sicurezza: se mancano altre sezioni AI sulla pagina, non fingiamo di
    // conoscerne lo stile. Il lettore vede comunque la provenienza.
    console.warn('SSSUP statistiche: nessuna intestazione AI originale riutilizzabile');
    return E('summary','',title + ' · Bozza AI · Da verificare');
  }

  function makeSection(stats, article) {
    const details=E('details','extra sssup-analytics');
    details.dataset.field='Statistiche';
    // Copia la testata di una sezione AI esistente, inclusa l'icona originale.
    // Il testo del titolo viene cambiato; stile e provenienza sono condivisi.
    const summary = nativeAISummary(article);
    details.append(summary);
    const inner=E('div','extra-body');
    const heading=E('div','sssup-a-top');
    heading.append(E('h3','','Fin dove sono arrivati i candidati?'));
    inner.append(heading);
    text(inner,'Bozza AI · Da verificare. I conteggi e le interpretazioni richiedono un controllo editoriale.','sssup-a-note');
    text(inner,`${stats.elaborati} elaborati corretti · conteggi anonimi`,'sssup-a-kicker');
    const legend=E('div','sssup-a-legend');
    for(const [label,cls] of [['Contributo utile','a'],['Sostanzialmente completo','b']]) {
      const item=E('span');item.append(E('i',`sssup-a-chip ${cls}`),document.createTextNode(label));legend.append(item);
    }
    inner.append(legend,makeChart(stats));
    if(stats.conteggi==='minimi_documentati_semiautomatici')
      text(inner,'I valori per sottodomanda sono conteggi minimi documentati dai verbalini e richiedono ancora verifica manuale.','sssup-a-note');
    inner.append(E('h4','','Che cosa hanno fatto i migliori della prova?'),makeTopTable(stats));
    inner.append(E('h4','','Che cosa suggeriscono le correzioni?'));
    const insights=E('div','sssup-a-takeaways');
    for(const t of stats.osservazioni) insights.append(E('p','',t));
    inner.append(insights);
    const method=E('details','sssup-a-method');
    method.append(E('summary','','Come leggere e interpretare questi dati?'));
    text(method,stats.metodologia);
    text(method,'Le classifiche Top 5/10/20 si riferiscono alla sola prova di matematica. Nessuna statistica descrive la graduatoria finale d’ammissione.');
    inner.append(method);
    details.append(inner);
    const qs=new URLSearchParams(location.search);
    if(qs.get('sezione')==='Statistiche') details.open=true;
    return details;
  }

  function addToProblem(article,stats) {
    if (article.dataset.sssupStatsAttached) return;
    article.dataset.sssupStatsAttached='1';
    let extra=article.querySelector('.extra-zone');
    if (!extra) {
      extra=E('div','extra-zone');
      extra.append(E('p','extra-label','Materiali aggiuntivi · clicca per aprire'));
      article.append(extra);
    }
    const details=makeSection(stats, article);
    extra.append(details);
    if(details.open) details.scrollIntoView({block:'nearest'});
  }

  function scan() {
    if(!Number.isInteger(pageYear) || pageYear<1990) return;
    for(const article of main.querySelectorAll('article.problem')) {
      if(article.dataset.sssupStatsAttached || article.dataset.sssupStatsLoading) continue;
      const match=article.id.match(/^problema-(\d+)$/);
      if(!match) continue;
      const key=`SA_${pageYear}_${Number(match[1])}`;
      if(!problemFiles.has(key))continue;
      article.dataset.sssupStatsLoading='1';
      const promise=loaded.has(key)?loaded.get(key):fetch(PREFIX+key+'.json').then(r=>{
        if(!r.ok) throw new Error('statistiche '+key+': '+r.status);
        return r.json();
      });
      loaded.set(key,promise);
      promise.then(stats=>{
        if(stats.problema===key && stats.schema===1 && article.isConnected) addToProblem(article,stats);
      }).catch(err=>console.warn('SSSUP statistiche:',err))
        .finally(()=>{delete article.dataset.sssupStatsLoading});
    }
  }

  fetch(PREFIX+'indice.json').then(r=>{
    if(!r.ok)throw new Error('Indice statistiche non disponibile');
    return r.json();
  }).then(manifest=>{
    if(manifest.schema!==1 || !Array.isArray(manifest.problemi))return;
    for(const key of manifest.problemi)if(/^SA_\d{4}_\d+$/.test(key))problemFiles.add(key);
    scan();
    const observer = new MutationObserver(scan);
    observer.observe(main,{childList:true,subtree:true});
  }).catch(err=>console.warn('SSSUP statistiche:',err.message));
})();

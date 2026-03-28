#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""papers.json + HTML 템플릿 → papers.html 생성"""
import json, os

BASE = r"C:\Users\hsj04\HR"

with open(os.path.join(BASE, "papers.json"), encoding="utf-8") as f:
    json_str = f.read().strip()

HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>논문 검색 — HR Study</title>
<style>
:root {
  --bg: #f7f5f0; --surface: #ffffff;
  --border: rgba(0,0,0,0.09); --border-strong: rgba(0,0,0,0.18);
  --text-primary: #1a1a18; --text-secondary: #5c5c56; --text-tertiary: #9c9a90;
  --radius: 14px; --radius-sm: 8px; --nav-h: 52px;
  --accent: #1D9E75; --accent-bg: #E1F5EE; --accent-border: #9FE1CB;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif; background: var(--bg); color: var(--text-primary); min-height: 100vh; }
/* Nav */
.site-nav { position: sticky; top: 0; z-index: 100; background: var(--surface); border-bottom: 1px solid var(--border-strong); padding: 0 24px; height: var(--nav-h); }
.nav-inner { max-width: 1100px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; height: 100%; }
.nav-brand { font-family: Georgia, serif; font-size: 15px; font-weight: 600; color: var(--text-primary); text-decoration: none; }
.nav-links { display: flex; gap: 4px; }
.nav-link { font-size: 13px; color: var(--text-secondary); text-decoration: none; padding: 6px 14px; border-radius: var(--radius-sm); transition: background 0.15s, color 0.15s; }
.nav-link:hover { background: #f0eeea; color: var(--text-primary); }
.nav-link.active { background: #f0eeea; color: var(--text-primary); font-weight: 600; }
/* Layout */
.page-wrap { max-width: 1100px; margin: 0 auto; padding: 40px 24px 80px; }
.page-header { margin-bottom: 24px; }
.page-header h1 { font-family: Georgia, serif; font-size: clamp(22px, 3vw, 28px); font-weight: 600; margin-bottom: 6px; }
.page-header p { font-size: 13px; color: var(--text-secondary); }
/* Search */
.search-row { display: flex; gap: 10px; align-items: center; margin-bottom: 14px; flex-wrap: wrap; }
.search-wrap { position: relative; flex: 1; min-width: 220px; max-width: 520px; }
.search-input { width: 100%; font-size: 14px; padding: 10px 14px 10px 38px; border: 1px solid var(--border-strong); border-radius: var(--radius-sm); background: var(--surface); color: var(--text-primary); font-family: inherit; outline: none; transition: border-color 0.15s, box-shadow 0.15s; }
.search-input:focus { border-color: var(--accent); box-shadow: 0 0 0 3px rgba(29,158,117,0.1); }
.s-icon { position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: var(--text-tertiary); font-size: 15px; pointer-events: none; }
.result-count { font-size: 13px; color: var(--text-tertiary); white-space: nowrap; }
/* Filters */
.filter-bar { display: flex; gap: 6px; align-items: center; flex-wrap: wrap; padding: 10px 0 14px; border-bottom: 1px solid var(--border); margin-bottom: 20px; }
.filter-label { font-size: 11px; color: var(--text-tertiary); letter-spacing: 0.08em; text-transform: uppercase; margin-right: 2px; }
.chip { font-size: 12px; padding: 4px 12px; border-radius: 20px; border: 1px solid var(--border-strong); background: var(--surface); color: var(--text-secondary); cursor: pointer; transition: all 0.15s; user-select: none; }
.chip:hover { border-color: var(--accent); color: var(--accent); }
.chip.on { background: var(--accent-bg); border-color: var(--accent-border); color: var(--accent); font-weight: 600; }
.chip-sep { width: 1px; height: 18px; background: var(--border-strong); flex-shrink: 0; margin: 0 2px; }
/* Grid */
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(310px, 1fr)); gap: 16px; }
.card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 20px; cursor: pointer; transition: border-color 0.15s, box-shadow 0.15s; display: flex; flex-direction: column; gap: 10px; }
.card:hover { border-color: var(--accent-border); box-shadow: 0 2px 12px rgba(29,158,117,0.08); }
.card-top { display: flex; align-items: center; gap: 6px; }
.badge { font-size: 11px; padding: 2px 8px; border-radius: 4px; font-weight: 600; }
.badge-master { background: #EEF2FF; color: #4C51BF; }
.badge-phd { background: #FFF3E0; color: #E65100; }
.card-year { font-size: 12px; color: var(--text-tertiary); margin-left: auto; }
.card-title { font-size: 14px; font-weight: 600; line-height: 1.5; color: var(--text-primary); }
.card-author { font-size: 12px; color: var(--text-secondary); }
.card-vars { display: flex; flex-wrap: wrap; gap: 4px; }
.tag { font-size: 11px; padding: 2px 8px; border-radius: 4px; }
.tag-iv { background: #E8F5E9; color: #2E7D32; }
.tag-mv { background: #FFF8E1; color: #F57F17; }
.tag-dv { background: #E3F2FD; color: #1565C0; }
.score-bar { height: 3px; background: #eee; border-radius: 2px; overflow: hidden; }
.score-fill { height: 100%; background: var(--accent); border-radius: 2px; transition: width 0.3s; }
.empty-state { grid-column: 1/-1; text-align: center; padding: 60px 20px; color: var(--text-tertiary); font-size: 14px; }
/* Modal */
.modal-bg { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.45); z-index: 1000; align-items: center; justify-content: center; padding: 20px; }
.modal-bg.open { display: flex; }
.modal { background: var(--surface); border-radius: var(--radius); max-width: 720px; width: 100%; max-height: 88vh; overflow-y: auto; box-shadow: 0 20px 60px rgba(0,0,0,0.2); }
.modal-head { padding: 24px 28px 16px; border-bottom: 1px solid var(--border); position: sticky; top: 0; background: var(--surface); z-index: 1; }
.modal-close { float: right; background: none; border: none; font-size: 22px; cursor: pointer; color: var(--text-tertiary); line-height: 1; padding: 2px 4px; margin-top: -2px; }
.modal-close:hover { color: var(--text-primary); }
.m-title { font-family: Georgia, serif; font-size: 17px; font-weight: 600; line-height: 1.45; margin-bottom: 10px; padding-right: 32px; }
.m-meta { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; font-size: 12px; color: var(--text-secondary); }
.modal-body { padding: 20px 28px 28px; display: flex; flex-direction: column; gap: 18px; }
.ms h3 { font-size: 11px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--text-tertiary); margin-bottom: 6px; }
.ms p { font-size: 13px; line-height: 1.75; color: var(--text-secondary); }
.vars-row { display: flex; gap: 12px; flex-wrap: wrap; }
.var-grp { flex: 1; min-width: 130px; }
.var-grp h4 { font-size: 11px; color: var(--text-tertiary); margin-bottom: 5px; font-weight: 600; }
.var-tags { display: flex; flex-wrap: wrap; gap: 4px; }
.sim-btn { width: 100%; padding: 11px; background: var(--accent-bg); border: 1px solid var(--accent-border); border-radius: var(--radius-sm); color: var(--accent); font-size: 13px; font-weight: 600; cursor: pointer; transition: background 0.15s; font-family: inherit; }
.sim-btn:hover { background: #c8ede2; }
</style>
</head>
<body>
<nav class="site-nav">
  <div class="nav-inner">
    <a class="nav-brand" href="index.html">HR Study</a>
    <div class="nav-links">
      <a class="nav-link" href="index.html">이론 카드</a>
      <a class="nav-link" href="leadership.html">리더십</a>
      <a class="nav-link" href="topics.html">주제 탐색</a>
      <a class="nav-link" href="references.html">참고자료</a>
      <a class="nav-link active" href="papers.html">논문 검색</a>
    </div>
  </div>
</nav>
<div class="page-wrap">
  <div class="page-header">
    <h1>논문 검색</h1>
    <p>윤제방 지도 논문 48편 · 키워드를 입력하면 유사한 논문을 찾아드립니다</p>
  </div>
  <div class="search-row">
    <div class="search-wrap">
      <span class="s-icon">&#128269;</span>
      <input class="search-input" id="q" type="text" placeholder="키워드 검색 (예: 리더십, 조직몰입, 혁신행동, 이직의도)" autocomplete="off">
    </div>
    <span class="result-count" id="cnt"></span>
  </div>
  <div class="filter-bar" id="filters"></div>
  <div class="grid" id="grid"></div>
</div>
<div class="modal-bg" id="modal">
  <div class="modal">
    <div class="modal-head">
      <button class="modal-close" id="mclose">&#215;</button>
      <div class="m-title" id="m-title"></div>
      <div class="m-meta" id="m-meta"></div>
    </div>
    <div class="modal-body" id="m-body"></div>
  </div>
</div>
<script>
const PAPERS = __JSON__;

const TOPICS = {
  '리더십':['리더십','리더'],
  '조직몰입':['조직몰입','직무몰입','몰입'],
  '혁신/창의':['혁신','창의성','혁신행동','혁신저항'],
  '커뮤니케이션':['커뮤니케이션','의사소통'],
  '조직시민행동':['조직시민행동','시민행동'],
  '이직의도':['이직의도','이직'],
  '창업/벤처':['창업','벤처','기업가'],
  '기술수용':['기술수용','수용의도','기술수용모델'],
};

let af = { degree:null, year:null, topic:null };
let terms = [];

function score(p, ts) {
  if (!ts.length) return 1;
  let s = 0;
  const tl = p.title;
  const vars = [...p.iv,...p.mv,...p.dv].join(' ');
  const pur = p.purpose;
  ts.forEach(t => {
    if (tl.includes(t)) s += 4;
    if (vars.includes(t)) s += 2;
    if (pur.includes(t)) s += 1;
  });
  return s;
}

function matchTopic(p, key) {
  const kws = TOPICS[key];
  const h = (p.title + ' ' + [...p.iv,...p.mv,...p.dv].join(' '));
  return kws.some(k => h.includes(k));
}

function esc(s) {
  return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function render() {
  let list = PAPERS.map(p => ({p, s:score(p, terms)}));
  if (terms.length) list = list.filter(x => x.s > 0);
  if (af.degree) list = list.filter(x => x.p.degree === af.degree);
  if (af.year) list = list.filter(x => String(x.p.year) === af.year);
  if (af.topic) list = list.filter(x => matchTopic(x.p, af.topic));
  list.sort((a,b) => b.s-a.s || b.p.year-a.p.year);
  const maxS = list.length ? Math.max(...list.map(x=>x.s),1) : 1;
  document.getElementById('cnt').textContent = list.length + '편';
  const grid = document.getElementById('grid');
  if (!list.length) { grid.innerHTML = '<div class="empty-state">검색 결과가 없습니다</div>'; return; }
  grid.innerHTML = list.map(({p,s}) => {
    const deg = p.degree==='박사'?'badge-phd':'badge-master';
    const ivT = p.iv.map(v=>'<span class="tag tag-iv">'+esc(v)+'</span>').join('');
    const mvT = p.mv.map(v=>'<span class="tag tag-mv">'+esc(v)+'</span>').join('');
    const dvT = p.dv.map(v=>'<span class="tag tag-dv">'+esc(v)+'</span>').join('');
    const all = ivT+mvT+dvT;
    const pct = terms.length ? Math.round(s/maxS*100) : 0;
    return '<div class="card" data-id="'+esc(p.id)+'">'+
      '<div class="card-top"><span class="badge '+deg+'">'+esc(p.degree)+'</span><span class="card-year">'+p.year+'</span></div>'+
      '<div class="card-title">'+esc(p.title)+'</div>'+
      '<div class="card-author">'+esc(p.author)+(p.professor?' · 지도: '+esc(p.professor):'')+'</div>'+
      (all?'<div class="card-vars">'+all+'</div>':'')+
      (pct>0?'<div class="score-bar"><div class="score-fill" style="width:'+pct+'%"></div></div>':'')+
    '</div>';
  }).join('');
}

function buildFilters() {
  const years = [...new Set(PAPERS.map(p=>p.year))].sort((a,b)=>b-a);
  let h = '<span class="filter-label">학위</span>';
  ['석사','박사'].forEach(d => h+='<span class="chip" data-t="degree" data-v="'+d+'">'+d+'</span>');
  h += '<div class="chip-sep"></div><span class="filter-label">연도</span>';
  years.forEach(y => h+='<span class="chip" data-t="year" data-v="'+y+'">'+y+'</span>');
  h += '<div class="chip-sep"></div><span class="filter-label">주제</span>';
  Object.keys(TOPICS).forEach(t => h+='<span class="chip" data-t="topic" data-v="'+t+'">'+t+'</span>');
  document.getElementById('filters').innerHTML = h;
  document.querySelectorAll('.chip').forEach(c => {
    c.addEventListener('click', () => {
      const t=c.dataset.t, v=c.dataset.v;
      if (af[t]===v) { af[t]=null; c.classList.remove('on'); }
      else { document.querySelectorAll('.chip[data-t="'+t+'"]').forEach(x=>x.classList.remove('on')); af[t]=v; c.classList.add('on'); }
      render();
    });
  });
}

document.getElementById('q').addEventListener('input', e => {
  terms = e.target.value.trim().split(/[\s,]+/).filter(Boolean);
  render();
});

document.getElementById('grid').addEventListener('click', e => {
  const card = e.target.closest('.card');
  if (card) { const p = PAPERS.find(x=>x.id===card.dataset.id); if(p) openModal(p); }
});

function openModal(p) {
  document.getElementById('m-title').textContent = p.title;
  document.getElementById('m-meta').innerHTML =
    '<span class="badge '+(p.degree==='박사'?'badge-phd':'badge-master')+'">'+esc(p.degree)+'</span>'+
    '<span>'+p.year+'년</span><span>저자: '+esc(p.author)+'</span>'+
    (p.professor?'<span>지도교수: '+esc(p.professor)+'</span>':'');
  let body = '';
  if (p.background) body += '<div class="ms"><h3>배경</h3><p>'+esc(p.background)+'</p></div>';
  if (p.purpose)    body += '<div class="ms"><h3>연구 목적</h3><p>'+esc(p.purpose)+'</p></div>';
  const hv = p.iv.length||p.mv.length||p.dv.length;
  if (hv) {
    body += '<div class="ms"><h3>연구 변수</h3><div class="vars-row">';
    if (p.iv.length) body += '<div class="var-grp"><h4>독립변수</h4><div class="var-tags">'+p.iv.map(v=>'<span class="tag tag-iv">'+esc(v)+'</span>').join('')+'</div></div>';
    if (p.mv.length) body += '<div class="var-grp"><h4>매개/조절변수</h4><div class="var-tags">'+p.mv.map(v=>'<span class="tag tag-mv">'+esc(v)+'</span>').join('')+'</div></div>';
    if (p.dv.length) body += '<div class="var-grp"><h4>종속변수</h4><div class="var-tags">'+p.dv.map(v=>'<span class="tag tag-dv">'+esc(v)+'</span>').join('')+'</div></div>';
    body += '</div></div>';
  }
  if (p.hypo_summary) body += '<div class="ms"><h3>가설 결과</h3><p>'+esc(p.hypo_summary)+'</p></div>';
  body += '<button class="sim-btn" id="sbtn">&#128269; 유사 논문 찾기 (변수 기반)</button>';
  document.getElementById('m-body').innerHTML = body;
  document.getElementById('modal').classList.add('open');
  document.getElementById('sbtn').addEventListener('click', () => {
    const kws = [...p.iv,...p.mv,...p.dv].slice(0,3);
    const q = kws.join(' ') || p.title.slice(0,8);
    document.getElementById('modal').classList.remove('open');
    const inp = document.getElementById('q');
    inp.value = q; inp.dispatchEvent(new Event('input')); inp.focus();
    window.scrollTo({top:0, behavior:'smooth'});
  });
}

document.getElementById('modal').addEventListener('click', e => { if(e.target.id==='modal') document.getElementById('modal').classList.remove('open'); });
document.getElementById('mclose').addEventListener('click', () => document.getElementById('modal').classList.remove('open'));
document.addEventListener('keydown', e => { if(e.key==='Escape') document.getElementById('modal').classList.remove('open'); });

buildFilters();
render();
</script>
</body>
</html>"""

HTML = HTML.replace('__JSON__', json_str)

out = os.path.join(BASE, "papers.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(HTML)

print(f"OK: papers.html ({len(HTML):,} bytes)")

import os,re,json
base=os.path.dirname(os.path.abspath(__file__))
OUT_ROOT='D:/AI/Dev/computer-mini-lessons'
_css_src=os.path.join(base,'browser','slides.html')
if not os.path.exists(_css_src): _css_src=os.path.join(OUT_ROOT,'browser-basics','index.html')
src=open(_css_src,encoding='utf-8').read()
CSS=src[src.index('<style>')+7:src.index('</style>')]

EXTRA_CSS=r'''
.hsgrid{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;width:min(1000px,100%)}
.hs{border:4px solid var(--primary);background:#fff;color:var(--primary);border-radius:18px;padding:.35em .9em;font-size:var(--t-body);font-weight:800}
.hs.on{background:var(--accent);border-color:var(--accent);color:#fff}
.lgf{display:flex;flex-direction:column;gap:10px;align-items:flex-start}
.lgf label{display:flex;gap:10px;align-items:center;font-size:var(--t-body);font-weight:800}
.lgf input,.dlg input{font:inherit;font-weight:700;border:4px solid var(--line);border-radius:14px;padding:.2em .5em;background:#fff;color:var(--ink);min-width:0}
.lgf input:focus,.dlg input:focus{border-color:var(--primary);outline:none}
.lgmsg{font-size:var(--t-caption);color:var(--accent);min-height:1.4em}
.desk{position:relative;min-height:clamp(190px,34vh,300px);background:#BFD9F2;border-radius:0}
.win{position:absolute;width:min(62%,420px);background:#fff;border:4px solid var(--line);border-radius:12px;overflow:hidden;box-shadow:0 6px 16px rgba(0,0,0,.18)}
.win.on{border-color:var(--primary)}
.wtitle{display:flex;justify-content:space-between;align-items:center;background:#E9E2D3;padding:4px 8px;font-size:var(--t-caption);font-weight:800}
.win.on .wtitle{background:var(--primary-soft)}
.wbtns{display:flex;gap:6px}
.wb{border:0;border-radius:8px;background:#fff;width:1.9em;height:1.9em;font-weight:900;font-size:var(--t-caption)}
.wbody{padding:8px 12px;font-size:var(--t-caption);color:var(--muted);min-height:3.2em}
.taskbar{display:flex;gap:6px;background:#2B3640;padding:6px 8px;flex-wrap:wrap;align-items:center}
.tbtn{border:0;border-radius:8px;background:#4A5865;color:#fff;padding:.25em .8em;font-size:var(--t-caption);font-weight:800}
.tbtn.on{background:var(--accent)}
.tbtn.alt{margin-left:auto;background:var(--primary)}
.dlg{background:#fff;border:4px solid var(--line);border-radius:14px;padding:10px 14px;display:flex;flex-direction:column;gap:10px;width:100%}
.dtitle{font-weight:900;font-size:var(--t-body)}
.drow{display:flex;gap:10px;align-items:center;flex-wrap:wrap;font-size:var(--t-body);font-weight:800}
.fd{border:4px solid var(--primary);background:#fff;color:var(--primary);border-radius:14px;padding:.2em .8em;font-size:var(--t-caption);font-weight:800}
.fd.on{background:var(--primary);color:#fff}
.flist{font-size:var(--t-caption);color:var(--muted);min-height:2em}
.rlist{display:flex;flex-direction:column;gap:8px;width:100%}
.res{display:block;text-align:left;border:4px solid var(--line);background:#fff;border-radius:16px;padding:.35em .8em;font-size:var(--t-caption);font-weight:800;color:var(--ink)}
.res small{display:inline-block;margin-left:.6em;color:#2B7A3E;font-size:.85em}
.slide>*{flex-shrink:0}
.res .ad{background:var(--accent);color:#fff;border-radius:6px;padding:0 .4em;margin-right:.4em;font-size:.85em}
.res.ok{border-color:var(--good);background:var(--good-soft)}
.res.no{border-color:var(--accent);background:var(--accent-soft)}
.popwrap{position:relative;min-height:clamp(170px,30vh,260px);display:flex;align-items:center;justify-content:center;background:repeating-linear-gradient(45deg,#fff,#fff 12px,#F6F0E2 12px,#F6F0E2 24px)}
.popup{position:relative;background:#FFE6E6;border:5px solid #E04B4B;border-radius:16px;padding:12px 16px 12px;display:flex;flex-direction:column;gap:8px;align-items:center;text-align:center;font-size:var(--t-body);font-weight:900;max-width:92%}
.popup .px{position:absolute;top:2px;right:4px;border:0;background:transparent;color:#666;font-size:.8rem;width:1.6em;height:1.6em}
.popup .claim{border:0;border-radius:999px;background:#E04B4B;color:#fff;padding:.3em 1.2em;font-size:var(--t-body);font-weight:900}
.sndrow{display:flex;gap:10px;align-items:center;flex-wrap:wrap;font-size:var(--t-body);font-weight:800;justify-content:center}
.sndicon{font-size:calc(var(--t-body)*2)}
input[type=range]{width:min(320px,60vw);height:2em;accent-color:var(--primary)}
@media (max-height:780px){.desk{min-height:150px}.popwrap{min-height:140px}.slide[data-type=stepper] .switch button{padding:.3em 1.2em}}
'''

CORE_JS=r'''
(function(){
  document.body.classList.remove('nojs');document.body.classList.add('js');
  var CFG=__CFG__;
  var slides=[].slice.call(document.querySelectorAll('.slide')),total=slides.length,cur=0;
  var phaseEl=document.getElementById('section-tag'),pageEl=document.getElementById('page-info'),progEl=document.getElementById('progress'),liveEl=document.getElementById('live');
  var prevB=document.getElementById('prev'),nextB=document.getElementById('next'),notesEl=document.getElementById('notes');
  function say(t){liveEl.textContent=t}
  function mark(sec,k){var e=sec.querySelector('[data-t="'+k+'"]');if(e)e.classList.add('done')}
  function unmark(sec){sec.querySelectorAll('[data-t]').forEach(function(e){e.classList.remove('done')})}
  function esc(s){return String(s).split('&').join('&amp;').split('<').join('&lt;').split('>').join('&gt;')}
  function go(n){
    n=Math.max(0,Math.min(total-1,n));cur=n;
    slides.forEach(function(s,i){s.classList.toggle('active',i===n)});
    var s=slides[n];phaseEl.textContent=s.getAttribute('data-section');pageEl.textContent=(n+1)+' / '+total;
    progEl.style.width=((n+1)/total*100)+'%';prevB.disabled=n===0;nextB.disabled=n===total-1;notesEl.textContent=CFG.notes[n]||'';
    if(history.replaceState)history.replaceState(null,'','#'+(n+1));
    say('第 '+(n+1)+' 頁，'+s.getAttribute('aria-label'));s.scrollTop=0;
    var h=s.querySelector('h1,h2');if(h){h.setAttribute('tabindex','-1');h.focus({preventScroll:true})}
  }
  prevB.addEventListener('click',function(){go(cur-1)});nextB.addEventListener('click',function(){go(cur+1)});
  document.querySelectorAll('[data-go]').forEach(function(b){b.addEventListener('click',function(){go(+b.getAttribute('data-go')-1)})});
  document.addEventListener('keydown',function(e){
    var t=e.target.tagName,k=e.key;
    if(t==='INPUT'||t==='TEXTAREA')return;
    if(t==='BUTTON'&&(k==='ArrowRight'||k==='ArrowLeft')){e.preventDefault();go(cur+(k==='ArrowRight'?1:-1));return}
    if(t==='BUTTON')return;
    if(k==='ArrowRight'||k==='PageDown'||k===' '){e.preventDefault();go(cur+1)}
    else if(k==='ArrowLeft'||k==='PageUp'){e.preventDefault();go(cur-1)}
    else if(k==='Home')go(0);else if(k==='End')go(total-1);
    else if(k==='f'||k==='F'){if(document.fullscreenElement)document.exitFullscreen();else document.documentElement.requestFullscreen&&document.documentElement.requestFullscreen()}
    else if(k==='n'||k==='N')notesEl.classList.toggle('show');
  });
  window.addEventListener('hashchange',function(){var x=parseInt(location.hash.slice(1),10);if(x>=1&&x<=total&&x-1!==cur)go(x-1)});

  /* hotspot */
  document.querySelectorAll('section[data-type=hotspot]').forEach(function(sec){
    var exp=sec.querySelector('.explain');
    sec.querySelectorAll('.hs').forEach(function(b){b.addEventListener('click',function(){
      sec.querySelectorAll('.hs').forEach(function(x){x.classList.remove('on')});b.classList.add('on');
      exp.innerHTML='<span><b style="color:var(--accent)">'+esc(b.getAttribute('data-name'))+'</b>　'+esc(b.getAttribute('data-info'))+'</span>';
      say(b.getAttribute('data-name')+'：'+b.getAttribute('data-info'));
    })});
  });
  /* quiz */
  document.querySelectorAll('section[data-type=quiz]').forEach(function(sec){
    var items=JSON.parse(sec.querySelector('.qdata').textContent);
    var qt=sec.querySelector('.qtext'),qo=sec.querySelector('.opts'),fb=sec.querySelector('.feedback'),sc=sec.querySelector('.qscore'),nx=sec.querySelector('.qnextbtn');
    var i=0,ok=0,done=false;
    function load(){
      var d=items[i];done=false;qt.textContent=(i+1)+'. '+d.q;fb.textContent='';qo.innerHTML='';nx.disabled=true;
      nx.textContent=i===items.length-1?'再玩一次 ↺':'下一題 ▶';
      d.o.forEach(function(t,j){
        var b=document.createElement('button');b.type='button';b.className='opt';b.textContent=t;
        b.addEventListener('click',function(){
          if(done)return;
          if(j===d.a){done=true;ok++;b.classList.add('ok');fb.textContent=d.e;nx.disabled=false;say(d.e);sc.textContent='第 '+(i+1)+' / '+items.length+' 題　答對 '+ok+' 題'}
          else{b.classList.add('no');fb.textContent='再想想看，還有別的選擇。';say('再想想看')}
        });qo.appendChild(b);
      });
      sc.textContent='第 '+(i+1)+' / '+items.length+' 題　答對 '+ok+' 題';
    }
    nx.addEventListener('click',function(){if(i===items.length-1){i=0;ok=0}else i++;load()});
    load();
  });
  /* stepper */
  document.querySelectorAll('section[data-type=stepper]').forEach(function(sec){
    var st=[].slice.call(sec.querySelectorAll('.step')),si=0,pb=sec.querySelector('.stprev'),nb=sec.querySelector('.stnext');
    function set(n){si=Math.max(0,Math.min(st.length-1,n));st.forEach(function(e,i){e.classList.toggle('now',i===si);e.classList.toggle('dim',i>si)});
      pb.style.opacity=si===0?.35:1;nb.style.opacity=si===st.length-1?.35:1;say('第 '+(si+1)+' 步：'+st[si].querySelector('.stext').textContent)}
    pb.addEventListener('click',function(){set(si-1)});nb.addEventListener('click',function(){set(si+1)});set(0);
  });
  /* reveal */
  document.querySelectorAll('section[data-type=reveal] .card3').forEach(function(c){c.addEventListener('click',function(){var on=c.getAttribute('aria-expanded')==='true';c.setAttribute('aria-expanded',!on);if(!on)say(c.querySelector('.detail').textContent)})});

  var SIMS={};
  /* ---- login ---- */
  SIMS.login=function(sec){
    var page=sec.querySelector('.lgpage'),state='user',show=false,t0=0;
    function render(msg){
      var h='';
      if(state==='user')h='<span class="big">登入</span><form class="lgf"><label>帳號 <input class="lgi" type="text" autocomplete="off" autocapitalize="off" spellcheck="false" aria-label="帳號"></label><div class="switch"><button type="submit" class="mini">下一步</button></div></form>';
      else if(state==='pass')h='<span class="big">歡迎，stu05</span><form class="lgf"><label>密碼 <input class="lgi" type="'+(show?'text':'password')+'" autocomplete="off" aria-label="密碼"></label><div class="switch"><button type="button" class="mini lgshow">'+(show?'隱藏密碼':'顯示密碼')+'</button><button type="submit" class="mini">登入</button></div></form>';
      else h='<span class="big">登入成功！</span><p class="caption">'+esc(msg||'')+'</p><div class="switch"><button type="button" class="mini lgav">👤 頭像（點我看選單）</button><button type="button" class="mini lgout" hidden>登出</button></div>';
      page.innerHTML=h+'<div class="lgmsg" aria-live="polite">'+(state!=='in'&&msg?esc(msg):'')+'</div>';
      var inp=page.querySelector('.lgi');
      if(inp){inp.addEventListener('focus',function(){if(!t0)t0=Date.now()});if(show&&state==='pass'){}}
      var f=page.querySelector('form');
      if(f)f.addEventListener('submit',function(e){e.preventDefault();var v=inp.value;
        if(state==='user'){
          if(!v.trim())return render('還沒打帳號喔。');
          if(v.trim()==='stu05@school.example'){mark(sec,'user');state='pass';render('');say('帳號正確，換打密碼');var n=page.querySelector('.lgi');if(n)n.focus()}
          else if(v.indexOf('@')<0)render('帳號少了 @。按住 Shift 再按 2。');
          else render('帳號有地方打錯了，對照看看。右下角是不是英文？');
        }else{
          if(v==='cat123'){mark(sec,'pass');mark(sec,'in');state='in';var sec2=t0?Math.round((Date.now()-t0)/1000):0;render('用了 '+sec2+' 秒。用完要登出：點下面的頭像。');say('登入成功')}
          else render('密碼不對。點「顯示密碼」看看打了什麼。');
        }
      });
      var sh=page.querySelector('.lgshow');if(sh)sh.addEventListener('click',function(){var v=page.querySelector('.lgi').value;show=!show;render('');var n=page.querySelector('.lgi');n.value=v;n.focus()});
      var av=page.querySelector('.lgav');if(av)av.addEventListener('click',function(){page.querySelector('.lgout').hidden=false});
      var lo=page.querySelector('.lgout');if(lo)lo.addEventListener('click',function(){mark(sec,'out');state='user';t0=0;show=false;render('已登出，下一個同學可以安心用了。');say('已登出')});
    }
    render('');
    var rs=sec.querySelector('.simreset');if(rs)rs.addEventListener('click',function(){unmark(sec);state='user';show=false;t0=0;render('')});
  };
  /* ---- windows ---- */
  SIMS.windows=function(sec){
    var desk=sec.querySelector('.desk'),bar=sec.querySelector('.taskbar'),exp=sec.querySelector('.explain');
    var W,act,webMin;
    var BODY={note:'今天要交的作業：我愛電腦課。',web:'這是一個網頁，正在看恐龍資料。',paint:'這是一幅還沒畫完的圖。'};
    function msg(t){exp.innerHTML='<span>'+esc(t)+'</span>';say(t)}
    function vis(){return W.filter(function(w){return !w.min&&!w.x})}
    function fixAct(){var v=vis();if(!v.some(function(w){return w.id===act}))act=v.length?v[v.length-1].id:''}
    function render(){
      desk.innerHTML='';
      var v=vis().sort(function(a,b){return (a.id===act)-(b.id===act)});
      v.forEach(function(w,i){
        var d=document.createElement('div');d.className='win'+(w.id===act?' on':'');d.style.left=(8+i*26)+'px';d.style.top=(8+i*22)+'px';
        d.innerHTML='<div class="wtitle"><span>'+w.t+'</span><span class="wbtns"><button type="button" class="wb wmin" aria-label="最小化 '+w.t+'">−</button><button type="button" class="wb wx" aria-label="關閉 '+w.t+'">×</button></span></div><div class="wbody">'+BODY[w.id]+'</div>';
        d.querySelector('.wmin').addEventListener('click',function(){w.min=true;if(w.id==='web'){webMin=true;mark(sec,'min')}fixAct();msg('「'+w.t+'」縮到下面的工作列了。');render()});
        d.querySelector('.wx').addEventListener('click',function(){w.x=true;if(w.id==='paint')mark(sec,'close');fixAct();msg('「'+w.t+'」關掉了。');render()});
        d.addEventListener('mousedown',function(){act=w.id;render()});
        desk.appendChild(d);
      });
      bar.innerHTML='';
      W.filter(function(w){return !w.x}).forEach(function(w){
        var b=document.createElement('button');b.type='button';b.className='tbtn'+(w.id===act&&!w.min?' on':'');b.textContent=w.t+(w.min?'（縮小了）':'');
        b.addEventListener('click',function(){
          if(w.min){w.min=false;act=w.id;if(w.id==='web'&&webMin){mark(sec,'restore');webMin=false}msg('從工作列叫回「'+w.t+'」。')}
          else if(w.id===act){w.min=true;if(w.id==='web'){webMin=true;mark(sec,'min')}fixAct();msg('再按一次，縮小「'+w.t+'」。')}
          else{act=w.id;msg('切換到「'+w.t+'」。')}
          render();
        });bar.appendChild(b);
      });
      var a=document.createElement('button');a.type='button';a.className='tbtn alt';a.textContent='Alt + Tab 切換';
      a.addEventListener('click',function(){var v=W.filter(function(w){return !w.min&&!w.x});if(!v.length)return;var i=0;v.forEach(function(w,j){if(w.id===act)i=j});act=v[(i+1)%v.length].id;if(act==='note')mark(sec,'alt');msg('Alt + Tab：換到下一個視窗。');render()});
      bar.appendChild(a);
    }
    function init(){W=[{id:'note',t:'📝 記事本',min:false,x:false},{id:'web',t:'🌐 瀏覽器',min:false,x:false},{id:'paint',t:'🎨 小畫家',min:false,x:false}];act='paint';webMin=false;unmark(sec);msg('試試看，每個動作都會打勾。');render()}
    var rs=sec.querySelector('.simreset');if(rs)rs.addEventListener('click',init);
    init();
  };
  /* ---- search results ---- */
  SIMS.search=function(sec){
    var list=sec.querySelector('.rlist'),exp=sec.querySelector('.explain');
    var R=CFG.results;
    R.forEach(function(r){
      var b=document.createElement('button');b.type='button';b.className='res';
      b.innerHTML=(r.ad?'<span class="ad">廣告</span>':'')+esc(r.t)+'<small>'+esc(r.u)+'</small>';
      b.addEventListener('click',function(){
        b.classList.add(r.ok?'ok':'no');exp.innerHTML='<span>'+esc(r.e)+'</span>';say(r.e);
        if(r.ok)mark(sec,'pick');
      });list.appendChild(b);
    });
    var rs=sec.querySelector('.simreset');if(rs)rs.addEventListener('click',function(){unmark(sec);list.querySelectorAll('.res').forEach(function(b){b.classList.remove('ok','no')});exp.innerHTML='<span>哪一個最可靠？點點看。</span>'});
  };
  /* ---- save ---- */
  SIMS.save=function(sec){
    var area=sec.querySelector('.savearea'),folder='',name='',files=[],view='dlg';
    function okName(s){if(!s)return false;for(var i=0;i<s.length;i++){var c=s.charCodeAt(i);if(!((c>=48&&c<=57)||(c>=65&&c<=90)||(c>=97&&c<=122)))return false}return true}
    function render(msg){
      var FD=['桌面','文件','下載'],h;
      if(view==='dlg'){
        h='<div class="dlg"><div class="dtitle">另存新檔</div><div class="drow"><span>存到哪裡：</span>'+FD.map(function(f){return '<button type="button" class="fd'+(folder===f?' on':'')+'" data-f="'+f+'">📁 '+f+'</button>'}).join('')+'</div><div class="drow"><label>檔名：<input class="fn" type="text" autocomplete="off" autocapitalize="off" spellcheck="false" placeholder="例如 amy05" aria-label="檔名"></label><span class="caption">.txt</span></div><div class="switch"><button type="button" class="mini sv">存檔</button></div><div class="lgmsg" aria-live="polite">'+esc(msg||'')+'</div></div>';
      }else{
        h='<div class="dlg"><div class="dtitle">檔案總管：找找看，你的檔案在哪個資料夾？</div><div class="drow">'+FD.map(function(f){return '<button type="button" class="fd ex" data-f="'+f+'">📁 '+f+'</button>'}).join('')+'</div><div class="flist" aria-live="polite">'+esc(msg||'點一個資料夾打開看看。')+'</div></div>';
      }
      area.innerHTML=h;
      var fn=area.querySelector('.fn');if(fn){fn.value=name;fn.addEventListener('input',function(){name=fn.value})}
      area.querySelectorAll('.fd:not(.ex)').forEach(function(b){b.addEventListener('click',function(){folder=b.getAttribute('data-f');if(folder==='文件')mark(sec,'folder');render('');var n=area.querySelector('.fn');if(n)n.focus()})});
      var sv=area.querySelector('.sv');
      if(sv)sv.addEventListener('click',function(){
        if(!folder)return render('還沒選要存到哪裡。');
        if(!name)return render('還沒取檔名。');
        if(!okName(name))return render('檔名只用英文和數字，不要空白或符號。');
        mark(sec,'name');files.push({f:folder,n:name+'.txt'});mark(sec,'save');view='find';
        render('存好了！存在「'+folder+'」。現在去找找看。');say('存好了');
      });
      area.querySelectorAll('.fd.ex').forEach(function(b){b.addEventListener('click',function(){
        var f=b.getAttribute('data-f'),hit=files.filter(function(x){return x.f===f});
        if(hit.length){mark(sec,'find');render('在「'+f+'」找到了：'+hit.map(function(x){return x.n}).join('、')+'。')}
        else render('「'+f+'」裡面沒有你的檔案，再找別的資料夾。');
      })});
    }
    render('');
    var rs=sec.querySelector('.simreset');if(rs)rs.addEventListener('click',function(){unmark(sec);folder='';name='';files=[];view='dlg';render('')});
  };
  /* ---- popup ---- */
  SIMS.popup=function(sec){
    var wrap=sec.querySelector('.popwrap'),exp=sec.querySelector('.explain'),cdEl=sec.querySelector('.cd'),tick=null;
    function msg(t){exp.innerHTML='<span>'+esc(t)+'</span>';say(t)}
    function start(){var s=599;cdEl.textContent='09:59';clearInterval(tick);tick=setInterval(function(){if(s<=0){clearInterval(tick);return}s--;var m=Math.floor(s/60),x=s%60;cdEl.textContent=(m<10?'0':'')+m+':'+(x<10?'0':'')+x},1000)}
    function reset(){unmark(sec);var p=wrap.querySelector('.popup');p.hidden=false;msg('網站突然跳出一個視窗，你要怎麼辦？');start()}
    wrap.querySelector('.claim').addEventListener('click',function(){msg('糟糕！點「立即領取」可能被騙走帳號密碼。不要輸入任何東西，馬上告訴老師。')});
    wrap.querySelector('.px').addEventListener('click',function(){wrap.querySelector('.popup').hidden=true;mark(sec,'close');msg('關掉了，很好！但它可能再跳出來，還是要告訴老師。')});
    sec.querySelector('.tell').addEventListener('click',function(){mark(sec,'tell');msg('最棒！遇到奇怪的彈出視窗：不點、不填、先告訴老師。')});
    var rs=sec.querySelector('.simreset');if(rs)rs.addEventListener('click',reset);
    reset();
  };
  /* ---- sound ---- */
  SIMS.sound=function(sec){
    var icon=sec.querySelector('.sndicon'),vol=sec.querySelector('.vol'),mu=sec.querySelector('.mute'),pl=sec.querySelector('.plug'),play=sec.querySelector('.play'),exp=sec.querySelector('.explain');
    var muted,plug;
    function msg(t){exp.innerHTML='<span>'+esc(t)+'</span>';say(t)}
    function paint(){
      var off=muted||+vol.value===0;icon.textContent=off?'🔇':'🔊';
      mu.textContent=muted?'🔇 靜音中（按我取消）':'🔈 沒有靜音';mu.setAttribute('aria-pressed',muted);
      pl.textContent=plug?'🎧 耳機插好了':'🎧 耳機沒插好（按我插好）';pl.setAttribute('aria-pressed',plug);
    }
    function init(){muted=true;plug=false;vol.value=0;unmark(sec);paint();msg('這台電腦沒有聲音！找找看有哪些原因。')}
    mu.addEventListener('click',function(){muted=!muted;if(!muted)mark(sec,'mute');paint()});
    vol.addEventListener('input',function(){if(+vol.value>=30)mark(sec,'vol');paint()});
    pl.addEventListener('click',function(){plug=!plug;if(plug)mark(sec,'plug');paint()});
    play.addEventListener('click',function(){
      if(muted)msg('還是沒聲音：喇叭被「靜音」了。');
      else if(+vol.value<30)msg('還是沒聲音：音量太小，把滑桿往右拉。');
      else if(!plug)msg('還是沒聲音：耳機沒插好，要插到底。');
      else{mark(sec,'ok');msg('🔊 有聲音了！下次沒聲音，照這個順序檢查。')}
    });
    var rs=sec.querySelector('.simreset');if(rs)rs.addEventListener('click',init);
    init();
  };
  document.querySelectorAll('section[data-type=sim]').forEach(function(sec){var f=SIMS[sec.getAttribute('data-sim')];if(f)f(sec)});

  var h=parseInt(location.hash.slice(1),10);go(h>=1&&h<=total?h-1:0);
})();
'''

def H(s):  # html escape for attribute values
    return s.replace('&','&amp;').replace('"','&quot;').replace('<','&lt;')

def page_html(n,pg,total):
    t=pg['type']
    phase='引起動機' if n==1 else ('喚起行動' if n>=total-1 else '維持注意')
    inter={'cover':'none','hotspot':'hotspot','quiz':'quiz','stepper':'stepper','sim':'quiz','reveal':'reveal'}[t]
    cls='slide cover active' if n==1 else 'slide'
    pga='' if n==1 else ' data-pg="brw"'
    simattr=' data-sim="%s"'%pg['sim'] if t=='sim' else ''
    head='<section class="%s" data-slide="%d" data-section="%s" data-interaction="%s" data-type="%s"%s aria-label="%s"%s>\n'%(cls,n,phase,inter,t,simattr,H(pg['label']),pga)
    k='  <p class="kicker">%s</p>\n'%pg.get('kicker','')
    if t=='cover':
        body='  <p class="kicker">電腦小知識</p>\n  <h1>%s</h1>\n  <div class="motif" aria-hidden="true">%s</div>\n  <p class="caption">%s</p>\n  <button class="startbtn" type="button" data-go="2">開始 ▶</button>\n'%(pg['title'],''.join('<span class="cap%s">%s</span>'%(' hot' if i==1 else '',m) for i,m in enumerate(pg['motif'])),pg['caption'])
    elif t=='hotspot':
        btns=''.join('<button type="button" class="hs" data-name="%s" data-info="%s">%s</button>'%(H(a),H(b),a) for a,b in pg['items'])
        stat=''.join('<p>%s：%s</p>'%(a,b) for a,b in pg['items'])
        body=k+'  <h2>%s</h2>\n  <div class="hsgrid">%s</div>\n  <div class="explain" aria-live="polite"><span>點上面的任何一個，看看它是什麼。</span></div>\n  <div class="static-only qstatic">%s</div>\n'%(pg['title'],btns,stat)
    elif t=='quiz':
        stat=''.join('<p>%s → %s</p>'%(it['q'],it['o'][it['a']]) for it in pg['items'])
        body=k+'  <h2>%s</h2>\n  <div class="quizbox"><p class="qtext"></p><div class="opts"></div><div class="feedback" aria-live="polite"></div><div class="qctl"><span class="caption qscore"></span><button type="button" class="mini qnextbtn">下一題 ▶</button></div></div>\n  <script type="application/json" class="qdata">%s</script>\n  <div class="static-only qstatic">%s</div>\n'%(pg['title'],json.dumps(pg['items'],ensure_ascii=False).replace('</','<\\/'),stat)
    elif t=='stepper':
        lis=''.join('<li class="step"><span class="num">%d</span><span class="stext">%s</span></li>'%(i+1,s) for i,s in enumerate(pg['steps']))
        body=k+'  <h2>%s</h2>\n  <ol class="steps">%s</ol>\n  <div class="switch"><button type="button" class="stprev">◀ 上一步</button><button type="button" class="stnext">下一步 ▶</button></div>\n'%(pg['title'],lis)
    elif t=='reveal':
        cards=''.join('<button type="button" class="card3" aria-expanded="false"><span class="ct">%s</span><span class="detail">%s</span></button>'%(a,b) for a,b in pg['cards'])
        cols='repeat(2,1fr)' if len(pg['cards'])<=4 else 'repeat(3,1fr)'
        body=k+'  <h2>%s</h2>\n  <div class="three" style="grid-template-columns:%s;width:min(1000px,100%%)">%s</div>\n  <p class="caption">點一張卡，看它的重點</p>\n'%(pg['title'],cols,cards)
    elif t=='sim':
        chips=''.join('<span class="cs" data-t="%s">%s</span>'%(a,b) for a,b in pg['tasks'])+'<button type="button" class="mini simreset">重來 ↺</button>'
        body=k+'  <h2>%s</h2>\n  <div class="chips">%s</div>\n%s\n  <div class="static-only qstatic"><p>%s</p></div>\n'%(pg['title'],chips,pg['html'],pg['static'])
    return head+body+'</section>\n'

def spec_for(L):
    sem={'cover':('focus','cover_hero','none'),'hotspot':('hierarchy','relationship_map','hotspot'),'quiz':('practice','question_focus','quiz'),'stepper':('sequence','process_timeline','stepper'),'sim':('practice','action_next_step','quiz'),'reveal':('synthesis','summary_three','reveal')}
    n=len(L['pages'])
    out='schema_version: "soil_interactive_deck_v1"\n\ndeck:\n  title: "%s"\n  audience: "國小三年級電腦課"\n  purpose: "%s"\n  takeaway: "%s"\n  language: "zh-TW"\n  slide_count: %d\n  output: "index.html"\n  portability: "single_file"\n\n'%(L['title'],L['purpose'],L['takeaway'],n)
    out+='''canvas:
  target_ratio: "16:9"
  responsive: true
  narrow_breakpoint_px: 900
  allow_active_slide_scroll: true

soil_flow:
  sequence: [hook, attention, action]

design_system:
  style_id: "warm_keycap_v1"
  palette: {background: "#FFF8EC", primary: "#1F6F8B", accent: "#F28C38", text: "#1E2A33"}
  fixed_shell: {title_anchor: "top_left", progress: true, phase_label: true, page_number: true}
  typography:
    font_feel: "粗圓、飽滿、低稜角、柔和端點"
    avoid: "尖角、窄長、機械感、科技模板字"
  motion: {duration_ms: 420, reduced_motion_fallback: true}

layout_router:
  allowed: [cover_hero, question_focus, misconception_dual, comparison_split, process_timeline, classification_grid, case_scene_analysis, relationship_map, data_focus, summary_three, action_next_step, section_divider]

interaction_router:
  allowed: [none, reveal, toggle_compare, stepper, filter_cards, tabs, decision_tree, sortable_table, chart, hotspot, slider, quiz, drag_match]
  min_interactive_slides: 2
  max_primary_interactions_per_slide: 1

validation:
  strict_offline: true
  require_keyboard: true
  require_touch: true
  require_reduced_motion: true
  require_static_fallback: true

slides:
'''
    for i,pg in enumerate(L['pages'],1):
        sm,lay,it=sem[pg['type']]
        ph='hook' if i==1 else ('action' if i>=n-1 else 'attention')
        out+='''  - page: %d
    soil_phase: "%s"
    role: "%s"
    learning_task: "%s"
    core_point: "%s"
    semantic_structure: "%s"
    layout: {id: "%s", variant: "%s"}
    visible_text: {title: "%s"}
    speaker_only: "見 NOTES"
    visual: {mode: "native", brief: "", source: ""}
    interaction: {type: "%s", goal: "%s", trigger: "click", initial_state: "start", states: %s, fallback: "靜態說明直接列出"}
    accessibility: {keyboard: true, touch: true, reduced_motion: true}
'''%(i,ph,pg['type'],pg['label'],pg['label'],sm,lay,pg['type'],pg['label'],it,pg['label'] if it!='none' else '',('[a, b]' if it!='none' else '[]'))
    return out

def build(L):
    pages=L['pages'];n=len(pages)
    secs=''.join(page_html(i,pg,n) for i,pg in enumerate(pages,1))
    cfg={'notes':[pg.get('note','') for pg in pages]}
    if 'results' in L: cfg['results']=L['results']
    js=CORE_JS.replace('__CFG__',json.dumps(cfg,ensure_ascii=False))
    html='''<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>電腦小知識：%s</title>
<style>%s%s</style>
</head>
<body class="nojs">
<div id="progress"></div>
<div id="section-tag"></div>
<main id="deck">
%s</main>
<button class="navbtn" id="prev" type="button">◀ 上一頁</button>
<span id="page-info"></span>
<button class="navbtn" id="next" type="button">下一頁 ▶</button>
<div id="notes" role="note"></div>
<div id="live" aria-live="polite"></div>
<script>%s</script>
</body>
</html>
'''%(L['title'],CSS,EXTRA_CSS,secs,js)
    d=os.path.join(base,'lessons',L['slug']);os.makedirs(d,exist_ok=True)
    open(os.path.join(d,'index.html'),'w',encoding='utf-8').write(html)
    open(os.path.join(d,'spec.yaml'),'w',encoding='utf-8').write(spec_for(L))
    return d

YN=['○ 可以','✕ 不可以']
exec(open(os.path.join(base,'lessons_content.py'),encoding='utf-8').read())

if __name__=='__main__':
    for L in LESSONS:
        print(build(L))

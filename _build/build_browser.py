import os,re
base=os.path.dirname(os.path.abspath(__file__))
src=open(os.path.join(base,'full','slides.html'),encoding='utf-8').read()
css=src[src.index('<style>')+7:src.index('</style>')]

extra_css='''
/* browser mock */
.bwin{width:min(980px,100%);background:#fff;border:5px solid var(--line);border-radius:20px;overflow:hidden;text-align:left}
.bbar{display:flex;gap:8px;align-items:center;background:#E9E2D3;padding:8px}
.bbtn{flex:0 0 auto;border:0;border-radius:10px;background:#fff;color:var(--ink);width:2.2em;height:2.2em;font-size:var(--t-caption);font-weight:900;box-shadow:0 3px 0 #C9C0AE}
.bbtn[disabled]{opacity:.35}
.baddr{flex:1;min-width:0;font:inherit;font-weight:700;font-size:var(--t-caption);border:3px solid transparent;border-radius:999px;padding:.3em .9em;background:#fff;color:var(--ink)}
.baddr:focus{border-color:var(--primary);outline:none}
.pill{flex:1;min-width:0;border-radius:999px;background:#fff;padding:.3em .9em;font-size:var(--t-caption);font-weight:700;border:0;text-align:left;color:var(--ink)}
.tabstrip{display:flex;gap:4px;background:#D6CDB8;padding:6px 8px 0;flex-wrap:wrap}
.tab{display:flex;align-items:center;gap:.5em;border:0;border-radius:12px 12px 0 0;background:#EFE8D8;color:var(--muted);padding:.3em .8em;font-size:var(--t-caption);font-weight:800}
.tab.on{background:#E9E2D3;color:var(--ink)}
.tab .x{display:inline-flex;width:1.4em;height:1.4em;align-items:center;justify-content:center;border-radius:50%;background:rgba(0,0,0,.08);font-size:.85em}
.tab.plus{background:transparent;color:var(--primary);font-size:var(--t-body);padding:.1em .6em}
.bpage{min-height:clamp(110px,22vh,220px);padding:clamp(10px,2vh,22px);display:flex;flex-direction:column;gap:10px;font-size:var(--t-body)}
.bpage .big{font-size:calc(var(--t-body)*1.1);font-weight:900}
.searchbox{display:flex;gap:8px;width:min(560px,100%)}
.searchbox input{flex:1;min-width:0;font:inherit;font-weight:700;border:4px solid var(--line);border-radius:999px;padding:.2em .8em;color:var(--ink)}
.searchbox input:focus{border-color:var(--primary);outline:none}
.part{border:3px dashed var(--accent)!important}
.parts-hint{font-size:var(--t-caption);color:var(--muted)}
.urlparts{display:flex;flex-wrap:wrap;justify-content:center;font-size:calc(var(--t-body)*1.2);font-weight:900;background:var(--card);border:5px solid var(--line);border-radius:22px;padding:.4em .8em;width:min(900px,100%);word-break:break-all}
.up{padding:.05em .15em;border-radius:8px;transition:background .3s}
.up.hl{background:var(--accent);color:#fff}
.chips{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;width:min(980px,100%)}
@media (max-height:780px){
  .slide[data-pg="brw"] .kicker{display:none}
  .bpage{min-height:90px}
}
'''

def sec(n,phase,inter,label,body,pg=True):
    cls='slide cover active' if n==1 else 'slide'
    pgattr='' if n==1 else ' data-pg="brw"'
    return ('<section class="%s" data-slide="%d" data-section="%s" data-interaction="%s" aria-label="%s"%s>' % (cls,n,phase,inter,label,pgattr)) + chr(10) + body + chr(10) + '</section>' + chr(10)

p1='''  <p class="kicker">電腦小知識</p>
  <h1>網址列和搜尋框<br>差在哪？</h1>
  <div class="motif" aria-hidden="true"><span class="cap">www</span><span class="cap hot">.com</span><span class="cap">🔍</span></div>
  <p class="caption">今天學：瀏覽器怎麼用，上網不迷路</p>
  <button class="startbtn" type="button" data-go="2">開始 ▶</button>'''
p1=p1.replace('class="slide','class="slide')

p2='''  <p class="kicker">先認識瀏覽器</p>
  <h2>點點看，每個地方叫什麼</h2>
  <div class="bwin" id="bw2">
    <div class="tabstrip"><button type="button" class="tab on" data-part="tab">🌐 Google 首頁</button><button type="button" class="tab plus" data-part="plus">＋</button></div>
    <div class="bbar">
      <button type="button" class="bbtn" data-part="back" aria-label="上一頁">←</button>
      <button type="button" class="bbtn" data-part="reload" aria-label="重新整理">⟳</button>
      <button type="button" class="pill" data-part="addr">https://www.google.com</button>
    </div>
    <div class="bpage"><span class="big">Google</span>
      <button type="button" class="pill" data-part="search" style="flex:0 0 auto;max-width:560px">🔍 在這裡搜尋或輸入網址…</button></div>
  </div>
  <div class="explain" id="bexp" aria-live="polite"><span>點上面的任何一個地方。</span></div>
  <div class="static-only qstatic"><p>分頁：同時開很多個網頁。← 上一頁。⟳ 重新整理。網址列：打網站的名字。搜尋框：不知道網址時找答案。</p></div>'''

quizhtml=lambda pre,extra='':f'''  <div class="quizbox">
    <p class="qtext" id="{pre}text"></p>
    <div class="opts" id="{pre}opts"></div>
    <div class="feedback" id="{pre}fb" aria-live="polite"></div>
    <div class="qctl"><span class="caption" id="{pre}score"></span><button type="button" class="mini" id="{pre}next">下一題 ▶</button></div>
  </div>'''

p3='''  <p class="kicker">兩個地方，用法不一樣</p>
  <h2>要打網址，還是要搜尋？</h2>
'''+quizhtml('a')+'''
  <div class="static-only qstatic"><p>知道網站名字（例如 classroom.google.com）：直接打網址。不知道網址、想找答案（例如怎麼折紙飛機）：用搜尋。</p></div>'''

p4='''  <p class="kicker">網址其實是一個地址</p>
  <h2>網址可以拆成三段</h2>
  <div class="urlparts" id="urlparts" aria-label="網址 https://www.google.com/search">
    <span class="up" data-u="0">https://</span><span class="up" data-u="1">www.google.com</span><span class="up" data-u="2">/search</span>
  </div>
  <div class="switch"><button type="button" id="uPrev">◀ 上一段</button><button type="button" id="uNext">下一段 ▶</button></div>
  <div class="explain" id="uexp" aria-live="polite"><span>按「下一段」，一段一段看。</span></div>
  <div class="static-only qstatic"><p>https:// 是安全連線的開頭。www.google.com 是網站的名字，要看這一段。/search 是網站裡的某一頁。</p></div>'''

p5='''  <p class="kicker">一次開好幾個網頁</p>
  <h2>分頁：開、切換、關</h2>
  <div class="chips" id="tchips">
    <span class="cs" data-tc="open">① 按 ＋ 開新分頁</span>
    <span class="cs" data-tc="switch">② 點別的分頁切換</span>
    <span class="cs" data-tc="close">③ 按 × 關掉一個</span>
  </div>
  <div class="bwin">
    <div class="tabstrip" id="tstrip"></div>
    <div class="bpage"><span class="big" id="tbody"></span></div>
  </div>
  <div class="explain" id="texp" aria-live="polite"><span>試試看，每個動作都會打勾。</span></div>
  <div class="switch"><button type="button" class="mini" id="tReset">重來</button></div>
  <div class="static-only qstatic"><p>＋ 開新分頁，點分頁名字切換，× 關掉分頁。至少留一個分頁。</p></div>'''

p6='''  <p class="kicker">遇到狀況怎麼辦</p>
  <h2>按哪一個鍵來救？</h2>
'''+quizhtml('c')+'''
  <div class="static-only qstatic"><p>點錯連結：按 ← 上一頁。畫面卡住：按 ⟳ 重新整理。分頁不用了：按 × 關掉。</p></div>'''

p7='''  <p class="kicker">假的瀏覽器，放心玩</p>
  <h2>自己上網走一圈</h2>
  <div class="chips">
    <span class="cs" data-pt="goto">① 網址列打 classroom.google.com</span>
    <span class="cs" data-pt="back">② 按 ← 回上一頁</span>
    <span class="cs" data-pt="search">③ 搜尋「紙飛機」</span>
    <span class="cs" data-pt="reload">④ 按 ⟳ 重新整理</span>
  </div>
  <div class="bwin">
    <div class="tabstrip"><span class="tab on" id="ptab">🌐 Google 首頁</span></div>
    <form class="bbar" id="pform" autocomplete="off">
      <button type="button" class="bbtn" id="pBack" aria-label="上一頁" disabled>←</button>
      <button type="button" class="bbtn" id="pReload" aria-label="重新整理">⟳</button>
      <input class="baddr" id="pAddr" type="text" aria-label="網址列" placeholder="在這裡打網址，按 Enter" autocapitalize="off" spellcheck="false">
    </form>
    <div class="bpage" id="ppage" aria-live="polite"></div>
  </div>
  <div class="static-only qstatic"><p>網址列打 classroom.google.com 按 Enter，再按 ← 回上一頁；在搜尋框打「紙飛機」；按 ⟳ 重新整理。</p></div>'''

p8='''  <p class="kicker">收尾</p>
  <h2>今天記住四件事</h2>
  <div class="three" style="grid-template-columns:repeat(2,1fr)">
    <button type="button" class="card3" aria-expanded="false"><span class="ct">① 打網址或搜尋</span><span class="detail">知道網站名字，就在網址列打。想找答案，就用搜尋。</span></button>
    <button type="button" class="card3" aria-expanded="false"><span class="ct">② 看網站名字那一段</span><span class="detail">網址裡 www 到 .com 那一段是網站的名字，打錯一個字就會去別的地方。</span></button>
    <button type="button" class="card3" aria-expanded="false"><span class="ct">③ 分頁：開、切、關</span><span class="detail">＋ 開新的，點名字切換，× 關掉不用的。</span></button>
    <button type="button" class="card3" aria-expanded="false"><span class="ct">④ 上一頁、重新整理</span><span class="detail">點錯了按 ←，卡住了按 ⟳，不要慌。</span></button>
  </div>
  <p class="caption">點一張卡，看它的重點</p>'''

sections=''.join([
 sec(1,'引起動機','none','封面',p1),
 sec(2,'維持注意','hotspot','認識瀏覽器',p2),
 sec(3,'維持注意','quiz','網址或搜尋',p3),
 sec(4,'維持注意','stepper','網址三段',p4),
 sec(5,'維持注意','tabs','分頁',p5),
 sec(6,'維持注意','quiz','按哪個鍵來救',p6),
 sec(7,'喚起行動','quiz','假瀏覽器練習',p7),
 sec(8,'喚起行動','reveal','今天記住四件事',p8),
])

NOTES=[
 '開場：問「想去 Classroom，要打在哪裡？」讓學生先猜。',
 '先不講答案，讓學生猜每個部位，再點開對答。重點是網址列和搜尋框是兩個不同的東西。',
 '四個例子。網址長得像「xxx.com」→直接打；一句話、有「怎麼」→用搜尋。答錯讓學生說理由。',
 '重點是中間那段「網站名字」。提醒：網址不能有空白，要在英文模式打（回扣上一課中英文切換）。',
 '請學生各自操作一次。重點：分頁不是視窗，可以同時開很多個；至少留一個。',
 '三個情境：點錯→←、卡住→⟳、不用了→×。學生舉手選，老師點。',
 '假瀏覽器，不會連網。四個任務都完成後，請學生到真的瀏覽器照做一次。',
 '請學生說出四件事，再點卡片對答案。下一課接 Google 登入。'
]

js='''
(function(){
  document.body.classList.remove('nojs');document.body.classList.add('js');
  var slides=[].slice.call(document.querySelectorAll('.slide')),total=slides.length,cur=0;
  var phaseEl=document.getElementById('section-tag'),pageEl=document.getElementById('page-info'),progEl=document.getElementById('progress'),liveEl=document.getElementById('live');
  var prevB=document.getElementById('prev'),nextB=document.getElementById('next'),notesEl=document.getElementById('notes');
  var NOTES=__NOTES__;
  function say(t){liveEl.textContent=t}
  function go(n){
    n=Math.max(0,Math.min(total-1,n));cur=n;
    slides.forEach(function(s,i){s.classList.toggle('active',i===n)});
    var s=slides[n];phaseEl.textContent=s.getAttribute('data-section');pageEl.textContent=(n+1)+' / '+total;
    progEl.style.width=((n+1)/total*100)+'%';prevB.disabled=n===0;nextB.disabled=n===total-1;notesEl.textContent=NOTES[n]||'';
    if(history.replaceState)history.replaceState(null,'','#'+(n+1));
    say('第 '+(n+1)+' 頁，'+s.getAttribute('aria-label'));s.scrollTop=0;
    var h=s.querySelector('h1,h2');if(h){h.setAttribute('tabindex','-1');h.focus({preventScroll:true})}
  }
  prevB.addEventListener('click',function(){go(cur-1)});nextB.addEventListener('click',function(){go(cur+1)});
  document.querySelectorAll('[data-go]').forEach(function(b){b.addEventListener('click',function(){go(+b.getAttribute('data-go')-1)})});
  document.addEventListener('keydown',function(e){
    var t=e.target.tagName;
    if(t==='INPUT'||t==='TEXTAREA')return;
    var k=e.key;
    if(t==='BUTTON'&&(k==='ArrowRight'||k==='ArrowLeft')){e.preventDefault();go(cur+(k==='ArrowRight'?1:-1));return}
    if(t==='BUTTON')return;
    if(k==='ArrowRight'||k==='PageDown'||k===' '){e.preventDefault();go(cur+1)}
    else if(k==='ArrowLeft'||k==='PageUp'){e.preventDefault();go(cur-1)}
    else if(k==='Home')go(0);else if(k==='End')go(total-1);
    else if(k==='f'||k==='F'){if(document.fullscreenElement)document.exitFullscreen();else document.documentElement.requestFullscreen&&document.documentElement.requestFullscreen()}
    else if(k==='n'||k==='N')notesEl.classList.toggle('show');
  });
  window.addEventListener('hashchange',function(){var x=parseInt(location.hash.slice(1),10);if(x>=1&&x<=total&&x-1!==cur)go(x-1)});

  /* page 2 hotspot */
  var PART={tab:['分頁','一個分頁就是一個網頁。可以同時開很多個。'],plus:['＋ 新分頁','按這裡開一個新的網頁，不會關掉舊的。'],
    back:['← 上一頁','點錯了，按它回到剛剛那一頁。'],reload:['⟳ 重新整理','畫面卡住或沒更新，按它重新載入。'],
    addr:['網址列','在這裡打網站的名字（網址），按 Enter 就會去那個網站。'],search:['搜尋框','不知道網址、想找答案，就在這裡打問題。']};
  var bexp=document.getElementById('bexp');
  document.querySelectorAll('#bw2 [data-part]').forEach(function(b){
    b.addEventListener('click',function(){
      document.querySelectorAll('#bw2 .part').forEach(function(x){x.classList.remove('part')});b.classList.add('part');
      var d=PART[b.getAttribute('data-part')];bexp.innerHTML='<span><b style="color:var(--accent)">'+d[0]+'</b>　'+d[1]+'</span>';say(d[0]+'：'+d[1]);
    });
  });

  /* generic quiz */
  function makeQuiz(pre,items){
    var qt=document.getElementById(pre+'text'),qo=document.getElementById(pre+'opts'),fb=document.getElementById(pre+'fb'),sc=document.getElementById(pre+'score'),nx=document.getElementById(pre+'next');
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
  }
  var A2=['我知道網站名字，直接打網址','我想找答案，用搜尋'];
  makeQuiz('a',[
    {q:'想去 classroom.google.com',o:A2,a:0,e:'對！知道網站名字，就直接在網址列打。'},
    {q:'想知道「怎麼折紙飛機」',o:A2,a:1,e:'對！想找答案、不知道哪個網站，就用搜尋。'},
    {q:'想去 www.yahoo.com.tw',o:A2,a:0,e:'對！有 www 和 .com 的就是網址，直接打。'},
    {q:'想知道「恐龍有哪些種類」',o:A2,a:1,e:'對！這是一個問題，用搜尋找答案。'}
  ]);
  var C3=['← 上一頁','⟳ 重新整理','× 關掉分頁'];
  makeQuiz('c',[
    {q:'不小心點到奇怪的連結，跑到別的頁面。',o:C3,a:0,e:'對！按 ← 回到剛剛那一頁。'},
    {q:'網頁卡住了，一直不動。',o:C3,a:1,e:'對！按 ⟳ 重新整理，讓它重新載入。'},
    {q:'這個網頁看完了，不用了。',o:C3,a:2,e:'對！按分頁上的 × 把它關掉。'}
  ]);

  /* page 4 url stepper */
  var UP=[].slice.call(document.querySelectorAll('.up')),ui=-1,uexp=document.getElementById('uexp');
  var UT=['https:// 是安全連線的開頭，每個網址最前面都有。','www.google.com 是「網站的名字」。看網址要看這一段，打錯一個字就會去別的地方。','/search 是網站裡的某一頁，像房子裡的某個房間。'];
  function setU(n){ui=Math.max(0,Math.min(2,n));UP.forEach(function(e,i){e.classList.toggle('hl',i===ui)});uexp.innerHTML='<span>'+UT[ui]+'</span>';say(UT[ui]);
    document.getElementById('uPrev').style.opacity=ui===0?.35:1;document.getElementById('uNext').style.opacity=ui===2?.35:1}
  document.getElementById('uPrev').addEventListener('click',function(){setU(ui-1)});
  document.getElementById('uNext').addEventListener('click',function(){setU(ui+1)});

  /* page 5 tabs */
  var tabs=[{id:1,t:'Google 首頁'}],tact=1,tn=1,tdone={};
  var tstrip=document.getElementById('tstrip'),tbody=document.getElementById('tbody'),texp=document.getElementById('texp');
  function tmark(k){tdone[k]=true;[].forEach.call(document.querySelectorAll('[data-tc]'),function(e){e.classList.toggle('done',!!tdone[e.getAttribute('data-tc')])})}
  function tmsg(t){texp.innerHTML='<span>'+t+'</span>';say(t)}
  function trender(){
    tstrip.innerHTML='';
    tabs.forEach(function(d){
      var b=document.createElement('button');b.type='button';b.className='tab'+(d.id===tact?' on':'');b.textContent='🌐 '+d.t+' ';
      var x=document.createElement('span');x.className='x';x.textContent='×';x.setAttribute('role','button');x.setAttribute('aria-label','關閉 '+d.t);
      x.addEventListener('click',function(e){e.stopPropagation();
        if(tabs.length===1){tmsg('至少要留一個分頁喔！');return}
        var i=tabs.indexOf(d);tabs.splice(i,1);if(tact===d.id)tact=tabs[Math.max(0,i-1)].id;tmark('close');tmsg('關掉了「'+d.t+'」。');trender()});
      b.appendChild(x);
      b.addEventListener('click',function(){if(tact!==d.id){tact=d.id;tmark('switch');tmsg('切換到「'+d.t+'」。')}trender()});
      tstrip.appendChild(b);
    });
    var p=document.createElement('button');p.type='button';p.className='tab plus';p.textContent='＋';p.setAttribute('aria-label','開新分頁');
    p.addEventListener('click',function(){if(tabs.length>=5){tmsg('分頁太多會變慢，先關幾個吧。');return}
      tn++;var d={id:tn,t:'新分頁 '+(tn-1)};tabs.push(d);tact=d.id;tmark('open');tmsg('開了一個新分頁。');trender()});
    tstrip.appendChild(p);
    var cur2=tabs.filter(function(d){return d.id===tact})[0];tbody.textContent='你現在在：'+cur2.t;
  }
  trender();
  document.getElementById('tReset').addEventListener('click',function(){tabs=[{id:1,t:'Google 首頁'}];tact=1;tn=1;tdone={};tmark('none');tmsg('重來了。');trender()});

  /* page 7 fake browser */
  var hist=['home'],hi=0,reloads=0,pdone={};
  var pAddr=document.getElementById('pAddr'),ppage=document.getElementById('ppage'),pBack=document.getElementById('pBack'),pReload=document.getElementById('pReload'),ptab=document.getElementById('ptab');
  function pmark(k){pdone[k]=true;[].forEach.call(document.querySelectorAll('[data-pt]'),function(e){e.classList.toggle('done',!!pdone[e.getAttribute('data-pt')])})}
  function pageOf(v){
    v=v.trim();
    if(!v)return null;
    if(v.indexOf(' ')<0&&v.indexOf('.')>0){
      var h=v.replace(/^https?:\\/\\//,'').replace(/\\/$/,'').toLowerCase();
      if(h==='classroom.google.com')return 'classroom';
      if(h==='www.google.com'||h==='google.com')return 'home';
      return 'nf:'+v;
    }
    return 'q:'+v;
  }
  function esc(s){return s.replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  function prender(){
    var p=hist[hi];pBack.disabled=hi===0;var note=reloads?'<span class="caption">已重新整理 '+reloads+' 次</span>':'';
    if(p==='home'){pAddr.value='';ptab.textContent='🌐 Google 首頁';
      ppage.innerHTML='<span class="big">Google</span><form class="searchbox" id="sform"><input id="sq" aria-label="搜尋框" placeholder="🔍 搜尋" autocomplete="off"><button type="submit" class="mini">搜尋</button></form>'+note;
      document.getElementById('sform').addEventListener('submit',function(e){e.preventDefault();var v=document.getElementById('sq').value.trim();if(v)nav('q:'+v)});}
    else if(p==='classroom'){pAddr.value='classroom.google.com';ptab.textContent='🌐 Google Classroom';
      ppage.innerHTML='<span class="big">Google Classroom（練習）</span><div class="tip" style="width:auto">三年級運算思維（115-1）</div>'+note}
    else if(p.indexOf('q:')===0){var q=p.slice(2);pAddr.value='google.com/search?q='+q;ptab.textContent='🌐 搜尋結果';
      ppage.innerHTML='<span class="big">搜尋「'+esc(q)+'」的結果</span><p class="caption">1. '+esc(q)+' 的做法和圖片</p><p class="caption">2. 很多人都在問：'+esc(q)+'</p><p class="caption">3. '+esc(q)+' 影片教學</p>'+note}
    else{var u=p.slice(3);pAddr.value=u;ptab.textContent='🌐 找不到網站';
      ppage.innerHTML='<span class="big">找不到這個網站</span><p class="caption">檢查看看：有沒有多打空白？是不是英文模式？字有沒有打錯？</p>'+note}
  }
  function nav(p){
    if(hist[hi]===p){return}
    hist=hist.slice(0,hi+1);hist.push(p);hi=hist.length-1;reloads=0;
    if(p==='classroom')pmark('goto');
    if(p.indexOf('q:')===0&&p.slice(2).indexOf('紙飛機')>=0)pmark('search');
    prender();say(ppage.textContent);
  }
  document.getElementById('pform').addEventListener('submit',function(e){e.preventDefault();var p=pageOf(pAddr.value);if(p)nav(p)});
  pBack.addEventListener('click',function(){if(hi>0){hi--;reloads=0;pmark('back');prender();say('回到上一頁')}});
  pReload.addEventListener('click',function(){reloads++;pmark('reload');prender();say('重新整理了')});
  prender();

  /* page 8 reveal */
  document.querySelectorAll('.card3').forEach(function(c){c.addEventListener('click',function(){var on=c.getAttribute('aria-expanded')==='true';c.setAttribute('aria-expanded',!on);if(!on)say(c.querySelector('.detail').textContent)})});

  var h=parseInt(location.hash.slice(1),10);go(h>=1&&h<=total?h-1:0);
})();
'''.replace('__NOTES__',str(NOTES).replace("'",'"') if False else __import__('json').dumps(NOTES,ensure_ascii=False))

html='''<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>電腦小知識：瀏覽器基本</title>
<style>'''+css+extra_css+'''</style>
</head>
<body class="nojs">
<div id="progress"></div>
<div id="section-tag"></div>
<main id="deck">
'''+sections+'''</main>
<button class="navbtn" id="prev" type="button">◀ 上一頁</button>
<span id="page-info"></span>
<button class="navbtn" id="next" type="button">下一頁 ▶</button>
<div id="notes" role="note"></div>
<div id="live" aria-live="polite"></div>
<script>'''+js+'''</script>
</body>
</html>
'''
os.makedirs(os.path.join(base,'browser'),exist_ok=True)
open(os.path.join(base,'browser','slides.html'),'w',encoding='utf-8').write(html)
print(len(html))

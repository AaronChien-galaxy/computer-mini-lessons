import os
base=os.path.dirname(os.path.abspath(__file__))
s=open(os.path.join(base,'trio','slides.html'),encoding='utf-8').read()

quiz='''<!-- 3 Shift 與 Caps Lock：quiz -->
<section class="slide" data-slide="3" data-section="維持注意" data-interaction="quiz" aria-label="大寫小測驗">
  <p class="kicker">想打大寫字母</p>
  <h2 id="qTitle">怎麼按才對？</h2>
  <div class="quizbox" id="quizbox">
    <p class="qtext" id="qtext"></p>
    <div class="opts" id="opts"></div>
    <div class="feedback" id="qfb" aria-live="polite"></div>
    <div class="qctl"><span class="caption" id="qscore"></span><button type="button" class="mini" id="qnext">下一題 ▶</button></div>
  </div>
  <div class="static-only qstatic">
    <p>1. 打一個大寫 A：按住 Shift 再按 a。</p>
    <p>2. 一直打大寫：按 Caps Lock。</p>
    <p>3. 回到小寫：再按一次 Caps Lock。</p>
  </div>
</section>

'''
hot_old='<section class="slide" data-slide="3" data-section="喚起行動" data-interaction="hotspot"'
hot_new='<section class="slide" data-slide="4" data-section="維持注意" data-interaction="hotspot"'
assert hot_old in s
s=s.replace(hot_old,quiz+hot_new)

tail='''
<!-- 5 符號小站：stepper -->
<section class="slide" data-slide="5" data-section="喚起行動" data-interaction="stepper" aria-label="符號小站怎麼玩">
  <p class="kicker">接下來練習打字</p>
  <h2>符號小站，四步驟</h2>
  <ol class="steps" id="steps">
    <li class="step"><span class="num">1</span><span class="stext">老師機投影，從 Classroom 的連結進入「Shift 符號練習小站」。</span></li>
    <li class="step"><span class="num">2</span><span class="stext">輸入你的 5 碼號碼：班級 3 碼＋座號 2 碼，再按 Enter。</span></li>
    <li class="step"><span class="num">3</span><span class="stext">從第一關開始，一關一關往下打，打錯了按倒退。</span></li>
    <li class="step"><span class="num">4</span><span class="stext">打完一組會得到星星，你的成績會自動送給老師。</span></li>
  </ol>
  <div class="switch">
    <button type="button" id="stPrev">◀ 上一步</button>
    <button type="button" id="stNext">下一步 ▶</button>
    <button type="button" class="linkbtn" id="openSite">打開符號小站 ↗</button>
  </div>
</section>

<!-- 6 收尾：reveal -->
<section class="slide" data-slide="6" data-section="喚起行動" data-interaction="reveal" aria-label="今天記住三件事">
  <p class="kicker">收尾</p>
  <h2>今天記住三件事</h2>
  <div class="three">
    <button type="button" class="card3" aria-expanded="false"><span class="ct">① 中英文開關</span><span class="detail">右下角看「中」或「A」，按一下 Shift 切換。登入要用英文。</span></button>
    <button type="button" class="card3" aria-expanded="false"><span class="ct">② Shift 變大寫</span><span class="detail">按住 Shift 再按字母，只變一個。要一直大寫就按 Caps Lock。</span></button>
    <button type="button" class="card3" aria-expanded="false"><span class="ct">③ Enter 確定</span><span class="detail">打完帳號、密碼，按 Enter 才會送出。</span></button>
  </div>
  <p class="caption">點一張卡，看它的重點</p>
</section>

</main>'''
assert '\n</main>' in s
s=s.replace('\n</main>',tail,1)

css='''
/* quiz */
.quizbox{background:var(--card);border:5px solid var(--line);border-radius:26px;padding:clamp(14px,2.4vh,26px);width:min(900px,100%);display:flex;flex-direction:column;gap:12px}
.qtext{font-size:var(--t-body);font-weight:900}
.opts{display:flex;flex-direction:column;gap:10px}
.opt{border:4px solid var(--primary);background:var(--card);color:var(--primary);border-radius:18px;padding:.55em 1em;font-size:var(--t-body);font-weight:800;text-align:left}
.opt.ok{background:var(--good);border-color:var(--good);color:#fff}
.opt.no{background:var(--accent-soft);border-color:var(--accent);color:var(--ink)}
.feedback{min-height:2.6em;font-size:var(--t-body);text-align:left;color:var(--ink)}
.qctl{display:flex;justify-content:space-between;align-items:center}
.mini{border:0;border-radius:999px;background:var(--primary);color:#fff;padding:.4em 1.2em;font-size:var(--t-caption);font-weight:800}
.mini[disabled]{opacity:.3}
.qstatic{text-align:left;width:min(900px,100%)}
.qstatic p{font-size:var(--t-caption)}
.js .qstatic{display:none}
/* stepper */
.steps{list-style:none;width:min(900px,100%);display:flex;flex-direction:column;gap:10px}
.step{display:flex;gap:14px;align-items:center;text-align:left;background:var(--card);border:5px solid var(--line);border-radius:22px;padding:.5em .9em;font-size:var(--t-body);transition:opacity .3s,border-color .3s}
.step .num{flex:0 0 auto;width:1.8em;height:1.8em;border-radius:50%;background:var(--line);color:var(--ink);display:flex;align-items:center;justify-content:center;font-weight:900}
.js .step.dim{opacity:.35}
.step.now{border-color:var(--primary);background:var(--primary-soft)}
.step.now .num{background:var(--primary);color:#fff}
.linkbtn{border:0;text-decoration:none;background:var(--accent);color:#fff;display:inline-block;border-radius:999px;padding:.55em 1.5em;font-size:var(--t-body);font-weight:900}
/* reveal */
.three{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(10px,2vw,24px);width:min(1100px,100%)}
.card3{background:var(--card);border:5px solid var(--line);border-radius:26px;padding:clamp(14px,2.4vh,26px);display:flex;flex-direction:column;gap:10px;text-align:center;align-items:center}
.card3[aria-expanded="true"]{border-color:var(--primary);background:var(--primary-soft)}
.card3 .ct{font-size:var(--t-body);font-weight:900;color:var(--primary)}
.card3 .detail{font-size:var(--t-caption);line-height:1.5;color:var(--ink);display:none}
.card3[aria-expanded="true"] .detail,.nojs .card3 .detail{display:block}
@media (max-width:900px){.three{grid-template-columns:1fr}}
@media (max-height:780px){
  .slide[data-interaction="quiz"] .kicker,.slide[data-interaction="stepper"] .kicker{display:none}
  .opt{padding:.3em .8em}.feedback{min-height:1.8em}.quizbox{gap:8px}
  .step{padding:.15em .8em}.steps{gap:5px}.slide[data-interaction="stepper"] h2{font-size:calc(var(--t-page)*.85)}
}
'''
assert '#notes{position:fixed' in s
s=s.replace('#notes{position:fixed',css+'\n#notes{position:fixed',1)
s=s.replace("document.body.classList.remove('nojs');","document.body.classList.remove('nojs');document.body.classList.add('js');")

i0=s.index("  var NOTES=[")
i1=s.index("  ];",i0)+4
new_notes="""  var NOTES=[
    '先在教室電腦確認：單按 Shift 真的會切換中／英（不同機器設定不同）。開場問：打 abc 卻出現怪字，有人遇過嗎？',
    '先不要說答案，讓學生猜。再點「中」「A」兩個按鈕。學生手指放 Shift 空手練 3 次，再到記事本實機打 abc。',
    '三題小測驗，全班舉手或手指比 1／2／3 選答案，老師點。答錯不批評，點出理由再讓他們看正解。',
    '三個重點鍵：Shift（按住＋字母＝大寫）、Caps Lock（鎖住大寫，燈亮就是開）、Enter（確定／換行）。先看再讓學生按。',
    '學生不會打網址：老師機投影，學生從 Classroom 連結進入。上課前先實機試玩一次，並確認試算表有收到紀錄。',
    '請學生說出三件事，再點卡片對答案。最後留 5 分鐘讓學生繼續玩符號小站。'
  ];"""
s=s[:i0]+new_notes+s[i1:]

js='''
  /* page 3 quiz */
  var Q=[
    {q:'想打一個大寫的 A，要怎麼按？',o:['按住 Shift，再按 a','按 Enter，再按 a','按倒退，再按 a'],a:0,e:'對！Shift 要按住，再按字母，只會變一個大寫。'},
    {q:'想一直打大寫 ABC，要按哪個鍵？',o:['Enter','Caps Lock','空白'],a:1,e:'對！Caps Lock 按一下，後面都是大寫，燈會亮。'},
    {q:'大寫打完了，想回到小寫，怎麼辦？',o:['再按一次 Caps Lock','按 Enter','關電腦重開'],a:0,e:'對！再按一次 Caps Lock，燈熄掉就回小寫。'}
  ];
  var qi=0,qok=0,qdone=false;
  var qtext=document.getElementById('qtext'),opts=document.getElementById('opts'),qfb=document.getElementById('qfb'),
      qscore=document.getElementById('qscore'),qnext=document.getElementById('qnext');
  function loadQ(){
    var d=Q[qi]; qdone=false;
    qtext.textContent=(qi+1)+'. '+d.q; qfb.textContent=''; opts.innerHTML='';
    qnext.disabled=true; qnext.textContent=qi===Q.length-1?'再玩一次 ↺':'下一題 ▶';
    d.o.forEach(function(t,i){
      var b=document.createElement('button'); b.type='button'; b.className='opt'; b.textContent=t;
      b.addEventListener('click',function(){
        if(qdone)return;
        if(i===d.a){qdone=true;qok++;b.classList.add('ok');qfb.textContent=d.e;qnext.disabled=false;say(d.e);qscore.textContent='第 '+(qi+1)+' / '+Q.length+' 題　答對 '+qok+' 題'}
        else{b.classList.add('no');qfb.textContent='再想想看，還有別的選擇。';say('再想想看')}
      });
      opts.appendChild(b);
    });
    qscore.textContent='第 '+(qi+1)+' / '+Q.length+' 題　答對 '+qok+' 題';
  }
  qnext.addEventListener('click',function(){
    if(qi===Q.length-1){qi=0;qok=0}else qi++;
    loadQ();
  });
  loadQ();

  /* page 5 stepper */
  var stepEls=[].slice.call(document.querySelectorAll('.step')),si=0;
  var stPrev=document.getElementById('stPrev'),stNext=document.getElementById('stNext');
  function setStep(n){
    si=Math.max(0,Math.min(stepEls.length-1,n));
    stepEls.forEach(function(e,i){e.classList.toggle('now',i===si);e.classList.toggle('dim',i>si)});
    stPrev.disabled=si===0; stNext.disabled=si===stepEls.length-1;
    stPrev.style.opacity=stPrev.disabled?.35:1; stNext.style.opacity=stNext.disabled?.35:1;
    say('第 '+(si+1)+' 步：'+stepEls[si].querySelector('.stext').textContent);
  }
  stPrev.addEventListener('click',function(){setStep(si-1)});
  stNext.addEventListener('click',function(){setStep(si+1)});
  setStep(0);

  /* page 6 reveal */
  document.querySelectorAll('.card3').forEach(function(c){
    c.addEventListener('click',function(){
      var on=c.getAttribute('aria-expanded')==='true';
      c.setAttribute('aria-expanded',!on);
      if(!on)say(c.querySelector('.detail').textContent);
    });
  });

'''
assert "  /* page 3 keyboard */" in s
s=s.replace("  /* page 3 keyboard */",js+"  /* page 4 keyboard */",1)

s=s.replace('id="phase"','id="section-tag"').replace('id="pageno"','id="page-info"').replace("#phase{","#section-tag{").replace("#pageno{","#page-info{").replace("getElementById('phase')","getElementById('section-tag')").replace("getElementById('pageno')","getElementById('page-info')")
s=s.replace('<div class="explain" id="explain" aria-live="polite">','<div class="scratchctl"><button type="button" class="mini" id="clearTxt">清除打的字</button></div>\n  <div class="explain" id="explain" aria-live="polite">')
s=s.replace("  /* page 4 keyboard */","  document.getElementById('openSite').addEventListener('click',function(){window.open('https://aaronchien-galaxy.github.io/shift-symbol-game/','_blank','noopener')});\n  /* page 4 keyboard */",1)
s=s.replace("  function render(){typedEl.textContent=text}","  function render(){typedEl.textContent=text}\n  document.getElementById('clearTxt').addEventListener('click',function(){text='';render()});",1)
s=s.replace(".qstatic{",".scratchctl{width:min(1000px,100%);text-align:right}\n.qstatic{",1)
os.makedirs(os.path.join(base,'full'),exist_ok=True)
open(os.path.join(base,'full','slides.html'),'w',encoding='utf-8').write(s)
print(s.count('data-slide='))

import os,re
base=os.path.dirname(os.path.abspath(__file__))
p=os.path.join(base,'full','slides.html')
s=open(p,encoding='utf-8').read()

rules='''<!-- 鍵盤公約：quiz（可以／不可以） -->
<section class="slide" data-slide="0" data-section="引起動機" data-interaction="quiz" aria-label="鍵盤公約">
  <p class="kicker">先學規矩，鍵盤才不會壞</p>
  <h2>這樣可以嗎？</h2>
  <div class="quizbox" id="rbox">
    <p class="qtext" id="rtext"></p>
    <div class="rbtns">
      <button type="button" class="opt" id="rYes">○ 可以</button>
      <button type="button" class="opt" id="rNo">✕ 不可以</button>
    </div>
    <div class="feedback" id="rfb" aria-live="polite"></div>
    <div class="qctl"><span class="caption" id="rscore"></span><button type="button" class="mini" id="rnext">下一題 ▶</button></div>
  </div>
  <div class="static-only qstatic">
    <p>○ 手洗乾淨再打字。</p>
    <p>✕ 用力拍鍵盤：會壞，輕輕按就好。</p>
    <p>✕ 邊吃東西邊打字：碎屑會掉進去。</p>
    <p>✕ 一個鍵按著不放：字會一直跑出來。</p>
  </div>
</section>

'''
fingers='''<!-- 手指歸位：tabs -->
<section class="slide" data-slide="0" data-section="維持注意" data-interaction="tabs" aria-label="手指歸位">
  <p class="kicker">十根手指各管幾個鍵</p>
  <h2>手指「回家」的位置</h2>
  <div class="switch" role="tablist" aria-label="選擇看哪一邊">
    <button type="button" class="ftab" data-f="L" aria-pressed="false">左手</button>
    <button type="button" class="ftab" data-f="R" aria-pressed="false">右手</button>
    <button type="button" class="ftab" data-f="H" aria-pressed="false">F 和 J 的小突起</button>
  </div>
  <div class="homerow" id="homerow" aria-label="中間那一排鍵">
    <span class="hk" data-key="a">a</span><span class="hk" data-key="s">s</span><span class="hk" data-key="d">d</span>
    <span class="hk bump" data-key="f">f</span><span class="hk" data-key="g">g</span><span class="hk" data-key="h">h</span>
    <span class="hk bump" data-key="j">j</span><span class="hk" data-key="k">k</span><span class="hk" data-key="l">l</span><span class="hk" data-key=";">;</span>
  </div>
  <div class="explain" id="fexplain" aria-live="polite"><span>點上面的按鈕，看每根手指放哪裡。</span></div>
  <div class="static-only qstatic">
    <p>左手：小指 a、無名指 s、中指 d、食指 f。右手：食指 j、中指 k、無名指 l、小指 ;。F 和 J 有小突起，摸到就知道手指回家了。大拇指放空白鍵。</p>
  </div>
</section>

'''
assert '<!-- 2 中英文切換' in s and '<!-- 5 符號小站' in s
s=s.replace('<!-- 2 中英文切換',rules+'<!-- 2 中英文切換',1)
s=s.replace('<!-- 5 符號小站',fingers+'<!-- 5 符號小站',1)

# summary: four cards
old_h2='<h2>今天記住三件事</h2>'
assert old_h2 in s
s=s.replace(old_h2,'<h2>今天記住四件事</h2>')
card4='''    <button type="button" class="card3" aria-expanded="false"><span class="ct">④ 輕按、手指回家</span><span class="detail">鍵盤輕輕按，不拍不壓。打字前食指放 F 和 J，摸到小突起。</span></button>
  </div>
  <p class="caption">點一張卡'''
s=s.replace('''  </div>
  <p class="caption">點一張卡''',card4,1)
s=s.replace('aria-label="今天記住三件事"','aria-label="今天記住四件事"')
s=s.replace('data-slide="0"','data-slide="X"')

# renumber
n=[0]
def rn(m):
    n[0]+=1; return 'data-slide="%d"'%n[0]
s=re.sub(r'data-slide="[^"]*"',rn,s)

css='''
.rbtns{display:flex;gap:12px;flex-wrap:wrap}
.rbtns .opt{flex:1 1 200px;text-align:center}
.homerow{display:flex;gap:clamp(5px,1vw,12px);justify-content:center;width:min(1000px,100%)}
.hk{flex:1 1 0;max-width:90px;height:clamp(46px,9vh,76px);display:flex;align-items:center;justify-content:center;position:relative;border-radius:12px;background:#fff;box-shadow:0 5px 0 #C9C0AE;font-size:var(--t-body);font-weight:900;transition:background .3s}
.hk.bump::after{content:"";position:absolute;bottom:10px;width:1.2em;height:4px;border-radius:3px;background:#C9C0AE}
.hk.f1{background:#F9C5C5}.hk.f2{background:#FFE29A}.hk.f3{background:#BFE5C8}.hk.f4{background:#BFD9F2}
.hk.hl{background:var(--accent);color:#fff}
@media (max-height:780px){
  .slide[data-interaction="tabs"] .kicker{display:none}
  .slide[data-interaction="quiz"][aria-label="鍵盤公約"] .kicker{display:none}
}
'''
s=s.replace('#notes{position:fixed',css+'#notes{position:fixed',1)
s=s.replace('.three{display:grid;grid-template-columns:repeat(3,1fr);','.three{display:grid;grid-template-columns:repeat(2,1fr);')
s=s.replace('width:min(1100px,100%)}\n.card3','width:min(1000px,100%)}\n.card3',1)

js='''
  /* rules quiz */
  var R=[
    {q:'手先洗乾淨，再來打字。',a:true,e:'對！乾淨的手，鍵盤才不會髒。'},
    {q:'電腦很慢，用力拍鍵盤讓它快一點。',a:false,e:'不可以！拍會把鍵盤弄壞，電腦也不會變快。輕輕按就好。'},
    {q:'一邊吃餅乾，一邊打字。',a:false,e:'不可以！碎屑會掉進鍵盤縫裡，按鍵會卡住。'},
    {q:'一個鍵按著不放。',a:false,e:'不可以！按著不放，字會一直跑出來。按一下，放開。'}
  ];
  var ri=0,rok=0,rdone=false;
  var rtext=document.getElementById('rtext'),rfb=document.getElementById('rfb'),rscore=document.getElementById('rscore'),
      rnext=document.getElementById('rnext'),rYes=document.getElementById('rYes'),rNo=document.getElementById('rNo');
  function loadR(){
    var d=R[ri]; rdone=false; rtext.textContent=(ri+1)+'. '+d.q; rfb.textContent='';
    rYes.className='opt'; rNo.className='opt'; rnext.disabled=true;
    rnext.textContent=ri===R.length-1?'再玩一次 ↺':'下一題 ▶';
    rscore.textContent='第 '+(ri+1)+' / '+R.length+' 題　答對 '+rok+' 題';
  }
  function ansR(v,btn){
    if(rdone)return; var d=R[ri];
    if(v===d.a){rdone=true;rok++;btn.className='opt ok';rfb.textContent=d.e;rnext.disabled=false;say(d.e);
      rscore.textContent='第 '+(ri+1)+' / '+R.length+' 題　答對 '+rok+' 題'}
    else{btn.className='opt no';rfb.textContent='再想想看。';say('再想想看')}
  }
  rYes.addEventListener('click',function(){ansR(true,rYes)});
  rNo.addEventListener('click',function(){ansR(false,rNo)});
  rnext.addEventListener('click',function(){if(ri===R.length-1){ri=0;rok=0}else ri++;loadR()});
  loadR();

  /* finger tabs */
  var FMAP={a:'f1',s:'f2',d:'f3',f:'f4',g:'f4',h:'f4',j:'f4',k:'f3',l:'f2',';':'f1'};
  var FTXT={
    L:'左手：小指放 a、無名指放 s、中指放 d、食指放 f（g 也是食指管）。',
    R:'右手：食指放 j（h 也是食指管）、中指放 k、無名指放 l、小指放 ;。',
    H:'F 和 J 上面有一條小突起。眼睛看螢幕，手指摸到突起，就知道食指回家了。大拇指放空白鍵。'
  };
  var hks=[].slice.call(document.querySelectorAll('.hk')),ftabs=[].slice.call(document.querySelectorAll('.ftab'));
  var fexp=document.getElementById('fexplain');
  function setF(m){
    ftabs.forEach(function(b){b.setAttribute('aria-pressed',b.getAttribute('data-f')===m)});
    hks.forEach(function(h){
      var k=h.getAttribute('data-key'); h.className='hk'+(h.classList.contains('bump')?' bump':'');
      var left='asdfg'.indexOf(k)>=0, right='hjkl;'.indexOf(k)>=0;
      if(m==='L'&&left)h.classList.add(FMAP[k]);
      if(m==='R'&&right)h.classList.add(FMAP[k]);
      if(m==='H'&&(k==='f'||k==='j'))h.classList.add('hl');
    });
    fexp.innerHTML='<span>'+FTXT[m]+'</span>'; say(FTXT[m]);
  }
  ftabs.forEach(function(b){b.addEventListener('click',function(){setF(b.getAttribute('data-f'))})});

'''
assert "  /* page 3 quiz */" in s
s=s.replace("  /* page 3 quiz */",js+"  /* page 3 quiz */",1)

i0=s.index("  var NOTES=[");i1=s.index("  ];",i0)+4
notes="""  var NOTES=[
    '開場問：打 abc 卻出現怪字，有人遇過嗎？先在教室電腦確認單按 Shift 真的會切換中／英（不同機器設定不同）。',
    '四個情境，全班舉手：○ 可以、✕ 不可以。答錯不批評，讓他們說理由，再看解答。重點：輕按、不拍、不吃東西、不按著不放。',
    '先不要說答案，讓學生猜。再點「中」「A」兩個按鈕。學生手指放 Shift 空手練 3 次，再到記事本實機打 abc。',
    '三題小測驗，全班舉手或手指比 1／2／3 選答案，老師點。答錯不批評，點出理由再讓他們看正解。',
    '三個重點鍵：Shift（按住＋字母＝大寫）、Caps Lock（鎖住大寫，燈亮就是開）、Enter（確定／換行）。先看再讓學生按。',
    '依序點左手、右手、F 和 J。讓學生用自己的食指摸實體鍵盤的小突起。不要求指法，只要求食指回家。',
    '學生不會打網址：老師機投影，學生從 Classroom 連結進入。上課前先實機試玩一次，並確認試算表有收到紀錄。',
    '請學生說出四件事，再點卡片對答案。最後留 5 分鐘讓學生繼續玩符號小站。'
  ];"""
s=s[:i0]+notes+s[i1:]
open(p,'w',encoding='utf-8').write(s)
print(n[0])

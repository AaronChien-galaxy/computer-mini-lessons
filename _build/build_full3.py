import os,re
base=os.path.dirname(os.path.abspath(__file__))
p=os.path.join(base,'full','slides.html')
s=open(p,encoding='utf-8').read()

sym='''<!-- 符號在數字鍵上面：toggle_compare -->
<section class="slide" data-slide="0" data-section="維持注意" data-interaction="toggle_compare" aria-label="數字鍵上的符號">
  <p class="kicker">數字鍵上面藏著符號</p>
  <h2>按住 Shift，數字變符號</h2>
  <div class="switch">
    <button type="button" id="symBtn" aria-pressed="false">按住 Shift：看符號</button>
  </div>
  <div class="numrow" id="numrow" role="group" aria-label="數字鍵"></div>
  <div class="explain" id="symexp" aria-live="polite"><span>點一個鍵，看它是什麼。真的按住 Shift 也可以。</span></div>
  <div class="static-only qstatic"><p>Shift＋2 是 @（電子郵件用），Shift＋1 是 !，Shift＋3 是 #。</p></div>
</section>

'''
ctrl='''<!-- 組合鍵：hotspot（複製貼上復原） -->
<section class="slide" data-slide="0" data-section="維持注意" data-interaction="hotspot" aria-label="複製貼上復原">
  <p class="kicker">兩個鍵一起按</p>
  <h2>Ctrl 組合鍵：複製、貼上、復原</h2>
  <div class="combo-steps" id="csteps">
    <span class="cs" data-cs="sel">① 雙擊文字選起來</span>
    <span class="cs" data-cs="copy">② Ctrl + C 複製</span>
    <span class="cs" data-cs="blank">③ 點一下空白處</span>
    <span class="cs" data-cs="paste">④ Ctrl + V 貼上</span>
    <span class="cs" data-cs="undo">⑤ Ctrl + Z 復原</span>
  </div>
  <div class="docbox" id="docbox" tabindex="0" aria-label="練習文件"><span id="docword" class="docword"></span><span class="cursor2"></span></div>
  <div class="switch">
    <button type="button" class="mini" id="bCopy">複製 Ctrl+C</button>
    <button type="button" class="mini" id="bPaste">貼上 Ctrl+V</button>
    <button type="button" class="mini" id="bUndo">復原 Ctrl+Z</button>
    <button type="button" class="mini" id="bReset">重來</button>
  </div>
  <div class="explain" id="cexp" aria-live="polite"><span>先雙擊上面的字，把它選起來。</span></div>
  <div class="static-only qstatic"><p>Ctrl＋C 複製，Ctrl＋V 貼上，Ctrl＋Z 復原。先把字選起來才能複製。</p></div>
</section>

'''
login='''<!-- 假登入練習：quiz -->
<section class="slide" data-slide="0" data-section="喚起行動" data-interaction="quiz" aria-label="假登入練習">
  <p class="kicker">登入前的暖身（假帳號）</p>
  <h2>用鍵盤完成登入</h2>
  <div class="card-hint">帳號：<b>Amy05@sch</b>　密碼：<b>cat123</b></div>
  <form class="fakeform" id="fform" autocomplete="off">
    <label>帳號 <input type="text" id="fUser" autocomplete="off" autocapitalize="off" spellcheck="false" aria-label="帳號"></label>
    <label>密碼 <input type="password" id="fPass" autocomplete="off" aria-label="密碼"></label>
    <div class="switch">
      <button type="button" class="mini" id="fShow" aria-pressed="false">顯示密碼</button>
      <button type="submit" class="mini" id="fGo">登入（或按 Enter）</button>
    </div>
  </form>
  <div class="explain" id="fres" aria-live="polite"><span>點帳號欄開始打。打完用 Tab 跳到密碼，再按 Enter。</span></div>
  <div class="static-only qstatic"><p>帳號 Amy05@sch：A 要大寫（Shift＋a），@ 是 Shift＋2。打完帳號按 Tab 到密碼欄，打完密碼按 Enter 登入。</p></div>
</section>

'''
marker='<!-- 5 符號小站'
assert marker in s
s=s.replace(marker,sym+ctrl+login+marker,1)

# summary six cards
old='''    <button type="button" class="card3" aria-expanded="false"><span class="ct">④ 輕按、手指回家</span>'''
assert old in s
newcards='''    <button type="button" class="card3" aria-expanded="false"><span class="ct">④ Ctrl 組合鍵</span><span class="detail">Ctrl＋C 複製、Ctrl＋V 貼上、Ctrl＋Z 復原。先選起來再複製。</span></button>
    <button type="button" class="card3" aria-expanded="false"><span class="ct">⑤ Tab 換欄位</span><span class="detail">登入時，打完帳號按 Tab 跳到密碼，不用拿滑鼠。</span></button>
    <button type="button" class="card3" aria-expanded="false"><span class="ct">⑥ 輕按、手指回家</span>'''
s=s.replace(old,newcards,1)
s=s.replace('今天記住四件事','今天記住六件事')

n=[0]
def rn(m):
    n[0]+=1; return 'data-slide="%d"'%n[0]
s=re.sub(r'data-slide="[^"]*"',rn,s)

# page-5 keyboard capture keyed on presence of #kb
old_on="var onKB=slides[cur].getAttribute('data-interaction')==='hotspot';"
assert old_on in s
s=s.replace(old_on,"var onKB=!!slides[cur].querySelector('#kb');")

css='''
.numrow{display:flex;gap:clamp(4px,.8vw,10px);justify-content:center;width:min(1000px,100%)}
.nk{flex:1 1 0;max-width:86px;height:clamp(54px,11vh,86px);border:0;border-radius:12px;background:#fff;box-shadow:0 5px 0 #C9C0AE;font-size:calc(var(--t-body)*1.1);font-weight:900;color:var(--ink);transition:background .25s}
.numrow.sym .nk{background:var(--primary-soft);box-shadow:0 5px 0 #A9CBD8;color:var(--primary)}
.nk.pick{background:var(--accent)!important;color:#fff!important}
.combo-steps{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;width:min(1000px,100%)}
.cs{background:var(--card);border:4px solid var(--line);border-radius:999px;padding:.15em .8em;font-size:var(--t-caption);font-weight:800;color:var(--muted)}
.cs.done{background:var(--good-soft);border-color:var(--good);color:var(--ink)}
.docbox{width:min(1000px,100%);min-height:2.6em;background:var(--card);border:5px solid var(--line);border-radius:22px;padding:.4em .8em;font-size:calc(var(--t-body)*1.15);text-align:left;word-break:break-all;cursor:text}
.docbox:focus-visible{border-color:var(--primary)}
.docword{border-radius:6px;padding:0 .1em}
.docword.sel{background:#BFD9F2}
.cursor2{display:inline-block;width:.08em;height:1em;background:var(--ink);vertical-align:-.12em;animation:blink 1s steps(1) infinite}
.card-hint{background:var(--accent-soft);border-left:10px solid var(--accent);border-radius:16px;padding:.35em 1em;font-size:var(--t-body)}
.fakeform{display:flex;flex-direction:column;gap:10px;width:min(700px,100%);background:var(--card);border:5px solid var(--line);border-radius:22px;padding:clamp(10px,2vh,20px)}
.fakeform label{display:flex;gap:12px;align-items:center;font-size:var(--t-body);font-weight:800;text-align:left}
.fakeform input{flex:1;min-width:0;font:inherit;font-weight:700;border:4px solid var(--line);border-radius:14px;padding:.2em .5em;background:#fff;color:var(--ink)}
.fakeform input:focus{border-color:var(--primary);outline:none}
@media (min-width:901px){.three{grid-template-columns:repeat(3,1fr)!important;width:min(1100px,100%)!important}}
@media (max-height:780px){
  .slide[data-interaction="toggle_compare"][aria-label="數字鍵上的符號"] .kicker,
  .slide[aria-label="複製貼上復原"] .kicker,
  .slide[aria-label="假登入練習"] .kicker{display:none}
  .slide[aria-label="複製貼上復原"] .docbox{min-height:1.8em}
  .card3{padding:10px}
}
'''
s=s.replace('#notes{position:fixed',css+'#notes{position:fixed',1)

js='''
  /* number row symbols */
  var NUMS=[['1','!','驚嘆號，表示很驚訝或很大聲'],['2','@','「小老鼠」，電子郵件帳號中間就是它'],['3','#','井字號'],['4','$','錢的符號'],['5','%','百分比'],['6','^','次方符號，很少用'],['7','&','「和」的意思'],['8','*','星號，密碼常用'],['9','(','左括號'],['0',')','右括號']];
  var numrow=document.getElementById('numrow'),symBtn=document.getElementById('symBtn'),symexp=document.getElementById('symexp');
  var symOn=false,nkEls=[];
  NUMS.forEach(function(d,i){
    var b=document.createElement('button');b.type='button';b.className='nk';
    b.addEventListener('click',function(){
      nkEls.forEach(function(x){x.classList.remove('pick')});b.classList.add('pick');
      var t=symOn?('Shift＋'+d[0]+' ＝ '+d[1]+'　'+d[2]):('數字 '+d[0]+'　按住 Shift 再按，會變 '+d[1]);
      symexp.innerHTML='<span>'+t+'</span>';say(t);
    });
    numrow.appendChild(b);nkEls.push(b);
  });
  function renderSym(){
    nkEls.forEach(function(b,i){b.textContent=symOn?NUMS[i][1]:NUMS[i][0]});
    numrow.classList.toggle('sym',symOn);
    symBtn.setAttribute('aria-pressed',symOn);
    symBtn.textContent=symOn?'放開 Shift：看數字':'按住 Shift：看符號';
  }
  symBtn.addEventListener('click',function(){symOn=!symOn;renderSym();say(symOn?'現在是符號':'現在是數字')});
  renderSym();
  document.addEventListener('keydown',function(e){
    if(e.key==='Shift'&&slides[cur].contains(numrow)&&!symOn&&!e.repeat){symOn=true;renderSym()}
  });
  document.addEventListener('keyup',function(e){
    if(e.key==='Shift'&&slides[cur].contains(numrow)&&symOn){symOn=false;renderSym()}
  });

  /* ctrl combo practice */
  var WORD='我愛電腦課';
  var docword=document.getElementById('docword'),docbox=document.getElementById('docbox'),cexp=document.getElementById('cexp');
  var doc,hist,sel,clip,cdone;
  function cmark(k){cdone[k]=true;[].forEach.call(document.querySelectorAll('.cs'),function(e){e.classList.toggle('done',!!cdone[e.getAttribute('data-cs')])})}
  function crender(){docword.textContent=doc;docword.classList.toggle('sel',sel)}
  function cmsg(t){cexp.innerHTML='<span>'+t+'</span>';say(t)}
  function creset(){doc=WORD;hist=[];sel=false;clip='';cdone={};crender();cmark('none');cmsg('先雙擊上面的字，把它選起來。')}
  function doCopy(){if(!sel){cmsg('還沒選起來喔！先雙擊文字。');return}clip=doc;cmark('copy');cmsg('複製好了，字被記在「剪貼簿」裡。接著點一下空白處。')}
  function doPaste(){if(!clip){cmsg('還沒複製，沒有東西可以貼。');return}
    if(sel){cmsg('字還是選起來的，貼上會蓋掉它。先點一下空白處。');return}
    hist.push(doc);doc=doc+clip;crender();cmark('paste');cmsg('貼上了！同一句話出現第二次。')}
  function doUndo(){if(!hist.length){cmsg('沒有可以復原的動作。');return}doc=hist.pop();crender();cmark('undo');cmsg('復原了，回到上一步。')}
  docword.addEventListener('dblclick',function(){sel=true;crender();cmark('sel');cmsg('選起來了（藍底）。按 Ctrl＋C 複製。')});
  docbox.addEventListener('click',function(e){if(e.target===docword&&e.detail>1)return;if(e.target!==docword||!sel){}
    if(e.target!==docword&&sel){sel=false;crender();cmark('blank');cmsg('游標回到最後面。按 Ctrl＋V 貼上。')}});
  document.getElementById('bCopy').addEventListener('click',doCopy);
  document.getElementById('bPaste').addEventListener('click',doPaste);
  document.getElementById('bUndo').addEventListener('click',doUndo);
  document.getElementById('bReset').addEventListener('click',creset);
  creset();
  document.addEventListener('keydown',function(e){
    if(!slides[cur].contains(docbox))return;
    if(!(e.ctrlKey||e.metaKey))return;
    var k=e.key.toLowerCase();
    if(k==='c'){e.preventDefault();doCopy()}
    else if(k==='v'){e.preventDefault();doPaste()}
    else if(k==='z'){e.preventDefault();doUndo()}
  });

  /* fake login */
  var fUser=document.getElementById('fUser'),fPass=document.getElementById('fPass'),fres=document.getElementById('fres'),fform=document.getElementById('fform');
  var fShow=document.getElementById('fShow'),ft0=0;
  function fmsg(t,ok){fres.innerHTML='<span>'+t+'</span>';fres.style.borderColor=ok?'var(--good)':'';say(t)}
  [fUser,fPass].forEach(function(i){i.addEventListener('focus',function(){if(!ft0)ft0=Date.now()})});
  fShow.addEventListener('click',function(){var on=fPass.type==='password';fPass.type=on?'text':'password';fShow.setAttribute('aria-pressed',on);fShow.textContent=on?'隱藏密碼':'顯示密碼'});
  fform.addEventListener('submit',function(e){
    e.preventDefault();
    var u=fUser.value,pw=fPass.value;
    if(u==='Amy05@sch'&&pw==='cat123'){
      var sec=ft0?Math.round((Date.now()-ft0)/1000):0;
      fmsg('登入成功！用了 '+sec+' 秒。再玩一次可以挑戰更快。',true);
      fUser.value='';fPass.value='';ft0=0;
    }else if(u!=='Amy05@sch'){
      if(u.toLowerCase()==='amy05@sch')fmsg('帳號大小寫不對。A 要大寫（Shift＋a）。',false);
      else if(u.indexOf('@')<0)fmsg('帳號少了 @。按住 Shift 再按 2。',false);
      else fmsg('帳號有地方打錯，再對照一次。看右下角是不是英文模式。',false);
    }else fmsg('密碼不對，點「顯示密碼」看看打了什麼。',false);
  });
'''
assert "  /* page 3 quiz */" in s
s=s.replace("  /* page 3 quiz */",js+"  /* page 3 quiz */",1)

i0=s.index("  var NOTES=[");i1=s.index("  ];",i0)+4
notes="""  var NOTES=[
    '開場問：打 abc 卻出現怪字，有人遇過嗎？先在教室電腦確認單按 Shift 真的會切換中／英（不同機器設定不同）。',
    '四個情境，全班舉手：○ 可以、✕ 不可以。以前教過，快速帶過，重點是學生自己說理由。',
    '複習：右下角「中」／「A」，按一下 Shift 切換。讓學生說出什麼時候一定要英文（登入）。',
    '複習：三題小測驗，答錯不批評，讓他們說理由再看正解。',
    '複習：Shift、Caps Lock、Enter 三顆鍵，加上倒退和空白。學生可以直接按實體鍵。',
    '複習：F 和 J 的小突起、食指回家。只要求食指，不要求標準指法。',
    '加深一：數字鍵上面的符號。重點是 Shift＋2＝@，之後登入、電子郵件都會用。讓學生真的按住 Shift 看畫面變化。',
    '加深二：Ctrl 組合鍵。步驟：雙擊選起來→Ctrl＋C→點空白處→Ctrl＋V→Ctrl＋Z。先讓學生看，再各自在記事本實機做一次。',
    '加深三：假登入。帳號有大寫和 @，是今天所有東西的總驗收。打完帳號按 Tab 換密碼欄，再按 Enter。鼓勵看「用了幾秒」，只跟自己比。',
    '學生不會打網址：老師機投影，學生從 Classroom 連結進入。上課前先實機試玩一次，並確認試算表有收到紀錄。',
    '請學生說出六件事，再點卡片對答案。最後留時間讓學生繼續玩符號小站。'
  ];"""
s=s[:i0]+notes+s[i1:]
open(p,'w',encoding='utf-8').write(s)
print(n[0])

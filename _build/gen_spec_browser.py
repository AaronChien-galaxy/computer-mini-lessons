import os,re
base=os.path.dirname(os.path.abspath(__file__))
t=open(os.path.join(base,'full','spec.yaml'),encoding='utf-8').read()
head=t.split('\nslides:\n')[0]
head=re.sub(r'slide_count: \d+','slide_count: 8',head)
head=re.sub(r'title: "[^"]*"','title: "電腦小知識：瀏覽器基本"',head,count=1)
head=re.sub(r'purpose: "[^"]*"','purpose: "分清網址列與搜尋框，會用分頁、上一頁、重新整理"',head,count=1)
head=re.sub(r'takeaway: "[^"]*"','takeaway: "知道網址就打網址，想找答案就搜尋"',head,count=1)
S=[
 (1,'hook','cover','知道今天要學什麼','網址列與搜尋框','focus','cover_hero','left_title','網址列和搜尋框差在哪？','none','','cover','[]','static cover'),
 (2,'attention','hierarchy','認識瀏覽器各部位','每個部位有名字','hierarchy','relationship_map','browser_hotspot','點點看，每個地方叫什麼','hotspot','認識瀏覽器部位','idle','[tab, plus, back, reload, addr, search]','部位說明列出'),
 (3,'attention','practice','分辨打網址或搜尋','知道網址就打，想找答案就搜尋','practice','question_focus','quiz','要打網址，還是要搜尋？','quiz','判斷用網址列還是搜尋','question_1','[q1, q2, q3, q4]','四題答案列出'),
 (4,'attention','sequence','看懂網址三段','看網站名字那一段','sequence','process_timeline','url_stepper','網址可以拆成三段','stepper','認識網址組成','segment_1','[s1, s2, s3]','三段說明列出'),
 (5,'attention','hierarchy','開關與切換分頁','分頁可以同時開很多個','hierarchy','relationship_map','tab_sim','分頁：開、切換、關','tabs','操作分頁','one_tab','[open, switch, close]','三個動作列出'),
 (6,'attention','practice','遇到狀況選對按鈕','上一頁、重新整理、關閉','practice','question_focus','quiz','按哪一個鍵來救？','quiz','判斷情境對應按鈕','question_1','[q1, q2, q3]','三題答案列出'),
 (7,'action','practice','在假瀏覽器完成任務','打網址、上一頁、搜尋、重新整理','practice','action_next_step','fake_browser','自己上網走一圈','quiz','整合瀏覽器操作','home','[home, classroom, search, notfound]','四個任務列出'),
 (8,'action','synthesis','回顧四個重點','四件事','synthesis','summary_three','reveal_cards','今天記住四件事','reveal','自我檢查重點','collapsed','[c1, c2, c3, c4]','四個重點全部展開'),
]
def blk(n,phase,role,task,point,sem,lay,var,title,itype,goal,init,states,fb):
    return f'''  - page: {n}
    soil_phase: "{phase}"
    role: "{role}"
    learning_task: "{task}"
    core_point: "{point}"
    semantic_structure: "{sem}"
    layout: {{id: "{lay}", variant: "{var}"}}
    visible_text: {{title: "{title}"}}
    speaker_only: "見 NOTES"
    visual: {{mode: "native", brief: "", source: ""}}
    interaction: {{type: "{itype}", goal: "{goal}", trigger: "click", initial_state: "{init}", states: {states}, fallback: "{fb}"}}
    accessibility: {{keyboard: true, touch: true, reduced_motion: true}}
'''
os.makedirs(os.path.join(base,'browser'),exist_ok=True)
open(os.path.join(base,'browser','spec.yaml'),'w',encoding='utf-8').write(head+'\nslides:\n'+''.join(blk(*x) for x in S))

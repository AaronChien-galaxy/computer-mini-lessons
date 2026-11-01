import os,re
base=os.path.dirname(os.path.abspath(__file__))
p=os.path.join(base,'full','spec.yaml')
t=open(p,encoding='utf-8').read()
head=t.split('\nslides:\n')[0]
head=re.sub(r'slide_count: \d+','slide_count: 11',head)
S=[
 (1,'hook','cover','知道今天要學什麼','打字會變怪字，是因為輸入法模式','focus','cover_hero','left_title','打字怎麼變成怪怪的字？','none','','cover','[]','static cover'),
 (2,'hook','practice','判斷鍵盤使用規矩','輕按、不拍、不吃東西、不按著不放','practice','question_focus','quiz','這樣可以嗎？','quiz','判斷哪些行為可以','question_1','[r1, r2, r3, r4]','四個情境與解答直接列出'),
 (3,'attention','comparison','比較中文與英文模式','按 Shift 切換','contrast','comparison_split','interactive_toggle','打 a b c，會出現什麼？','toggle_compare','看見兩種模式的差別','overview','[zh, en]','兩個面板並排顯示'),
 (4,'attention','practice','判斷大寫的按法','Shift 與 Caps Lock 的差別','practice','question_focus','quiz','怎麼按才對？','quiz','判斷大寫的按法','question_1','[q1, q2, q3]','三題答案直接列出'),
 (5,'attention','hierarchy','認識功能鍵','每個鍵各有作用','hierarchy','relationship_map','keyboard_hotspot','按一個鍵，看它做什麼','hotspot','認識功能鍵作用','idle','[shift, capslock, enter, backspace, space]','按鍵說明文字列出'),
 (6,'attention','hierarchy','知道手指放哪裡','食指回家，摸 F 和 J 的突起','hierarchy','relationship_map','finger_tabs','手指「回家」的位置','tabs','記得手指擺位','idle','[left, right, bumps]','手指擺位文字直接列出'),
 (7,'attention','comparison','知道數字鍵上的符號','Shift＋2 是 @','contrast','comparison_split','number_row_toggle','按住 Shift，數字變符號','toggle_compare','認識數字鍵與符號的對應','numbers','[numbers, symbols]','符號對照直接列出'),
 (8,'attention','practice','用 Ctrl 組合鍵複製貼上','選起來再複製','hierarchy','relationship_map','ctrl_practice','Ctrl 組合鍵：複製、貼上、復原','hotspot','完成選取、複製、貼上、復原','idle','[select, copy, blank, paste, undo]','五個步驟文字列出'),
 (9,'action','practice','用鍵盤完成登入','Tab 換欄位、Enter 送出','practice','action_next_step','fake_login','用鍵盤完成登入','quiz','整合大小寫、符號、Tab、Enter','empty','[empty, wrong, success]','登入步驟文字列出'),
 (10,'action','sequence','知道符號小站怎麼玩','四個步驟','sequence','process_timeline','stepper','符號小站，四步驟','stepper','記得登入與練習流程','step_1','[s1, s2, s3, s4]','四步驟全部列出'),
 (11,'action','synthesis','回顧六個重點','六件事','synthesis','summary_three','reveal_cards','今天記住六件事','reveal','自我檢查重點','collapsed','[c1, c2, c3, c4, c5, c6]','六個重點全部展開'),
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
open(p,'w',encoding='utf-8').write(head+'\nslides:\n'+''.join(blk(*x) for x in S))

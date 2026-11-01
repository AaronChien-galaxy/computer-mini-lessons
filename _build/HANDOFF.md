# 交接：電腦小知識系列（computer-mini-lessons）

## 已完成（已 commit，尚未 push／上架，Aaron 自己跑 gh）
- keyboard-basics/：鍵盤小高手 11 頁（11/2 用）
- browser-basics/：瀏覽器小達人 8 頁（11/9 用）
- 首頁 index.html：課程選單（目前只列兩課）

## 進行中：一次做完剩下 6 課（Aaron 說先全做完，每週上課前再討論細節修改）
`_build/build_lessons.py` 已寫好（通用元件＋6 個模擬器 SIMS：login / windows / search / save / popup / sound），
它在最後 exec 同資料夾的 `lessons_content.py`，**這個檔還沒寫**——要定義 `LESSONS` 清單，每課一個 dict：
`slug, title, purpose, takeaway, pages[]`；頁型別 cover / hotspot / quiz / stepper / sim / reveal，欄位見 build_lessons.py 的 page_html()。
sim 頁要給 `sim`（SIMS 名稱）、`tasks`（[(key,label)]，key 對應 JS 的 mark 鍵）、`html`（模擬器骨架）、`static`。
search 課要在課的 dict 加 `results`（[{t,u,ad,ok,e}]）。build_lessons.py 的 CSS 取自 scratchpad 的 browser/slides.html（需先跑 build_browser.py，或改成讀 browser-basics/index.html）。
輸出到 scratchpad\lessons\<slug>\index.html + spec.yaml；驗證用 skill soil-html-deck 的 verify_html.py（--strict-offline）；通過後複製到本倉庫 <slug>/index.html，更新首頁選單，commit。

### 6 課內容規劃
| slug | 課名 | 日期 | 頁面 |
|---|---|---|---|
| login-basics | 登入小達人 | 11/16 | 封面→hotspot（帳號欄／密碼欄／顯示密碼／登入／Tab）→quiz 密碼規矩（可以/不可以）→stepper 登入口訣六步→sim login（假帳號 stu05@school.example／密碼 cat123，兩步驟登入、顯示密碼、頭像登出、計秒）→quiz 登入出錯怎麼辦→reveal |
| window-switching | 視窗小管家 | 11/30 | 封面→hotspot（工作列／− / □ / × / Alt+Tab）→quiz→sim windows（四任務：最小化瀏覽器、工作列叫回、Alt+Tab 切記事本、關小畫家）→quiz→reveal |
| search-skills | 搜尋小偵探 | 12/7 | 封面→stepper 關鍵字三步→quiz 選關鍵字→sim search（挑最可靠結果：看網址 .edu.tw／.gov.tw、廣告標示）→quiz 網址線索→reveal |
| save-files | 存檔小管家 | 12/14 | 封面→hotspot 另存新檔視窗→stepper 存檔五步（Ctrl+S、選資料夾、取名只用英數）→sim save（四任務）→quiz 找不到檔案→reveal |
| web-safety | 網路安全小盾牌 | 12/21 前 | 封面→hotspot 假彈窗特徵→quiz 可以點嗎（○✕ 六題）→sim popup（假中獎彈窗，關掉＋告訴老師）→stepper 口訣「不點、不填、不下載、先問老師」→reveal |
| first-aid | 電腦小急救 | 彈性 | 封面→hotspot（音量／靜音／耳機孔／亮度／截圖鍵）→sim sound（靜音、音量、耳機三原因）→stepper 截圖三步（Win+Shift+S→拉框→Ctrl+V）→quiz→reveal |

### 踩坑（寫腳本時）
- 用 bash heredoc 寫含中文的 Python 會變亂碼（cp950）；一律用 Write 工具寫 .py 檔再跑。
- Python 字串裡的 JS 用 r''' 原始字串；不要在一般字串裡放 \n 之類跳脫。
- 預覽面板開 file:// 不跑 JS，要用 python -m http.server 起本機伺服器再導覽。
- verify_html 要求：id=progress／section-tag／page-info、aria-live="polite"、互動頁要有靜態 <button>；strict-offline 不能有外部 href。
- 1280×720 高度很緊：每頁最底元素要在下方按鈕（top≈657px）之上；手機寬度 390 不可橫向捲動。
- 前面各課共用的鍵盤盤／學生已教過的內容，簡報前幾頁可快速複習。

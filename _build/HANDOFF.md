# 交接：電腦小知識系列（computer-mini-lessons）

## 已完成（已 commit，尚未 push／上架，Aaron 自己跑 gh）
- keyboard-basics/：鍵盤小高手 11 頁（11/2 用）
- browser-basics/：瀏覽器小達人 8 頁（11/9 用）
- 首頁 index.html：課程選單（目前只列兩課）

## 第二批 6 課（11/1 完成，已 commit，未 push）
login-basics 7 頁、window-switching 6 頁、search-skills 6 頁、save-files 6 頁、web-safety 6 頁、first-aid 6 頁；首頁選單已列 8 課。
內容在 `_build/lessons_content.py`，通用元件／模擬器在 `build_lessons.py`。改內容流程：改 lessons_content.py → 把兩個 .py 複製到 scratchpad 跑 `python build_lessons.py`（CSS 自動讀 browser-basics/index.html，輸出在 scratchpad\lessons\）→ verify_html --strict-offline → 複製 index.html 回倉庫 → commit。
細節修改：Aaron 每週上課前再討論。

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

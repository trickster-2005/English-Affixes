# English Affixes｜英文構詞學習筆記

把英文單字拆成「詞綴＋字根」，再往上追到印歐語的共同祖先。三份中文學習筆記由淺入深，所有例字都附上中文意義與**美式 IPA 音標**。

**線上閱讀**：<https://trickster-2005.github.io/English-Affixes/>

## 內容

| 頁面 | 說明 | 規模 |
|---|---|---|
| [英文詞綴主題大全](affixes.html) | 依 affixes.org 的 29 個主題整理字首、字尾與組合形式，附例字、中文、構詞拆解與詞源；另有拼寫同化規則、希臘／拉丁詞綴對照等附錄 | 約 400 個詞綴、6,000 個附音標的單字 |
| [英文字根大全](roots.html) | 約 110 個最常見的拉丁語與希臘語字根，依意義分成 12 類 | 約 1,700 個單字 |
| [印歐語根與同源字](pie.html) | 從原始印歐語追溯英語本土字、拉丁系與希臘系的同源關係，含格林定律、元音變換等入門說明 | 123 個印歐語根、約 1,500 個單字 |

每一頁左側都有可篩選的目錄，手機版可由左上角「☰ 目錄」開啟。

## 資料來源

- **主題分類與詞綴清單**：Michael Quinion, *Dictionary of Affixes*（[affixes.org](https://www.affixes.org/)；原書為 *Ologies and Isms*, Oxford University Press, 2002）。本專案只沿用其主題架構與詞綴名稱，例字、中文解釋與拆解皆為另行撰寫。
- **印歐語根**：Calvert Watkins, *The American Heritage Dictionary of Indo-European Roots*（3rd ed.），並以 [Etymonline](https://www.etymonline.com/) 與 [Wiktionary](https://en.wiktionary.org/) 交叉查證。有爭議的說法標註「一說」。
- **音標**：[CMU Pronouncing Dictionary](https://github.com/cmusphinx/cmudict) 轉換為 IPA；字典未收的字以 [eSpeak NG](https://github.com/espeak-ng/espeak-ng) 產生，再人工修正。
- **詞頻**：[wordfreq](https://github.com/rspeer/wordfreq)，用於挑選常用但不冷僻的中高級單字。

## 製作方式

內容由 Claude（Anthropic 的 AI 助理）依使用者需求逐步整理撰寫；音標以程式自動產生並人工校正。AI 整理的內容難免有疏漏，尤其是詞源，歡迎開 issue 指正。

## 專案結構

```
.
├── index.html          首頁（資料來源與製作說明）
├── affixes.html        英文詞綴主題大全
├── roots.html          英文字根大全
├── pie.html            印歐語根與同源字
├── assets/
│   ├── style.css       版面樣式（含深色模式、手機版）
│   └── site.js         目錄篩選、目前章節標示、手機選單
├── md/                 Markdown 原稿（修改內容請改這裡）
│   ├── affixes.md
│   ├── roots.md
│   └── pie.md
└── build.py            由 md/ 產生 HTML 的腳本
```

## 修改與重新產生網頁

```bash
pip install markdown
python3 build.py
```

修改 `md/` 裡的 Markdown 後執行 `build.py`，就會重新產生四個 HTML 檔與左側目錄。

## 啟用 GitHub Pages

1. 到 repository 的 **Settings → Pages**。
2. **Source** 選 **Deploy from a branch**，Branch 選 `main`、資料夾選 `/ (root)`，按 Save。
3. 約一分鐘後即可在 `https://trickster-2005.github.io/English-Affixes/` 瀏覽。

根目錄的 `.nojekyll` 讓 GitHub Pages 直接提供靜態檔案，不經 Jekyll 處理。

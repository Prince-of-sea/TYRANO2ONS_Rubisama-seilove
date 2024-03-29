# TYRANO2ONS_Rubisama-seilove
⚠必ず注意事項を読んでください⚠
## なにこれ
  2022年に[るび様を崇める会](https://rubisama.com/)から発売された、18禁PC向けノベルゲーム'[セイラに夢みたいないちゃラブご奉仕させていただけますか](https://rubisama.com/seira/)'を<br>
  ONScripter形式へ変換するためのコンバータです<br>

## 再現度
原作との違いは主に以下
 - ゲーム進行時のUIはすべて未実装<br>
   セーブ等は右クリックで行う仕様
 - ゲーム終了時の操作が少々特殊<br>
   (環境設定→終了する)
 - タイトル画面のCGがランダムではなく固定
 - キャラ移動/一部エフェクト/可変文字未実装
 - コンフィグ/CG/回想未実装
 - **エンディング未実装**
 - その他細かいバグ有り(?)

v0.8.0現在ではとりあえず最後まで読めるだけ、な状態です

## 使い方
※事前に[ffmpegのパスを通して](https://www.google.com/search?q=ffmpeg+%E3%83%91%E3%82%B9+%E9%80%9A%E3%81%99+windows)ください

 1. 専用ツールを利用して"resources/app.asar"を展開します<br>
    (筆者は[Asar7z](https://www.google.com/search?q=Asar7z)を利用しました)

 2. 適当な作業フォルダを作成し、展開したasar内の"data"フォルダを移動させます

 3. 展開先のディレクトリで[このコンバータ](https://github.com/Prince-of-sea/TYRANO2ONS_Rubisama-seilove/releases/latest)をDL<br>

 4. 起動させ変換(性能次第では数十秒で終わります)<br>
    変換前の時点で以下のような構成になっていればOKです↓<br>
```
C:.
│  TYRANO2ONS_Rubisama-seilove.py
│  
└─data
    ├─bgimage
    │      bg_cg.png
    │      (～略)
    │      食堂.jpg
    │      
    ├─bgm
    │      ChilledCow-Mom.mp3
    │      (～略)
    │      高貴なご趣味.mp3
    │      
    ├─fgimage
    │  ├─chara
    │  │  └─seira
    │  │          mainvisual.jpg
    │  │          (～略)
    │  │          裸_腕広げ_驚き_眼鏡.png
    │  │          
    │  └─default
    ├─image
    │  │  frame.png
    │  │  (～略)
    │  │  obon.png
    │  │  
    │  ├─button
    │  │      auto.png
    │  │      (～略)
    │  │      title2.png
    │  │      
    │  ├─config
    │  │      arrow_next.png
    │  │      (～略)
    │  │      skipon.png
    │  │      
    │  └─title
    │          button_cg.png
    │          (～略)
    │          button_start_hover.png
    │          
    ├─others
    │  ├─3d
    │  │  ├─model
    │  │  ├─sprite
    │  │  └─texture
    │  └─plugin
    │      └─seira
    │          │  backlog.css
    │          │  (～略)
    │          │  title.css
    │          │  
    │          ├─html
    │          │      backlog.html
    │          │      load.html
    │          │      save.html
    │          │      
    │          ├─images
    │          │  ├─background
    │          │  │      background.png
    │          │  │      (～略)
    │          │  │      title_2.png
    │          │  │      
    │          │  ├─button
    │          │  │      arrow_down.png
    │          │  │      (～略)
    │          │  │      title2.png
    │          │  │      
    │          │  ├─frame
    │          │  │      saveslot.png
    │          │  │      saveslot_hover.png
    │          │  │      
    │          │  └─logo
    │          │          logo.png
    │          │          
    │          └─testMessagePlus
    │                  gMessageTester.js
    │                  sampletext.ks
    │                  style.css
    │                  
    ├─scenario
    │      cg.ks
    │      (～略)
    │      tyrano.ks
    │      
    ├─sound
    │  │  caster.mp3
    │  │  (～略)
    │  │  電車輪_2.mp3
    │  │  
    │  ├─noname_1
    │  │      SeiraVoice(1).ogg
    │  │      (～略)
    │  │      SeiraVoice(9).ogg
    │  │      
    │  ├─seira_1
    │  │      SeiraVoice(1).ogg
    │  │      (～略)
    │  │      SeiraVoice(999).ogg
    │  │      
    │  └─seira_2
    │          SeiraVoice(1).ogg
    │          (～略)
    │          SeiraVoice(6).ogg
    │          
    ├─system
    │      Config.tjs
    │      KeyConfig.js
    │      
    └─video
            endroll.webm
```

 5. ウィンドウが消え、0.txtができれば完成<br>
    変換済みファイルと共に利用ハードへ転送


## 注意事項
 - 当然ですが公式ツールではありません
 - DLSite DL版、2022/8/9時点での最新バージョンで動作確認しています
 - 本ツールの使用において生じた問題や不利益などについて、作者は一切の責任を負いません
 - 制作サークル様に迷惑をかけたくないので、<br>
   本ツールのSNS等での拡散は**ご遠慮ください**<br>
   ~~(拡散されるほどのツールでもない気はするが一応)~~<br>



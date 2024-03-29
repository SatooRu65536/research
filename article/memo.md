# 論文

## はじめに
現在、日本の都市では交通事故が多発しており、それを未然に防ぐために都市を完全に歩車分離し、完全自動運転を目標としました。
自動運転は景観を保つために信号を無くし、自動走行中の無駄には給油や給電があるので、自動運転中の自動給電も行いました。
今回はこのテーマを実現するために、「都市づくり」「車両製作」「システム制作」の３チームで行いました。
この論文では、このテーマのうちの「システム制作」について記述します。

## 問題提起
現在の自動運転は、画像認識が主体ですが、天候により認識しづらいなどの問題があります。
また信号は混雑していないときにも一時停止する必要があり、自動運転が発展した社会では柔軟性に欠けると考えます。
そこで画像認識に頼らない、NFCタグを用いた、全ての車を一括制御する新しい自動運転のシステムを開発することにし、有効性を検証するためシュミレーターを制作しました。

## シミュレーターについて
シミュレーターを制作する上で使用した言語は Python3.8 で、ライブラリは
`conccurent.futures` `sqlite3` です。
シミュレーターを立ち上げると交差点一つに対し、交差点制御が立ち上げられ、
クライアントから接続されるとその交差点に進入できるかの判断をし、クライアントに返した上でデータベースに登録します。
クライアントは一定時間に1台立ち上げられます。
このクライアントの間隔は車の間隔に当たります。

## 検証1
### 実験内容
交差点単体に着目し、クライアントが立ち上げられる時間(車の間隔)を `650ms/台` ~ `1200ms/台` の範囲で変更し、
5分経過時点での処理数と待機数を比較しました。
クライアントはランダムな方角から方角へ移動するようになっています。

### 実験結果
結果をグラフ化すると以下のようになりました。

(new1は消す)
![処理数-1](https://docs.google.com/spreadsheets/d/e/2PACX-1vSDcloY71481hB0FpkomezlnNjGZpPEFegFVnGm2JX5h_pkD8_AO-UcSNwicodauZi7aXvQntKbFgBz/pubchart?oid=1751094130&format=image)  
![待機数-1](https://docs.google.com/spreadsheets/d/e/2PACX-1vSDcloY71481hB0FpkomezlnNjGZpPEFegFVnGm2JX5h_pkD8_AO-UcSNwicodauZi7aXvQntKbFgBz/pubchart?oid=1814756461&format=image)  


信号と新システムを比較した結果、処理数のグラフより、車の間隔が狭いほど新システムが優位だと分かります。
車の間隔が広くなるにつれ等しくなっていますが、待機数のグラフより待機数が限りなく少ないため共に車を捌き切れていると分かります。

交差点単体では、新システムの方が効率的であるという結果が得られましたが、
現実では複数の交差点間の兼ね合いがあるため、2回目ではマップ全体として検証しました。  

## 検証2
### 実験内容
交差点単体に着目していたのを、12x12 のおよそ碁盤の目状のマップ上で、クライアントはランダムな交差点から交差点へと移動します。
また、移動は最短経路を辿るようになっており、これにはA*アルゴリズムを使用しています。
1回目同様、信号と新システムの処理数と待機数で比較します。  
また、ある交差点が混雑していた場合はその交差点を除いた最短経路で移動するシステムも比較します。
回避するようにしたものを `信号'` `新システム'` と表します。

### 実験結果
結果をグラフ化すると以下のようになりました。

![2-処理数](https://docs.google.com/spreadsheets/d/e/2PACX-1vSDcloY71481hB0FpkomezlnNjGZpPEFegFVnGm2JX5h_pkD8_AO-UcSNwicodauZi7aXvQntKbFgBz/pubchart?oid=522272234&format=image)  
![2-待機数](https://docs.google.com/spreadsheets/d/e/2PACX-1vSDcloY71481hB0FpkomezlnNjGZpPEFegFVnGm2JX5h_pkD8_AO-UcSNwicodauZi7aXvQntKbFgBz/pubchart?oid=1762092698&format=image)  

new2は信号よりも処理数が多く待機数が少ない理想的な状況で、特に車の間隔が狭い場合は差が顕著に表れています。
これは交差点単体での遅延は少なかったが、経路全体とすると大きくなっているからだと考えられます。
また、信号は混雑度に関わらず一定数待機する必要がありますが、new2は混雑していない場合は待機する必要がなくなったことが分かります。
しかし、新たに追加したnew2に注目すると、
`信号` と `信号'` 、`new` と `new'` をそれぞれ比較すると、回避しない方が効率的という結果が得られました。
これは12x12というサイズで検証したため、混雑により回避できる経路がなく余計な処理が増えたからだと考えられます。

### 結論
既存の信号より効率的なシステムを制作することができ、有効性を確認することができた。
今後はシュミレーターに、車の進入間隔以外のアクシデント等ランダム性や、Y字路などの複雑な構造を追加し、より現実的にし検証を重ねていくことが必要がある

##　それぞれの担当
### 小松
・説明で理解しづらい部分を補完するために After Effects を使い動画で図式しました。
・問題提起部分を理解しやすくするために illustrator でイラストを制作しました。
・視覚的に飽きさせないようなスライドを制作しました。
・制作したシュミレーターでの検証をしました。

### 多田
・新システムの概要の考案しました。
・シミュレーター全体を制作しました。
・制作したシュミレーターでの検証をしました。
・全体発表用のスライドを制作しました。
・発表の台本を制作しました。

### 吉田
・新システムの概要の考案しました。
・Astarアルゴリズムで最短経路を求めるシステムを制作しました。
・制作したシュミレーターでの検証をしました。
・発表の台本を制作しました。

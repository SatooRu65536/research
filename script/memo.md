# メモ

## 大まかな流れ (5分)
1. 目次
2. 前提条件
   - 歩車分離
   - 完全自動運転(レベル5)
3. 目標・問題提起
   - 理想のシステム形態について
4. システムについて
   1. 説明
      - 使用言語(Python) / ライブラリ / データベース(sqltie3) / 通信手段
      - 信号の問題点/タグ検知の利点
   2. 結果・考察
      - 信号あり / 時間順 を比較
   3. 改善
      - 交差点制御の改善
      - マップ全体としての制御(Astar)
   4. 改善の結果・考察
5. 結論
   - 画像


## 問題提起
- 車側の問題
  - 画像処理では問題があるのではないか
    - 気候や障害物により認識が困難になる可能性がある => 事故が起きるかも
- 信号側の問題
  - 非混雑時の一時停止時間が非効率
  - 気候や障害物により認識が困難になる可能性がある
- ロータリー
  - 場所が必要(市街地は難しい)
  - 交通量が多いと渋滞がおきやすい


## 解決策
- 視覚以外の情報も使って制御

## テーマ
- 視覚の情報だけに依存しない制御方法の提唱

## 結論
- 視覚以外の手段を使って制御することはできた


## 比較
### 内容
- 処理時間
- 停止回数

### 環境
- 十字路
- T字路

### 状況
- 同じ方向から多く来る場合
- 全体的に来る場合

### システム
- 時間順
- 時間順 + 同方向優先(改善案)
- 信号
# WikiGolf

## 概要

WikiGolfは、あるWikipediaページから別のページへの「意味的に最も近い」経路を見つけるためのPythonスクリプトです。

一般的な最短経路探索とは異なり、このツールは[Word2Vec](https://radimrehurek.com/gensim/models/word2vec.html)モデルを利用して、各ページのリンクの中からゴールページと意味的に最も関連性の高いリンクを優先的にたどります。これにより、単にクリック数が少ないだけでなく、内容的に関連の深い経路を発見することを目指します。

このプロジェクトは、いわゆる「ウィキゴルフ」や「ウィキレーシング」を、計算言語学的なアプローチで解く試みです。

## 特徴

- 日本語のWikipediaに対応
- Word2Vecによる意味的類似度に基づいた経路探索
- 探索の深さや一度に考慮するリンク数を調整可能

## 動作要件

- Python 3.x
- 必要なライブラリ (詳細は `requirements.txt` を参照)
- 日本語Word2Vecモデル

## セットアップ

1.  **リポジトリをクローンします。**
    ```bash
    git clone https://github.com/YOUR_USERNAME/WikiGolf.git
    cd WikiGolf
    ```

2.  **必要なPythonライブラリをインストールします。**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Word2Vecモデルをダウンロードします。**

    このプロジェクトでは、WikiEntVecで公開されている日本語Wikipediaの学習済みモデルを使用します。

    -   上記リポジトリから、`jawiki.all_vectors.100d.txt.bz2` などのモデルファイルをダウンロードしてください。
    -   ダウンロードしたファイルを解凍します (例: `bzip2 -d jawiki.all_vectors.100d.txt.bz2`)。
    -   解凍してできた `.txt` ファイルを、このプロジェクトのディレクトリ内に配置するか、任意の場所に置いてください。

4.  **スクリプト内のモデルパスを編集します。**

    `WikiGolf_ja.py` を開き、`model_path` の値を、ステップ3で配置したモデルファイルの実際のパスに書き換えてください。

    ```python
    # WikiGolf_ja.py の main() 関数内
    model_path = r'C:\path\to\your\jawiki.all_vectors.100d.txt'
    ```

## 使い方

1.  ターミナルでスクリプトを実行します。
    ```bash
    python WikiGolf_ja.py
    ```

2.  プロンプトに従って、Wikipedia APIのユーザーエージェントとして使用するメールアドレスを入力します。

3.  「Startページ」と「Goalページ」のタイトルをそれぞれ入力します。

### 実行例
```
ユーザーエージェント用のメールアドレスを入力してください: your.email@example.com
モデルを読み込んでいます... (これには数分かかる場合があります)
モデルの読み込みが完了しました。

Startページを入力してください (終了するにはEnterキーのみ): 量子力学
Goalページを入力してください: 相対性理論

探索開始: 量子力学 -> 相対性理論
探索中 (深さ 1): 量子力学
探索中 (深さ 2): 物理学
ゴールに到達しました！ ステップ数: 2

--- 発見した経路 ---
量子力学 → 物理学 → 相対性理論
--------------------
```

## ライセンス

### ソースコード
このプロジェクトのソースコードは MIT License の下で公開されています。

### Word2Vecモデル
このプロジェクトで使用しているWord2Vecモデルは、WikiEntVec プロジェクトによって作成されたものであり、Creative Commons Attribution-ShareAlike 3.0 ライセンスの下で提供されています。モデルの利用にあたっては、このライセンス条項に従ってください。

## 謝辞

素晴らしい日本語Word2Vecモデルを公開してくださっている WikiEntVec の開発者様に感謝申し上げます。
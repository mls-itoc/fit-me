FitMe
=====

## Getting Started

#### 前提条件

pythonの3.4以上とpipがインストールされていること

memo: pyenvの入れ方
```
$ brew install pyenv
```

#### パッケージインストール

pipから必要なパッケージをインストールします

```
pip install requests
pip install pyquery
```

## 学習データ作成

```
python scripts/scraping.py
```

ml_data.csvが作成されます

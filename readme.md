# proto

自分が使うためのライブラリ

# eda.py

探索的データ分析（EDA : Exploratory Data Analysis）のためのライブラリ。テーブルデータの操作と可視化（pandas, matplotlib, seaborn)

## 初期化
```
import eda

eda.init("plots")  # プロットのサブフォルダ
```

## 主な関数

- 欠損値と要約統計量の確認

```
eda.describe(df)
```

- プロットを整形して保存

```
eda.plot(df.plot()
        ,tl="タイトル", xl="Xラベル", yl="Yラベル")
```


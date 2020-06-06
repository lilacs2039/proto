# EDA : Exploratory Data Analysis

import gc
from tqdm import tqdm
import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display


save_dir = "./output"  # プロットの自動保存ディレクトリ


def init(sub_dir=""):
    # --------------  グラフサイズ設定パラメータ  -----------------------
    size_inch, size_px = 15, 2000  #15, 2000が基本。(15,800)も可能（保存したグラフは見切れる）　　colabは、グラフの横幅[px]が画面の横幅[px]を超えると縮小表示、満たないときはそのままグラフ表示する。

    # 横幅（インチ）を指定したときに、指定pxとなるようなDPIを計算。
    # Jupyter表示時はインチ単位指定だが、ファイル保存時はpx単位になるため。
    _h_inch = size_inch * 9/16
    _dpi = int(size_px / size_inch)
    _fontsize = size_inch * 2  # 15インチ・2kpxなら30px, 5インチ・2kpxなら10px　でちょうどよかった。
    # グラフのデフォルト設定。 ↑と同一セルだと初期化がうまくいかなかった。
    sns.set_style(style="whitegrid")
    plt.rcParams.update({
      'font.size' : _fontsize
      ,'font.family' : 'Meiryo' if os.name == 'nt' else ''  # Colabでは日本語フォントがインストールされてないので注意
      ,'figure.figsize' : [size_inch, _h_inch]  #[20.0, 10.0]
      ,'figure.dpi' : _dpi  #300
      ,'savefig.dpi' : _dpi
      ,'figure.titlesize' : 'large'
      ,'legend.fontsize' : 'small'
      ,'axes.labelsize' : 'medium'
      ,'xtick.labelsize' : 'small'
      ,'ytick.labelsize' : 'small'
      })
    global save_dir
    save_dir = (Path(save_dir)/sub_dir).resolve()

def describe(df):
    "DataFrameの要約統計量と欠損値など"
    print("データ形式")
    data = df.head(1).copy()
    dtype_row = data.dtypes
    if(len(data.index.names)>=2): dtype_row.name = tuple(["dtype"] * len(data.index.names))
    else: dtype_row.name = "dtype"
    data = data.append(dtype_row)
    display(data)
    def my_describe(_df):
        smry = _df.describe()
        smry.loc["欠損数"] = _df.isna().sum()
        smry.loc["欠損率"] = smry.loc["欠損数"] / df.index.size * 100
        display(smry.round(3))

    if df.select_dtypes('number').columns.size !=0:
        print("要約統計量（数値）")
        my_describe(df.select_dtypes('number'))
    if df.select_dtypes(exclude='number').columns.size !=0:
        print("要約統計量（数値以外）")
        my_describe(df.select_dtypes(exclude='number'))


        
        
        
        
def plot(ax_grid, tl=None, xl=None, yl=None, xtl=None, savename=None, ld_out=False):
    """
    パワーポイント用のグラフの生成

    Note:figsizeとtitleのy位置について
    figsizeの指定の仕方によってtitle位置の設定のされ方が違う
    figsizeをsns.jointplot(height=15)のように指定するなら、「, y=1.02」を追加
      seabornはfigsize指定がpltとは別になっているのでheightパラメータを使う。
      https://qiita.com/nj_ryoo0/items/9105ddfdf1b08b58398e
    """
    fig=None
    if isinstance(ax_grid, plt.Axes):
        # seabornのAxesレベル関数か、pyplotで生成したグラフの場合
        ax = ax_grid
        fig = ax.figure
        if tl is not None : ax.set_title(tl)
        if xl is not None : ax.set_xlabel(xl)
        if yl is not None : ax.set_ylabel(yl)
        if xtl is not None : ax.set(xtickLabels = xtl)
        if ld_out : ax.legend(loc="upper left", bbox_to_anchor=(1,1))  # 凡例をグラフ枠の外側へ配置
    elif isinstance(ax_grid,  (sns.FacetGrid, sns.PairGrid, sns.JointGrid, sns.pairplot, sns.jointplot)):
        # seaborn のfigureレベル関数で生成したグラフの場合
        g = ax_grid
        fig = g.fig
        # g.fig.set_figheight(size_inch);  g.fig.set_figwidth(size_inch)  # figsizeの修正。あとから修正すると余白やタイトル位置が変になるので、面倒だがグラフ生成のたびにheightで指定することにした。
        if tl is not None : 
            # タイトルを追加するときは、そのまま追加するとファイル保存したときにタイトルが見切れるので、
            # グラフを縦に90%に縮めてタイトルを設置
            g.fig.subplots_adjust(top=0.9)
            g.fig.suptitle(tl)  #, y=1.02
        ax = g.fig.axes[0] #Gridに対しては、最初のAxesにだけラベル名変更などの操作をする
        if xl is not None : ax.set_xlabel(xl)
        if yl is not None : ax.set_ylabel(yl)
        if xtl is not None : ax.set(xtickLabels = xtl)
        if ld_out : ax.legend(loc="upper left", bbox_to_anchor=(1,1))  # 凡例をグラフ枠の外側へ配置
    # save figure
    p = Path(save_dir); p.mkdir(parents=True, exist_ok=True)
    if savename is not None : fig.savefig(savepath(savename))
    elif tl is not None : fig.savefig(savepath(tl))

def savepath(filename):
    _suffix = ""
    if Path(filename).suffix == '' : _suffix = ".png"
    p = Path(save_dir)/f"{filename}{_suffix}"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p.resolve()




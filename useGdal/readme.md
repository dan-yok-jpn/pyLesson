
## QGIS に含まれる Python を用いる仮想環境

### 概　要

サブディレクトリの構成は以下となっている。

- [basic](basic/readme.md) -- 基本的な地理データの操作
- [census2015](census2015/readme.md) -- 流域内人口の計数
- [tile_2_DEM](tile_2_DEM/readme.md) -- 標高タイルから水平解像度 5m の DEM を GeoTiff 形式で出力

これらでは、QGIS に含まれている Python を用いた仮想環境下で osgeo パッケージをインポートしている。
osgeo は Python から [GDAL/OGR](https://gdal.org/index.html) 
の DLL を呼び出すための外部モジュールである。

なお、仮想環境を用いずに、別途、
GDAL を[インストール](https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal)することも可能ではあるが、
Python のバージョンや CPU に依存するものとなっており、
後日の管理が面倒になるので不適当である。

### 仮想環境の作成

仮想環境の作成はそれぞれのディレクトリ内の ```set_venv.bat``` を実行することで自動化している。
実行後には ```.venv``` と ```.vscode``` の 2 つのディレクトリが新たに作成される。

ただし、オリジナルの ```set_venv.bat``` の 3 行目、4 行目は著者の実行環境に合わせて以下となっている。
```%PYTHON%``` が存在しない場合にはエラーメッセージを出力して実行が停止するので、
自分の環境に応じて ```%OSGEO_ROOT%``` と ```%PYTHON%``` を変更することが必要である。

```
set OSGEO_ROOT=C:\OSGeo4W
set PYTHON=%OSGEO_ROOT%\apps\Python39\python.exe
```

例えば、```C:\Program Files\QGIS 3.20``` 以下の ```python.exe```
を用いる場合は次のように変更する必要がある。

```
set OSGEO_ROOT="C:\Program Files\QGIS 3.20"
set PYTHON=%OSGEO_ROOT%\apps\Python39\python.exe
```

また、QGIS のバージョンアップやディレクトリの移動・名前の変更などを行った場合は、
再度 ```set_venv.bat``` を実行して、
仮想環境を作り直す必要がある。

あるいは、pip で SSL 通信のエラーが発生する場合は、
```C:\Windows\System32\DriverStore\FileRepository\iclsclient.inf_amd64_75ffca5eec865b4b\lib```
にある ```libssl-1_1-x64.dll``` と ```libcrypto-1_1-x64.dll``` を
```%OSGEO_ROOT%\apps\Python39\DLLs``` にコピーする。

### osgeeo のインポート

```.venv\Lib\site-packages``` には GDAL/OGR が用いる環境変数と DLL のサーチパスを設定する
```gdal_env.py``` が配置される。
```osgeo``` をインポートする前に必ずこれをインポートする必要がある。

```Python
from gdal_env import gdal_env
gdal_env()
from osgeo import gdal, ogr, osr
```

### 仮想環境下でのプログラムの実行

VSCode 内で操作する場合は自動的に仮想環境下で実行する設定となっているが、
コマンドラインから実行する場合は以下の操作が必要である。

```bash
$ .venv\Scripts\activate.bat
(.venv) $ python -m foo.py [option]
(.venv) $ deactivate
$
``` 

### 補　遺

- ```tile_2_DEM``` とそれ以外のディレクトリで ```set_venv.bat``` の内容が若干異なっている。
具体的には、前者では新たな外部パッケージをインストールしているのに対して、
後者では既にインストールされているパッケージのみを用いている。
これに対応して、前者では

  ```bash
  # python -m venv --system-site-packages --symlinks --clear --upgrade-deps .venv
  $ .venv\Scripts\activate.bat
  (.venv) $ pip install -r requirements.txt
  ```

  が実行される。```requirements.txt``` には追加するパッケージ名が列挙されている。
  一方、後者では

  ```bash
  # python -m venv --system-site-packages --symlinks --without-pip --clear .venv
  ```

  が実行される。

### 関連サイト

- [Python GDAL/OGR Cookbook 1.0 documentation](https://pcjericks.github.io/py-gdalogr-cookbook/)
- [GDAL/OGR Python API](https://gdal.org/python/index.html)
- [Python3×地理空間データ　地理空間データプログラミングの流れ](https://ujicya.jp/blog-mapping/workflow-of-python-geospatial-development/)
- [Python3×地理空間データ　GDAL Python API 【未完】](https://ujicya.jp/blog-mapping/python-gdal-api/)
- [Anaconda環境でのSSLモジュールエラーの解決方法](https://qiita.com/moo046/items/a6454adf140263f2df8a)

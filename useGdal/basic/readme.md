# useGdal

仮想環境を設けて OSGeo4W ないし QGIS にバンドルされている osgeo パッケージを利用する事例

## DEMO

```ex1_useGdal.py``` で作成される 2 つのポリゴン

![](img/snap_qgis.png)

## Features

### 何故、仮想環境上で実行するか

仮想環境で実行する理由は下記の３点

- osgeo の使用頻度は高くない
- osgeo の内部で大量の dll （ [GDAL/OGR](https://gdal.org/index.html) の本体）
をインポートしているので Python の版毎にこれをインストールするのは好ましくない。
- OSGeo4W 内のライブラリであれば動作の安定が保障されている。

３点目に関しては、pip によるインストールが失敗するケースがある、との
[報告](https://hacker.trickstorm.com/?p=988)もある。


### 環境構築の自動化

```Make_Gdal_App_Env.bat``` は仮想環境の作成と VSCode 向けの設定を自動化したものである。
これを実行した後のファイル構成は以下の通りで、
```.venv\Scripts``` 下の ```activate*``` と ```deactivate.bat```
以外はすべてシンボリックリンクとなっている。
また、```.venv\Lib\site-packages``` には ```osgeo```
で用いる環境変数を設定する ```gdal_env.py``` を配置している。
```
useGdal
|   ex1_useGdal.py
|   ex2_useGdal.py
|   Make_Gdal_App_Env.bat
|   readme.md
|   tmp.bat
|   
+---.venv
|   |   pyvenv.cfg
|   |   
|   +---Include
|   +---Lib
|   |   \---site-packages
|   |           gdal_env.py
|   |           
|   \---Scripts
|           activate
|           activate.bat
|           Activate.ps1
|           deactivate.bat
|           python.exe
|           python3.dll
|           python3.exe
|           python39.dll
|           pythonw.exe
|           pythonw3.exe
|           
+---.vscode
        launch.json
        settings.json
```

## Requirement

- OSGeo4W or QGIS
- libcrypto-1_1-x64.dll、libssl-1_1-x64.dll
  - pip が正常動作するために必要。
    C:\Windows\System32\DriverStore\FileRepository\iclsclient.inf_amd64_75ffca5eec865b4b\lib
    にあるこれらを C:\OSGeo4W\apps\Python39\DLLs にコピー

## Installation

osgeo パッケージを利用するモジュールがあるフォルダで以下をタイプして
```.venv\*``` と ```.vscode\*``` を作成する。
途中で管理者に昇格するためのダイヤログが表示される。

```bash
$ Make_Gdal_App_Env
```

## Usage

ベクターデータ用のライブラリ ogr を利用する簡単な例として２つのモジュールを示した。

```bash
$ .venv\Scripts\activate
(.venv) $ python ex1_useGdal.py
(.venv) $ python ex2_useGdal.py poly4.json
(.venv) $ deactivate
$
```

何れのモジュールでも ogr のインポートは以下のコードで行っている。

```Python
from gdal_env import gdal_env
gdal_env()
from osgeo import ogr
```

- ex1_useGdal.py では簡単な図形の地理演算（Intersection、Union）の結果を geoJSON で出力している（前出の図）。
- ex2_useGdal.py では上記の geoJSON を読み込んで座標を出力している。

  ```
  (.venv) $ python ex2_useGdal.py poly4.json
  feature[0]
          type : Polygon
          codinates[0] :  137.0   37.0
          codinates[1] :  137.0   36.0
          codinates[2] :  135.0   36.0
          codinates[3] :  135.0   38.0
          codinates[4] :  136.0   38.0
          codinates[5] :  136.0   39.0
          codinates[6] :  138.0   39.0
          codinates[7] :  138.0   37.0
          codinates[8] :  137.0   37.0
  ```

## Note

- ```Make_Gdal_App_Env.bat``` ではトップディレクトリが C:\OSGeo4W であることを想定している。

  ```
  set EXE=C:\OSGeo4W\apps\Python39\python.exe
  ```

  これと異なる場合は書き換える必要がある。例えば

  ```
  set EXE="C:\Program Files\QGIS 3.20\apps\Python39\python.exe"
  ```
- venv の引数は最小構成の仮想環境とするため以下としている。

  - ```--system-site-packages```：OSGE4W のサイトパッケージを使用
  - ```--symlinks```：.venv/Scripts/python.exe はシンボリックリンク
  - ```--clear```：.venv が既存の場合は初期化した後に仮想環境を構築
  - ```--without-pip```：.veenv/Scripts に pip を含めない。.venv/Lib/site-packages は空

- Python の仕様変更に対応
    - On Windows, with Python >= 3.8, DLLs are no longer imported from the PATH.
If gdalXXX.dll is in the PATH, then set the USE_PATH_FOR_GDAL_PYTHON=YES environment variable
to feed the PATH into os.add_dll_directory().

## Reference

- [Python GDAL/OGR Cookbook 1.0 documentation](https://pcjericks.github.io/py-gdalogr-cookbook/)
- [GDAL/OGR Python API](https://gdal.org/python/index.html)
- [Python3×地理空間データ　地理空間データプログラミングの流れ](https://ujicya.jp/blog-mapping/workflow-of-python-geospatial-development/)
- [Python3×地理空間データ　GDAL Python API 【未完】](https://ujicya.jp/blog-mapping/python-gdal-api/)
- [Anaconda環境でのSSLモジュールエラーの解決方法](https://qiita.com/moo046/items/a6454adf140263f2df8a)

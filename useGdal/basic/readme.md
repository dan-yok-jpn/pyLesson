# basic

仮想環境内で osgeo パッケージを利用する基本的な事例

## DEMO

```ex1_useGdal.py``` で作成される 2 つのポリゴン

![](img/snap_qgis.png)


## Install

```bash
$ set_venv.bat
```

- 何らかのエラーが発生する場合は、
```set_env.bat``` の内容を[チェック](../readme.md#%E4%BB%AE%E6%83%B3%E7%92%B0%E5%A2%83%E3%81%AE%E4%BD%9C%E6%88%90)する。

## Usage

```bash
(.venv) $ python ex1_useGdal.py
(.venv) $ python ex2_useGdal.py poly4.json
```

- 
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

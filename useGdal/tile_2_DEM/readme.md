
# tile_2_DEM

国土地理院が配信している[標高タイル](https://maps.gsi.go.jp/development/ichiran.html#dem)から空間解像度 5m の DEM を Geotiff 形式で作成する。

![](img/mkDem.PNG)

## Requirement

* python3
* osgeo パッケージ
* tqdm パッケージ

## Installation

set_venv.bat で仮想環境を作成する。

```bash
$ set_venv.bat
```

- 何らかのエラーが発生する場合は
```set_env.bat``` の内容を[チェック](../readme.md#%E4%BB%AE%E6%83%B3%E7%92%B0%E5%A2%83%E3%81%AE%E4%BD%9C%E6%88%90)する。

## Usage

```bash
 python tile_2_DEM.py [(-h|--help)] (lat_sw lng_sw lat_ne lng_ne | poly) [output]

   lat_sw : 南西端の緯度（度）
   lng_sw : 南西端の経度（度）
   lat_ne : 北東端の緯度（度）
   lng_ne : 北東端の経度（度）
   poly   : バウンドボックスを取得する GIS データ（GeoJSON, WGS84）
   output : 出力ファイル名. 無指定の場合は 'dem.tif'
```

## Sample

1. 仮想環境を有効化する。

    ```bash
    $ .venv\Scripts\activate.bat
    ```

2. bbox.html を起動して DEM を作成する区画を設定する。
右上のボタンをクリックすると南西端と北東端の緯度経度が表示される。

    ![](img/bbox.PNG)

3. 上記の緯度経度をクリップボードにコビーして下記のコマンドを実行する

    ```bash
    (.venv) $ python tile_2_DEM.py 35.3538601 139.1604541 35.2705697 139.0023191

    100%|███████████████████████████████████████████████████████████████████████████████████████| 150/150 [00:31<00:00,  4.70it/s] 

    (.venv) $ colorrelief.bat
    Computing source raster statistics...
    0...10...20...30...40...50...60...70...80...90...100 - done.

    (.venv) $ deactivate
    $
    ```
4. 結果（colorrelief.png）を確認する（冒頭の図）。

- 次のコマンドでも同様の結果が得られる。

    ```bash
    $ python sample.json
    ```

## Reference

* Pythonで国土地理院のDEM5A標高タイルからGeoTiffを作成
https://tm23forest.com/contents/python-gdal-cyberjapandata-dem5tile
* 地図タイルと標高タイルの関係について
https://maps.gsi.go.jp/development/demtile.html
* 標高タイルの作成方法と地理院地図で表示される標高値について
https://maps.gsi.go.jp/development/hyokochi.html
* 座標の変換（世界座標、ピクセル座標、タイル座標、緯度・経度）
https://www.trail-note.net/tech/coordinate/

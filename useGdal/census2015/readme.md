### census2015

#### 概　要
- QGIS 同梱の Python の地理分析パッケージを利用して
流域界の GIS データ<small><sup>※</sup></small>から流域内の総人口を求める

  ![](../img/mesh.png)

  <small>※ <span style="color:red;">地理座標で作った GroJSON 限定<span></small>

- そもそも QGIS をインストールした段階で Python がインストールされている
（実は QGIS のユーザーは既に Python が使える状態にあった）
- この Python には QGIS が使用するダイナミック・リンク・ライブラリ（```GDAL``` という）を呼び出す
パッケージが含まれている
- GDAL は容量が大きいので Python で使用するため（だけ）に複数インストールするのは NG。
- こういう時こそ仮想環境

#### 準 備（1）
- 必要であれば<small><sup>※</sup></small>、```Make_Gdal_App_Env.bat``` の「```set OSGEO_ROOT=C:\OSGeo4W64```」を変更。
<br>例えば QGIS のバージョンが 3.12 の場合は

  ```sh
  set OSGEO_ROOT=C:\Progra~1\QGIS3~1.12
  ```
  <small>※ QGIS のインストーラにより Python.exe の在処が違う</small>

- 作業フォルダで以下を実行して仮想環境を作る
  ```sh
  Make_Gdal_App_Env
  ```
- 以後、仮想環境下で作業
  ```sh
  .venv\Scripts\activate
  ```

#### 準 備（2）
- 流域界の GIS データ（hoge.json）を用意する
- 同封の meshes.py を実行して第一次地域区画（80km 四方）のコードを列挙する

  ```sh
  python meshes.py -1 hoge.json
  ```
- [このサイト](https://www.e-stat.go.jp/gis/statmap-search?page=1&type=1&toukeiCode=00200521&toukeiYear=2015&aggregateUnit=Q&serveyId=Q002005112015&statsId=T000876)で都道府県の絞り込みをかけて上記の区画のデータを全てダウンロードする
- 再度、meshes.py を実行して第五次地域区画（250m 四方）のコードを列挙する
  ```sh
  python meshes.py -5 -g hoge.json
  ```

- 直前のコマンドの「```-g```」オプションは流域内の区画の GIS データを出力（必須ではない）
- ```meshes.py``` の中で前記のパッケージを使った地理演算を行っている。
具体的には流域界のエンベロープ（対角頂点が南西端・北東端の矩形）
内の全ての地域区画の内、流域内に含まれるものを抽出している。
- 抽出された区画のメッシュコードは ```sqlite3``` のデータベース（```temp.db```）
の mesh5 テーブルに出力される。
```sqlite3``` は Python に標準装備されている。

#### 仕上げ

- 次のコマンドで流域内の総人口を求める

  ```sh
  (.venv) % python census2015.py

  Population : 95,409
  ```
- 仮想環境で作業を続ける必要がなければ次のコマンドで仮想環境から抜ける

  ```sh
  (.venv) % .venv\Scripts\deactivate
  %
  ```

- ダウンロードした[国勢調査のデータ](https://www.e-stat.go.jp/help/data-definition-information/shuroku/T000876.pdf)
（zip ファイル）は ```pandas``` で読み込み
```temp.db``` の ```population``` テーブルに書き出している。
QGIS の Python には ```pandas``` もインストールされている
- 流域内の総人口を求める SQL は以下で単純至極
  ```SQL
  SELECT SUM(population) FROM mesh5 JOIN population
  ON mesh5.code = population.code
  ```
- 求めた人口を転記したならば ```temp.db``` を保存しておく必要はない

#### 補　遺
- ```census2015.py``` は 2015 年の国勢調査の第五次区画内の人口総数に特化したものとなっている
- 国の統計データの多くは地域区画毎で提供されているので
使用するデータに合わせてこのモジュールを書き換えれば他でも使用できる
- この際、```meshes.py``` の「-数字」オプションにはデータに対応する地域区画のオーダーを与える
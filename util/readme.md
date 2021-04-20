## Python を使用する際の設定

* mkPyProj.bat - Visual Studio のスタートアップファイル（Python 用）の生成
```sh
% dir /b *.py*
% foo.py
% mkPyProj foo
% mkPyProj bar
% dir /b *.py*
bar.py // print('Hello World')
bar.pyproj
foo.py
foo.pyproj
% foo.pyproj // Visual Studio 起動
```
* setupVSCode.bat - Visual Studio Code で QGIS 同梱の Python の編集・実行・デバッグを行うための環境設定
```sh
% setupVSCode // %APPDATA%\Code\User に settings.json と launch.json を配置
```
* setenv.cmd - コマンドプロンプトで QGIS 同梱の Python を起動するための環境設定
```sh
% setenv
% python --version
Python 3.7.0
```
* subst.bat - 文字列の置換（setupVSCode で使用）
```sh
% type foo.txt
bar baz
% subst foo.txt b v
var vaz
```

## その他

* showClip.bat - クリップボード内のテキストの出力

　　　![xls](img/xls_snap.png)
<br>　　　　　　　　　　　　　　↓<br>
　　　![xls](img/showClip.png)
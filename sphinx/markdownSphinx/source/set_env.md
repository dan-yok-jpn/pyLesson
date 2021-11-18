# 環境設定からビルドまで

## 仮想環境の作成

トップ・ディレクトリ（ここでは、「`sphinx`」とする）で下記のバッチファイル（`set_venv.bat`）を実行して `Sphinx` 専用の仮想環境を作成する。 

```doscon
@echo off
setlocal

set PYTHONHOME=C:\Progra~2\micros~4\shared\Python37_64
set PATH=%PYTHONHOME%;%PYTHONHOME%\DLLs;%PYTHONHOME%\Scripts;%PATH%
call :genBat > tmp.bat
powershell Start-Process tmp.bat -Verb runas -Wait
del tmp.bat
pip install -r requirements.txt -t .venv\Lib\site-packages 1>nul 2>nul
goto :eof

:genBat
    echo @echo off
    echo cd "%~dp0"
    echo "%PYTHONHOME%\python" -m venv --system-site-packages --symlinks --without-pip --clear .venv
    exit /b
```

`requirements.txt` は次の通りである。
[myst-parser](https://myst-parser.readthedocs.io/en/latest/) が `Markdown` を使用するための拡張パッケージとなっている。1st. commit が 2 年前で v0.15.2。日本語のアンチョコなし。
`sphinx_rtd_theme` はサイトの外観。

```
sphinx
myst-parser
sphinx_rtd_theme
```

## 自動生成ファイルの編集

トップ・ディレクトリ以下の最終的なフォルダーの構成は次のようになる。

```
sphinx
│  .venv  ............ Python と requirements.txt で指定したライブラリはここにある
│  .vscode  .......... 本文では説明を省いているが VSCode 内で作業が完結するようにしてある
|  set_venv.bat
|  requirements.txt
└─ markdownSpinx
    |
    │  make.bat
    │  Makefile
    │  
    ├─build
    │  ├─doctrees
    │  └─html
    │                  
    └─source
        │  conf.py
        │  index.md  ............ index..rst の代替
        │  set_env.md  .......... 新規作成
        │  markdown.md  ......... 新規作成
        │  
        ├─_static
        └─_templates
```

先ず、`.venv\Lib\site-packages\bin\sphinx-quickstart.exe` を実行してワーク・ディレクトリ（ここでは「`markdownSpinx`」とする）以下にビルドに必要な既定のディレクトリとファイルを作成する。
ここでの応答は `conf.py` に反映されるので必要であれば後で変更すれば良い。

```doscon
sphinx> mkdir markdownSphinx
sphinx> cd markdownSphinx
markdownSphinx> ..\.venv\Lib\site-packages\bin\sphinx-quickstart.exe
```

次に、生成された `make.bat`、`index.md`、および `conf.py` に以下の変更を加えて `Markdown` が適用できるようにした。

### make.bat

冒頭で `sphinx-build.exe` の絶対パスを `SPHINXBUILD` 環境変数にセットする。

```doscon
set SPHINXBUILD=<path_to_sphinx>\.venv\Lib\site-packages\bin\sphinx-build.exe
```

### index.md

`index.rst` を `index.md` にリネームして書き下ろしの文書ファイル `set_env.md`、`markdown.md` を目次を加えるため次のように記述。

````md
```{toctree}
set_env.md
markdown.md
```
````

### conf.py

変更点は次の 3 箇所である。

* `PYTHONPATH` を追加
* `myst_parser` を `extensions` に追加
* テーマを今回インストールした `sphinx_rtd_theme` に変更

```Python
import os
import sys
sys.path.append(r"<path_to_sphinx>\.venv\Lib\site-packages")
project = 'MarkdownSphinx'
copyright = '2021, T.Dan'
author = 'T.Dan'
extensions = ['myst_parser']
templates_path = ['_templates']
language = 'ja'
exclude_patterns = []
html_static_path = ['_static']
import sphinx_rtd_theme
html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
```

## ビルド

仮想環境下で `make html` を実行すると `build/html` に 5 種の `html` ファイルが作成される。

```doscon
sphinx> .venv\Scripts\activate
(.venv) sphinx> cd markdownSphinx
(.venv) markdownSphinx> make html
Sphinx v4.4.0+ を実行中
翻訳カタログをロードしています [ja]... 完了
出力先ディレクトリを作成しています... 完了
myst v0.15.2: MdParserConfig(renderer='sphinx', commonmark_only=False, enable_extensions=['dollarmath'], dmath_allow_labels=True, dmath_allow_space=True, dmath_allow_digits=True, dmath_double_inline=False, update_mathjax=True, mathjax_classes='tex2jax_process|mathjax_process|math|output_area', disable_syntax=[], url_schemes=['http', 'https', 'mailto', 'ftp'], heading_anchors=None, 
heading_slug_func=None, html_meta=[], footnote_transition=True, substitutions=[], sub_delimiters=['{', '}'], words_per_minute=200)
ビルド中 [mo]: 更新された 0 件のpoファイル
ビルド中 [html]: 更新された 3 件のソースファイル
環境データを更新中[新しい設定] 3 件追加, 0 件更新, 0 件削除
ソースを読み込み中...[100%] set_env
更新されたファイルを探しています... 見つかりませんでした
環境データを保存中... 完了
整合性をチェック中... 完了
ドキュメントの出力準備中... 完了
出力中...[100%] set_env
索引を生成中... genindex 完了
追加のページを出力中... search 完了
画像をコピー中... [100%] img/logo-wide.svg
静的ファイルをコピー中... 完了
extraファイルをコピー中... 完了
Japanese (code: ja) の検索インデックスを出力... 完了
オブジェクト インベントリを出力... 完了
ビルド 成功.

HTMLページはbuild\htmlにあります。

(.venv) markdownSphinx>
```
# 環境設定からビルドまで

## 仮想環境の作成

トップ・ディレクトリで下記のバッチファイルを実行して ```Sphinx``` 専用の仮想環境を作成した。 

```
@echo off
setlocal

set PYTHONHOME=C:\Progra~2\micros~4\shared\Python37_64
set PATH=%PYTHONHOME%;%PYTHONHOME%\DLLs;%PYTHONHOME%\Scripts;%PATH%
call :genBat    > tmp.bat
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

```requirements.txt``` は次の通りである。
[myst-parser](https://myst-parser.readthedocs.io/en/latest/) が ```Markdown``` を使用するための拡張パッケージとなっている。1st. commit が 2 年前で v0.15.2。日本語のアンチョコなし。

```
sphinx
myst-parser
sphinx_rtd_theme
```

## 自動生成ファイルの編集

最終的なフォルダーの構成は次のようになる。```document_root``` 以下は ```.venv\Lib\site-packages\bin\sphinx-quickstart.exe``` で自動的に生成される既定のファイルを編集して ```Markdown``` が適用できるようにした。

```
sphinx
|  set_venv.bat
|  requirements.txt
│  .venv
└─ document_root
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
        │  index.md
        │  set_env.md
        │  markdown.md
        │  
        ├─_static
        └─_templates
```

### make.bat

冒頭で ```sphinx-build.exe``` の絶対パスを ```SPHINXBUILD``` 環境変数にセットした。

```
set SPHINXBUILD=<path_to_sphinx>\.venv\Lib\site-packages\bin\sphinx-build.exe
```

### index.md

```index.rst``` は ```index.md``` にリネームして ```set_env.md```、```markdown.md``` の目次を作成する命令を記述。

```
```{toctree}
set_env.md
markdown.md
```

### source/conf.py

変更点は次の 2 箇所である。

* ```PYTHONPATH``` を追加
* ```myst_parser``` を ```extensions``` に追加

```Python
import os
import sys
sys.path.append(r"<path_to_sphinx>\.venv\Lib\site-packages")
project = 'test'
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

```make html``` で ```build/html``` に 3 種の ```html``` ファイルが作成される。

```
% .venv\Scripts\activate
(.venv) % cd document_root
(.venv) % make html
Sphinx v4.4.0+ を実行中
翻訳カタログをロードしています [ja]... 完了
保存された環境データを読み込み中... 完了
myst v0.15.2: MdParserConfig(renderer='sphinx', commonmark_only=False, enable_extensions=['dollarmath'], dmath_allow_labels=True, dmath_allow_space=True, dmath_allow_digits=True, dmath_double_inline=False, update_mathjax=True, mathjax_classes='tex2jax_process|mathjax_process|math|output_area', disable_syntax=[], url_schemes=['http', 'https', 'mailto', 'ftp'], heading_anchors=None, heading_slug_func=None, html_meta=[], footnote_transition=True, substitutions=[], sub_delimiters=['{', '}'], words_per_minute=200)
ビルド中 [mo]: 更新された 0 件のpoファイル
ビルド中 [html]: 更新された 1 件のソースファイル
環境データを更新中0 件追加, 1 件更新, 0 件削除
ソースを読み込み中...[100%] index
更新されたファイルを探しています... 見つかりませんでした
環境データを保存中... 完了
整合性をチェック中... 完了
ドキュメントの出力準備中... 完了
出力中...[100%] index
索引を生成中... genindex 完了
追加のページを出力中... search 完了
静的ファイルをコピー中... 完了
extraファイルをコピー中... 完了
Japanese (code: ja) の検索インデックスを出力... 完了
オブジェクト インベントリを出力... 完了
ビルド 成功.

HTMLページはbuild\htmlにあります。

(.venv) %
```
# Markdown で Sphinx

Dr.Shimizu の「[現場のための水理学 令和版](https://i-ric.org/yasu/nbook2/index.html)」に触発されて久しぶりに `Sphinx` を使ってみた。
ただし、`reStructuredText` はすっかり忘れているので、以下に記すような設定を行って `Markdown`（正確には `Myst-Markdown`）で記述できるようにした。

```{toctree}
---
maxdepth: 2
---
set_env.md
markdown.md
```
* [索引](genindex)
* [検索](search)
#!/usr/bin/env python3
"""从 docs/projects.json 生成四个项目详情页（projects/p01.html ~ p04.html）。

用法：
    python docs/build_projects.py          # 生成页面
    python docs/build_projects.py --check  # 只校验：index.html 的数字是否与 JSON 一致

为什么要有这个脚本：
    项目详情页和首页都要展示同一批数字（行数、文件数、用例数、提交数）。
    两处手写必然漂移，所以数字只存 docs/projects.json 一份，页面由本脚本渲染。
    --check 模式进一步确认 index.html 里的数字也来自同一份数据。

数据口径见 docs/VERIFY.md。改数字只改 projects.json，然后重跑本脚本。
"""

from __future__ import annotations

import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "docs", "projects.json")
OUT_DIR = os.path.join(ROOT, "projects")
INDEX = os.path.join(ROOT, "index.html")

# 能力等级 → 圆点字符。与 index.html 里 03 节的矩阵保持同一套视觉语言。
DOT = {"core": "●", "part": "◐", "light": "○", "none": "–"}
LEVEL_TEXT = {
    "core": "主力实现",
    "part": "有实现，非重点",
    "light": "仅基础形态",
    "none": "未涉及",
}


def e(s: str) -> str:
    return html.escape(s, quote=True)


def fmt(n: int) -> str:
    """千分位，逗号单独包一层 .num-sep —— 与首页同一套处理。"""
    return re.sub(r"\B(?=(\d{3})+(?!\d))", r'<span class="num-sep">,</span>', f"{n:,}")


def render_nav(prefix: str, active: str = "") -> str:
    """项目页的导航。区块锚点在首页，项目页里指向 ../index.html#xxx。"""
    items = [
        ("matrix", "矩阵"),
        ("demo", "演示"),
        ("capability", "能力"),
        ("architecture", "架构"),
        ("evidence", "数字"),
        ("boundary", "边界"),
        ("about", "关于"),
        ("contact", "联系"),
    ]
    links = "\n".join(
        f'      <a class="nav__link" href="{prefix}index.html#{i}">{t}</a>'
        for i, t in items
    )
    return f"""<header class="nav" id="nav">
  <div class="wrap nav__inner">
    <a class="brand" href="{prefix}index.html" aria-label="王鑫鸿个人作品矩阵 · 回到首页">
      <span class="brand__mark" aria-hidden="true">WX</span>
      <span class="brand__text">
        <span class="brand__name">王鑫鸿 · 个人作品矩阵</span>
        <span class="brand__sub">Personal Work Matrix</span>
      </span>
    </a>

    <nav class="nav__links" aria-label="首页区块">
{links}
    </nav>

    <div class="nav__actions">
      <button class="icon-btn nav__toggle" id="menu-toggle" aria-label="打开菜单" aria-expanded="false" aria-controls="menu">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18" stroke-linecap="round"/></svg>
      </button>
      <button class="icon-btn" id="theme-toggle" aria-label="切换明暗主题" title="切换明暗主题">
        <svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M4.9 4.9l1.4 1.4m11.4 11.4 1.4 1.4M19.1 4.9l-1.4 1.4M6.3 17.7l-1.4 1.4" stroke-linecap="round"/></svg>
        <svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M20 14.5A8.5 8.5 0 1 1 9.5 4a6.8 6.8 0 0 0 10.5 10.5Z" stroke-linejoin="round"/></svg>
      </button>
      <a class="btn btn--sm" href="https://github.com/xinhongwang138-hue" target="_blank" rel="noopener">
        <svg viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8Z"/></svg>
        <span>GitHub</span>
      </a>
    </div>
  </div>
</header>

<div class="menu" id="menu">
  <a href="{prefix}index.html#matrix">01 · 作品矩阵</a>
  <a href="{prefix}index.html#demo">02 · 界面演示</a>
  <a href="{prefix}index.html#capability">03 · 能力矩阵</a>
  <a href="{prefix}index.html#architecture">04 · 架构主线</a>
  <a href="{prefix}index.html#evidence">05 · 可复核的数字</a>
  <a href="{prefix}index.html#boundary">06 · 已知边界</a>
  <a href="{prefix}index.html#about">07 · 关于</a>
</div>"""


def render_pipeline(pl: dict) -> str:
    lanes = []
    for lane in pl["lanes"]:
        nodes = []
        for i, nd in enumerate(lane["nodes"]):
            if i:
                nodes.append('<span class="pipe__arrow" aria-hidden="true"></span>')
            cls = "pipe__node pipe__node--key" if nd.get("key") else "pipe__node"
            nodes.append(
                f'<span class="{cls}"><b>{e(nd["b"])}</b><i>{e(nd["i"])}</i></span>'
            )
        tag = (
            f'<span class="pipe__tag">{e(lane["tag"])}</span>' if lane.get("tag") else ""
        )
        lanes.append(f'            <div class="pipe__line">{tag}\n              <div class="pipe__lane">\n                ' + "\n                ".join(nodes) + "\n              </div>\n            </div>"
        )
    return f"""<figure class="pipe{" pipe--lanes" if len(pl["lanes"]) > 1 else ""}" aria-label="{e(pl["aria"])}">
{chr(10).join(lanes)}
          <div class="pipe__note">{e(pl["note"])}</div>
        </figure>"""


def render_caps(caps: list) -> str:
    rows = []
    for c in caps:
        rows.append(
            f"""            <div class="pcap__row" data-level="{e(c["level"])}">
              <span class="pcap__dot" aria-hidden="true">{DOT[c["level"]]}</span>
              <span class="pcap__dim">{e(c["dim"])}</span>
              <span class="pcap__note">{e(c["note"])}</span>
              <span class="pcap__lv">{LEVEL_TEXT[c["level"]]}</span>
            </div>"""
        )
    return "\n".join(rows)


def render_bounds(bounds: list) -> str:
    out = []
    for i, b in enumerate(bounds, 1):
        out.append(
            f"""        <div class="bound">
          <div class="bound__n">{i:02d}</div>
          <div>
            <h3>{e(b["title"])}</h3>
            <p>{b["html"]}</p>
          </div>
        </div>"""
        )
    return "\n".join(out)


def render_page(p: dict, prev_p: dict, next_p: dict, site: dict) -> str:
    prefix = "../"
    shot = p["shot"]
    root = site["root"]

    facts = "\n".join(
        f"""          <div class="pfact">
            <span class="pfact__label">{e(f["label"])}</span>
            <span class="pfact__text">{f["html"]}</span>
          </div>"""
        for f in p["facts"]
    )

    tags = "\n".join(f'          <span class="tag">{e(t)}</span>' for t in p["tags"])

    needs = "\n".join(f'            <li>{e(n)}</li>' for n in p["needs"])

    prev_link = (
        f'<a class="pnav__link" href="{prefix}projects/{prev_p["id"]}.html">'
        f'<span class="pnav__dir">← 上一个</span>'
        f'<span class="pnav__name">{e(prev_p["no"])} · {e(prev_p["name"])}</span></a>'
        if prev_p
        else '<span class="pnav__link pnav__link--empty"></span>'
    )
    next_link = (
        f'<a class="pnav__link pnav__link--next" href="{prefix}projects/{next_p["id"]}.html">'
        f'<span class="pnav__dir">下一个 →</span>'
        f'<span class="pnav__name">{e(next_p["no"])} · {e(next_p["name"])}</span></a>'
        if next_p
        else '<span class="pnav__link pnav__link--empty"></span>'
    )

    return f"""<!DOCTYPE html>
<html lang="zh-CN" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(p["no"])} · {e(p["name"])} | 王鑫鸿 · 个人作品矩阵</title>
<meta name="description" content="{e(p["name"])}（{e(p["en"])}）：{e(p["summary"])} {p["loc"]:,} 行源码、{p["tests_note"]}。附架构链路、工程约束、已知边界与本地复现步骤。">
<meta name="author" content="{e(site["owner"])}">
<meta name="theme-color" content="#07090E">
<meta property="og:type" content="article">
<meta property="og:site_name" content="王鑫鸿 · 个人作品矩阵">
<meta property="og:title" content="{e(p["no"])} · {e(p["name"])} | 王鑫鸿 · 个人作品矩阵">
<meta property="og:description" content="{e(p["lead"])}">
<meta property="og:url" content="{root}projects/{p["id"]}.html">
<meta property="og:image" content="{root}assets/img/demo-{p["id"]}.webp">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{root}projects/{p["id"]}.html">
<link rel="icon" href="{prefix}assets/img/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{prefix}assets/css/tokens.css">
<link rel="stylesheet" href="{prefix}assets/css/app.css">
<link rel="stylesheet" href="{prefix}assets/css/project.css">
<script>
  // 首屏前定主题，避免闪白；同时标记 JS 可用，供入场动效做渐进增强
  (function () {{
    document.documentElement.classList.add("js");
    try {{
      var saved = localStorage.getItem("wxh-theme");
      var mql = window.matchMedia("(prefers-color-scheme: light)");
      var theme = saved || (mql.matches ? "light" : "dark");
      document.documentElement.setAttribute("data-theme", theme);
    }} catch (e) {{}}
  }})();
</script>
</head>
<body class="pbody">
<a class="skip-link" href="#main">跳到主要内容</a>

{render_nav(prefix)}

<main id="main">

  <!-- ============ 项目头 ============ -->
  <section class="phero">
    <div class="wrap">
      <nav class="pcrumb reveal" aria-label="面包屑">
        <a href="{prefix}index.html">作品矩阵</a>
        <span aria-hidden="true">/</span>
        <span aria-current="page">{e(p["no"])}</span>
      </nav>

      <div class="phero__grid">
        <div class="phero__main reveal">
          <div class="phero__id">
            <span class="phero__no">{e(p["no"])}</span>
            <span class="phero__en">{e(p["en"])}</span>
          </div>
          <h1>{e(p["name"])}</h1>
          <p class="phero__lead">{e(p["lead"])}</p>
          <div class="phero__tags">
{tags}
          </div>
          <div class="phero__actions">
            <a class="btn btn--primary" href="https://github.com/xinhongwang138-hue/{e(p["repo"])}" target="_blank" rel="noopener">
              查看仓库
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M7 17 17 7M8 7h9v9" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </a>
            <a class="btn" href="#pcap">看能力坐标</a>
            <a class="btn" href="{prefix}index.html#matrix">回到矩阵</a>
          </div>
        </div>

        <dl class="pmeta reveal">
          <div class="pmeta__item">
            <dt>源码行数</dt>
            <dd><span class="pmeta__num">{fmt(p["loc"])}</span><span class="pmeta__unit">LOC</span></dd>
          </div>
          <div class="pmeta__item">
            <dt>源码文件</dt>
            <dd><span class="pmeta__num">{fmt(p["files"])}</span><span class="pmeta__unit">files</span></dd>
          </div>
          <div class="pmeta__item">
            <dt>测试用例</dt>
            <dd><span class="pmeta__num">{fmt(p["tests"])}</span><span class="pmeta__unit">cases</span></dd>
          </div>
          <div class="pmeta__item">
            <dt>提交次数</dt>
            <dd><span class="pmeta__num">{fmt(p["commits"])}</span><span class="pmeta__unit">commits</span></dd>
          </div>
        </dl>
      </div>
    </div>
  </section>

  <!-- ============ 界面实拍 ============ -->
  <section class="section psection" id="pshot">
    <div class="wrap">
      <div class="sec-head reveal">
        <div class="sec-head__main">
          <div class="sec-kicker">01 / Screen</div>
          <h2>这是跑起来的界面</h2>
          <p>本地实例直接截屏，没有后期修图，地址条就是当时的地址。</p>
        </div>
        <div class="sec-head__aside">
          实拍<br>
          本机 {e(shot["addr"].split("/")[0])}
        </div>
      </div>

      <figure class="shot shot--full reveal">
        <div class="shot__screen">
          <div class="shot__chrome" aria-hidden="true">
            <span class="shot__dots"><i></i><i></i><i></i></span>
            <span class="shot__addr">{e(shot["addr"])}</span>
          </div>
          <div class="shot__canvas">
            <img src="{prefix}assets/img/{e(shot["img"])}" width="1280" height="800" loading="lazy" decoding="async"
                 alt="{e(shot["alt"])}">
          </div>
        </div>
        <figcaption class="shot__cap">
          <div class="shot__head">
            <span class="shot__name">{e(shot["title"])}</span>
            <span class="shot__badge shot__badge--real">实拍</span>
          </div>
          <p class="shot__desc">{e(shot["desc"])}</p>
        </figcaption>
      </figure>
    </div>
  </section>

  <!-- ============ 架构链路 ============ -->
  <section class="section psection" id="parch">
    <div class="wrap">
      <div class="sec-head reveal">
        <div class="sec-head__main">
          <div class="sec-kicker">02 / Architecture</div>
          <h2>主链路</h2>
          <p>链路图里的每一格都来自仓库代码或 README，不按印象画。</p>
        </div>
      </div>

      <div class="pgrid">
        <div class="reveal">
          <div class="pblock">
            <div class="pblock__label">数据怎么走</div>
{render_pipeline(p["pipeline"])}
          </div>
        </div>

        <div class="reveal">
          <div class="pblock">
            <div class="pblock__label">工程约束与验收</div>
            <div class="pfacts">
{facts}
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- ============ 能力坐标 ============ -->
  <section class="section psection" id="pcap">
    <div class="wrap">
      <div class="sec-head reveal">
        <div class="sec-head__main">
          <div class="sec-kicker">03 / Capability</div>
          <h2>这个系统在哪几行是主力</h2>
          <p>与首页 03 节是同一张表，这里只截出本项目这一列。<b>没做过的格子不填</b>。</p>
        </div>
        <div class="sec-head__aside">
          rows 7<br>
          口径与首页一致
        </div>
      </div>

      <div class="pcap reveal">
{render_caps(p["caps"])}
      </div>
      <p class="pcap__legend">
        <span><i style="color:var(--brand)">●</i>主力实现</span>
        <span><i style="color:color-mix(in srgb, var(--brand) 62%, var(--ink3))">◐</i>有实现，非重点</span>
        <span><i style="color:var(--ink3)">○</i>仅基础形态</span>
        <span><i style="color:var(--line-strong)">–</i>未涉及</span>
      </p>
    </div>
  </section>

  <!-- ============ 本地复现 ============ -->
  <section class="section psection" id="prepro">
    <div class="wrap">
      <div class="sec-head reveal">
        <div class="sec-head__main">
          <div class="sec-kicker">04 / Reproduce</div>
          <h2>在自己机器上跑一遍</h2>
          <p>下面是从零拉起这个系统要的东西。缺依赖时链路会明确失败，不返回编造的结果。</p>
        </div>
      </div>

      <div class="prepro reveal">
        <div class="prepro__block">
          <div class="pblock__label">启动命令</div>
          <pre class="prepro__code"><code>{e(p["repro"]["cmd"])}</code></pre>
        </div>
        <div class="prepro__block">
          <div class="pblock__label">访问地址</div>
          <p class="prepro__url"><a href="{e(p["repro"]["url"])}">{e(p["repro"]["url"])}</a></p>
        </div>
        <div class="prepro__block prepro__block--wide">
          <div class="pblock__label">还需要准备</div>
          <ul class="prepro__needs">
{needs}
          </ul>
          <p class="prepro__note">{e(p["repro"]["note"])}</p>
        </div>
      </div>
    </div>
  </section>

  <!-- ============ 已知边界 ============ -->
  <section class="section psection" id="pbound">
    <div class="wrap">
      <div class="sec-head reveal">
        <div class="sec-head__main">
          <div class="sec-kicker">05 / Boundary</div>
          <h2>这个系统跑不到哪</h2>
          <p>能跑的部分写清楚，跑不动的部分也写清楚。以下是当前真实状态，不是「后续规划」。</p>
        </div>
      </div>

      <div class="pbounds reveal">
{render_bounds(p["bounds"])}
      </div>
    </div>
  </section>

  <!-- ============ 上下项目 ============ -->
  <section class="section section--flush pnav-sec">
    <div class="wrap">
      <nav class="pnav reveal" aria-label="项目导航">
{prev_link}
{next_link}
      </nav>
    </div>
  </section>

</main>

<!-- ============ 页脚 ============ -->
<footer class="foot">
  <div class="wrap foot__inner">
    <div class="foot__left">
      <b>王鑫鸿 · 个人作品矩阵</b> · 静态站点，无追踪脚本<br>
      数据由仓库静态统计得出 · 与 GitHub 仓库同步维护
    </div>
    <div class="foot__links">
      <a href="{prefix}index.html">回到首页</a>
      <a href="https://github.com/xinhongwang138-hue" target="_blank" rel="noopener">GitHub</a>
      <a href="mailto:{e(site["email"])}">{e(site["email"])}</a>
    </div>
  </div>
</footer>

<script src="{prefix}assets/js/app.js" defer></script>
</body>
</html>
"""


def check_index(data: dict) -> int:
    """确认 index.html 里的数字与 projects.json 一致。"""
    if not os.path.exists(INDEX):
        print("找不到 index.html，跳过校验", file=sys.stderr)
        return 0
    with open(INDEX, encoding="utf-8") as f:
        html_src = f.read()
    # 去掉标签再比对，避免 <span> 把数字拆开
    plain = re.sub(r"<[^>]+>", "", html_src)

    problems = []
    for p in data["projects"]:
        for label, val in (
            ("LOC", p["loc"]),
            ("文件", p["files"]),
            ("用例", p["tests"]),
            ("提交", p["commits"]),
        ):
            token = f"{val:,}" if label == "LOC" else str(val)
            if label in ("文件", "用例", "提交") and p["id"] == "p03" and label == "用例":
                token = "0"
            if token not in plain:
                problems.append(f"{p['no']} {label} {token} 在 index.html 里找不到")

    if problems:
        print("index.html 与 projects.json 不一致：", file=sys.stderr)
        for x in problems:
            print("  " + x, file=sys.stderr)
        return 1
    print("index.html 数字与 projects.json 一致 ✓")
    return 0


def main() -> int:
    with open(DATA, encoding="utf-8") as f:
        data = json.load(f)
    projects = data["projects"]
    site = data["site"]

    if "--check" in sys.argv:
        return check_index(data)

    os.makedirs(OUT_DIR, exist_ok=True)
    for i, p in enumerate(projects):
        prev_p = projects[i - 1] if i > 0 else None
        next_p = projects[i + 1] if i < len(projects) - 1 else None
        out = os.path.join(OUT_DIR, f"{p['id']}.html")
        with open(out, "w", encoding="utf-8", newline="\n") as f:
            f.write(render_page(p, prev_p, next_p, site))
        print(f"生成 {os.path.relpath(out, ROOT)}  ({p['no']} {p['name']})")

    return check_index(data)


if __name__ == "__main__":
    sys.exit(main())

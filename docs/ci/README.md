# CI 模板（待放进项目仓库）

本目录放的是**给项目仓库准备的 GitHub Actions 模板**，不在这个静态站里运行。
只有落到对应仓库的 `.github/workflows/` 并**跑绿**，那个项目才算真有自动校验。

| 文件 | 目标仓库 | 落到哪里 | 状态 |
| --- | --- | --- | --- |
| `p02-tests.yml` | `xinhongwang138-hue/contract-approval` | `.github/workflows/tests.yml` | 未落地 |

## 已经落地的

- **P04 深度搜索**：仓库里的 `.github/workflows/ci.yml`（后端 `uv run pytest -q` + 前端
  `vue-tsc --noEmit` 与构建）。本目录原先那份 `p04-tests.yml` 已被它取代并删除。

  这条流水线 2026-10-29 加入后**连续 6 次全红**，2026-11-26 才修绿，两个根因都不在断言本身：
  1. `tests/test_guards.py` 的工作区越界用例断的是 `C:/Windows/...`，Linux 下这只是普通相对名、
     会落回 workspace 内，于是「越界拒绝」从未在 CI 上被真正验证过；改成用解释器路径与临时目录
     构造必然越界的绝对样本。
  2. `ui/vite.config.ts` 读 `process.env`，但没装 `@types/node` 且 `tsconfig.json` 的 `types`
     写死成 `["vite/client"]`，`vue-tsc` 直接报 TS2591。

## 还没配的

- **P01 电商运营助手**：仓库里没有 `.github`。它的测试用内存 SQLite
  （`api/tests/conftest.py:4` 把 `DATABASE_URL` 设成 `sqlite:///:memory:`），不需要任何 service
  容器，一条 `cd api && pytest -q` 就能跑完 469 项——是四个里最容易补的。
- **P03 企业知识库**：只有 `test/04-test_graph_flow.py` 一个链路脚本、没有断言，
  量撑不起一条独立流水线；等链路级断言补齐再加。
- **P05 AI 电商客服**：`smoke_test.py` 那 27 项断言要真实起两个进程（18081 与 18082），
  进 CI 得先把启动方式收敛成一条命令。

## 落地后要同步的三件事

1. 把模板复制到对应仓库的 `.github/workflows/`；
2. 在仓库页确认 Actions 已启用，并等它**跑绿**——配了不等于绿，P04 就是六次红的例子；
3. 回来更新作品集三处：首页 06 节「只有一个仓库有 CI」这条要收窄，
   `docs/projects.json` 里该项目的「没有 CI 流水线」边界要改写，
   项目卡「验收」一行补 CI 徽章或首次运行结论。

# CI 流水线（待放入各自仓库）

本目录放的是**给另外两个仓库准备的 GitHub Actions 模板**，不在这个静态站里运行。
放到位并推送后，对应项目才算真的「有 CI」。

| 文件 | 目标仓库 | 落到哪里 |
| --- | --- | --- |
| `p02-tests.yml` | `xinhongwang138-hue/contract-approval` | `.github/workflows/tests.yml` |
| `p04-tests.yml` | `xinhongwang138-hue/deep-search-agent` | `.github/workflows/tests.yml` |

## 为什么 P01、P03 不在这里

- **P01 电商运营助手**：流水线已经写进仓库本体（`.github/workflows/tests.yml`），
  因为测试用内存 SQLite（见 `api/tests/conftest.py`），不需要任何 service 容器，
  一条 `pytest -q` 就能跑完 469 项。
- **P03 企业知识库**：目前只有纯函数单测（17 项），量还撑不起一条独立流水线；
  等链路级断言补齐后再加。

## 落地后要同步的三件事

1. 把上面两个文件复制到对应仓库的 `.github/workflows/tests.yml`；
2. 在 GitHub 仓库页确认 Actions 已启用（首次推送后会出现在 Actions 标签下）；
3. 回来更新作品集的「已知边界」——把「没有 CI 流水线」那条删掉，
   并在项目卡「验收」一行补上 CI 徽章或首次运行结论。

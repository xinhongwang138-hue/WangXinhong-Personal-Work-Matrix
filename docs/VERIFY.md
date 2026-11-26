# 数字的统计口径

首屏与 05 节的数字，全部由本地克隆的仓库静态统计得出。
任何人可以按本文的命令复算，得到同样的结果。

> 一句话原则：**报的是「有多少」，不是「通过了多少」**。

## 一、复算方法

```bash
# 1. 克隆五个项目仓库（浅克隆即可）
mkdir -p /tmp/repos && cd /tmp/repos
for r in ecommerce-operation-assistant contract-approval knowledge_base deep-search-agent customer-service; do
  git clone --depth 1 https://github.com/xinhongwang138-hue/$r.git
done

# 2. 回到本仓库，跑统计脚本
cd /path/to/WangXinhong-Personal-Work-Matrix
python docs/count_loc.py /tmp/repos/ecommerce-operation-assistant \
                         /tmp/repos/contract-approval \
                         /tmp/repos/knowledge_base \
                         /tmp/repos/deep-search-agent \
                         /tmp/repos/customer-service
```

脚本输出与页面一致：

```
repo                                        LOC  files  tests
--------------------------------------------------------------
ecommerce-operation-assistant            67,262    402    428
                                       .py 42,721 · .tsx 16,553 · .ts 6,050 · .ps1 725 · .html 666 · .css 547
contract-approval                        38,026    203    259
                                       .ts 23,826 · .tsx 13,050 · .sql 996 · .css 129 · .sh 25
knowledge_base                           10,785     64      0
                                       .py 9,129 · .html 1,490 · .ps1 166
deep-search-agent                         3,105     35     11
                                       .py 2,243 · .css 314 · .vue 266 · .sql 182 · .ts 87 · .html 13
customer-service                          7,710     80      0
                                       .py 7,000 · .html 710
--------------------------------------------------------------
TOTAL                                   126,888    784    698
```

> 统计时点：**2026-11-26**，对象为五个项目仓库的远端默认分支，现已统一为 `main`。

## 二、口径明细

### 1. 源码行数（126,888）

- 计入扩展名：`.py` `.ts` `.tsx` `.js` `.jsx` `.vue` `.sql` `.css` `.html` `.ps1` `.sh`
- 排除目录：`.git` `node_modules` `.next` `dist` `build` `__pycache__` `.venv` `venv` `.pytest_cache` `coverage` `.turbo`
- 排除文件名含 `lock` 的依赖锁文件
- 空行与注释**计入**（这是 `wc -l` 式的物理行数，不是有效代码行 SLOC）
- 行尾换行按 1 行计（`text.count("\n") + 1`）

### 2. 源码文件数（784）

与行数同一次遍历，同一套排除规则，只统计上述扩展名的文件。

分项：402 + 203 + 64 + 35 + 80 = 784。

### 3. 测试用例数（698）

静态匹配，两类模式：

- Python：行首 `def test_`（含 `async def test_`）
- JS / TS：行首 `it(` 或 `test(`

这意味着：

- 不是**执行结果**，不代表「698 个全部通过」；
- 不是**覆盖率**，仓库里没有覆盖率报告；
- 参数化用例（`@pytest.mark.parametrize`）只按函数计 1 个，实际展开数更多——P01 静态计 428 个函数，`pytest --collect-only -q` 实测 **469 项**；
- P03 的 `test/04-test_graph_flow.py` 与 P05 的 `smoke_test.py` 都是链路脚本，没有 `def test_` 函数，因此各计 0，页面写「未建套件」而不是「0 通过」。P05 那 27 项冒烟断言单独记在它的详情页与第四节，不混进这个合计。

### 4. 公开仓库数（5）

五个项目仓库都是 public，默认分支统一为 `main`，`git clone` 下来按各自 README 就能起。

**为什么不报提交数**：这几个仓库的历史在整理时压缩成了单次初始提交，`commits` 现在只能反映「整理方式」，不能反映「做了多少事」。与其报一个 1，不如换成能复算的量——行数、文件数、用例数。这条同样适用于任何想拿提交数当活跃度指标的地方。

### 5. 语言构成

页面里每个项目的「语言」取 GitHub Languages API 的主语言
（`GET /repos/xinhongwang138-hue/:repo/languages`），不是行数占比。

## 三、没有统计、也不写的数字

| 指标 | 为什么没有 |
| --- | --- |
| 五套统一通过率 | P01 与 P05 已实测（见第四节），P02 / P03 / P04 依赖 PostgreSQL / Milvus / MinIO 等外部服务，未在本机统一复跑 |
| 覆盖率 | 未接入 coverage / c8，无报告 |
| QPS / P95 / 错误率 | 未做并发压测，任何性能数字都只能靠猜 |
| 用户数 / 访问量 | 项目为本地实现，未上线公网，没有真实流量 |
| 代码质量分 | 未接入 SonarQube 之类的静态扫描 |

## 四、已实测的项（不是静态计数）

静态统计回答「写了多少个」，下面这几行回答「跑起来是什么样」。两者分开写，免得混成一个数。

| 项目 | 命令 | 结果 | 时间 |
| --- | --- | --- | --- |
| P01 电商运营助手 | `cd api && pytest -q` | **469 passed in 54.46s** | 2026-11-10 |
| P05 AI 电商客服 | `python start.py` → `python smoke_test.py` | **27/27 通过**，8 组场景全部走真实 HTTP | 2026-11-26 |

428 是测试**函数**数（静态匹配），469 是 pytest **收集项**数（参数化展开后）——同一批代码的两种量法，不是两个不同的套件。
P05 同理：静态匹配为 0（不是 pytest 套件），`smoke_test.py` 里有 27 项断言。

## 五、页面数字与本文的对应关系

| 页面位置 | 数字 | 本文对应 |
| --- | --- | --- |
| 首屏统计条 | 5 / 126,888 / 698 / 784 | 一、二节 |
| 05 节四张卡 | 126,888 / 698 / 784 / 5 | 一、二节 |
| 项目卡右上 | 67,262 / 38,026 / 10,785 / 3,105 / 7,710 | 一、二节 |
| 项目卡底部 | 文件数 / 用例数 | 一、二节 |

各项目行数占比（供参考，页面未直接展示）：67262 ÷ 126888 = 53.0%，38026 = 30.0%，10785 = 8.5%，7710 = 6.1%，3105 = 2.4%。

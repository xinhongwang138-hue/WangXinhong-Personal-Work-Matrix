# 数字的统计口径

首屏与 04 节的数字，全部由本地克隆的仓库静态统计得出，统计时间 **2026-11-01**。
任何人可以按本文的命令复算，得到同样的结果。

> 一句话原则：**报的是「有多少」，不是「通过了多少」**。

## 一、复算方法

```bash
# 1. 克隆四个仓库（浅克隆即可）
mkdir -p /tmp/repos && cd /tmp/repos
for r in ecommerce-operation-assistant contract-approval knowledge_base deep-search-agent; do
  git clone --depth 1 https://github.com/xinhongwang138-hue/$r.git
done

# 2. 回到本仓库，跑统计脚本
cd /path/to/WangXinhong-Personal-Work-Matrix
python docs/count_loc.py /tmp/repos/ecommerce-operation-assistant \
                         /tmp/repos/contract-approval \
                         /tmp/repos/knowledge_base \
                         /tmp/repos/deep-search-agent
```

脚本输出与页面一致：

```
repo                                        LOC  files  tests
--------------------------------------------------------------
ecommerce-operation-assistant            43,068    274    181
                                       .py 25,595 · .tsx 12,146 · .ts 4,057 · .ps1 723 · .css 547
contract-approval                        37,702    201    259
                                       .ts 23,629 · .tsx 12,923 · .sql 996 · .css 129 · .sh 25
knowledge_base                           10,785     64      0
                                       .py 9,129 · .html 1,490 · .ps1 166
deep-search-agent                         3,098     35     11
                                       .py 2,243 · .css 314 · .vue 266 · .sql 182 · .ts 80 · .html 13
--------------------------------------------------------------
TOTAL                                    94,653    574    451
```

## 二、口径明细

### 1. 源码行数（94,653）

- 计入扩展名：`.py` `.ts` `.tsx` `.js` `.jsx` `.vue` `.sql` `.css` `.html` `.ps1` `.sh`
- 排除目录：`.git` `node_modules` `.next` `dist` `build` `__pycache__` `.venv` `venv` `.pytest_cache` `coverage` `.turbo`
- 排除文件名含 `lock` 的依赖锁文件
- 空行与注释**计入**（这是 `wc -l` 式的物理行数，不是有效代码行 SLOC）
- 行尾换行按 1 行计（`text.count("\n") + 1`）

### 2. 源码文件数（574）

与行数同一次遍历，同一套排除规则，只统计上述扩展名的文件。

### 3. 测试用例数（451）

静态匹配，两类模式：

- Python：行首 `def test_`（含 `async def test_`）
- JS / TS：行首 `it(` 或 `test(`

这意味着：

- 不是**执行结果**，不代表「451 个全部通过」；
- 不是**覆盖率**，仓库里没有覆盖率报告；
- 参数化用例（`@pytest.mark.parametrize`）只按函数计 1 个，实际展开数更多；
- P03 的 `test/04-test_graph_flow.py` 是链路脚本，没有 `def test_` 函数，因此计 0，页面写「未建套件」而不是「0 通过」。

### 4. 提交数（61）

```bash
for r in ecommerce-operation-assistant contract-approval knowledge_base deep-search-agent; do
  echo -n "$r "
  gh api "repos/xinhongwang138-hue/$r/commits?per_page=100" --jq 'length'
done
```

单仓库均少于 100 次提交，因此该接口不会截断。
分项：P01 17 · P02 27 · P03 14 · P04 3。

### 5. 语言构成

页面里每个项目的「语言」取 GitHub Languages API 的主语言
（`GET /repos/xinhongwang138-hue/:repo/languages`），不是行数占比。

## 三、没有统计、也不写的数字

| 指标 | 为什么没有 |
| --- | --- |
| 测试通过率 | 四套系统依赖 MySQL / PostgreSQL / Redis / Milvus / MinIO 等外部服务，未在本机统一复跑 |
| 覆盖率 | 未接入 coverage / c8，无报告 |
| QPS / P95 / 错误率 | 未做并发压测，任何性能数字都只能靠猜 |
| 用户数 / 访问量 | 项目为本地实现，未上线公网，没有真实流量 |
| 代码质量分 | 未接入 SonarQube 之类的静态扫描 |

## 四、页面数字与本文的对应关系

| 页面位置 | 数字 | 本文对应 |
| --- | --- | --- |
| 首屏统计条 | 4 / 94,653 / 451 / 61 | 一、二节 |
| 04 节四张卡 | 94,653 / 451 / 574 / 61 | 一、二节 |
| 项目卡右上 | 43,068 / 37,702 / 10,785 / 3,098 | 一、二节 |
| 项目卡底部 | 文件数 / 用例数 / 提交数 | 一、二节 |
| 首屏矩阵面板 | 45.5% / 39.8% / 11.4% / 3.3% | 各项目行数 ÷ 94,653 |

占比复算：43068 ÷ 94653 = 45.5%，37702 ÷ 94653 = 39.8%，10785 ÷ 94653 = 11.4%，3098 ÷ 94653 = 3.3%。

# X 推文数据研究模板

用自己的 X 单帖导出，按「原创」和「回复」两组，算每千次曝光的点赞、收藏、新增关注、主页访问的中位数，以及每项恰好为 0 的比例。

配套文章：我在 X（[@AYi_AInotes](https://x.com/AYi_AInotes)）发的《开源10个月7万粉丝的涨粉心法：我把流量巅峰期的662条推文拆了一遍》。

> 仓库里的示例数据是模拟生成的 300 行，不是我的真实账号数据，也不代表任何真实账号。

## 文件

| 文件 | 是什么 |
| --- | --- |
| `x-post-study-template.science` | AIPOCH Open-Science 研究包，导入后能回放每一步 |
| `x_post_study.py` | 分析脚本 |
| `sample-x-export-SYNTHETIC-v6.csv` | 模拟的示例数据 |
| `demo-study-metrics.csv` | 用示例数据跑出来的结果 |
| `HOW_TO_RERUN.md` | 在 Open-Science 里重跑的说明 |

## 用法一：在 AIPOCH Open-Science 里跑

1. 安装 [AIPOCH Open-Science](https://aipoch.com/open-science)（建议最新版），接上你自己的模型。研究包里不带任何模型账号或 Key。
2. 新建项目，导入会话包，选 `x-post-study-template.science`。
3. 导入后是只读记录，可以先看回放；再点 Fork，生成一份能改的副本。
4. 附上你自己的 X 单帖导出 CSV，发送这句：

```text
用我附上的 CSV 运行 x_post_study.py，--output-prefix mine。不要修改示例文件。回复里只贴中位数表。新增关注中位数如果是 0，写明恰好为 0 的比例，不要写成完全没有新增关注。
```

想看别人用 .science 做的研究，可以翻官方用例库：https://aipoch.com/open-science/use-cases

## 用法二：不装 Open-Science，直接用 Python 跑

需要 Python 3 和 numpy：

```bash
pip install numpy
python3 x_post_study.py 你的导出.csv --output-prefix mine
```

结果会写到 `mine-study-metrics.csv`。

## 跑之前先改一下你的 CSV

- 必须有这几列：`Impressions`、`Likes`、`Bookmarks`、`New follows`、`Profile visits`。X 官方单帖导出里都有。
- 官方导出**没有** `content_type` 这一列，脚本又要求有。先手动加一列：原创填 `original`，回复填 `reply`。不加的话，脚本会直接退出并提示缺列。
- 少于 20 条的组不计算中位数，只给样本数。

## 这个模板说明不了的事

- 单帖的新增关注是 X 的归因估算，账号到底涨了多少粉，以后台的按天总览为准。
- 结果是相关，不是因果。
- 模板只算原创和回复这一刀；按话题、篇幅、配图分组的分析，用文章里的提示词跑。

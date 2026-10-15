# workbuddy-hub 资产市场站点 — 规格与验收标准

> 阶段：Phase 1 立规格 → Phase 5 按四路审查结论修订
> 日期：2026-10-15
> 状态：代码审查与安全审计发现项已修复并回归通过

## 1. 目标（一句话定界）

**从 `registry/*.yaml` 自动生成一个静态单页站点，由 GitHub Actions 部署到 GitHub Pages，公开地址 `https://airen.github.io/workbuddy-hub/`。**

让任何人（无需安装 WorkBuddy）打开一个链接即可浏览本仓库全部专家与专家团。

> 范围说明：**技能（skills）仅计入头部统计数字，本期不作为卡片列出**。卡片主体是 27 个专家 + 8 个专家团。

## 2. 非目标（本期明确不做）

- 不做每个资产的独立详情页
- 不做技能卡片列表
- 不做站内后端、数据库、登录
- 不做资产 zip 下载
- 不绑定自定义域名
- 不做多语言（仅中文）
- 不引入前端框架或 Node 构建链（Vite/React/Tailwind 等一律不用）

## 3. 交付物

| 文件 | 性质 | 是否入库 |
|---|---|---|
| `scripts/build_site.py` | 生成器：registry → 站点 | ✅ 入库 |
| `templates/site/page.html` | 页面模板（内联 CSS/JS） | ✅ 入库 |
| `.github/workflows/pages.yml` | CI 构建 + 部署 | ✅ 入库 |
| `tests/verify_site.py` | 站点验收自检（静态 + 浏览器） | ✅ 入库 |
| `tests/test_build_site.py` | 生成器单元回归（安全与边界） | ✅ 入库 |
| `docs/hub-site-spec.md` | 本规格 | ✅ 入库（`docs/` 未被 gitignore） |
| `site/` | 构建产物（index.html + 压缩头像） | ❌ gitignore（产物不入库） |

> 「产物不入库」与本仓库既有架构一致：README 明确「单一事实来源 + 派生索引，全部由脚本自动派生，永不双份」。

## 4. 数据源与字段映射

数据源（均已存在，无需新增）：`registry/experts.yaml`、`registry/teams.yaml`、`registry/skills.yaml`、`registry/categories.yaml`。

**卡片字段映射**

| 卡片元素 | 来源 |
|---|---|
| 头像 | `experts/<id>/avatars/<id>.{jpg,png}`，缺失回退 `assets/avatars/_default.jpg` |
| 标题 | `name` |
| 类型徽章 | `type`：`expert` → 「专家」，`team` → 「专家团」 |
| 描述 | `description`（卡片内 CSS 截断 3 行；全文保留在 DOM 中，读屏与检索都能读到，不塞进 `title` 提示气泡） |
| 分类 | `category` → 经 `categories.yaml` 映射为中文 label |
| 标签 | `tags[]`（最多展示 3 个） |
| 技能数 | `len(skills)`（仅 expert） |
| 成员数 | `len(members)`（仅 team） |
| 版本 | `version` |
| 外链 | `https://github.com/airen/workbuddy-hub/tree/main/<path>` |

**页面级字段**：头部统计（专家数 / 专家团数 / 技能条目数）；`<link rel="canonical">` 与 `og:url` 取 `--site-url`（默认 `https://airen.github.io/workbuddy-hub/`）。

## 5. 功能规格

| 编号 | 功能 |
|---|---|
| F1 | 头部：站名、一句话说明、统计数字 |
| F2 | 搜索框：对 `name` / `description` / `tags` / `id` / **分类中文名** 做不区分大小写的子串匹配 |
| F3 | 类型筛选：全部 / 专家 / 专家团 |
| F4 | 分类筛选：全部 + 仅列出实际有资产的分类 |
| F5 | 卡片网格：手机 1 列 / 平板 2 列 / 桌面 3 列 |
| F6 | 结果计数：显示「当前 X / 共 Y」，并写明口径为「项资产（专家 / 专家团）」 |
| F7 | 空状态：无匹配时给出提示与「清除全部筛选」按钮 |
| F8 | 筛选状态写入 URL hash，可分享与刷新保持 |
| F9 | 键盘可达：Tab 顺序合理、焦点样式可见、卡片为真实 `<a>` |
| F10 | 卡片外链新标签打开，带 `rel="noopener"` |
| F11 | **渐进增强**：卡片由服务端静态渲染，禁用 JavaScript 时仍可浏览全部资产（筛选失效） |

## 6. 视觉与可访问性

- 亮色为主，跟随 `prefers-color-scheme: dark` 提供深色
- 中文优先字体栈（系统字体，不加载 Web Font）
- 正文对比度 ≥ 4.5:1，大字 ≥ 3:1（次要文字色 `#667085` 在 `#ffffff` 与 `#f5f6f8` 两种背景上均达标）
- 点击区：**主要操作控件（类型筛选、空状态按钮）≥ 44×44 px**；**次要筛选标签（分类 chips）≥ 36×36 px**（WCAG 2.1 AA 要求 24×24，此处取更严标准）；卡片整体为链接，点击区远大于 44 px
- 语义化标签 + 必要 `aria-label`；装饰性元素 `aria-hidden`

## 7. 性能预算

| 项 | 预算 | 实测 |
|---|---|---|
| `index.html`（含内联 CSS/JS） | ≤ 250 KB | 52.2 KB |
| 单张头像 | ≤ 40 KB（256×256 JPEG，quality 82） | 最大 19.9 KB |
| 头像总量 | ≤ 1.5 MB | 约 0.6 MB |
| 首屏外部请求 | 0（除头像） | 0 |
| 头像加载 | `loading="lazy"` + `decoding="async"` | 已实现 |

## 8. 构建与部署

- **构建**：`python3 scripts/build_site.py`，依赖见 `scripts/requirements.txt`（版本锁定为精确值）
- **部署**：GitHub Actions，push 到 `main` 触发
- **⚠️ 人工前置**：必须在仓库 Settings → Pages → Source 选择「GitHub Actions」，此步骤无法脚本化
- **⚠️ 路径约束**：project site 地址含子路径 `/workbuddy-hub/`，页面内所有资源引用**必须为相对路径**，禁止 `href="/..."` 或 `src="/..."`

**安全约定**（对应安全审计发现项）：

1. **权限最小化**：workflow 默认仅 `contents: read`；仅 `deploy` job 持有 `pages: write` + `id-token: write`；`build` job 执行仓库代码，保持只读
2. **供应链固定**：所有第三方 Action 固定到 commit SHA（tag 可被上游重指向），注释保留语义版本
3. **凭据不落盘**：`checkout` 设 `persist-credentials: false`
4. **依赖锁定**：`scripts/requirements.txt` 全部 pin 精确版本
5. **输入白名单**：registry 的 `id` / `path` 必须过白名单校验（`id` 需匹配 `^[a-z0-9][a-z0-9._-]{0,63}$`——**含长度上限 64**，避免超长名触发 `ENAMETOOLONG`；且 path 恰好为 `<bucket>/<id>`），写入前再做 `is_relative_to` 归属断言
6. **输出目录白名单**：`--out` 必须是「不存在的目录 / 空目录 / 含本脚本专属标记 `.hub-site-build` 的产物目录」，其余一律拒绝（**不用通用的 `.nojekyll` 当归属判据**——任何静态站都可能有它）
7. **转义纪律**：所有插入 HTML 的值统一走 `html.escape(quote=True)`；卡片由服务端渲染，模板 JS 不使用 `innerHTML`

## 9. 验收标准（可执行）

`tests/verify_site.py`（站点验收，`--browser` 启用真实浏览器检查）：

| 编号 | 标准 |
|---|---|
| AC1 | 生成器退出码 0，无异常 |
| AC2 | `index.html` 与 `.nojekyll` 存在；**每张卡片引用的头像文件都真实存在** |
| AC3 | 卡片数与 registry 一致（专家 27/27、专家团 8/8） |
| AC4 | 无 `href="/` 或 `src="/` 绝对路径 |
| AC5 | 卡片外链均指向真实存在的仓库路径 |
| AC6 | `index.html` ≤ 250 KB |
| AC7 | 单张头像 ≤ 40 KB |
| AC8 | 浏览器无控制台错误 / 日志错误 / 4xx·5xx / 加载失败 / **未捕获异常**（事件缓冲区先排干再判定，避免晚到错误漏判） |
| AC9 | 搜索、类型/分类筛选、空状态、重置、URL 状态**写入**行为正确 |
| AC9d | URL 状态**还原**（刷新/分享后筛选保持） |
| AC12 | 卡片外链均 `target="_blank"` + `rel="noopener"` |
| AC10 | 幂等：连续两次生成的**全部产物**（含头像）逐字节一致 |

`tests/test_build_site.py`（生成器单元回归）：

| 编号 | 标准 |
|---|---|
| AC11 | 路径穿越被拦截（id/path 白名单）、`--out` 白名单生效、`--no-avatars` 不产生失效引用、模板缺占位符报错、HTML 转义完备 |

## 10. 风险

| 编号 | 风险 | 应对 |
|---|---|---|
| R1 | 源头像最大 1.4 MB，直接发布拖慢首屏 | 构建时统一压缩至 256×256 JPEG（已实测最大 19.9 KB） |
| R2 | 首次部署需人工在 Settings 开 Pages 源 | 在交付报告中给出逐步指引 |
| R3 | Action 版本号随时间漂移 | 已 pin 到 commit SHA，可用 Dependabot 跟进 |
| R4 | Pillow 在 CI 中安装失败 | 降级为直接复制原图，站点仍可构建 |
| R5 | 受限环境下删除旧头像失败 | `_prune_stale_avatars` 收集失败项为警告，不中断构建 |
| R6 | 构建被中断（Ctrl-C / 进程被杀 / CI 超时）导致产物半残 | **先写后删**：新产物全部落盘后才清理旧头像，中断时目录内仍是上一次的完整产物（曾实测「先删后写」在中断后留下「无 index.html + 8/35 张头像」） |

# Fengmin Li

前端与 AI Agent 开发，关注交互体验、智能体工作流与 AI 应用。主要使用 **TypeScript / React / Python**。

[个人站点](https://omnili.site) · [联系我](mailto:2080291162@qq.com) · [开源贡献](#开源贡献)

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/chiikawa-engineering-dark.svg" />
    <img src="./assets/chiikawa-engineering.svg" width="960" alt="前端交互、AI Agent 和 AI 应用三个方向的动态示意，八位 Chiikawa 角色作为边角注解。" />
  </picture>
</p>

## 代表项目

### [collabboard](https://github.com/0717lee/collabboard)

实时协作白板：把绘图、多人编辑、实时光标、权限分享和版本快照放进同一块画布，支持图表嵌入与 PNG/SVG 导出。

<code>React</code> · <code>TypeScript</code> · <code>Fabric.js</code> · <code>Liveblocks</code>

### [OSS Maintainer Assistant](https://github.com/0717lee/OSS-Maintainer-Assistant)

多 Agent 开源维护助手：协作完成问题分诊、查重、质量评审和回复草拟。React 工作台展示判断依据，并让维护者确认后再执行操作。

<code>LangGraph</code> · <code>Python</code> · <code>FastAPI</code> · <code>React</code>

### [WenDao · 古籍智解](https://github.com/0717lee/WenDao)

AI 古籍阅读平台：React 对照阅读器支持渐进加载、同步滚动和逐句追问，结合原文引用式 RAG 问答与竖排 OCR。

<code>React</code> · <code>TypeScript</code> · <code>FastAPI</code> · <code>RAG</code>

### [Lumina Flow](https://github.com/0717lee/lumina-flow)

空间思维导图：围绕无限画布设计节点编辑、自动布局、聚焦模式和键盘操作，支持本地多画布管理与搜索。

<code>React Flow</code> · <code>Zustand</code> · <code>Tailwind CSS</code>

## 技术探索

- [PixelForge](https://github.com/0717lee/pixelforge)：MoonBit 图像处理、滤镜与编解码，配套浏览器 Playground。
- [MoonHostABI](https://github.com/0717lee/moonhostabi)：检查 Wasm-GC 宿主接口变化，生成 TypeScript 适配器。

## 开源贡献

以下记录均为已合入的上游改动，共 33 个 PR：

<details>
<summary>查看 8 个项目的已合入记录</summary>

| 项目 | 已合入 | 改动 |
| :-- | :-: | :-- |
| [Rivus Product](https://github.com/rivusglobal/rivus-product) | 19 | Agent 交易平台：订阅档位与真实额度、API/MCP 可观测性面板、研究与首页 dashboard、移动端与聊天体验 |
| [MoonBit Rabbita](https://github.com/moonbit-community/rabbita/pull/218) | 4 | DOM：SVG 集合绑定、可变集合接口、媒体轨道与 TimeRanges 查询；JS：拒绝 undefined 的序列化结果 |
| [MoonBit Core](https://github.com/moonbitlang/core/pull/4181) | 3 | 标准库 builtin 文档与可执行示例 |
| [OpenSeek](https://github.com/moonbitlang/openseek/pull/1132) | 2 | 桌面端：浏览器标签复用时重新导航、项目侧栏拖拽调宽 |
| [ContextForge Web UI](https://github.com/contextforge-org/contextforge-web-ui/pull/106) | 2 | MCP 管理界面：区分组件加载失败与空列表、移除工具预览的重复参数 |
| [nanobot](https://github.com/HKUDS/nanobot/pull/5602) | 1 | Agent WebUI：回合完成提示音 |
| [DeerFlow](https://github.com/bytedance/deer-flow/pull/5453) | 1 | Agent 运行时：保留内存模式下的运行历史 |
| [Proton](https://github.com/moonbit-community/proton/pull/300) | 1 | Windows 高 DPI 窗口过渡的回归测试 |

Rivus Product 另有部分工作由维护者在拆分后的 PR 中提交并署名 Credit: 0717lee（[#998](https://github.com/rivusglobal/rivus-product/pull/998)、[#999](https://github.com/rivusglobal/rivus-product/pull/999)、[#1006](https://github.com/rivusglobal/rivus-product/pull/1006)、[#1008](https://github.com/rivusglobal/rivus-product/pull/1008)、[#1009](https://github.com/rivusglobal/rivus-product/pull/1009)）。

</details>

[全部合入记录](https://github.com/search?q=is%3Apr+author%3A0717lee+is%3Amerged&type=pullrequests) · [正在推进的 PR](https://github.com/search?q=is%3Apr+author%3A0717lee+is%3Aopen&type=pullrequests)

<details>
<summary>生态 fork</summary>

参与过 [sandbase-harness](https://github.com/sandbaseai/sandbase-harness)、[dsh-plugin-store](https://github.com/sandbaseai/dsh-plugin-store)、[awesome-agent-runtime](https://github.com/sandbaseai/awesome-agent-runtime) 和 [deepseek-harness-handbook](https://github.com/sandbaseai/deepseek-harness-handbook) 生态；个人账号下的对应仓库是上游 fork。

</details>

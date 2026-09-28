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

以下记录均为已合入的上游改动：

<details>
<summary>查看 6 条已合入记录</summary>

| 项目 | 改动 |
| :-- | :-- |
| [ContextForge Web UI #106](https://github.com/contextforge-org/contextforge-web-ui/pull/106) | MCP 管理界面：区分组件加载失败与空列表，提供重试 |
| [nanobot #5602](https://github.com/HKUDS/nanobot/pull/5602) | Agent WebUI：增加回合完成提示音 |
| [DeerFlow #5453](https://github.com/bytedance/deer-flow/pull/5453) | Agent 运行时：保留内存模式下的运行历史 |
| [OpenSeek #1132](https://github.com/moonbitlang/openseek/pull/1132) | 桌面浏览器：修复标签复用时地址与页面脱节 |
| [MoonBit Core #4181](https://github.com/moonbitlang/core/pull/4181) | 标准库文档与可执行示例 |
| [Proton #300](https://github.com/moonbit-community/proton/pull/300) | Windows 高 DPI 窗口过渡的回归测试 |

</details>

[全部合入记录](https://github.com/search?q=is%3Apr+author%3A0717lee+is%3Amerged&type=pullrequests) · [正在推进的 PR](https://github.com/search?q=is%3Apr+author%3A0717lee+is%3Aopen&type=pullrequests)

<details>
<summary>生态 fork</summary>

参与过 [sandbase-harness](https://github.com/sandbaseai/sandbase-harness)、[dsh-plugin-store](https://github.com/sandbaseai/dsh-plugin-store)、[awesome-agent-runtime](https://github.com/sandbaseai/awesome-agent-runtime) 和 [deepseek-harness-handbook](https://github.com/sandbaseai/deepseek-harness-handbook) 生态；个人账号下的对应仓库是上游 fork。

</details>

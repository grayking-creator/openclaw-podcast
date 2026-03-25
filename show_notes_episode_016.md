# OpenClaw Daily — Episode 016

**Title:** OpenClaw Sheds Its Skin  
**Subtitle:** The v2026.3.22 and v2026.3.23 Double Release Deep Dive

## 1) Episode summary
In this episode, we unpack OpenClaw's back-to-back 2026.3.22 and 2026.3.23 releases, focusing on the most meaningful changes for maintainers, plugin developers, and self-hosted users. We break down migration pressure points (especially plugin SDK, browser tooling, and matrix/skill ecosystems), what breaks, and what to do before and after upgrading. The goal is a cleaner, safer platform state with fewer runtime surprises, better auth/proxy behavior, and cleaner defaults for UI, models, and extension integrations.

## 2) What we cover
- High-impact highlights from **v2026.3.22** and **v2026.3.23**
- Why `openclaw doctor --fix` became the upgrade anchor command
- Browser/Chrome MCP migration details and what changed for existing-session flows
- Plugin ecosystem shifts: SDK migration, runtime behavior, and removal of old compatibility layers
- ClawHub-first plugin installation and marketplace/plugin compatibility fixes
- Matrix plugin migration guidance and reliability fixes
- Accessibility + UI polish updates (including WCAG-aligned contrast tuning)
- Qwen/DashScope provider changes and model configuration cleanup
- Practical upgrade sequencing and verification checklist

## 3) Release notes links
- [OpenClaw v2026.3.22](https://github.com/openclaw/openclaw/releases/tag/v2026.3.22)
- [OpenClaw v2026.3.23](https://github.com/openclaw/openclaw/releases/tag/v2026.3.23)

## 4) Key topics with links
- [`openclaw doctor --fix`](https://docs.openclaw.ai/gateway/doctor) — migration and repair entry point for environment, plugins, and known config drift
- [Browser / Chrome MCP](https://docs.openclaw.ai/tools/browser) — updates around existing-session browser attachment and legacy Chrome extension path removal
- [Plugin SDK migration](https://docs.openclaw.ai/plugins/sdk-migration) — replacing legacy import/interop assumptions with the new SDK surface
- [Plugin SDK overview](https://docs.openclaw.ai/plugins/sdk-overview) — how plugin runtime boundaries and APIs are intended to work now
- [Matrix migration](https://docs.openclaw.ai/install/migrating-matrix) — upgrades required for the new Matrix plugin stack
- [ClawHub](https://docs.openclaw.ai/tools/clawhub) — new default flow for install/update/search and package compatibility
- [OpenClaw migration guide](https://docs.openclaw.ai/install/migrating) — broader config/state migration essentials
- [Qwen/DashScope (Model Studio)](https://www.alibabacloud.com/en/product/modelstudio) — provider changes and endpoint path updates
- [WCAG 2.1 AA](https://www.w3.org/TR/WCAG21/) — accessibility baseline for UI contrast and control updates in the release

## 5) Upgrade checklist (9 steps)
- [ ] **Backup your current OpenClaw config/state** before upgrades (including `.openclaw` + any custom plugin state).
- [ ] **Update in sequence**: install/upgrade to `2026.3.22` first, then `2026.3.23` so transitional fixes land in order.
- [ ] **Run `openclaw doctor --fix` immediately after each upgrade stage** to repair migration drift and stale config references.
- [ ] **Switch legacy plugin/agent imports** from removed compatibility surfaces to the new `openclaw/plugin-sdk/*` patterns and runtime execution model.
- [ ] **Migrate plugin installs and metadata paths** toward ClawHub (`clawhub:<package>` flows where available) and refresh skill/plugin compatibility state.
- [ ] **Update Matrix plugin setup** using the migration guide if coming from the old Matrix stack.
- [ ] **Migrate config hygiene**: replace legacy env names and legacy state locations (`CLAWDBOT_*`/`MOLTBOT_*`, `~/.moltbot`) with current OpenClaw equivalents.
- [ ] **Review browser tooling config** for Chrome/Browser MCP changes (existing sessions, userDataDir attachment, extension relay path removal).
- [ ] **Verify providers and UI/accessibility after restart** (Qwen/DashScope endpoints, model defaults, and key UI flows) and run a short smoke test of assistant tools.

## 6) Links mentioned
- https://github.com/openclaw/openclaw/releases/tag/v2026.3.22
- https://github.com/openclaw/openclaw/releases/tag/v2026.3.23
- https://docs.openclaw.ai/gateway/doctor
- https://docs.openclaw.ai/tools/browser
- https://docs.openclaw.ai/plugins/sdk-migration
- https://docs.openclaw.ai/plugins/sdk-overview
- https://docs.openclaw.ai/install/migrating-matrix
- https://docs.openclaw.ai/tools/clawhub
- https://docs.openclaw.ai/install/migrating
- https://www.alibabacloud.com/en/product/modelstudio
- https://www.w3.org/TR/WCAG21/

## 7) Where to find us
Visit us at: **[tobyonfitnesstech.com](https://tobyonfitnesstech.com)**

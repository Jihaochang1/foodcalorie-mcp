# Changelog

## [0.1.5] - 2026-11-23

### Fixed
- Removed all suspension-era wording from the README and package metadata
  ("temporarily unavailable", account-action notices, 401/404 claims). The GitHub
  account was reinstated on 2026-11-20; Docker/GHCR, Pages and all package links
  are verified working again. Tool surface and data are unchanged from 0.1.4.

## [0.1.4] - 2026-11-06

### Fixed
- Replaced every GitHub link in the README with a working one. The repository hosting
  account was suspended, so the repository, its releases page, the container registry
  entry and the upstream pull-request links all returned 404 or 401, and the README sent
  every reader to dead pages. The home page, the English page, the contact address and
  the source-distribution route are now the documented paths.
- The "give it a Star" closing line pointed at a page that no longer exists. It now asks
  for the thing that actually keeps the project going: use it.

### Changed
- Version 0.1.4. Tool surface and data are unchanged from 0.1.3.

## [0.1.3] - 2026-10-31

### Fixed
- `initialize` now reports the real package version in `serverInfo.version`. It was an
  empty string since 0.1.0 because `MCPServer` defaults to `version=""`. MCPB clients
  compare this against the bundle manifest, so an empty value is a mismatch signal.

### Added
- `scripts/build_mcpb.py` and the published `foodcalorie-mcp-0.1.3.mcpb` bundle, so
  Claude Desktop users can install with one click instead of editing JSON by hand.

Tool surface and data are unchanged from 0.1.2.

## [0.1.2] - 2026-10-31

### Added
- `mcp-name: io.github.Jihaochang1/foodcalorie-mcp` marker in the README, required by the
  official MCP Registry to prove PyPI package ownership before publishing.

No code changes; data and tool surface are identical to 0.1.1.

## [0.1.1] - 2026-10-25

### Added
- `list_foods_by_category` 工具：按类别浏览食品数据
- `compare_foods` 工具：多个食品营养成分并排对比
- 扩展数据包支持：`load_extra_data()` 函数 + `FOODCALORIE_EXTRA_DATA` 环境变量，
  可将同构 JSON 数据包（如 FoodCalorie Pro 数据包）合并进内置数据库
- SUPPORT.md：支持方式与进阶产品说明
- .gitignore：防止构建产物与许可数据库误提交

### Changed
- README：PyPI 徽章、更新后的工具列表、服务说明
- pyproject：作者邮箱改用 GitHub noreply 地址；补充 keywords/classifiers/urls

### Removed
- pyproject 中失效的 Sponsor 链接与 similarity 扩展组

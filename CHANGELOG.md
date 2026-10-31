# Changelog

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

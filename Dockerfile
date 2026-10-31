# FoodCalorie MCP Server — 供 Glama 等目录站做容器化检查用
# 检查方式：构建镜像 → 启动 → 发 MCP initialize / tools/list，能正常响应即通过
FROM python:3.12-slim

LABEL org.opencontainers.image.title="foodcalorie-mcp"
LABEL org.opencontainers.image.description="Chinese food & chain-restaurant nutrition data MCP server"
LABEL org.opencontainers.image.source="https://github.com/Jihaochang1/foodcalorie-mcp"
LABEL org.opencontainers.image.licenses="Apache-2.0"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# 从 PyPI 装已发布版本：目录站检查的是「用户实际装到的那个包」，不是本地源码
RUN pip install --no-cache-dir foodcalorie-mcp==0.1.2

# stdio 传输：不要加 -u 之外的任何交互参数，检查器通过 stdin/stdout 通信
ENTRYPOINT ["python", "-m", "foodcalorie_mcp.server"]

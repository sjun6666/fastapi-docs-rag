# 001 登录返回 500：数据库表不存在

- 症状：在 Swagger 里登录返回 Internal Server Error（HTTP 500），但 backend 容器显示 healthy。
- 日志里的关键那一行：relation "user" does not exist
- 原因：开发配置启动时不会自动执行初始化脚本 → 数据库迁移没跑 → 表没建出来
- 怎么修的（命令）：docker compose exec backend bash scripts/prestart.sh
- 怎么确认修好了：Authorize 成功；GET /api/v1/users/me 返回 200，内容里有 admin@example.com 和 "is_superuser": true
- 备注：健康检查返回 200、容器状态是 healthy，但它只检查服务活没活着、数据库连不连得上，不检查表在不在
- 排查步骤：先看 docker compose logs backend，再看 docker compose ps -a，发现没有初始化容器。
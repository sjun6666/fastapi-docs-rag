# 002 后端启动失败：FIRST_SUPERUSER 不是合法邮箱

- **症状**：打开 http://localhost:8000/docs，点 Authorize 报 `auth error TypeError: Failed to fetch`；所有接口都连不上，包括登录。
- **关键行**（`docker compose logs backend`）：
  ```
  ValidationError: 1 validation error for Settings
  FIRST_SUPERUSER
    value is not a valid email address: The part after the @-sign contains invalid characters: '@'.
  ```
- **原因**：`.env` 里的 `FIRST_SUPERUSER` 被改成了 `admin@@example.com`。它在 `app/core/config.py` 里的类型是 `EmailStr`。后端启动时会执行 `settings = Settings()`（config.py:91）校验配置，邮箱格式不合法就抛出 ValidationError，进程退出。结果 backend 容器没在运行，所有请求都连不上。
- **修复**：
  ```powershell
  # 把 FIRST_SUPERUSER 改回合法邮箱（本次从备份恢复）
  Copy-Item $HOME\template-env-backup.txt .env
  Select-String -Path .env -Pattern "FIRST_SUPERUSER="   # 确认已改回
  docker compose up -d backend                           # 配置变了才会重建容器
  ```
- **验证**：
  1. `docker compose ps -a`：backend 显示 `Up ... (healthy)`，CREATED 是刚刚
  2. Swagger 里 Authorize 登录成功
  3. `GET /api/v1/users/me` 返回 200，email 为 admin@example.com，is_superuser 为 true
- **排查步骤**（不知道原因时）：
  1. 浏览器报 Failed to fetch，先判断服务在不在：`docker compose ps -a`，看 backend 是不是 Up、healthy
  2. backend 没在运行或在反复重启：`docker compose logs backend --tail 50`，看 traceback 最后几行
  3. 最后一行是 `ValidationError ... for Settings`，说明是配置校验失败，记下出错的字段名
  4. 查配置文件里的这个字段：`Select-String -Path .env -Pattern "字段名="`
  5. 对照 `app/core/config.py` 里这个字段的类型，确认值不合法，改正后按"修复"执行
- **备注**：
  - 第一次注入时 `.env` 没保存，故障根本没生效，看到的"一切正常"毫无意义。要先确认故障生效（看文件内容、容器里的 `printenv`、`ps -a` 的 CREATED），再观察现象。
  - `docker compose restart` 不会重新读 `.env`，`up -d` 才会在配置变化时重建容器。判断有没有重建要看 CREATED，`up` 的输出不管重没重建都写 Started。
  - 三种症状的区别：Failed to fetch 表示服务没在运行；500 表示服务在运行但有异常没被接住（如 001 缺表）；4xx 是代码主动返回的错误。
  - 这个字段只在启动读配置和创建初始超级用户时用到。登录查的是数据库，不读 `.env`。
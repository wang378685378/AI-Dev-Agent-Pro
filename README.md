# AI Dev Agent Pro

一个基于 LLM 的自动化代码生成与测试修复系统，支持 SSE 流式返回实时进度。

## 功能说明

- **需求分析**：接收自然语言需求描述
- **代码生成**：调用 LLM API 自动生成 Python 代码
- **测试生成**：自动生成对应的 pytest 测试用例
- **自动测试**：执行 pytest 测试验证代码正确性
- **自动修复**：测试失败时自动修复代码（最多可配置循环次数）
- **实时进度**：通过 SSE (Server-Sent Events) 实时展示执行步骤
- **多供应商支持**：支持 OpenAI API 及兼容 API（如 Azure、本地模型等）

## 项目结构

```
AI Dev Agent Pro/
├── backend/
│   ├── main.py          # FastAPI 入口 + 健康检查
│   ├── config.py        # 配置管理（环境变量）
│   ├── orchestrator.py  # 流程编排（SSE 输出）
│   ├── agents.py        # Agent 类（Code/Test/Fix）
│   ├── generator.py     # 代码和测试生成（已整合到 agents.py）
│   ├── runner.py        # pytest 执行（含超时处理）
│   ├── llm.py           # LLM API 封装（含重试机制）
│   └── requirements.txt
├── frontend/
│   ├── index.html       # 页面
│   ├── style.css        # 样式
│   └── script.js        # EventSource 客户端
├── backend.Dockerfile   # Backend 镜像
├── frontend.Dockerfile  # Frontend 镜像
└── docker-compose.yml   # 编排配置
```

## 启动方式

### 前置条件

- Docker & Docker Compose 已安装
- LLM API Key（默认 OpenAI，也支持兼容 API）

### 环境变量配置

创建 `.env` 文件（项目根目录）：

```bash
# 必填：API Key
OPENAI_API_KEY=your_api_key_here

# 可选：自定义 API 地址（支持 Azure、本地模型等兼容 API）
OPENAI_BASE_URL=https://your-custom-endpoint/v1

# 可选：模型配置
MODEL_NAME=gpt-4
TEMPERATURE=0.2

# 可选：重试和超时配置
MAX_RETRIES=3
TIMEOUT=60
MAX_FIX_ATTEMPTS=3
```

### 自定义 API 供应商配置

系统支持任何兼容 OpenAI API 格式的供应商。配置位置有两个：

#### 1. 通过 `.env` 文件配置（推荐）

在项目根目录创建 `.env` 文件：

**示例 1：默认 OpenAI**
```bash
OPENAI_API_KEY=sk-your_openai_key
# OPENAI_BASE_URL 留空，使用默认 OpenAI API
MODEL_NAME=gpt-4
```

**示例 2：Azure OpenAI**
```bash
OPENAI_API_KEY=your_azure_key
OPENAI_BASE_URL=https://your-resource.openai.azure.com/openai/deployments/your-deployment
MODEL_NAME=gpt-4
```

**示例 3：本地模型（Ollama）**
```bash
OPENAI_API_KEY=ollama
OPENAI_BASE_URL=http://localhost:11434/v1
MODEL_NAME=qwen2.5-coder:7b
```
启动 Ollama：`ollama serve` 并拉取模型：`ollama pull qwen2.5-coder:7b`

**示例 4：LM Studio**
```bash
OPENAI_API_KEY=lm-studio
OPENAI_BASE_URL=http://localhost:1234/v1
MODEL_NAME=model-identifier
```

**示例 5：其他兼容服务（如 Anyscale、Together 等）**
```bash
OPENAI_API_KEY=your_service_key
OPENAI_BASE_URL=https://api.your-service.com/v1
MODEL_NAME=model-name
```

#### 2. 通过 docker-compose.yml 配置

在 `docker-compose.yml` 的 `environment` 部分直接配置：

```yaml
services:
  backend:
    build:
      context: .
      dockerfile: backend.Dockerfile
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=your_key_here
      - OPENAI_BASE_URL=http://your-custom-endpoint/v1  # 可选
      - MODEL_NAME=your_model_name                       # 可选
      - TEMPERATURE=0.2
      - MAX_RETRIES=3
      - TIMEOUT=60
      - MAX_FIX_ATTEMPTS=3
    restart: unless-stopped
```

#### 配置优先级

`.env` 文件 > docker-compose.yml environment > 默认值

#### 验证配置

启动后访问健康检查端点验证配置：
```bash
curl http://localhost:8000/health
```

成功响应：
```json
{"status": "ok", "model": "gpt-4"}
```

### 使用 Docker Compose 启动

```bash
docker-compose up --build
```

启动后访问：
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **健康检查**: http://localhost:8000/health

## 示例

### 输入

```
写一个函数计算斐波那契数列，输入 n 返回前 n 项
```

### 输出流程

```
🧠 [start] 开始分析需求...
📦 [generate] 生成代码中...
📦 [generate] 生成测试中...
🧪 [test] 运行测试 (attempt 1)...
✅ [done] 所有测试通过！
```

### 生成结果示例

```json
{
  "fibonacci.py": "def fibonacci(n):\n    result = [0, 1]\n    for i in range(2, n):\n        result.append(result[i-1] + result[i-2])\n    return result[:n]",
  "test_fibonacci.py": "import pytest\nfrom fibonacci import fibonacci\n\ndef test_fibonacci():\n    assert fibonacci(5) == [0, 1, 1, 2, 3]"
}
```

## 架构优化

### 重构改进

1. **配置管理**：新增 `config.py`，统一管理环境变量，支持自定义供应商 API
2. **Agent 模式**：将生成器重构为 `CodeAgent`、`TestAgent`、`FixAgent` 类
3. **重试机制**：LLM 调用增加指数退避重试，提高稳定性
4. **错误处理**：
   - 输入验证
   - 异常捕获与 SSE 错误传播
   - 测试超时保护（30秒）
   - 启动配置验证
5. **日志系统**：引入 logging 模块，便于调试
6. **健康检查**：新增 `/health` 端点监控服务状态

## 注意事项

⚠️ **LLM 生成不稳定**
- 代码生成质量依赖 LLM API 的响应，可能存在随机性
- 复杂需求可能需要多次尝试才能生成正确代码
- 建议将需求描述尽量清晰、具体

⚠️ **测试循环限制**
- 最多自动修复 `MAX_FIX_ATTEMPTS` 次（默认 3 次）
- 某些逻辑错误可能无法通过自动修复解决

⚠️ **安全提示**
- 生成的代码会在临时目录执行测试，请勿用于生产环境
- 妥善保管 API Key，避免泄露
- 建议使用防火墙限制容器网络访问

## 技术栈

- **Backend**: FastAPI + OpenAI API (兼容) + pytest
- **Frontend**: 原生 HTML + CSS + JavaScript (EventSource)
- **部署**: Docker + Docker Compose + Nginx

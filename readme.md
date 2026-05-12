# AI Playwright MCP - 智能自动化测试平台

> 告别传统脚本编写，迎接智能自动化测试新时代！

## 项目简介

这是一个基于自然语言 AI 驱动的 Playwright MCP 自动化测试软件。用户可以通过自然语言指令来控制浏览器执行自动化测试任务，无需编写传统测试脚本。

## 核心特性

- **自然语言驱动**：用简单指令替代复杂脚本编写
- **实时交互调试**：每一步操作都可即时验证和调整
- **降低技术门槛**：非技术人员也能参与自动化流程创建
- **AI 智能决策**：LLM 自动分析页面状态并执行操作
- **可视化控制台**：Web 界面管理测试用例和查看报告

## 技术栈

- **后端**: Python 3.10+ / FastAPI
- **浏览器自动化**: Playwright
- **AI 集成**: OpenAI API (GPT-4o)
- **前端**: Vue.js 3 / Element Plus
- **数据库**: SQLite

## 快速开始

### 1. 环境准备

```bash
# 检查 Python 版本（需要3.8+）
python --version

# 安装依赖
cd backend
pip install -r requirements.txt

# 安装 Playwright 浏览器驱动
playwright install
```

### 2. 配置 OpenAI API Key

```bash
# 复制环境变量文件
cp .env.example .env

# 编辑 .env 文件，填入你的 OpenAI API Key
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4o
```

### 3. 启动后端服务

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

服务启动后，访问 http://localhost:8000/docs 查看 API 文档。

### 4. 启动前端控制台

```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:3000 打开 Web 控制台。

## 项目结构

```
ai_playwright/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI 入口
│   │   ├── api/                    # API 路由
│   │   │   ├── test_cases.py       # 测试用例管理
│   │   │   ├── execution.py        # 测试执行
│   │   │   ├── reports.py          # 测试报告
│   │   │   └── browser.py          # 浏览器控制
│   │   ├── core/                   # 核心模块
│   │   │   ├── agent.py            # AI 智能体
│   │   │   ├── playwright_mcp.py   # MCP 封装
│   │   │   ├── browser.py          # 浏览器管理
│   │   │   └── snapshot.py         # 快照生成
│   │   ├── models/                 # 数据模型
│   │   │   ├── database.py         # 数据库模型
│   │   │   └── schemas.py          # Pydantic 模型
│   │   ├── services/               # 业务服务
│   │   │   └── test_service.py     # 测试服务
│   │   └── config.py               # 配置
│   ├── requirements.txt
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   │   ├── HomeView.vue        # 首页
│   │   │   ├── TestCaseList.vue    # 测试用例管理
│   │   │   └── ExecutionReport.vue # 测试报告
│   │   ├── App.vue
│   │   ├── main.js
│   │   └── router.js
│   ├── package.json
│   └── vite.config.js
├── mcp_server/
│   └── config.json
├── .env.example
└── README.md
```

## 核心功能

### AI Agent 工作流程

1. **目标理解**：LLM 解析用户指令
2. **导航**：打开目标 URL
3. **观察**：获取页面快照
4. **决策与操作**：分析快照，识别元素并执行操作
5. **验证**：检查操作结果
6. **报告**：生成最终测试报告

### API 接口

| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/test-cases` | GET | 获取测试用例列表 |
| `/api/test-cases` | POST | 创建测试用例 |
| `/api/test-cases/{id}` | GET | 获取测试用例详情 |
| `/api/test-cases/{id}` | PUT | 更新测试用例 |
| `/api/test-cases/{id}` | DELETE | 删除测试用例 |
| `/api/execution/start` | POST | 启动测试执行 |
| `/api/execution/{id}` | GET | 获取执行状态 |
| `/api/reports/{id}` | GET | 获取测试报告 |
| `/api/browser/session/{id}` | POST | 创建浏览器会话 |
| `/api/browser/session/{id}/snapshot` | GET | 获取页面快照 |

## 使用示例

### 创建测试用例

```json
{
  "name": "登录功能测试",
  "description": "验证网站登录流程",
  "instruction": "打开登录页面，输入用户名'test@example.com'和密码'123456'，点击登录按钮，验证是否成功登录并跳转到仪表盘页面。",
  "start_url": "https://example.com/login"
}
```

### 执行测试

```bash
curl -X POST http://localhost:8000/api/execution/start \
  -H "Content-Type: application/json" \
  -d '{"test_case_id": 1}'
```

## 最佳实践

### 性能优化

- **浏览器实例池化**：预热一定数量的浏览器实例
- **并行执行与隔离**：每个 AI 会话拥有独立的 BrowserContext
- **优化操作序列**：提供"宏工具"，将常用操作序列打包

### 稳定性保障

- **重试机制**：指数退避重试策略
- **稳健选择器**：优先使用 role 选择器和包含文本的选择器
- **超时控制**：合理设置操作超时时间

### 应对挑战

- **快照信息丢失**：结合视觉截图辅助 AI 理解复杂组件状态
- **元素定位稳定性**：在关键元素上添加稳定的 data-testid 属性

## 运行测试

```bash
cd backend
pytest tests/
```

## 配置说明

### 环境变量

| 变量 | 描述 | 默认值 |
|------|------|--------|
| `OPENAI_API_KEY` | OpenAI API 密钥 | - |
| `OPENAI_API_BASE` | OpenAI API 地址（支持兼容 OpenAI 接口的模型） | `https://api.openai.com/v1` |
| `OPENAI_MODEL` | 使用的模型 | `gpt-4o` |
| `DATABASE_URL` | 数据库连接 | `sqlite:///./ai_playwright.db` |
| `BROWSER_TYPE` | 浏览器类型 | `chromium` |
| `HEADLESS` | 无头模式 | `false` |
| `VIEWPORT_WIDTH` | 视口宽度 | `1280` |
| `VIEWPORT_HEIGHT` | 视口高度 | `720` |
| `MAX_RETRIES` | 最大重试次数 | `3` |
| `TIMEOUT_MS` | 超时时间(毫秒) | `30000` |

## 未来展望

随着 MCP 生态的日益成熟，Playwright MCP Server 必将成为连接 AI 与数字世界的核心组件之一，释放出前所未有的自动化潜力。

## 许可证

MIT License

# Claude Code GitHub Actions 配置完整指南

## 📋 项目概述

**项目名称**: ip-monitor
**GitHub仓库**: https://github.com/likun206/ip-monitor
**目标**: 配置Claude Code GitHub Actions，实现通过@claude命令自动处理issue和PR
**当前状态**: 🟡 **99%完成 - 仅需正确的API密钥**

---

## 🎯 当前状态总结

### ✅ 已完成配置
- [x] Git仓库初始化和远程推送
- [x] CLAUDE.md项目配置文件
- [x] GitHub Actions工作流文件 (.github/workflows/claude-code.yml)
- [x] Claude Code GitHub App安装
- [x] GitHub Secrets配置 (ANTHROPIC_API_KEY)
- [x] 权限配置 (contents, issues, pull-requests, id-token)
- [x] Node.js环境配置
- [x] 工作流触发机制

### ❌ 待解决问题
- [ ] **API密钥格式问题** - 当前使用Claude CLI密钥 (sk-cli-v1-*)，需要标准Anthropic API密钥 (sk-ant-*)

### 🔧 错误诊断
根据最新日志分析，所有基础设施运行正常：
- Claude Code Action成功安装 (v1.0.112)
- GitHub权限验证通过 (admin级别)
- 分支创建成功 (claude/issue-1-20250918-1103)
- MCP服务器连接正常
- **唯一错误**: "Invalid API key · Fix external API key"

---

## 🛠️ 完整配置步骤

### 步骤1: 初始化Git仓库
```bash
# 在项目目录中
cd /Users/likun/Desktop/code/ai-social/ip_monitor
git init
git add .
git commit -m "Initial commit: IP monitor project"
```

### 步骤2: 创建GitHub远程仓库
1. 访问 https://github.com/new
2. 仓库名称: `ip-monitor`
3. 可见性: Public
4. 不勾选 "Add a README file"
5. 创建后获得仓库地址: https://github.com/likun206/ip-monitor

### 步骤3: 推送代码到远程仓库
```bash
git remote add origin https://github.com/likun206/ip-monitor.git
git branch -M main
git push -u origin main
```

### 步骤4: 创建CLAUDE.md项目配置文件
创建文件: `/CLAUDE.md`

```markdown
# Claude Code 项目配置

## 项目介绍
这是一个IP监控和变化通知工具，用于监控公网IP地址变化并发送通知。

## 代码规范
### Python代码规范
- 使用Python 3.7+
- 遵循PEP 8代码风格
- 使用类型提示（type hints）
- 函数和类需要添加文档字符串
- 使用logging模块记录日志
- 异常处理要具体明确

### 文件结构
- `ip_monitor.py` - 主程序文件
- `config.json` - 配置文件
- `ip_history.json` - IP历史记录
- `ip_monitor.log` - 日志文件

### 功能模块
1. **IP检测** - 获取当前公网IP地址
2. **变化监控** - 比较IP地址变化
3. **通知系统** - 发送邮件/微信通知
4. **历史记录** - 保存IP变化历史
5. **配置管理** - 读取和管理配置

### 开发指南
- 添加新功能时要保持代码的模块化
- 所有配置项都应该在config.json中定义
- 新增功能需要添加相应的日志记录
- 确保异常情况下程序能够正常运行

### 测试要求
- 重要功能需要添加单元测试
- 测试覆盖率应该达到80%以上
- 测试文件命名格式：test_*.py

## 依赖项
- requests - HTTP请求库
- smtplib - 邮件发送（Python标准库）
- json - JSON处理（Python标准库）
- logging - 日志记录（Python标准库）
- datetime - 时间处理（Python标准库）
```

### 步骤5: 创建GitHub Actions工作流文件
创建目录和文件: `/.github/workflows/claude-code.yml`

**最终配置 (经过多次优化)**:
```yaml
name: Claude Code Test

on:
  issue_comment:
    types: [created]

permissions:
  contents: write
  pull-requests: write
  issues: write
  id-token: write

jobs:
  claude:
    runs-on: ubuntu-latest
    steps:
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'

      - name: Checkout code
        uses: actions/checkout@v4

      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

### 步骤6: 推送配置文件
```bash
git add .
git commit -m "Add Claude Code configuration and GitHub Actions workflow"
git push
```

### 步骤7: 安装Claude Code GitHub App
1. 访问: https://github.com/apps/claude-code
2. 点击 "Install" 按钮
3. 选择账户: `likun206`
4. 为 `ip-monitor` 仓库安装App
5. 确认权限并完成安装

### 步骤8: 配置Anthropic API密钥
1. 访问仓库设置: https://github.com/likun206/ip-monitor/settings/secrets/actions
2. 点击 "New repository secret"
3. Name: `ANTHROPIC_API_KEY`
4. Value: [你的Anthropic API密钥]
5. 点击 "Add secret"

---

## 📊 配置历史和问题解决

### 配置迭代历史

#### 版本1: 初始复杂配置
```yaml
# 包含过多参数，导致 "Unexpected input parameters" 错误
max_tokens: 4000
temperature: 0.1
```
**问题**: 不支持的参数
**解决**: 移除不支持的参数

#### 版本2: 权限问题
**错误**: "Could not fetch an OIDC token"
**解决**: 添加 `id-token: write` 权限

#### 版本3: App安装问题
**错误**: "Claude Code is not installed on this repository"
**解决**: 安装Claude Code GitHub App

#### 版本4: Node.js问题
**错误**: 基于GitHub Issues #346的已知bug
**解决**: 添加Node.js安装步骤

#### 版本5: 当前状态
**错误**: "Invalid API key · Fix external API key"
**原因**: 使用了Claude CLI专用密钥 (sk-cli-v1-*) 而非API密钥 (sk-ant-*)

### 诊断日志分析
最新成功运行的部分：
- ✅ Bun安装成功
- ✅ 149个包安装成功
- ✅ Claude Code v1.0.112安装成功
- ✅ OIDC token获取成功
- ✅ GitHub权限验证通过 (admin)
- ✅ 分支 `claude/issue-1-20250918-1103` 创建成功
- ✅ Git配置成功 (claude[bot])
- ✅ MCP服务器连接成功
- ❌ API密钥验证失败

---

## 🔑 API密钥配置说明

### Claude MAX Plan vs API密钥
根据官方文档 (GitHub Issue #4):
- **Claude Code GitHub Actions目前不支持Max订阅认证**
- **必须使用标准的Anthropic API密钥**
- Max订阅用户需要单独创建API密钥

### 密钥格式说明
- **Claude CLI密钥**: `sk-cli-v1-*` (仅用于本地Claude CLI)
- **Anthropic API密钥**: `sk-ant-*` (用于API调用和GitHub Actions)

### 获取正确的API密钥
1. 访问: https://console.anthropic.com/
2. 登录你的Anthropic账户
3. 创建新的API密钥 (确保是API用途，不是CLI用途)
4. 复制以 `sk-ant-` 开头的密钥
5. 在GitHub Secrets中更新 `ANTHROPIC_API_KEY`

---

## 🧪 测试使用方法

### 基本测试
1. 在任何issue中添加评论: `@claude hello`
2. 观察Actions页面: https://github.com/likun206/ip-monitor/actions

### 实际功能测试
创建issue并评论:
```
@claude 请帮我添加单元测试功能

请帮我：
1. 创建一个tests目录
2. 为ip_monitor.py中的主要功能添加单元测试
3. 添加一个requirements.txt文件，包含必要的依赖项
4. 确保测试能够覆盖IP获取、配置读取等核心功能
```

### 期望结果
Claude会自动：
1. 分析代码和需求
2. 创建单元测试文件
3. 生成requirements.txt
4. 提交到新分支
5. 创建PR供review

---

## 🚀 其他同事使用此配置

### 前置条件
- GitHub账户和仓库
- Anthropic账户和API密钥
- 项目代码准备就绪

### 快速配置清单
1. [ ] 创建/克隆GitHub仓库
2. [ ] 复制 `CLAUDE.md` 到项目根目录
3. [ ] 复制 `.github/workflows/claude-code.yml` 到对应目录
4. [ ] 安装Claude Code GitHub App
5. [ ] 在console.anthropic.com创建API密钥
6. [ ] 在GitHub Secrets中添加 `ANTHROPIC_API_KEY`
7. [ ] 推送代码并测试

### 自定义配置
- 修改 `CLAUDE.md` 中的项目规范和开发指南
- 根据项目需要调整工作流触发条件
- 添加项目特定的权限配置

---

## 📋 故障排除

### 常见错误和解决方案

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| "Unexpected input parameters" | 使用了不支持的配置参数 | 移除不支持的参数 |
| "Could not fetch an OIDC token" | 缺少必需的权限 | 添加 `id-token: write` 权限 |
| "Claude Code is not installed" | 未安装GitHub App | 安装Claude Code GitHub App |
| "Invalid API key" | API密钥格式错误或无效 | 使用标准Anthropic API密钥 |
| "Process completed with exit code 1" | 通常是API密钥问题 | 检查API密钥配置 |

### 调试方法
1. 查看Actions页面的详细日志
2. 检查GitHub Secrets配置
3. 验证API密钥有效性
4. 确认App安装状态

### 联系支持
- Claude Code文档: https://docs.claude.com/en/docs/claude-code/github-actions
- GitHub Issues: https://github.com/anthropics/claude-code-action/issues

---

## 📈 项目状态

**创建时间**: 2025年9月18日
**最后更新**: 2025年9月18日
**配置完成度**: 99%
**下一步**: 更新为正确的Anthropic API密钥

**文件清单**:
- ✅ `CLAUDE.md` - 项目配置文件
- ✅ `.github/workflows/claude-code.yml` - GitHub Actions工作流
- ✅ 基础项目文件 (ip_monitor.py, config.json等)
- ✅ Claude Code GitHub App已安装
- 🟡 `ANTHROPIC_API_KEY` - 需要更新为正确格式

**测试状态**:
- ✅ 工作流能够成功触发
- ✅ 所有基础设施运行正常
- ❌ API认证失败 (密钥格式问题)

---

## 🔮 未来优化建议

1. **监控使用情况**: 跟踪API调用成本和频率
2. **扩展功能**: 配置更多触发条件 (PR review, issue labels等)
3. **安全增强**: 定期轮换API密钥
4. **文档完善**: 根据实际使用经验更新配置指南
5. **团队推广**: 将配置模板化，方便其他项目使用

---

*📝 此文档由Claude Code配置过程自动生成，包含完整的配置历史和故障排除信息。*
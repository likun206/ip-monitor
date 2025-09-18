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
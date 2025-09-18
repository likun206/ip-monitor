# IP监控工具

这个工具可以监控你的公网IP地址和地理位置变化。

## 功能特性

- 检测公网IP地址变化
- 监控IP地理位置变化（国家、地区、城市、ISP）
- 记录历史变化日志
- 支持一次性检测和持续监控
- 可配置检测间隔和API服务

## 使用方法

### 1. 安装依赖
```bash
pip install requests
```

### 2. 运行脚本

#### 单次检测
```bash
cd /Users/likun/Desktop/code/ai-social/ip_monitor
python ip_monitor.py once
```

#### 持续监控
```bash
# 使用配置文件中的默认间隔（300秒/5分钟）
python ip_monitor.py monitor

# 自定义检测间隔（秒数）
python ip_monitor.py monitor 60      # 每分钟检测一次
python ip_monitor.py monitor 1800    # 每30分钟检测一次
python ip_monitor.py monitor 3600    # 每小时检测一次
```

#### 查看历史记录
```bash
python ip_monitor.py history
```

## 配置说明

编辑 `config.json` 文件可以自定义配置：

- `check_interval`: 检测间隔（秒），默认300秒（5分钟）
- `ip_apis`: IP地址获取API列表，支持多个备用API
- `location_api`: 地理位置查询API

## 输出文件

- `ip_history.json`: IP变化历史记录
- `ip_monitor.log`: 运行日志文件
- `config.json`: 配置文件

## 测试建议

1. 先运行单次检测：`python ip_monitor.py once`
2. 如果需要持续监控：
   - 使用默认间隔：`python ip_monitor.py monitor`
   - 自定义间隔：`python ip_monitor.py monitor 60`
3. 可以通过VPN等方式改变IP来测试变化检测功能
4. 使用 `python ip_monitor.py history` 查看所有变化记录

## 命令行参数说明

- `once`: 运行一次检测
- `monitor`: 持续监控模式
- `monitor <秒数>`: 持续监控并指定检测间隔
- `history`: 查看历史记录

## 注意事项

- 需要网络连接才能正常工作
- 免费API有请求频率限制，不建议设置小于10秒的检测间隔
- 持续监控模式可以通过 Ctrl+C 停止
- 间隔时间可以通过命令行参数或配置文件设置
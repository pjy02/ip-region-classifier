# GitHub Codespaces 使用指南

## 🚀 快速开始

### 1. 创建 Codespace
1. 在GitHub仓库页面点击 **Code** 按钮
2. 选择 **Codespaces** 标签
3. 点击 **New codespace** 或 **Create codespace**
4. 等待环境构建完成（通常2-3分钟）

### 2. 环境验证
Codespaces启动后会自动运行初始化脚本，你可以看到：
```
🚀 ================================================
🚀 IP地区分类工具 - GitHub Codespaces 环境
🚀 ================================================
📋 系统信息:
   - 操作系统: Linux
   - Python版本: Python 3.11.x
   - 工作目录: /workspaces/ip-region-classifier
📦 安装Python依赖...
   ✅ 依赖安装成功
✨ 环境准备完成！开始使用吧！
```

## 📖 使用方法

### 基本使用
```bash
# 查看帮助
python iptest.py --help

# 基本查询（使用默认5线程）
python iptest.py ips.txt

# 使用8线程并发查询
python iptest.py ips.txt -t 8

# 交互模式
python iptest.py
```

### 文件管理
- **输入文件**: `ips.txt` - 包含要查询的IP地址列表
- **输出文件**: `iptest_results.json` - 详细的查询结果
- **分类文件**: `country_files/` - 按国家分类的IP列表

### 结果下载
1. 在VS Code左侧文件浏览器中找到结果文件
2. 右键点击文件选择 **Download**
3. 或者使用命令行：
   ```bash
   # 下载到本地（需要配置GitHub CLI）
   gh codespace cp -c /workspaces/ip-region-classifier/iptest_results.json ./
   ```

## ⚡ 性能优化

### 线程数建议
- **免费Codespaces**: 2核CPU，建议5-8线程
- **付费Codespaces**: 4核CPU，建议8-12线程
- **最大线程数**: 不超过20（避免API限制）

### 批量处理建议
```bash
# 小批量测试（10-50个IP）
python iptest.py small_batch.txt -t 5

# 中等批量（50-500个IP）
python iptest.py medium_batch.txt -t 8

# 大批量（500+个IP）
python iptest.py large_batch.txt -t 10
```

## 🔧 环境配置

### VS Code 扩展
Codespaces已预装以下扩展：
- Python 扩展包
- Pylance 语言服务器
- 代码格式化工具

### 自定义配置
你可以修改 `.devcontainer/devcontainer.json` 来自定义环境：
```json
{
  "name": "IP Region Classifier",
  "image": "mcr.microsoft.com/devcontainers/python:1-3.11-bullseye",
  "settings": {
    "python.pythonPath": "/usr/local/bin/python"
  },
  "extensions": [
    "ms-python.python"
  ]
}
```

## 🌐 网络配置

### API 访问
项目使用 `ipapi.is` API，Codespaces提供稳定的公网访问。

### 代理设置
如果需要使用代理，可以在终端中设置：
```bash
# 设置HTTP代理
export HTTP_PROXY="http://proxy.example.com:8080"
export HTTPS_PROXY="http://proxy.example.com:8080"

# 或者为当前会话设置
python iptest.py ips.txt
```

## 📊 监控和调试

### 资源监控
```bash
# 查看CPU使用
top

# 查看内存使用
free -h

# 查看磁盘使用
df -h
```

### 日志查看
```bash
# 查看实时输出
tail -f /tmp/codespaces.log

# 查看系统日志
journalctl -f
```

## 🚨 故障排除

### 常见问题

#### 1. 依赖安装失败
```bash
# 手动重新安装
pip install --upgrade pip
pip install -r requirements.txt
```

#### 2. API连接问题
```bash
# 测试API连接
curl -I https://api.ipapi.is

# 检查网络连接
ping -c 3 api.ipapi.is
```

#### 3. 权限问题
```bash
# 确保脚本有执行权限
chmod +x .devcontainer/codespaces-start.sh

# 检查文件权限
ls -la iptest.py
```

### 性能问题
- **查询速度慢**: 减少线程数到3-5个
- **内存不足**: 分批处理IP列表
- **CPU占用高**: 降低并发线程数

## 💡 最佳实践

### 开发工作流
1. **本地开发**: 在Codespaces中编写和测试代码
2. **版本控制**: 使用Git提交和推送更改
3. **团队协作**: 分享Codespaces链接给团队成员
4. **部署准备**: 在Codespaces中测试完整流程

### 数据管理
- **及时备份**: 定期下载重要的查询结果
- **清理文件**: 删除不需要的临时文件
- **版本控制**: 使用Git管理代码版本

### 安全考虑
- **敏感数据**: 不要在Codespaces中处理敏感IP数据
- **API密钥**: 使用环境变量存储，不要硬编码
- **访问控制**: 设置适当的仓库访问权限

## 📚 扩展功能

### 添加新API
修改 `iptest.py` 中的 `get_ip_location` 方法：
```python
def get_ip_location(self, ip: str) -> Optional[Dict]:
    # 添加新的API支持
    pass
```

### 自定义输出
修改 `save_results` 方法来支持不同的输出格式。

### 集成其他工具
可以集成到CI/CD流程中，或与其他网络工具配合使用。

## 📞 支持

如果遇到问题，请：
1. 检查本文档的故障排除部分
2. 查看项目的GitHub Issues
3. 创建新的Issue描述问题
4. 提供详细的错误信息和环境描述

---

**提示**: Codespaces有使用时长限制，请及时保存重要工作并下载结果文件。
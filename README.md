# IP地区分类工具

一个基于Python的IP地址地理位置查询和分类工具，支持多线程并发查询，可以快速批量处理大量IP地址。支持GitHub Codespaces、Docker部署和多种运行方式。

## 🚀 快速开始

### GitHub Codespaces (推荐)

点击下方按钮直接在浏览器中打开和运行项目：

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=YOUR_USERNAME/ip-region-classifier)

### 本地运行

```bash
# 克隆项目
git clone https://github.com/YOUR_USERNAME/ip-region-classifier.git
cd ip-region-classifier

# 安装依赖
pip install -r requirements.txt

# 运行程序
python iptest.py
```

### Docker运行

```bash
# 构建镜像
docker build -t ip-region-classifier .

# 运行容器
docker run -v $(pwd)/data:/app/data -v $(pwd)/output:/app/output ip-region-classifier

# 或使用Docker Compose
docker-compose up ip-classifier
```

## 📦 项目目录结构

```
dns 地区分类/
├── README.md                 # 项目说明文档
├── iptest.py                # 主程序脚本
├── requirements.txt         # Python依赖包列表
├── ips.txt                  # 默认IP地址输入文件
├── iptest_results.json      # 默认JSON格式输出文件
├── ip_classification_results.json  # 旧版JSON输出文件
├── country_files/           # 国家分类文件目录
├── Dockerfile               # Docker镜像配置
├── docker-compose.yml       # Docker Compose配置
├── .devcontainer/           # Codespaces配置目录
│   ├── devcontainer.json    # 开发容器配置
│   ├── codespaces-start.sh  # 启动脚本
│   └── README.md            # Codespaces使用指南
└── .github/workflows/       # GitHub Actions工作流
    └── ci.yml               # CI/CD配置
```

## 文件说明

### 📄 README.md
项目的主要说明文档，包含项目介绍、功能特点、使用方法、安装指南和故障排除等信息。

### 🐍 iptest.py
**主程序脚本**，项目的核心文件，包含以下主要功能：
- **IPClassifier类**：主要的IP分类器类，负责与ipapi.is API交互
- **地理位置查询**：使用ipapi.is API获取IP的详细地理位置信息
- **中文翻译**：内置完整的中文翻译映射表，支持国家、地区、城市等信息的中文显示
- **增量更新**：支持JSON结果文件的增量更新，新IP添加，旧IP覆盖
- **IP排序**：支持按IP数值大小排序，确保输出结果有序
- **批量处理**：支持批量处理多个IP地址，自动添加延迟避免API限制
- **多格式输出**：支持JSON格式输出和国家分类文件输出
- **多线程并发**：支持多线程并发查询，大幅提升处理速度

### 📦 requirements.txt
**Python依赖包列表**，定义了项目运行所需的第三方库：
- `requests>=2.25.0`：用于发送HTTP请求到ipapi.is API

### 📝 ips.txt
**默认IP地址输入文件**，包含待处理的IP地址列表。每行一个IP地址，例如：
```
47.239.155.200
8.217.228.46
38.165.7.95
```

### 📊 iptest_results.json
**默认JSON格式输出文件**，存储IP分类结果的JSON格式数据。按国家/地区分类，包含每个IP的详细信息，如：
- 基本信息：IP地址、国家、地区代码、城市、经纬度
- 网络信息：ASN、组织、路由、类型
- 安全信息：是否为VPN、代理、数据中心、滥用者等
- 时间信息：时区、本地时间、UTC偏移等
- 公司信息：公司名称、类型、网络范围、滥用联系人等

### 📊 ip_classification_results.json
**旧版JSON输出文件**，与iptest_results.json功能相同，为保持兼容性而保留。

### 📁 country_files/
**国家分类文件目录**，用于存储按国家/地区分类的文本文件。每个文件以国家代码命名（如US.txt、CN.txt），包含对应国家的所有IP地址，按数值大小排序。

### 🐳 Dockerfile
**Docker镜像配置文件**，定义了项目的Docker镜像构建过程，支持一键容器化部署。

### 🐳 docker-compose.yml
**Docker Compose配置文件**，支持多容器编排和一键启动服务。

### 🌐 .devcontainer/
**Codespaces配置目录**，包含GitHub Codespaces的完整配置，支持一键云端开发环境。

### 🔄 .github/workflows/
**GitHub Actions工作流目录**，包含CI/CD自动化流程配置。

## 功能特点

### 🌍 完整的地理位置信息
- 使用ipapi.is API获取准确的IP地理位置数据
- 支持全球所有国家和地区的IP定位
- 提供详细的省/州、城市、经纬度信息

### 🏷️ 智能分类功能
- 按国家/地区自动分类IP地址
- 支持中文显示国家、地区、城市名称
- 提供详细的分类统计和摘要信息

### 💾 增量更新支持
- 支持JSON结果文件的增量更新
- 新IP自动添加到现有结果中
- 重复IP自动覆盖更新信息
- 保持历史数据的完整性

### 📊 IP排序功能
- 支持按IP数值大小排序
- 确保输出结果中的IP地址有序排列
- 提高结果的可读性和使用便利性

### 🔧 灵活的配置选项
- 支持命令行参数和交互式操作
- 可自定义输入文件、输出文件路径
- 支持API密钥配置（提高请求限制）

### ⚡ 批量处理能力
- 支持批量处理大量IP地址
- 自动添加请求延迟避免API限制
- 提供实时处理进度显示

## 📋 系统要求

- Python 3.7+
- requests库
- 网络连接（访问ipapi.is API）
- 可选：Docker、Docker Compose

## 🔧 安装依赖

### 本地安装
```bash
pip install -r requirements.txt
```

### Docker安装
```bash
# 确保已安装Docker和Docker Compose
docker --version
docker-compose --version
```

### GitHub Codespaces
无需安装，直接在浏览器中使用！

## 🎯 使用方法

### 1. 命令行模式

```bash
# 使用默认设置运行
python iptest.py

# 指定输入文件
python iptest.py -i your_ip_list.txt

# 指定输出文件
python iptest.py -o custom_results.json

# 指定API密钥
python iptest.py -k your_api_key

# 指定国家文件输出目录
python iptest.py -c ./country_output

# 指定线程数（多线程模式）
python iptest.py -t 8

# 查看帮助
python iptest.py --help
```

### 2. 交互式模式

运行脚本后，按照提示操作：
```
IP地区分类工具
使用ipapi.is API服务

请输入包含IP地址的文件路径 [默认: ips.txt]: 
请输入ipapi.is的API密钥 [可选，直接回车跳过]: 
请输入输出文件名 [默认: iptest_results.json]: 
请输入国家文件输出目录 [可选，直接回车跳过]: 
请输入线程数 [默认: 5]: 
```

### 3. Docker模式

```bash
# 使用Docker运行
sudo docker run -v $(pwd)/ips.txt:/app/ips.txt -v $(pwd)/output:/app/output ip-region-classifier

# 指定线程数
sudo docker run -e MAX_THREADS=10 -v $(pwd)/ips.txt:/app/ips.txt ip-region-classifier python iptest.py ips.txt -t 10
```

### 4. Docker Compose模式

```bash
# 启动服务
docker-compose up ip-classifier

# 后台运行
docker-compose up -d

# 查看日志
docker-compose logs -f
```

### 3. 输入文件格式

创建一个文本文件，每行一个IP地址：
```
8.8.8.8
1.1.1.1
114.114.114.114
223.5.5.5
208.67.222.222
```

## 输出示例

### 控制台输出

```
IP地区分类工具
使用ipapi.is API服务

加载了 3 个IP地址
开始处理 3 个IP地址...
处理进度: 1/3 (33.3%) - 47.239.155.200
处理进度: 2/3 (66.7%) - 8.217.228.46
处理进度: 3/3 (100.0%) - 38.165.7.95

=== IP地区分类摘要 ===
总共处理了 3 个IP地址
涉及 2 个国家/地区

中国香港: 2 个IP
  - 8.217.228.46 (中国香港, 中西区)
  - 47.239.155.200 (中国香港, 中西区)

美国: 1 个IP
  - 38.165.7.95 (美国, 加利福尼亚州, San Jose)

结果已保存到: iptest_results.json

处理完成！
```

### JSON输出文件结构

```json
{
  "中国香港": [
    {
      "IP地址": "8.217.228.46",
      "国家": "中国香港",
      "国家代码": "HK",
      "地区/州": "中西区",
      "城市": "中国香港",
      "纬度": 22.2783,
      "经度": 114.175,
      "自治系统号": 45102,
      "组织": "Alibaba (US) Technology Co., Ltd.",
      "是否为数据中心": true,
      "是否为VPN": true,
      "公司名称": "Aliyun Computing Co.LTD",
      "公司类型": "企业"
    }
  ],
  "美国": [
    {
      "IP地址": "38.165.7.95",
      "国家": "美国",
      "国家代码": "US",
      "地区/州": "加利福尼亚州",
      "城市": "San Jose",
      "纬度": 37.33939,
      "经度": -121.89496,
      "自治系统号": 23470,
      "组织": "ReliableSite.Net LLC",
      "是否为数据中心": true,
      "是否为VPN": true,
      "公司名称": "PEG Tech Inc.",
      "公司类型": "托管服务"
    }
  ]
}
```

### 国家分类文件

在country_files目录下生成按国家分类的文本文件：

**HK.txt**:
```
8.217.228.46
47.239.155.200
```

**US.txt**:
```
38.165.7.95
```

## API说明

### ipapi.is API
- **API地址**: https://api.ipapi.is/
- **免费版本**: 每月1000次请求，建议每秒最多1次请求
- **付费版本**: 更高的请求限制和更快的响应时间
- **API密钥**: 可选参数，使用免费版本可以跳过

### 请求限制处理
- 脚本自动在每次请求间添加1秒延迟
- 包含错误处理和重试机制
- 提供详细的错误信息和处理建议

## 高级功能

### 增量更新
- 支持在现有结果文件基础上添加新IP
- 自动检测并更新已存在IP的信息
- 保持历史数据的完整性和一致性

### IP排序
- 支持按IP数值大小排序
- 确保输出结果中的IP地址有序排列
- 提高结果的可读性和后续处理的便利性

### 中文翻译
- 内置完整的中文翻译映射表
- 支持国家、地区、城市、公司类型等信息的中文显示
- 提供更好的中文用户体验

## 故障排除

### 常见问题

**Q: 出现"API错误"提示**
A: 可能是API服务暂时不可用或达到请求限制，请稍后重试或检查API密钥

**Q: 网络请求错误**
A: 检查网络连接，确保能够访问外网和ipapi.is服务

**Q: JSON解析错误**
A: API返回格式可能发生变化，请检查脚本版本是否为最新

**Q: 文件权限错误**
A: 确保对输出目录有写入权限，或使用不同的输出路径

### 调试建议

1. **检查网络连接**: 确保能够访问 https://api.ipapi.is/
2. **验证API密钥**: 如果使用付费版本，确保API密钥正确
3. **检查IP格式**: 确保输入文件中的IP地址格式正确
4. **查看详细日志**: 修改脚本中的日志级别获取更多信息
5. **分批测试**: 先用少量IP测试，确认功能正常后再处理大量IP

## 更新日志

### v2.0 (当前版本)
- 重构项目结构，将主文件从ip_classifier.py改为iptest.py
- 实现增量更新功能，支持新IP添加和旧IP覆盖
- 添加IP排序功能，确保输出结果有序
- 完善中文翻译映射表，支持更多字段翻译
- 优化错误处理和用户体验
- 更新默认输出文件名为iptest_results.json

### v1.0
- 初始版本，支持基本的IP地理位置分类
- 使用ipapi.co API服务
- 支持JSON格式输出
- 基础的中文翻译功能

## 许可证

本项目采用MIT许可证。

## 贡献

欢迎提交Issue和Pull Request来改进这个工具。如果您发现任何问题或有改进建议，请通过GitHub Issues联系我们。

## 联系方式

如有问题或建议，请通过GitHub Issues联系。我们会尽快回复并处理您的问题。
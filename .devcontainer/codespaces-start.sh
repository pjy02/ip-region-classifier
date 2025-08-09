#!/bin/bash

# GitHub Codespaces 启动脚本
# IP地区分类工具 - 环境初始化

echo "🚀 ================================================"
echo "🚀 IP地区分类工具 - GitHub Codespaces 环境"
echo "🚀 ================================================"

# 显示系统信息
echo "📋 系统信息:"
echo "   - 操作系统: $(uname -s)"
echo "   - 内核版本: $(uname -r)"
echo "   - Python版本: $(python --version 2>&1)"
echo "   - 工作目录: $(pwd)"
echo ""

# 检查必要文件
echo "🔍 检查项目文件..."
required_files=("iptest.py" "requirements.txt" "ips.txt")
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✅ $file - 存在"
    else
        echo "   ❌ $file - 缺失"
    fi
done
echo ""

# 安装依赖
echo "📦 安装Python依赖..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo "   ✅ 依赖安装成功"
    else
        echo "   ❌ 依赖安装失败"
    fi
else
    echo "   ❌ requirements.txt 文件不存在"
fi
echo ""

# 检查网络连接
echo "🌐 检查网络连接..."
if curl -s --connect-timeout 5 https://api.ipapi.is > /dev/null 2>&1; then
    echo "   ✅ API服务连接正常"
else
    echo "   ⚠️  API服务连接可能存在问题"
fi
echo ""

# 显示使用说明
echo "📖 使用说明:"
echo "   ================================================"
echo "   基本用法:"
echo "     python iptest.py ips.txt"
echo "   "
echo "   多线程查询 (推荐5-10线程):"
echo "     python iptest.py ips.txt -t 8"
echo "   "
echo "   交互模式:"
echo "     python iptest.py"
echo "   "
echo "   查看帮助:"
echo "     python iptest.py --help"
echo "   ================================================"
echo ""

# 显示项目信息
echo "📊 项目信息:"
echo "   - 项目名称: IP地区分类工具"
echo "   - 功能: 使用ipapi.is API进行IP地理位置查询"
echo "   - 特性: 多线程并发查询、中文翻译、增量更新"
echo "   - 输出: JSON格式结果 + 按国家分类的文本文件"
echo ""

# 显示示例IP数量
if [ -f "ips.txt" ]; then
    ip_count=$(wc -l < ips.txt | tr -d ' ')
    echo "📈 当前IP列表包含 $ip_count 个IP地址"
    echo "   预计处理时间: 约 $((ip_count / 10 / 60)) 分钟 (使用10线程)"
else
    echo "⚠️  请在ips.txt中添加要查询的IP地址"
fi
echo ""

echo "✨ 环境准备完成！开始使用吧！"
echo "🔗 提示: 在VS Code中按Ctrl+` 打开终端开始使用"
echo ""
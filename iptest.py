#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IP地区分类脚本
使用ipapi.is API服务对IP进行地理位置分类
"""

import os
import sys
import requests
import json
import time
import argparse
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional
from collections import defaultdict

# 中文翻译映射表
CHINESE_TRANSLATIONS = {
    # 国家名称映射
    'United States': '美国',
    'China': '中国',
    'Hong Kong': '中国香港',
    'Taiwan': '中国台湾',
    'Japan': '日本',
    'South Korea': '韩国',
    'Singapore': '新加坡',
    'Germany': '德国',
    'United Kingdom': '英国',
    'France': '法国',
    'Canada': '加拿大',
    'Australia': '澳大利亚',
    'Russia': '俄罗斯',
    'India': '印度',
    'Brazil': '巴西',
    'Netherlands': '荷兰',
    'Sweden': '瑞典',
    'Switzerland': '瑞士',
    'Spain': '西班牙',
    'Italy': '意大利',
    'Unknown': '未知',
    
    # 地区名称映射（常见地区）
    'California': '加利福尼亚州',
    'New York': '纽约州',
    'Texas': '德克萨斯州',
    'Florida': '佛罗里达州',
    'Beijing': '北京',
    'Shanghai': '上海',
    'Guangdong': '广东',
    'Zhejiang': '浙江',
    'Jiangsu': '江苏',
    'Tokyo': '东京',
    'Osaka': '大阪',
    'Seoul': '首尔',
    'Berlin': '柏林',
    'London': '伦敦',
    'Paris': '巴黎',
    'Sydney': '悉尼',
    'Moscow': '莫斯科',
    'Mumbai': '孟买',
    'São Paulo': '圣保罗',
    'Amsterdam': '阿姆斯特丹',
    'Stockholm': '斯德哥尔摩',
    'Zurich': '苏黎世',
    'Madrid': '马德里',
    'Rome': '罗马',
    'Central and Western': '中西区',
    
    # 大洲映射
    'Asia': '亚洲',
    'North America': '北美洲',
    'South America': '南美洲',
    'Europe': '欧洲',
    'Africa': '非洲',
    'Oceania': '大洋洲',
    'Antarctica': '南极洲',
    
    # 公司类型映射
    'hosting': '托管服务',
    'isp': '互联网服务提供商',
    'business': '企业',
    'education': '教育机构',
    'government': '政府机构',
    
    # 字段名称映射
    'ip': 'IP地址',
    'country': '国家',
    'country_code': '国家代码',
    'region': '地区/州',
    'city': '城市',
    'latitude': '纬度',
    'longitude': '经度',
    'asn': '自治系统号',
    'org': '组织',
    'timezone': '时区',
    'utc_offset': 'UTC偏移',
    'country_calling_code': '国家电话代码',
    'currency': '货币',
    'languages': '语言',
    'country_flag': '国旗',
    'country_flag_emoji': '国旗表情',
    'country_area': '国家面积',
    'country_population': '国家人口',
    'continent': '大洲',
    'in_eu': '是否在欧盟',
    'postal': '邮政编码',
    
    # 新增完整API字段映射
    'rir': '区域互联网注册机构',
    'is_bogon': '是否为保留IP',
    'is_mobile': '是否为移动网络',
    'is_satellite': '是否为卫星网络',
    'is_crawler': '是否为爬虫',
    'is_datacenter': '是否为数据中心',
    'is_tor': '是否为Tor网络',
    'is_proxy': '是否为代理',
    'is_vpn': '是否为VPN',
    'is_abuser': '是否为滥用者',
    'is_eu_member': '是否为欧盟成员国',
    'is_dst': '是否为夏令时',
    'abuser_score': '滥用评分',
    'route': '路由',
    'descr': '描述',
    'active': '是否活跃',
    'domain': '域名',
    'abuse': '滥用联系人',
    'type': '类型',
    'updated': '更新时间',
    'network': '网络',
    'datacenter': '数据中心',
    'name': '名称',
    'address': '地址',
    'email': '邮箱',
    'phone': '电话',
    'calling_code': '电话代码',
    'currency_code': '货币代码',
    'state': '州/省',
    'zip': '邮编',
    'local_time': '本地时间',
    'local_time_unix': '本地时间戳',
    'elapsed_ms': '耗时(毫秒)',
    
    # 嵌套对象名称映射
    'company': '公司信息',
    'abuse': '滥用联系人信息',
    'asn': '自治系统信息',
    'location': '位置信息'
}

def translate_to_chinese(text: str) -> str:
    """
    将文本翻译成中文
    :param text: 原始文本
    :return: 中文翻译
    """
    if not text:
        return text
    return CHINESE_TRANSLATIONS.get(text, text)

class IPClassifier:
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化IP分类器
        :param api_key: ipapi.is的API密钥
        """
        self.api_base_url = "https://api.ipapi.is/"
        self.api_key = api_key or "11111111111111111111111111111111"

        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'IP-Classifier/1.0'
        })
        
    def get_ip_location(self, ip: str) -> Optional[Dict]:
        """
        获取IP的完整地理位置信息
        :param ip: IP地址
        :return: 包含完整地理位置信息的字典，如果失败返回None
        """
        try:
            url = f"{self.api_base_url}"
            params = {
                'q': ip,
                'key': self.api_key
            }
                
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # 检查API返回是否有效
            if data.get('error'):
                print(f"API错误 for IP {ip}: {data.get('error', 'Unknown error')}")
                return None
            
            # 直接使用官方API的原始结构，不翻译值
            translated_data = {
                'ip': data.get('ip', ip),
                'rir': data.get('rir'),
                'is_bogon': data.get('is_bogon'),
                'is_mobile': data.get('is_mobile'),
                'is_satellite': data.get('is_satellite'),
                'is_crawler': data.get('is_crawler'),
                'is_datacenter': data.get('is_datacenter'),
                'is_tor': data.get('is_tor'),
                'is_proxy': data.get('is_proxy'),
                'is_vpn': data.get('is_vpn'),
                'is_abuser': data.get('is_abuser'),
                'elapsed_ms': data.get('elapsed_ms'),
                
                # company信息（嵌套结构）
                'company': {
                    'name': data.get('company', {}).get('name'),
                    'abuser_score': data.get('company', {}).get('abuser_score'),
                    'domain': data.get('company', {}).get('domain'),
                    'type': data.get('company', {}).get('type'),
                    'network': data.get('company', {}).get('network'),
                    'whois': data.get('company', {}).get('whois')
                },
                
                # abuse信息（嵌套结构）
                'abuse': {
                    'name': data.get('abuse', {}).get('name'),
                    'address': data.get('abuse', {}).get('address'),
                    'email': data.get('abuse', {}).get('email'),
                    'phone': data.get('abuse', {}).get('phone')
                },
                
                # asn信息（嵌套结构）
                'asn': {
                    'asn': data.get('asn', {}).get('asn'),
                    'abuser_score': data.get('asn', {}).get('abuser_score'),
                    'route': data.get('asn', {}).get('route'),
                    'descr': data.get('asn', {}).get('descr'),
                    'country': data.get('asn', {}).get('country'),
                    'active': data.get('asn', {}).get('active'),
                    'org': data.get('asn', {}).get('org'),
                    'domain': data.get('asn', {}).get('domain'),
                    'abuse': data.get('asn', {}).get('abuse'),
                    'type': data.get('asn', {}).get('type'),
                    'updated': data.get('asn', {}).get('updated'),
                    'rir': data.get('asn', {}).get('rir'),
                    'whois': data.get('asn', {}).get('whois')
                },
                
                # location信息（嵌套结构）
                'location': {
                    'is_eu_member': data.get('location', {}).get('is_eu_member'),
                    'calling_code': data.get('location', {}).get('calling_code'),
                    'currency_code': data.get('location', {}).get('currency_code'),
                    'continent': data.get('location', {}).get('continent'),
                    'country': data.get('location', {}).get('country'),
                    'country_code': data.get('location', {}).get('country_code'),
                    'state': data.get('location', {}).get('state'),
                    'city': data.get('location', {}).get('city'),
                    'latitude': data.get('location', {}).get('latitude'),
                    'longitude': data.get('location', {}).get('longitude'),
                    'zip': data.get('location', {}).get('zip'),
                    'timezone': data.get('location', {}).get('timezone'),
                    'local_time': data.get('location', {}).get('local_time'),
                    'local_time_unix': data.get('location', {}).get('local_time_unix'),
                    'is_dst': data.get('location', {}).get('is_dst')
                }
            }
            
            # 将布尔值转换为中文描述
            for key, value in translated_data.items():
                if isinstance(value, bool) and key.startswith('is_'):
                    translated_data[key] = '是' if value else '否'
            
            # 处理嵌套结构中的布尔值
            for section in ['company', 'abuse', 'asn', 'location']:
                if section in translated_data and isinstance(translated_data[section], dict):
                    for key, value in translated_data[section].items():
                        if isinstance(value, bool):
                            translated_data[section][key] = '是' if value else '否'
                        elif isinstance(value, str):
                            translated_data[section][key] = translate_to_chinese(value)
            
            return translated_data
            
        except requests.RequestException as e:
            print(f"网络请求错误 for IP {ip}: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON解析错误 for IP {ip}: {e}")
            return None
        except Exception as e:
            print(f"未知错误 for IP {ip}: {e}")
            return None
    
    def classify_ips_by_country(self, ip_list: list[str], max_workers: int = 5) -> tuple[dict[str, list[dict]], list[str]]:
        """
        按国家对IP列表进行分类（多线程并发版本）
        :param ip_list: IP地址列表
        :param max_workers: 最大线程数，默认为5
        :return: (按国家分类的IP信息字典, 失败的IP列表)
        """
        classified_ips = defaultdict(list)
        failed_ips = []
        total_ips = len(ip_list)
        
        print(f"开始处理 {total_ips} 个IP地址...")
        print(f"使用 {max_workers} 个线程并发查询...")
        
        # 创建线程锁，用于线程安全的进度更新
        progress_lock = threading.Lock()
        completed_count = 0
        
        def process_single_ip(ip):
            """
            处理单个IP的函数，供线程池使用
            """
            nonlocal completed_count
            
            try:
                location_data = self.get_ip_location(ip)
                
                with progress_lock:
                    completed_count += 1
                    progress = completed_count / total_ips * 100
                    print(f"处理进度: {completed_count}/{total_ips} ({progress:.1f}%) - {ip}")
                
                if location_data:
                    return ip, location_data, None
                else:
                    return ip, None, "查询失败"
                    
            except Exception as e:
                with progress_lock:
                    completed_count += 1
                    progress = completed_count / total_ips * 100
                    print(f"处理进度: {completed_count}/{total_ips} ({progress:.1f}%) - {ip} (错误: {str(e)})")
                return ip, None, str(e)
        
        # 使用线程池并发处理
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交所有任务
            future_to_ip = {executor.submit(process_single_ip, ip): ip for ip in ip_list}
            
            # 处理完成的任务
            for future in as_completed(future_to_ip):
                ip, location_data, error = future.result()
                
                if location_data:
                    # 从嵌套结构中获取国家信息
                    if 'location' in location_data and 'country' in location_data['location']:
                        country = location_data['location']['country']
                    else:
                        # 如果没有位置信息，使用默认值
                        country = 'Unknown'
                    classified_ips[country].append(location_data)
                else:
                    failed_ips.append(ip)
        
        return dict(classified_ips), failed_ips
    
    def create_country_files(self, classified_ips: Dict[str, List[Dict]], output_dir: str = 'country_files', merge_mode: bool = False):
        """
        为每个国家/地区创建单独的txt文件，保存到指定文件夹
        :param classified_ips: 分类结果
        :param output_dir: 输出目录名称
        :param merge_mode: 是否为合并模式（True=合并现有文件，False=覆盖现有文件）
        """
        print("\n=== 创建国家/地区IP文件 ===")
        
        # 确定实际输出目录
        actual_output_dir = output_dir
        if merge_mode:
            # 合并模式下，在output_dir下创建merged子目录
            actual_output_dir = os.path.join(output_dir, 'merged')
        
        # 创建输出目录
        try:
            os.makedirs(actual_output_dir, exist_ok=True)
            print(f"创建输出目录: {actual_output_dir}")
        except Exception as e:
            print(f"创建目录 {actual_output_dir} 时出错: {e}")
            return
        
        for country, ips in classified_ips.items():
            # 使用国家代码作为文件名，如果没有则使用国家名称的拼音或英文
            if ips and 'location' in ips[0] and 'country_code' in ips[0]['location']:
                country_code = ips[0]['location']['country_code']
            else:
                country_code = 'Unknown'
            filename = os.path.join(actual_output_dir, f"{country_code}.txt")
            
            try:
                # 准备IP列表
                new_ips = [ip_data['ip'] for ip_data in ips]
                
                if merge_mode and os.path.exists(filename):
                    # 合并模式：读取现有文件并合并
                    try:
                        with open(filename, 'r', encoding='utf-8') as f:
                            existing_ips = [line.strip() for line in f if line.strip()]
                        print(f"读取现有文件: {filename} (包含 {len(existing_ips)} 个IP)")
                        
                        # 合并IP列表，去重
                        merged_ips = list(set(existing_ips + new_ips))
                        # 按IP地址排序
                        sorted_ips = sorted(merged_ips, key=lambda x: self.ip_to_tuple(x))
                        
                        print(f"合并后: {len(sorted_ips)} 个IP (新增 {len(new_ips)} 个，去重后净增 {len(sorted_ips) - len(existing_ips)} 个)")
                    except Exception as e:
                        print(f"读取现有文件失败，将创建新文件: {e}")
                        # 按IP地址排序
                        sorted_ips = sorted(new_ips, key=lambda x: self.ip_to_tuple(x))
                else:
                    # 覆盖模式或文件不存在：直接使用新IP
                    # 按IP地址排序
                    sorted_ips = sorted(new_ips, key=lambda x: self.ip_to_tuple(x))
                
                # 写入文件
                with open(filename, 'w', encoding='utf-8') as f:
                    for ip in sorted_ips:
                        f.write(f"{ip}\n")
                
                mode_desc = "合并模式" if merge_mode else "覆盖模式"
                print(f"已创建文件: {filename} ({mode_desc}，包含 {len(sorted_ips)} 个IP，按IP排序)")
            except Exception as e:
                print(f"创建文件 {filename} 时出错: {e}")
    
    def ip_to_tuple(self, ip_str: str) -> tuple:
        """
        将IP地址转换为可排序的元组
        :param ip_str: IP地址字符串
        :return: 可排序的元组
        """
        try:
            return tuple(map(int, ip_str.split('.')))
        except:
            return (0, 0, 0, 0)
    
    def translate_field_names_to_chinese(self, data: Dict) -> Dict:
        """
        将字典中的字段名翻译成中文
        :param data: 原始数据字典
        :return: 字段名翻译后的字典
        """
        if not isinstance(data, dict):
            return data
        
        translated_data = {}
        for key, value in data.items():
            # 翻译字段名
            chinese_key = CHINESE_TRANSLATIONS.get(key, key)
            
            # 如果值是字典，递归翻译
            if isinstance(value, dict):
                translated_data[chinese_key] = self.translate_field_names_to_chinese(value)
            # 如果值是列表，对列表中的每个元素进行翻译
            elif isinstance(value, list):
                translated_data[chinese_key] = [
                    self.translate_field_names_to_chinese(item) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                translated_data[chinese_key] = value
        
        return translated_data
    
    def save_results(self, classified_ips: Dict[str, List[Dict]], output_file: str):
        """
        保存分类结果到JSON文件，支持增量更新，字段名翻译成中文
        :param classified_ips: 分类结果
        :param output_file: 输出文件路径
        """
        try:
            # 确保输出目录存在
            output_dir = os.path.dirname(output_file)
            if output_dir:  # 只有当目录路径不为空时才创建目录
                os.makedirs(output_dir, exist_ok=True)
            
            # 尝试读取现有数据
            existing_classified_ips = {}
            if os.path.exists(output_file):
                try:
                    with open(output_file, 'r', encoding='utf-8') as f:
                        existing_classified_ips = json.load(f)
                    print(f"已读取现有数据: {output_file}")
                except Exception as e:
                    print(f"读取现有文件失败，将创建新文件: {e}")
            
            # 合并数据：新IP添加，已有IP的覆盖旧数据
            merged_classified_ips = existing_classified_ips.copy()
            
            for country, new_ip_list in classified_ips.items():
                if country not in merged_classified_ips:
                    merged_classified_ips[country] = []
                
                # 创建IP到数据的映射，方便快速查找
                existing_ip_map = {ip_data['ip']: ip_data for ip_data in merged_classified_ips[country]}
                
                for new_ip_data in new_ip_list:
                    ip_address = new_ip_data['ip']
                    # 覆盖已有IP的数据或添加新IP
                    existing_ip_map[ip_address] = new_ip_data
                
                # 转换回列表并按IP排序
                merged_ip_list = list(existing_ip_map.values())
                merged_ip_list.sort(key=lambda x: self.ip_to_tuple(x['ip']))
                merged_classified_ips[country] = merged_ip_list
            
            # 删除空的国家
            empty_countries = [country for country, ip_list in merged_classified_ips.items() if not ip_list]
            for country in empty_countries:
                del merged_classified_ips[country]
            
            # 将字段名翻译成中文
            translated_classified_ips = self.translate_field_names_to_chinese(merged_classified_ips)
            
            # 保存合并后的数据
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(translated_classified_ips, f, ensure_ascii=False, indent=2)
            print(f"结果已保存到: {output_file} (增量更新，按IP排序，字段名已翻译成中文)")
        except Exception as e:
            print(f"保存文件时出错: {e}")
    
    def print_summary(self, classified_ips: Dict[str, List[Dict]]):
        """
        打印详细的分类摘要和完整检测信息
        :param classified_ips: 分类结果
        """
        print("\n=== IP地区分类详细报告 ===")
        total_ips = sum(len(ips) for ips in classified_ips.values())
        print(f"总共处理了 {total_ips} 个IP地址")
        print(f"涉及 {len(classified_ips)} 个国家/地区\n")
        
        for country, ips in sorted(classified_ips.items(), key=lambda x: len(x[1]), reverse=True):
            print(f"【{country}】 - 共 {len(ips)} 个IP")
            print("=" * 50)
            
            # 显示每个IP的完整信息
            for i, ip_data in enumerate(ips, 1):
                print(f"\nIP #{i}: {ip_data['ip']}")
                print("-" * 30)
                
                # 基本信息
                print(f"区域互联网注册机构: {ip_data.get('rir', 'Unknown')}")
                print(f"查询耗时: {ip_data.get('elapsed_ms', 'Unknown')}毫秒")
                
                # 位置信息
                if 'location' in ip_data:
                    location = ip_data['location']
                    print(f"\n【位置信息】")
                    print(f"国家: {translate_to_chinese(location.get('country', 'Unknown'))}")
                    print(f"国家代码: {location.get('country_code', 'Unknown')}")
                    print(f"地区/州: {translate_to_chinese(location.get('state', 'Unknown'))}")
                    print(f"城市: {translate_to_chinese(location.get('city', 'Unknown'))}")
                    print(f"大洲: {translate_to_chinese(location.get('continent', 'Unknown'))}")
                    print(f"邮政编码: {location.get('zip', 'Unknown')}")
                    print(f"时区: {location.get('timezone', 'Unknown')}")
                    print(f"本地时间: {location.get('local_time', 'Unknown')}")
                    print(f"电话代码: {location.get('calling_code', 'Unknown')}")
                    print(f"货币代码: {location.get('currency_code', 'Unknown')}")
                    
                    if location.get('latitude') and location.get('longitude'):
                        print(f"坐标: {location['latitude']}, {location['longitude']}")
                    
                    # 标识字段
                    print("\n【网络特征】")
                    flag_fields = {
                        'is_bogon': '是否为保留IP',
                        'is_mobile': '是否为移动网络',
                        'is_satellite': '是否为卫星网络',
                        'is_crawler': '是否为爬虫',
                        'is_datacenter': '是否为数据中心',
                        'is_tor': '是否为Tor网络',
                        'is_proxy': '是否为代理',
                        'is_vpn': '是否为VPN',
                        'is_abuser': '是否为滥用者'
                    }
                    
                    for field, chinese_name in flag_fields.items():
                        value = ip_data.get(field)
                        if value is not None:
                            print(f"{chinese_name}: {'是' if value else '否'}")
                    
                    # ASN信息
                    if 'asn' in ip_data:
                        asn = ip_data['asn']
                        print("\n【自治系统信息】")
                        print(f"自治系统号: {asn.get('asn', 'Unknown')}")
                        print(f"组织: {translate_to_chinese(asn.get('org', 'Unknown'))}")
                        print(f"路由: {asn.get('route', 'Unknown')}")
                        print(f"描述: {translate_to_chinese(asn.get('descr', 'Unknown'))}")
                        print(f"国家: {asn.get('country', 'Unknown')}")
                        print(f"类型: {translate_to_chinese(asn.get('type', 'Unknown'))}")
                        print(f"滥用评分: {asn.get('abuser_score', 'Unknown')}")
                        print(f"域名: {asn.get('domain', 'Unknown')}")
                        print(f"滥用联系人: {asn.get('abuse', 'Unknown')}")
                        print(f"更新时间: {asn.get('updated', 'Unknown')}")
                        print(f"区域注册机构: {asn.get('rir', 'Unknown')}")
                        print(f"是否活跃: {'是' if asn.get('active') else '否'}")
                    
                    # 公司信息
                    if 'company' in ip_data:
                        company = ip_data['company']
                        print("\n【公司信息】")
                        print(f"公司名称: {translate_to_chinese(company.get('name', 'Unknown'))}")
                        print(f"域名: {company.get('domain', 'Unknown')}")
                        print(f"类型: {translate_to_chinese(company.get('type', 'Unknown'))}")
                        print(f"滥用评分: {company.get('abuser_score', 'Unknown')}")
                        print(f"网络范围: {company.get('network', 'Unknown')}")
                        print(f"WHOIS信息: {company.get('whois', 'Unknown')}")
                    
                    # 滥用联系人信息
                    if 'abuse' in ip_data:
                        abuse = ip_data['abuse']
                        print("\n【滥用联系人】")
                        print(f"联系人: {translate_to_chinese(abuse.get('name', 'Unknown'))}")
                        print(f"地址: {translate_to_chinese(abuse.get('address', 'Unknown'))}")
                        print(f"邮箱: {abuse.get('email', 'Unknown')}")
                        print(f"电话: {abuse.get('phone', 'Unknown')}")
                
                # 如果不是最后一个IP，添加分隔线
                if i < len(ips):
                    print("\n" + "·" * 40)
            
            print("\n" + "=" * 50 + "\n")

def load_ip_list(file_path: str) -> List[str]:
    """
    从文件加载IP列表
    :param file_path: 文件路径
    :return: IP地址列表
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            ips = [line.strip() for line in f if line.strip()]
        return ips
    except FileNotFoundError:
        print(f"文件未找到: {file_path}")
        return []
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return []

def get_user_input(prompt: str, default: str = None) -> str:
    """
    获取用户输入，支持默认值
    :param prompt: 提示信息
    :param default: 默认值
    :return: 用户输入的值
    """
    if default:
        user_input = input(f"{prompt} (默认: {default}): ").strip()
        return user_input if user_input else default
    else:
        return input(f"{prompt}: ").strip()

def interactive_mode() -> tuple:
    """
    交互式模式，获取用户输入
    :return: (input_file, output_file, api_key, country_files_dir, merge_mode, max_workers)
    """
    print("\n=== 交互式配置 ===")
    
    # 获取输入文件
    while True:
        input_file = get_user_input("请输入包含IP地址的文件路径", "ips.txt")
        if os.path.exists(input_file):
            break
        else:
            print(f"文件 '{input_file}' 不存在，请重新输入或创建该文件。")
    
    # 获取输出文件
    output_file = get_user_input("请输入JSON结果输出文件路径", "iptest_results.json")
    
    # 获取API密钥（可选）
    api_key = get_user_input("请输入ipapi.is的API密钥（可选，直接回车使用内置密钥）", "")
    api_key = api_key if api_key else None
    
    # 获取国家文件输出目录
    country_files_dir = get_user_input("请输入国家分类文件输出目录", "country_files")
    
    # 获取并发线程数
    while True:
        try:
            threads_input = get_user_input("请输入并发线程数（1-20，默认: 5）", "5")
            max_workers = int(threads_input)
            if 1 <= max_workers <= 20:
                break
            else:
                print("线程数必须在1-20之间，请重新输入。")
        except ValueError:
            print("请输入有效的数字，请重新输入。")
    
    # 询问是否使用合并模式
    merge_input = get_user_input("是否使用合并模式（y/n，默认: n）", "n")
    merge_mode = merge_input.lower() in ['y', 'yes', '是']
    
    return input_file, output_file, api_key, country_files_dir, merge_mode, max_workers

def main():
    """
    主函数
    """
    parser = argparse.ArgumentParser(description='IP地区分类工具 - 使用ipapi.is API服务')
    parser.add_argument('input_file', nargs='?', default='ips.txt', help='包含IP地址的文件路径（默认: ips.txt）')
    parser.add_argument('-o', '--output', default='iptest_results.json', help='输出文件名（默认: iptest_results.json）')
    parser.add_argument('-k', '--api-key', help='ipapi.is的API密钥（可选，默认使用内置密钥）')
    parser.add_argument('-d', '--country-dir', default='country_files', help='国家分类文件输出目录（默认: country_files）')
    parser.add_argument('-t', '--threads', type=int, default=5, help='并发线程数（1-20，默认: 5）')
    parser.add_argument('--merge', action='store_true', help='合并模式：将新IP合并到现有文件中，而不是覆盖')
    parser.add_argument('--no-interactive', action='store_true', help='非交互模式，使用默认值')
    
    args = parser.parse_args()
    
    # 验证线程数参数
    if not (1 <= args.threads <= 20):
        print("错误：线程数必须在1-20之间")
        return
    
    print("IP地区分类工具")
    print("使用ipapi.is API服务\n")
    
    # 检查是否使用交互模式
    if not args.no_interactive and len(sys.argv) == 1:
        # 没有命令行参数，使用交互模式
        input_file, output_file, api_key, country_files_dir, merge_mode, max_workers = interactive_mode()
    else:
        # 使用命令行参数
        input_file = args.input_file
        output_file = args.output
        api_key = args.api_key
        country_files_dir = args.country_dir
        max_workers = args.threads
        merge_mode = args.merge
    
    # 加载IP列表
    ip_list = load_ip_list(input_file)
    if not ip_list:
        print(f"未找到有效的IP地址，程序退出。")
        return
    
    print(f"\n加载了 {len(ip_list)} 个IP地址")
    print(f"输入文件: {input_file}")
    print(f"JSON输出文件: {output_file}")
    print(f"国家分类文件目录: {country_files_dir}")
    
    # 创建分类器实例
    classifier = IPClassifier(api_key)
    
    # 进行分类
    classified_ips, failed_ips = classifier.classify_ips_by_country(ip_list, max_workers)
    
    # 打印摘要
    classifier.print_summary(classified_ips)
    
    # 输出统计信息
    total_ips = len(ip_list)
    successful_ips = total_ips - len(failed_ips)
    failed_count = len(failed_ips)
    
    print("\n" + "=" * 50)
    print("处理统计信息")
    print("=" * 50)
    print(f"总IP数量: {total_ips}")
    print(f"成功查询: {successful_ips}")
    print(f"查询失败: {failed_count}")
    
    if failed_count > 0:
        print("\n失败的IP地址:")
        for i, failed_ip in enumerate(failed_ips, 1):
            print(f"  {i}. {failed_ip}")
    
    print("=" * 50)
    
    # 保存结果
    classifier.save_results(classified_ips, output_file)
    
    # 创建按国家/地区分类的txt文件
    if merge_mode:
        print("\n使用合并模式创建国家分类文件...")
        classifier.create_country_files(classified_ips, country_files_dir, merge_mode=True)
        print(f"合并后的国家分类文件已保存到: {country_files_dir}/merged/")
    else:
        print("\n使用覆盖模式创建国家分类文件...")
        classifier.create_country_files(classified_ips, country_files_dir, merge_mode=False)
        print(f"国家分类文件已保存到: {country_files_dir}/")
    
    print(f"\n处理完成！")
    print(f"JSON结果已保存到: {output_file}")

if __name__ == "__main__":
    main()
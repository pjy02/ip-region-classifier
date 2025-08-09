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
    'elapsed_ms': '耗时(毫秒)'
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
                
            # 获取完整的检测信息
            location = data.get('location', {})
            asn_info = data.get('asn', {})
            company_info = data.get('company', {})
            abuse_info = data.get('abuse', {})
            datacenter_info = data.get('datacenter', {})
            
            # 构建完整的IP信息
            complete_info = {
                # 基本信息
                'ip': data.get('ip', ip),
                'rir': data.get('rir'),
                'elapsed_ms': data.get('elapsed_ms'),
                
                # 标识字段
                'is_bogon': data.get('is_bogon'),
                'is_mobile': data.get('is_mobile'),
                'is_satellite': data.get('is_satellite'),
                'is_crawler': data.get('is_crawler'),
                'is_datacenter': data.get('is_datacenter'),
                'is_tor': data.get('is_tor'),
                'is_proxy': data.get('is_proxy'),
                'is_vpn': data.get('is_vpn'),
                'is_abuser': data.get('is_abuser'),
                
                # 位置信息
                'country': location.get('country', 'Unknown'),
                'country_code': location.get('country_code', 'Unknown'),
                'region': location.get('state', 'Unknown'),
                'city': location.get('city', 'Unknown'),
                'latitude': location.get('latitude'),
                'longitude': location.get('longitude'),
                'continent': location.get('continent'),
                'in_eu': location.get('is_eu_member'),
                'postal': location.get('zip'),
                'timezone': location.get('timezone'),
                'calling_code': location.get('calling_code'),
                'currency_code': location.get('currency_code'),
                'local_time': location.get('local_time'),
                'local_time_unix': location.get('local_time_unix'),
                'is_dst': location.get('is_dst'),
                
                # ASN信息
                'asn': asn_info.get('asn'),
                'asn_route': asn_info.get('route'),
                'asn_descr': asn_info.get('descr'),
                'asn_country': asn_info.get('country'),
                'asn_active': asn_info.get('active'),
                'asn_org': asn_info.get('org'),
                'asn_domain': asn_info.get('domain'),
                'asn_abuse': asn_info.get('abuse'),
                'asn_type': asn_info.get('type'),
                'asn_updated': asn_info.get('updated'),
                'asn_rir': asn_info.get('rir'),
                'asn_abuser_score': asn_info.get('abuser_score'),
                
                # 公司信息
                'company_name': company_info.get('name'),
                'company_abuser_score': company_info.get('abuser_score'),
                'company_domain': company_info.get('domain'),
                'company_type': company_info.get('type'),
                'company_network': company_info.get('network'),
                'company_whois': company_info.get('whois'),
                
                # 滥用信息
                'abuse_name': abuse_info.get('name'),
                'abuse_address': abuse_info.get('address'),
                'abuse_email': abuse_info.get('email'),
                'abuse_phone': abuse_info.get('phone'),
                
                # 数据中心信息
                'datacenter_network': datacenter_info.get('network'),
                'datacenter_name': datacenter_info.get('datacenter'),
                
                # 兼容性字段（保持原有结构）
                'org': asn_info.get('org'),
                'timezone': location.get('timezone'),
                'utc_offset': None,  # ipapi.is不直接提供此字段
                'country_calling_code': location.get('calling_code'),
                'currency': location.get('currency_code'),
                'languages': None,  # ipapi.is不直接提供此字段
                'country_flag': None,  # ipapi.is不提供此字段
                'country_flag_emoji': None,  # ipapi.is不提供此字段
                'country_area': None,  # ipapi.is不提供此字段
                'country_population': None  # ipapi.is不提供此字段
            }
            
            # 翻译成中文
            translated_info = {}
            for key, value in complete_info.items():
                if key in ['ip', 'country_code', 'latitude', 'longitude', 'asn', 'asn_route', 'utc_offset', 
                          'country_area', 'country_population', 'in_eu', 'postal', 'local_time_unix', 
                          'elapsed_ms', 'is_bogon', 'is_mobile', 'is_satellite', 'is_crawler', 
                          'is_datacenter', 'is_tor', 'is_proxy', 'is_vpn', 'is_abuser', 'asn_active', 
                          'is_dst']:
                    # 这些字段保持原值
                    translated_info[key] = value
                elif isinstance(value, str):
                    # 字符串字段进行翻译
                    translated_info[key] = translate_to_chinese(value)
                elif isinstance(value, bool):
                    # 布尔值转换为中文描述
                    translated_info[key] = '是' if value else '否'
                else:
                    # 其他类型保持原值
                    translated_info[key] = value
            
            return translated_info
            
        except requests.RequestException as e:
            print(f"网络请求错误 for IP {ip}: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON解析错误 for IP {ip}: {e}")
            return None
        except Exception as e:
            print(f"未知错误 for IP {ip}: {e}")
            return None
    
    def classify_ips_by_country(self, ip_list: list[str]) -> tuple[dict[str, list[dict]], list[str]]:
        """
        按国家对IP列表进行分类
        :param ip_list: IP地址列表
        :return: (按国家分类的IP信息字典, 失败的IP列表)
        """
        classified_ips = defaultdict(list)
        failed_ips = []
        total_ips = len(ip_list)
        
        print(f"开始处理 {total_ips} 个IP地址...")
        
        for i, ip in enumerate(ip_list, 1):
            print(f"处理进度: {i}/{total_ips} ({i/total_ips*100:.1f}%) - {ip}")
            
            location_data = self.get_ip_location(ip)
            if location_data:
                country = location_data['country']
                classified_ips[country].append(location_data)
            else:
                failed_ips.append(ip)
            
            # 添加延迟以避免API限制（ipapi.is限制）
            if i < total_ips:
                time.sleep(1)  # 1秒延迟，避免触发API限制
        
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
            country_code = ips[0].get('country_code', 'Unknown') if ips else 'Unknown'
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
    
    def save_results(self, classified_ips: Dict[str, List[Dict]], output_file: str = 'iptest_results.json'):
        """
        保存分类结果到JSON文件，将字段名也转换为中文
        支持增量更新：新IP添加，已有IP的覆盖旧数据，并按IP从小到大排序
        :param classified_ips: 分类结果
        :param output_file: 输出文件名
        """
        try:
            # 字段名映射表（英文 -> 中文）
            field_name_mapping = {
                'ip': 'IP地址',
                'rir': '区域互联网注册机构',
                'elapsed_ms': '查询耗时',
                'is_bogon': '是否为保留IP',
                'is_mobile': '是否为移动网络',
                'is_satellite': '是否为卫星网络',
                'is_crawler': '是否为爬虫',
                'is_datacenter': '是否为数据中心',
                'is_tor': '是否为Tor网络',
                'is_proxy': '是否为代理',
                'is_vpn': '是否为VPN',
                'is_abuser': '是否为滥用者',
                'country': '国家',
                'country_code': '国家代码',
                'region': '地区/州',
                'city': '城市',
                'latitude': '纬度',
                'longitude': '经度',
                'continent': '大洲',
                'in_eu': '是否为欧盟成员国',
                'postal': '邮政编码',
                'timezone': '时区',
                'calling_code': '电话代码',
                'currency_code': '货币代码',
                'local_time': '本地时间',
                'local_time_unix': '本地时间戳',
                'is_dst': '是否为夏令时',
                'asn': '自治系统号',
                'asn_route': '路由',
                'asn_descr': '描述',
                'asn_country': 'ASN国家',
                'asn_active': 'ASN是否活跃',
                'asn_org': 'ASN组织',
                'asn_domain': 'ASN域名',
                'asn_abuse': 'ASN滥用联系人',
                'asn_type': 'ASN类型',
                'asn_updated': 'ASN更新时间',
                'asn_rir': 'ASN区域注册机构',
                'asn_abuser_score': 'ASN滥用评分',
                'company_name': '公司名称',
                'company_abuser_score': '公司滥用评分',
                'company_domain': '公司域名',
                'company_type': '公司类型',
                'company_network': '公司网络范围',
                'company_whois': '公司WHOIS信息',
                'abuse_name': '滥用联系人姓名',
                'abuse_address': '滥用联系人地址',
                'abuse_email': '滥用联系人邮箱',
                'abuse_phone': '滥用联系人电话',
                'datacenter_network': '数据中心网络',
                'datacenter_name': '数据中心名称',
                'org': '组织',
                'utc_offset': 'UTC偏移量',
                'country_calling_code': '国家电话代码',
                'currency': '货币',
                'languages': '语言',
                'country_flag': '国家旗帜',
                'country_flag_emoji': '国家旗帜表情',
                'country_area': '国家面积',
                'country_population': '国家人口'
            }
            
            # 创建新的分类结果，将字段名转换为中文
            new_chinese_classified_ips = {}
            for country, ip_list in classified_ips.items():
                chinese_ip_list = []
                for ip_data in ip_list:
                    chinese_ip_data = {}
                    for eng_field, value in ip_data.items():
                        chinese_field = field_name_mapping.get(eng_field, eng_field)
                        chinese_ip_data[chinese_field] = value
                    chinese_ip_list.append(chinese_ip_data)
                new_chinese_classified_ips[country] = chinese_ip_list
            
            # 尝试读取现有数据
            existing_chinese_classified_ips = {}
            if os.path.exists(output_file):
                try:
                    with open(output_file, 'r', encoding='utf-8') as f:
                        existing_chinese_classified_ips = json.load(f)
                    print(f"已读取现有数据: {output_file}")
                except Exception as e:
                    print(f"读取现有文件失败，将创建新文件: {e}")
            
            # 合并数据：新IP添加，已有IP的覆盖旧数据
            merged_chinese_classified_ips = existing_chinese_classified_ips.copy()
            
            for country, new_ip_list in new_chinese_classified_ips.items():
                if country not in merged_chinese_classified_ips:
                    merged_chinese_classified_ips[country] = []
                
                # 创建IP到数据的映射，方便快速查找
                existing_ip_map = {ip_data['IP地址']: ip_data for ip_data in merged_chinese_classified_ips[country]}
                
                for new_ip_data in new_ip_list:
                    ip_address = new_ip_data['IP地址']
                    # 覆盖已有IP的数据或添加新IP
                    existing_ip_map[ip_address] = new_ip_data
                
                # 转换回列表并按IP排序
                merged_ip_list = list(existing_ip_map.values())
                merged_ip_list.sort(key=lambda x: self.ip_to_tuple(x['IP地址']))
                merged_chinese_classified_ips[country] = merged_ip_list
            
            # 删除空的国家
            empty_countries = [country for country, ip_list in merged_chinese_classified_ips.items() if not ip_list]
            for country in empty_countries:
                del merged_chinese_classified_ips[country]
            
            # 保存合并后的数据
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(merged_chinese_classified_ips, f, ensure_ascii=False, indent=2)
            print(f"结果已保存到: {output_file} (增量更新，按IP排序)")
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
                basic_fields = {
                    'country': '国家',
                    'country_code': '国家代码',
                    'region': '地区/州',
                    'city': '城市',
                    'continent': '大洲',
                    'postal': '邮政编码',
                    'timezone': '时区',
                    'local_time': '本地时间',
                    'calling_code': '电话代码',
                    'currency_code': '货币代码'
                }
                
                for field, chinese_name in basic_fields.items():
                    value = ip_data.get(field)
                    if value and value != 'Unknown':
                        print(f"{chinese_name}: {value}")
                
                # 坐标信息
                if ip_data.get('latitude') and ip_data.get('longitude'):
                    print(f"坐标: {ip_data['latitude']}, {ip_data['longitude']}")
                
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
                    'is_abuser': '是否为滥用者',
                    'is_eu_member': '是否为欧盟成员国',
                    'is_dst': '是否为夏令时'
                }
                
                for field, chinese_name in flag_fields.items():
                    value = ip_data.get(field)
                    if value is not None:
                        print(f"{chinese_name}: {value}")
                
                # ASN信息
                if ip_data.get('asn'):
                    print("\n【自治系统信息】")
                    asn_fields = {
                        'asn': '自治系统号',
                        'asn_org': '组织',
                        'asn_route': '路由',
                        'asn_descr': '描述',
                        'asn_country': '国家',
                        'asn_type': '类型',
                        'asn_abuser_score': '滥用评分'
                    }
                    
                    for field, chinese_name in asn_fields.items():
                        value = ip_data.get(field)
                        if value and value != 'Unknown':
                            print(f"{chinese_name}: {value}")
                
                # 公司信息
                if ip_data.get('company_name'):
                    print("\n【公司信息】")
                    company_fields = {
                        'company_name': '公司名称',
                        'company_domain': '域名',
                        'company_type': '类型',
                        'company_abuser_score': '滥用评分',
                        'company_network': '网络范围'
                    }
                    
                    for field, chinese_name in company_fields.items():
                        value = ip_data.get(field)
                        if value and value != 'Unknown':
                            print(f"{chinese_name}: {value}")
                
                # 滥用联系人信息
                if ip_data.get('abuse_name'):
                    print("\n【滥用联系人】")
                    abuse_fields = {
                        'abuse_name': '联系人',
                        'abuse_email': '邮箱',
                        'abuse_phone': '电话'
                    }
                    
                    for field, chinese_name in abuse_fields.items():
                        value = ip_data.get(field)
                        if value and value != 'Unknown':
                            print(f"{chinese_name}: {value}")
                
                # 数据中心信息
                if ip_data.get('datacenter_name'):
                    print("\n【数据中心信息】")
                    dc_fields = {
                        'datacenter_name': '数据中心',
                        'datacenter_network': '网络'
                    }
                    
                    for field, chinese_name in dc_fields.items():
                        value = ip_data.get(field)
                        if value and value != 'Unknown':
                            print(f"{chinese_name}: {value}")
                
                # 其他信息
                if ip_data.get('rir'):
                    print(f"\n区域互联网注册机构: {ip_data['rir']}")
                if ip_data.get('elapsed_ms'):
                    print(f"查询耗时: {ip_data['elapsed_ms']}毫秒")
                
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
    :return: (input_file, output_file, api_key, country_files_dir, merge_mode)
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
    
    # 询问是否使用合并模式
    merge_input = get_user_input("是否使用合并模式（y/n，默认: n）", "n")
    merge_mode = merge_input.lower() in ['y', 'yes', '是']
    
    return input_file, output_file, api_key, country_files_dir, merge_mode

def main():
    """
    主函数
    """
    parser = argparse.ArgumentParser(description='IP地区分类工具 - 使用ipapi.is API服务')
    parser.add_argument('input_file', nargs='?', default='ips.txt', help='包含IP地址的文件路径（默认: ips.txt）')
    parser.add_argument('-o', '--output', default='iptest_results.json', help='输出文件名（默认: iptest_results.json）')
    parser.add_argument('-k', '--api-key', help='ipapi.is的API密钥（可选，默认使用内置密钥）')
    parser.add_argument('-d', '--country-dir', default='country_files', help='国家分类文件输出目录（默认: country_files）')
    parser.add_argument('--merge', action='store_true', help='合并模式：将新IP合并到现有文件中，而不是覆盖')
    parser.add_argument('--no-interactive', action='store_true', help='非交互模式，使用默认值')
    
    args = parser.parse_args()
    
    print("IP地区分类工具")
    print("使用ipapi.is API服务\n")
    
    # 检查是否使用交互模式
    if not args.no_interactive and len(sys.argv) == 1:
        # 没有命令行参数，使用交互模式
        input_file, output_file, api_key, country_files_dir, merge_mode = interactive_mode()
    else:
        # 使用命令行参数
        input_file = args.input_file
        output_file = args.output
        api_key = args.api_key
        country_files_dir = args.country_dir
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
    classified_ips, failed_ips = classifier.classify_ips_by_country(ip_list)
    
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
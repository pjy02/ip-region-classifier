import unittest
import json
import os
import sys
from unittest.mock import Mock, patch, MagicMock

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from iptest import IPClassifier


class TestIPClassifier(unittest.TestCase):
    """IPClassifier类的单元测试"""
    
    def setUp(self):
        """测试前的设置工作"""
        self.classifier = IPClassifier()
        self.test_ips = [
            "8.8.8.8",      # Google DNS
            "1.1.1.1",      # Cloudflare DNS
            "208.67.222.222", # OpenDNS
            "invalid_ip",   # 无效IP
            "256.256.256.256" # 格式错误的IP
        ]
        
    def test_is_valid_ip(self):
        """测试IP地址验证功能"""
        # 有效IP地址
        self.assertTrue(self.classifier.is_valid_ip("8.8.8.8"))
        self.assertTrue(self.classifier.is_valid_ip("192.168.1.1"))
        self.assertTrue(self.classifier.is_valid_ip("0.0.0.0"))
        self.assertTrue(self.classifier.is_valid_ip("255.255.255.255"))
        
        # 无效IP地址
        self.assertFalse(self.classifier.is_valid_ip("invalid_ip"))
        self.assertFalse(self.classifier.is_valid_ip("256.256.256.256"))
        self.assertFalse(self.classifier.is_valid_ip("1.1.1.1.1"))
        self.assertFalse(self.classifier.is_valid_ip(""))
        self.assertFalse(self.classifier.is_valid_ip(None))
        
    def test_get_continent(self):
        """测试大洲信息获取功能"""
        # 测试已知国家的大洲映射
        self.assertEqual(self.classifier.get_continent("US"), "北美洲")
        self.assertEqual(self.classifier.get_continent("CN"), "亚洲")
        self.assertEqual(self.classifier.get_continent("DE"), "欧洲")
        self.assertEqual(self.classifier.get_continent("BR"), "南美洲")
        self.assertEqual(self.classifier.get_continent("AU"), "大洋洲")
        
        # 测试未知国家
        self.assertEqual(self.classifier.get_continent("UNKNOWN"), "未知")
        self.assertEqual(self.classifier.get_continent(""), "未知")
        
    @patch('requests.get')
    def test_get_ip_location_success(self, mock_get):
        """测试成功的IP地理位置查询"""
        # 模拟成功的API响应
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "country_code": "US",
            "country_name": "United States",
            "region": "California",
            "city": "Mountain View",
            "latitude": 37.405992,
            "longitude": -122.078515,
            "asn": "AS15169 Google LLC",
            "org": "Google LLC"
        }
        mock_get.return_value = mock_response
        
        result = self.classifier.get_ip_location("8.8.8.8")
        
        # 验证结果
        self.assertIsNotNone(result)
        self.assertEqual(result["country_code"], "US")
        self.assertEqual(result["country_name"], "United States")
        self.assertEqual(result["region"], "California")
        
        # 验证API调用
        mock_get.assert_called_once()
        
    @patch('requests.get')
    def test_get_ip_location_failure(self, mock_get):
        """测试失败的IP地理位置查询"""
        # 模拟API调用失败
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        result = self.classifier.get_ip_location("8.8.8.8")
        
        # 验证结果为None
        self.assertIsNone(result)
        
    @patch('requests.get')
    def test_get_ip_location_exception(self, mock_get):
        """测试IP地理位置查询的异常处理"""
        # 模拟网络异常
        mock_get.side_effect = Exception("Network error")
        
        result = self.classifier.get_ip_location("8.8.8.8")
        
        # 验证结果为None
        self.assertIsNone(result)
        
    def test_process_single_ip(self):
        """测试单个IP处理功能"""
        # 创建临时结果字典
        temp_results = {}
        
        # 测试有效IP
        with patch.object(self.classifier, 'get_ip_location') as mock_get_location:
            mock_get_location.return_value = {
                "country_code": "US",
                "country_name": "United States"
            }
            
            result = self.classifier.process_single_ip("8.8.8.8", temp_results)
            
            # 验证结果
            self.assertEqual(result["country_code"], "US")
            self.assertIn("8.8.8.8", temp_results)
            
    def test_process_single_ip_invalid(self):
        """测试无效IP的处理"""
        temp_results = {}
        
        # 测试无效IP
        result = self.classifier.process_single_ip("invalid_ip", temp_results)
        
        # 验证结果
        self.assertIsNone(result)
        self.assertNotIn("invalid_ip", temp_results)
        
    def test_save_results(self):
        """测试结果保存功能"""
        # 创建测试数据
        test_results = {
            "8.8.8.8": {
                "country_code": "US",
                "country_name": "United States",
                "continent": "北美洲"
            },
            "1.1.1.1": {
                "country_code": "US",
                "country_name": "United States",
                "continent": "北美洲"
            }
        }
        
        test_filename = "test_results.json"
        
        try:
            # 保存结果
            self.classifier.save_results(test_results, test_filename)
            
            # 验证文件是否创建
            self.assertTrue(os.path.exists(test_filename))
            
            # 验证文件内容
            with open(test_filename, 'r', encoding='utf-8') as f:
                saved_data = json.load(f)
                
            self.assertEqual(saved_data, test_results)
            
        finally:
            # 清理测试文件
            if os.path.exists(test_filename):
                os.remove(test_filename)
                
    def test_save_country_files(self):
        """测试国家文件保存功能"""
        # 创建测试数据
        test_results = {
            "8.8.8.8": {
                "country_code": "US",
                "country_name": "United States",
                "continent": "北美洲"
            },
            "1.1.1.1": {
                "country_code": "US",
                "country_name": "United States",
                "continent": "北美洲"
            },
            "114.114.114.114": {
                "country_code": "CN",
                "country_name": "China",
                "continent": "亚洲"
            }
        }
        
        test_dir = "test_country_files"
        
        try:
            # 保存国家文件
            self.classifier.save_country_files(test_results, test_dir)
            
            # 验证目录是否创建
            self.assertTrue(os.path.exists(test_dir))
            
            # 验证国家文件是否创建
            us_file = os.path.join(test_dir, "US.txt")
            cn_file = os.path.join(test_dir, "CN.txt")
            
            self.assertTrue(os.path.exists(us_file))
            self.assertTrue(os.path.exists(cn_file))
            
            # 验证文件内容
            with open(us_file, 'r', encoding='utf-8') as f:
                us_content = f.read().strip().split('\n')
                self.assertIn("8.8.8.8", us_content)
                self.assertIn("1.1.1.1", us_content)
                
            with open(cn_file, 'r', encoding='utf-8') as f:
                cn_content = f.read().strip()
                self.assertEqual(cn_content, "114.114.114.114")
                
        finally:
            # 清理测试目录
            if os.path.exists(test_dir):
                import shutil
                shutil.rmtree(test_dir)
                
    def test_print_summary(self):
        """测试统计信息打印功能"""
        # 创建测试数据
        test_results = {
            "8.8.8.8": {
                "country_code": "US",
                "country_name": "United States",
                "continent": "北美洲"
            },
            "1.1.1.1": {
                "country_code": "US",
                "country_name": "United States",
                "continent": "北美洲"
            },
            "114.114.114.114": {
                "country_code": "CN",
                "country_name": "China",
                "continent": "亚洲"
            }
        }
        
        # 测试统计信息打印（不抛出异常即可）
        try:
            self.classifier.print_summary(test_results)
        except Exception as e:
            self.fail(f"print_summary() raised an exception: {e}")
            
    def test_load_ip_list(self):
        """测试IP列表加载功能"""
        # 创建测试文件
        test_filename = "test_ips.txt"
        test_ips = ["8.8.8.8", "1.1.1.1", "114.114.114.114"]
        
        try:
            # 写入测试文件
            with open(test_filename, 'w', encoding='utf-8') as f:
                for ip in test_ips:
                    f.write(f"{ip}\n")
                    
            # 加载IP列表
            loaded_ips = self.classifier.load_ip_list(test_filename)
            
            # 验证结果
            self.assertEqual(loaded_ips, test_ips)
            
        finally:
            # 清理测试文件
            if os.path.exists(test_filename):
                os.remove(test_filename)
                
    def test_load_ip_list_file_not_found(self):
        """测试文件不存在的情况"""
        # 测试不存在的文件
        result = self.classifier.load_ip_list("nonexistent_file.txt")
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
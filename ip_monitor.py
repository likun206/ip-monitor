#!/usr/bin/env python3
import requests
import json
import time
import datetime
import os
import sys
from pathlib import Path

class IPMonitor:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.data_file = "ip_history.json"
        self.log_file = "ip_monitor.log"
        self.load_config()
        
    def load_config(self):
        default_config = {
            "check_interval": 300,  # 5分钟
            "ip_apis": [
                "https://api.ipify.org?format=json",
                "https://httpbin.org/ip",
                "https://api.ip.sb/ip"
            ],
            "location_api": "http://ip-api.com/json/{ip}?fields=status,country,regionName,city,isp,query"
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            except:
                self.config = default_config
        else:
            self.config = default_config
            self.save_config()
    
    def save_config(self):
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def get_public_ip(self):
        for api in self.config["ip_apis"]:
            try:
                response = requests.get(api, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    return data.get('ip') or data.get('origin', '').split(',')[0].strip()
            except:
                continue
        return None
    
    def get_ip_location(self, ip):
        try:
            url = self.config["location_api"].format(ip=ip)
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    return {
                        'country': data.get('country', 'Unknown'),
                        'region': data.get('regionName', 'Unknown'),
                        'city': data.get('city', 'Unknown'),
                        'isp': data.get('isp', 'Unknown')
                    }
        except:
            pass
        return None
    
    def load_history(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def save_history(self, history):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    
    def log_message(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')
    
    def check_ip(self):
        current_time = datetime.datetime.now().isoformat()
        
        # 获取当前IP
        current_ip = self.get_public_ip()
        if not current_ip:
            self.log_message("错误: 无法获取公网IP地址")
            return False
        
        # 获取IP位置信息
        location_info = self.get_ip_location(current_ip)
        if not location_info:
            self.log_message(f"警告: 无法获取IP {current_ip} 的位置信息")
            location_info = {'country': 'Unknown', 'region': 'Unknown', 'city': 'Unknown', 'isp': 'Unknown'}
        
        # 读取历史记录
        history = self.load_history()
        
        # 构建当前记录
        current_record = {
            'timestamp': current_time,
            'ip': current_ip,
            'location': location_info
        }
        
        # 检查是否有变化
        ip_changed = False
        location_changed = False
        
        if history:
            last_record = history[-1]
            if last_record['ip'] != current_ip:
                ip_changed = True
                self.log_message(f"IP地址发生变化: {last_record['ip']} -> {current_ip}")
            
            if last_record['location'] != location_info:
                location_changed = True
                self.log_message(f"位置信息发生变化:")
                self.log_message(f"  原位置: {last_record['location']['country']}, {last_record['location']['region']}, {last_record['location']['city']} ({last_record['location']['isp']})")
                self.log_message(f"  新位置: {location_info['country']}, {location_info['region']}, {location_info['city']} ({location_info['isp']})")
        else:
            self.log_message("首次检测")
            ip_changed = True
        
        if ip_changed or location_changed or not history:
            # 保存新记录
            history.append(current_record)
            self.save_history(history)
            
            self.log_message(f"当前IP: {current_ip}")
            self.log_message(f"位置: {location_info['country']}, {location_info['region']}, {location_info['city']}")
            self.log_message(f"ISP: {location_info['isp']}")
        else:
            self.log_message(f"IP和位置未发生变化: {current_ip}")
        
        return True
    
    def run_once(self):
        """运行一次检测"""
        self.log_message("开始IP监控检测...")
        success = self.check_ip()
        if success:
            self.log_message("检测完成")
        return success
    
    def run_continuous(self, interval=None):
        """持续监控模式"""
        if interval is not None:
            check_interval = interval
        else:
            check_interval = self.config['check_interval']
            
        self.log_message(f"开始持续IP监控，检测间隔: {check_interval}秒")
        
        try:
            while True:
                self.check_ip()
                self.log_message(f"等待 {check_interval} 秒...")
                time.sleep(check_interval)
        except KeyboardInterrupt:
            self.log_message("用户中断监控")
        except Exception as e:
            self.log_message(f"监控过程中出现错误: {str(e)}")
    
    def show_history(self):
        """显示历史记录"""
        history = self.load_history()
        if not history:
            print("暂无历史记录")
            return
        
        print(f"\n=== IP变化历史 (共{len(history)}条记录) ===")
        for i, record in enumerate(history, 1):
            timestamp = datetime.datetime.fromisoformat(record['timestamp']).strftime("%Y-%m-%d %H:%M:%S")
            location = record['location']
            print(f"{i:2d}. {timestamp}")
            print(f"    IP: {record['ip']}")
            print(f"    位置: {location['country']}, {location['region']}, {location['city']}")
            print(f"    ISP: {location['isp']}")
            print()

def main():
    monitor = IPMonitor()
    
    if len(sys.argv) < 2:
        print("IP监控工具")
        print("使用方法:")
        print("  python ip_monitor.py once              - 运行一次检测")
        print("  python ip_monitor.py monitor           - 持续监控模式（使用配置文件间隔）")
        print("  python ip_monitor.py monitor <秒数>    - 持续监控模式（指定间隔秒数）")
        print("  python ip_monitor.py history           - 查看历史记录")
        print("")
        print("示例:")
        print("  python ip_monitor.py monitor 60       - 每60秒检测一次")
        print("  python ip_monitor.py monitor 1800     - 每30分钟检测一次")
        return
    
    command = sys.argv[1].lower()
    
    if command == "once":
        monitor.run_once()
    elif command == "monitor":
        interval = None
        if len(sys.argv) >= 3:
            try:
                interval = int(sys.argv[2])
                if interval < 10:
                    print("警告: 检测间隔不建议小于10秒，以避免API限制")
            except ValueError:
                print("错误: 间隔时间必须是数字")
                return
        monitor.run_continuous(interval)
    elif command == "history":
        monitor.show_history()
    else:
        print("未知命令，请使用 once、monitor 或 history")

if __name__ == "__main__":
    main()
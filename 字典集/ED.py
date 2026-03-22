#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Windows 用户名密码字典生成器
用于生成基于 Windows 用户名的常见密码组合
"""

from itertools import product
from datetime import datetime
import re


class WindowsUsernameDictGenerator:
    """Windows 用户名密码字典生成器"""
    
    def __init__(self):
        self.common_passwords = [
            '123456', 'password', '12345678', 'qwerty', '123456789',
            '12345', '1234567', '1234567890', 'iloveyou', 'admin',
            'welcome', 'monkey', 'dragon', 'master', 'login',
            'abc123', '111111', '123123', 'sunshine', 'princess'
        ]
        
        self.special_chars = ['!', '@', '#', '$', '%', '&', '*', '.']
        
        self.common_years = ['2020', '2021', '2022', '2023', '2024', '2025', '2026']
        
        self.common_numbers = ['1', '12', '123', '01', '001', '666', '888', '999']
    
    def extract_username_parts(self, username):
        """从用户名中提取各个部分"""
        parts = {
            'full': username,
            'lower': username.lower(),
            'upper': username.upper(),
            'capitalized': username.capitalize(),
        }
        
        # 分离数字和字母
        alpha_part = ''.join(filter(str.isalpha, username))
        digit_part = ''.join(filter(str.isdigit, username))
        
        parts['alpha'] = alpha_part
        parts['digits'] = digit_part
        parts['alpha_lower'] = alpha_part.lower()
        parts['alpha_upper'] = alpha_part.upper()
        
        return parts
    
    def generate_basic_variations(self, username):
        """生成基础变体"""
        parts = self.extract_username_parts(username)
        passwords = set()
        
        # 原始用户名及其大小写变体
        passwords.add(parts['full'])
        passwords.add(parts['lower'])
        passwords.add(parts['upper'])
        passwords.add(parts['capitalized'])
        
        if parts['alpha']:
            passwords.add(parts['alpha'])
            passwords.add(parts['alpha_lower'])
            passwords.add(parts['alpha_upper'])
        
        return list(passwords)
    
    def generate_with_numbers(self, username):
        """添加数字后缀/前缀"""
        passwords = set()
        base_variations = self.generate_basic_variations(username)
        
        for base in base_variations:
            # 添加常见数字
            for num in self.common_numbers:
                passwords.add(base + num)
                passwords.add(num + base)
            
            # 添加年份
            for year in self.common_years:
                passwords.add(base + year)
                passwords.add(year + base)
            
            # 添加 1-100 的数字
            for i in range(1, 101):
                passwords.add(base + str(i))
                passwords.add(str(i) + base)
        
        return list(passwords)
    
    def generate_with_special_chars(self, username):
        """添加特殊字符"""
        passwords = set()
        base_variations = self.generate_basic_variations(username)
        
        for base in base_variations:
            for char in self.special_chars:
                passwords.add(base + char)
                passwords.add(char + base)
                passwords.add(base + char + char)
            
            # 特殊字符在中间
            if len(base) > 2:
                mid = len(base) // 2
                for char in self.special_chars:
                    passwords.add(base[:mid] + char + base[mid:])
        
        return list(passwords)
    
    def generate_complex_combinations(self, username):
        """生成复杂组合"""
        passwords = set()
        base_variations = self.generate_basic_variations(username)
        
        for base in base_variations:
            # 数字 + 特殊字符
            for num in ['1', '12', '123', '666', '888']:
                for char in self.special_chars:
                    passwords.add(base + num + char)
                    passwords.add(base + char + num)
                    passwords.add(char + base + num)
                    passwords.add(num + base + char)
            
            # 年份 + 特殊字符
            for year in self.common_years:
                for char in self.special_chars:
                    passwords.add(base + year + char)
                    passwords.add(char + base + year)
            
            # leet 语转换 (a->@, o->0, i->1, e->3, s->$)
            leet = base.replace('a', '@').replace('o', '0').replace('i', '1').replace('e', '3').replace('s', '$')
            if leet != base:
                passwords.add(leet)
                passwords.add(leet + '123')
                passwords.add(leet + '!')
        
        return list(passwords)
    
    def generate_with_common_passwords(self, username):
        """结合常见密码"""
        passwords = set()
        parts = self.extract_username_parts(username)
        
        for pwd in self.common_passwords:
            passwords.add(pwd)
            passwords.add(parts['lower'] + pwd)
            passwords.add(pwd + parts['lower'])
            passwords.add(parts['upper'] + pwd)
            passwords.add(pwd + parts['upper'])
            
            # 添加特殊字符分隔
            for char in ['_', '.', '-']:
                passwords.add(parts['lower'] + char + pwd)
                passwords.add(pwd + char + parts['lower'])
        
        return list(passwords)
    
    def generate_date_based(self, username):
        """生成基于日期的密码"""
        passwords = set()
        base_variations = self.generate_basic_variations(username)
        now = datetime.now()
        
        # 月份 (01-12)
        for month in range(1, 13):
            month_str = str(month).zfill(2)
            for base in base_variations:
                passwords.add(base + month_str)
                passwords.add(month_str + base)
        
        # 日期 (01-31)
        for day in range(1, 32):
            day_str = str(day).zfill(2)
            for base in base_variations:
                passwords.add(base + day_str)
                passwords.add(day_str + base)
        
        # 年月组合
        for year in self.common_years:
            for month in range(1, 13):
                month_str = str(month).zfill(2)
                for base in base_variations:
                    passwords.add(base + year + month_str)
                    passwords.add(year + month_str + base)
        
        return list(passwords)
    
    def generate_all(self, usernames, output_file=None, target_count=None):
        """
        为所有用户名生成完整字典
        
        Args:
            usernames: 用户名列表
            output_file: 输出文件路径 (可选)
            target_count: 目标密码数量 (可选)
        
        Returns:
            生成的密码集合
        """
        all_passwords = set()
        
        for username in usernames:
            all_passwords.update(self.generate_basic_variations(username))
            all_passwords.update(self.generate_with_numbers(username))
            all_passwords.update(self.generate_with_special_chars(username))
            all_passwords.update(self.generate_complex_combinations(username))
            all_passwords.update(self.generate_with_common_passwords(username))
            all_passwords.update(self.generate_date_based(username))
        
        # 移除空字符串和过短的密码
        all_passwords = {pwd for pwd in all_passwords if pwd and len(pwd) >= 4}
        
        # 如果已有足够密码，直接返回或截取
        if target_count and len(all_passwords) >= target_count:
            all_passwords = set(list(all_passwords)[:target_count])
        
        # 如果不足，生成更多变体
        if target_count and len(all_passwords) < target_count:
            # 生成额外用户名变体
            extra_usernames = []
            for username in usernames:
                extra_usernames.extend([
                    username + username,
                    username * 2,
                    username + username[::-1],
                ])
                for num in range(1000):
                    extra_usernames.append(f"{username}{num:03d}")
                    extra_usernames.append(f"{num:03d}{username}")
            
            for username in extra_usernames:
                if len(all_passwords) >= target_count:
                    break
                all_passwords.update(self.generate_basic_variations(username))
                all_passwords.update(self.generate_with_numbers(username))
                all_passwords.update(self.generate_with_special_chars(username))
            
            # 最终截取目标数量
            if len(all_passwords) > target_count:
                all_passwords = set(list(all_passwords)[:target_count])
        
        # 保存到文件
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                for pwd in sorted(all_passwords):
                    f.write(pwd + '\n')
            print(f"已生成 {len(all_passwords)} 个唯一密码并保存到 {output_file}")
        else:
            print(f"共生成 {len(all_passwords)} 个唯一密码")
        
        return all_passwords


def main():
    """示例使用"""
    generator = WindowsUsernameDictGenerator()
    
    # 扩展的 Windows 用户名列表
    sample_usernames = [
        'Administrator', 'Admin', 'User', 'Guest', 'Default', 'Public',
        'All Users', 'John', 'Mike', 'Sarah', 'Tom', 'Jack', 'Owner',
        'Test', 'Dev', 'IT', 'Support', 'Manager', 'wang', 'li', 'zhang',
        'admin123', 'user123', 'administrator1', 'root', 'system',
        'service', 'network', 'local', 'domain', 'backup', 'sql',
        'www', 'ftp', 'mail', 'web', 'app', 'data', 'file', 'print',
        'chen', 'liu', 'huang', 'wu', 'zhou', 'xu', 'sun', 'ma',
        'zhu', 'hu', 'guo', 'he', 'gao', 'lin', 'luo', 'zheng',
        'Administrator1', 'Admin1', 'User1', 'Test1', 'Guest1',
        'admin001', 'user001', 'test001', 'root001', 'admin888',
        'wangwei', 'lijing', 'zhangwei', 'liuyang', 'chenjing',
        'ITAdmin', 'SysAdmin', 'NetAdmin', 'DbAdmin', 'WebAdmin',
        'PowerUser', 'SuperUser', 'DefaultUser', 'NewUser', 'OldUser'
    ]
    
    # 生成字典，确保 10 万条不重复
    passwords = generator.generate_all(
        sample_usernames,
        output_file='windows_username_dict.txt',
        target_count=100000
    )
    
    # 显示统计信息
    print("\n前 20 个密码示例:")
    for i, pwd in enumerate(sorted(passwords)[:20], 1):
        print(f"{i}. {pwd}")
    
    print(f"\n总密码数：{len(passwords)}")
    print(f"唯一密码数：{len(set(passwords))}")


if __name__ == '__main__':
    main()

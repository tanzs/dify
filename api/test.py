
from datetime import datetime
import pytz
import re


def add_space_after_mini_app_link(text: str) -> str:
    # 匹配可能缺少井号的小程序链接
    pattern = r'(?<!#)#?小程序://[\u4e00-\u9fa5]+/[A-Za-z0-9]+'

    def replacement(match: re.Match) -> str:
        return '#' + match.group(0).replace('#', '') + ' '

    return re.sub(pattern, replacement, text)

def is_working_hours(start_hour: int, end_hour: int, initial_text: str, append_text: str) -> str:
    """判断给定时间是否在指定工作时间内，并拼接文本"""
    tz = pytz.timezone("Asia/Shanghai")
    now = datetime.now(tz)

    if not (start_hour <= now.hour < end_hour):
        initial_text += append_text  # 如果在工作时间内，拼接内容

    return initial_text


def add_space_after_mini_app_link(text: str) -> str:
    # 匹配可能缺少井号的小程序链接
    pattern = r'(?<!#)#?小程序://[\u4e00-\u9fa5]+/[A-Za-z0-9]+'

    def replacement(match: re.Match) -> str:
        return '#' + match.group(0).replace('#', '') + ' '

    return re.sub(pattern, replacement, text)

if __name__ == '__main__':
    print(add_space_after_mini_app_link("小程序://翼企购/xqbN5uVmtiGr9Gn"))
'''
Author: caozhenwei cao.zhenwei@foxmail.com
Date: 2022-07-04 17:27:25
LastEditors: caozhenwei cao.zhenwei@foxmail.com
LastEditTime: 2022-07-08 00:45:46
FilePath: /Scripts/arm.uops.info/uops.py
Description: 
验证uops分解的正确性，找出最大互相验证的分解集合

Copyright (c) 2022 by caozhenwei cao.zhenwei@foxmail.com, All Rights Reserved. 
'''
import re
import pandas as pd
from typing import List


class Instr:
    # uops
    def __init__(self, inst):
        self.inst = inst  # 指令
        # TODO: 具体指令（add x4, x3, x2）到指令格式（ADDrrr）的转换
        self.inst_name = inst.split()[0]  # 助记符
        self.uops = None
        self.tp_gt = get_throughput(inst)
        self.tp_pred = -1


class Uop:
    def __init__(self):
        self.uop = ""


def get_uops(insts_file: str) -> List:
    """生成insts file文件中的uops信息，以列表格式返回

    Args:
        insts_file (str): file path, each line represents for a insts

    Returns:
        List: a list of class Instr
    """
    instrs = []
    with open(insts_file, 'r') as f:
        instrs = [Instr(line.strip()) for line in f.readlines()]
    process_td("/Users/zhenwei/Codes/Scripts/arm.uops.info/AArch64SchedTSV110.td")
    for instr in instrs:
        instr.tp_gt = get_throughput(instr.name)
        for mapping in inst_uop_mapping:
            if mapping.match(instr.inst_head):
                pass
    print("hello")


def get_throughput(inst: str) -> int:
    """使用寄存器版本的bhive，测量每个指令的throughput

    Args:
        inst (str): 指令字符串，示例："add x4, x3, x2"

    Returns:
        int: 平均throughput，每次将指令展开1000次测量throughput，然后对100次的测量结果取平均（共10w次）
    """
    pass


def get_uops(instr: Instr) -> None:
    """得到指令对应的uops和预测的throughput

    Args:
        instr (Instr): 类型为Instr的指令

    """


class UopMapping:
    # 存储uop到对应指令的映射关系
    def __init__(self, uop_name, tp_pred, port, inst_pattern):
        self.uop_name = uop_name
        self.tp_pred = tp_pred
        self.port = port
        self.inst_pattern = inst_pattern  # 能产生此uop的正则表达式

    def match(self, inst_head: str) -> bool:
        # TODO：一个思路是将指令的正则表达式展开成单个的指令形式，另一个思路是单个的指令形式与指令正则进行匹配
        re.compile(self.inst_pattern)
        match = re.search(self.insts, inst_head)
        return match is not None


inst_uop_mapping = list()


def process_td(file_path: str):
    # 提取只匹配生成一个uop的指令
    pattern = "def:InstRW<\[[a-zA-Z0-9_]*\],\(((instregex\".*\")|(instrs.*))\)>;"
    with open(file_path, 'r') as f:
        for _ in f.readlines():
            line = _.replace(" ", "").strip()
            if not re.match(pattern, line):
                continue
            print(f"line content without blank space: \n{line}")
            uop_pattern = "\[[a-zA-Z0-9_]*\]"
            uop_info = re.findall(uop_pattern, line)[0][1:-1]
            if len(uop_info.split("_")) != 3:  # 部分uop格式不正常
                print(f"\nget wrong format uop, pass: {uop_info}\n")
                continue
            print(f"uop_info: {uop_info}\n")
            uop_name, tp_pred, port = uop_info.split("_")
            print(
                f"uop name: {uop_name}, prediction throughput: {tp_pred}, port: {port}")
            inst_pattern1 = "instregex\".*\""
            inst_pattern2 = "instrs[a-zA-Z0-9]*"
            inst_pattern = ""
            if re.search(inst_pattern1, line):
                inst_pattern = re.findall(inst_pattern1, line)[0].replace(
                    "instregex", "").replace("\"", "")
            if re.search(inst_pattern2, line):
                inst_pattern = re.findall(inst_pattern2, line)[
                    0].replace("instrs", "")
            print(f"inst pattern: {inst_pattern}")
            inst_uop_mapping.append(UopMapping(
                uop_name, tp_pred, port, inst_pattern))


if __name__ == '__main__':
    process_td("/Users/zhenwei/Codes/Scripts/arm.uops.info/AArch64SchedTSV110.td")
    for uop_mapping in inst_uop_mapping:
        print(uop_mapping.inst_pattern)
    # get_uops("/Users/zhenwei/Codes/Scripts/arm.uops.info/insts.txt")

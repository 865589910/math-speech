#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数学学习工具 - AI语音批量生成脚本
使用 Edge TTS 为所有字词生成高质量AI语音音频文件
"""

import asyncio
import edge_tts
import os
from pathlib import Path

# 配置
VOICE = "zh-CN-XiaoxiaoNeural"  # 使用晓晓的声音（女声，温柔自然，适合小朋友）
OUTPUT_DIR = "audio"  # 音频文件输出目录
RATE = "-4%"  # 语速：稍慢一点，适合学习
VOLUME = "+0%"  # 音量：正常

# 多音字正确读音映射（使用同音字或数字标调拼音）
POLYPHONE_MAP = {
    '行': '航',  # 行列的行，用同音字"航"来生成正确读音
}

# 所有需要生成的字词数据
learning_data = {
    "section1_numbers": [
        "零", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十",
        "个", "百", "千", "万"
    ],
    "section1_operations": [
        "加", "减", "乘", "除", "差", "和", "积", "商",
        "加号", "减号", "乘号", "除号",
        "加数", "被减数", "减数", "乘数", "被除数", "除数",
        "等号", "大于号", "小于号", "算式", "计算"
    ],
    "section1_positions": [
        "行", "列", "排", "上", "下", "左", "右", "前", "后",
        "东", "西", "南", "北", "里", "内", "外"
    ],
    "section1_comparisons": [
        "大", "小", "多", "少", "长", "短", "高", "矮",
        "轻", "重", "厚", "薄", "快", "慢"
    ],
    "section1_units": [
        "厘米", "米", "元", "角", "分", "时", "秒", "克", "千克"
    ],
    "section1_quantifiers": [
        "个", "位", "名", "人", "只", "辆", "块", "瓶", "支", "本",
        "颗", "张", "把", "棵", "盒", "箱", "盘", "堆", "粒", "串",
        "架", "艘", "拃", "步", "庹", "倍"
    ],
    "section2_questionTypes": [
        "填一填", "算一算", "写一写", "画一画", "读一读", "选一选",
        "做一做", "分一分", "圈一圈", "摆一摆", "拨一拨", "涂颜色",
        "找规律", "列竖式", "口算", "解决问题", "列式计算",
        "找信息", "提问题", "看图列式"
    ],
    "section2_basicConcepts": [
        "大于", "小于", "等于", "一共", "还有", "剩下", "几个", "第几",
        "数数", "顺着数", "倒着数", "从左往右", "从上往下", "相邻数",
        "组成", "数位", "位数", "写数", "读数", "单数", "双数", "奇数",
        "偶数", "规律", "整时", "大小", "多少", "长短", "平均分",
        "乘法口诀", "最大", "最小", "连加", "连减", "混合运算",
        "分与合", "凑十法", "破十法", "平十法", "画图法", "线段",
        "长度", "重量", "测量", "猜测", "估计", "合适", "对半",
        "购物", "付给", "找回", "售出", "购买"
    ],
    "section2_items": [
        "积木", "拼图", "玩具汽车", "玩具飞机", "气球",
        "风筝", "毽子", "坦克", "火车", "船"
    ],
    "section2_animals": [
        "小鸡", "小鸭", "兔子", "小猫", "小狗",
        "小鸟", "青蛙", "猴子", "企鹅", "小鱼"
    ],
    "section2_foods": [
        "苹果", "香蕉", "桃子", "橘子", "草莓", "西瓜", "葡萄",
        "糖果", "蛋糕", "面包", "牛奶", "薯片", "巧克力"
    ],
    "section2_shapes": [
        "长方形", "正方形", "圆", "三角形", "平行四边形",
        "长方体", "正方体", "圆柱", "球", "三棱柱"
    ],
    "section3_fillMethods": [
        "加数加加数等于和",
        "和减加数等于加数",
        "被减数减减数等于差",
        "被减数减差等于减数",
        "减数加差等于被减数",
        "乘数乘乘数等于积",
        "积除乘数等于乘数",
        "被除数除除数等于商",
        "被除数除商等于除数",
        "除数乘商等于被除数"
    ],
    "section3_comparisonRules": [
        "加数变大和变大",
        "加数变小和变小",
        "加数一增一减和不变",
        "被减数变大差变大",
        "减数变大差变小",
        "被减数减数同增减差不变",
        "乘数变大积变大",
        "乘数变小积变小"
    ],
    "section3_hundredTable": [
        "往上减10",
        "往下加10",
        "往左减1",
        "往右加1"
    ],
    "section4_additionProblems": [
        "一共",
        "总共",
        "共有",
        "一共或总共或共有",
        "和",
        "增加",
        "添上",
        "增加或添上",
        "合起来",
        "倒入",
        "飞来了",
        "游来了",
        "开来了"
    ],
    "section4_subtractionProblems": [
        "还剩",
        "剩下",
        "还剩或剩下",
        "比多",
        "比少",
        "比多或比少",
        "多多少",
        "少多少",
        "多多少或少多少",
        "花了",
        "用去",
        "减少",
        "减少或用去",
        "送给",
        "飞走了",
        "游走了",
        "飞走或游走",
        "相差"
    ],
    "section4_multiplicationProblems": [
        "每……有……",
        "每",
        "每……有……或每",
        "倍",
        "积",
        "几个几",
        "一共"
    ],
    "section4_divisionProblems": [
        "平均分",
        "每几个装一",
        "商",
        "平均每个是几",
        "能分几份"
    ]
}


def sanitize_filename(word):
    """将字词转换为安全的文件名"""
    # 特殊字符替换
    replacements = {
        '＋': '加号', '－': '减号', '×': '乘号', '÷': '除号',
        '=': '等号', '>': '大于号', '<': '小于号',
        '/': '_', '\\': '_', ':': '_', '*': '_',
        '?': '_', '"': '_', '|': '_'
    }
    
    filename = word
    for char, replacement in replacements.items():
        filename = filename.replace(char, replacement)
    
    return filename


async def generate_audio(word, category=""):
    """为单个字词生成音频文件"""
    try:
        # 创建安全的文件名
        safe_filename = sanitize_filename(word)
        filename = f"{safe_filename}.mp3"
        
        # 创建目录结构
        if category:
            output_path = os.path.join(OUTPUT_DIR, category)
        else:
            output_path = OUTPUT_DIR
        
        os.makedirs(output_path, exist_ok=True)
        filepath = os.path.join(output_path, filename)
        
        # 如果文件已存在，跳过
        if os.path.exists(filepath):
            print(f"  ⏭️  跳过 {word} (已存在)")
            return True
        
        # 检查是否是多音字，如果是，使用拼音代替
        if word in POLYPHONE_MAP:
            # 对于多音字，直接使用拼音生成语音
            text_to_speak = POLYPHONE_MAP[word]
            print(f"  🔊 多音字修正: {word} -> 使用拼音 {text_to_speak}")
            communicate = edge_tts.Communicate(text_to_speak, VOICE, rate=RATE, volume=VOLUME)
        else:
            # 普通字词
            text_to_speak = word
            communicate = edge_tts.Communicate(word, VOICE, rate=RATE, volume=VOLUME)
        
        await communicate.save(filepath)
        
        print(f"  ✅ 生成 {word} -> {filepath}")
        return True
        
    except Exception as e:
        print(f"  ❌ 失败 {word}: {str(e)}")
        return False


async def generate_all_audio():
    """批量生成所有字词的音频"""
    print("=" * 60)
    print("🎙️  开始批量生成AI语音...")
    print(f"📁 输出目录: {OUTPUT_DIR}/")
    print(f"🎤 使用音色: {VOICE} (晓晓-温柔女声)")
    print(f"⚡ 语速: {RATE}")
    print("=" * 60)
    
    total = 0
    success = 0
    
    # 遍历所有分类
    for category_name, words_list in learning_data.items():
        print(f"\n📚 处理 {category_name} ({len(words_list)} 个)")
        
        # 生成每个字词的音频
        for word in words_list:
            total += 1
            result = await generate_audio(word, category_name)
            if result:
                success += 1
            
            # 每生成5个音频稍微暂停一下
            if total % 5 == 0:
                await asyncio.sleep(0.3)
    
    print("\n" + "=" * 60)
    print(f"🎉 生成完成！")
    print(f"📊 总计: {total} 个 | 成功: {success} 个 | 失败: {total - success} 个")
    print(f"📁 音频文件保存在: {os.path.abspath(OUTPUT_DIR)}")
    print("=" * 60)


async def main():
    """主函数"""
    await generate_all_audio()


if __name__ == "__main__":
    print("\n" + "🐼" * 20)
    print("   数学学习工具 - AI语音批量生成")
    print("🐼" * 20 + "\n")
    
    # 运行异步任务
    asyncio.run(main())
    
    print("\n✨ 全部完成！现在可以在网站中使用这些高质量AI语音了！\n")

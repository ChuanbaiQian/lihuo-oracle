import streamlit as st
from lunar_python import Solar, Lunar
from PIL import Image, ImageDraw, ImageFont
import random
from datetime import datetime
import io
import os

# 设置网页标题和图标
st.set_page_config(page_title="离火每日神谕", page_icon="🏮")

def generate_card():
    # 1. 数据逻辑
    today = datetime.now()
    solar = Solar.fromYmd(today.year, today.month, today.day)
    lunar = solar.getLunar()
    lunar_date = f"{lunar.getMonthInChinese()}月{lunar.getDayInChinese()}"
    gan_zhi = f"{lunar.getYearInGanZhi()} {lunar.getYearShengXiao()}年"
    pi_yu = random.choice(["虽有冷雨，朱砂不灭", "一念清净，烈焰成池", "在孤寂中，听见生机", "秩序所在，即是归处"])

    # 2. 绘图逻辑
    width, height = 600, 900
    if os.path.exists("bg.jpg"):
        img = Image.open("bg.jpg").resize((width, height))
    else:
        img = Image.new('RGB', (width, height), color=(245, 245, 240))
    
    draw = ImageDraw.Draw(img)
    
    # 字体处理（网页部署建议使用系统自带或上传的ttf）
    font_path = "font.ttf"
    if os.path.exists(font_path):
        font_main = ImageFont.truetype(font_path, 45)
        font_sub = ImageFont.truetype(font_path, 22)
    else:
        # 兼容性处理
        font_main = font_sub = ImageFont.load_default()

    # 3. 绘制元素 (沿用你的排版逻辑)
    draw.rectangle([40, 40, 90, 140], outline=(180, 40, 40), width=2)
    draw.text((50, 55), "离\n火", fill=(180, 40, 40), font=font_sub)
    draw.text((120, 80), f"{solar.toYmd()}", fill=(60, 60, 60), font=font_sub)
    y_start = 280
    for i, char in enumerate(pi_yu):
        draw.text((width//2 - 25, y_start + i*65), char, fill=(40, 40, 40), font=font_main)
    draw.text((80, 780), "宜：逻辑拆解", fill=(180, 40, 40), font=font_sub)
    draw.text((380, 860), "—— 逻辑架构师 · 存真", fill=(160, 160, 160), font=font_sub)

    return img

# --- Streamlit 前端界面 ---
st.title("🏮 离火每日神谕")
st.write("在清冷现实中，抽取属于你的那抹朱砂。")

if st.button('点击抽取今日神谕'):
    with st.spinner('正在感应意象...'):
        result_img = generate_card()
        
        # 将图片转为内存字节流以便显示和下载
        buf = io.BytesIO()
        result_img.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        st.image(byte_im, caption="今日神谕已送达", use_container_width=True)
        
        # 提供下载按钮
        st.download_button(
            label="保存这张神谕卡片",
            data=byte_im,
            file_name=f"fortune_{datetime.now().strftime('%m%d')}.png",
            mime="image/png"
        )
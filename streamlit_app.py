import streamlit as st
import pytesseract
from PIL import Image
import re

# تابع برای اصلاح خطاهای متداول در لینک‌ها
def correct_link(link):
    # اصلاح خطاهای احتمالی در https و www
    link = re.sub(r'(^ww\s?)', 'https://www.', link)  # اصلاح ww به www
    link = re.sub(r'(^Ottps)', 'https', link)  # اصلاح Ottps به https
    return link

# تابع برای استخراج لینک‌ها از متن و اعمال اصلاحات
def extract_links_from_text(text):
    # الگوی منظم برای شناسایی لینک‌ها
    links = re.findall(r'(https?://[^\s]+|ww[^\s]+)', text)
    # اصلاح لینک‌ها
    corrected_links = [correct_link(link) for link in links]
    return corrected_links

# تابع برای استخراج متن از تصویر
def extract_text_from_image(image):
    try:
        # پیکربندی برای زبان فارسی و انگلیسی
        custom_config = r'-l eng+fas --psm 6'
        # استخراج متن از تصویر
        text = pytesseract.image_to_string(image, config=custom_config)
        return text
    except Exception as e:
        return f"Error occurred: {e}"

# عنوان اصلی برنامه
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>سیستم خواندن متن های موجود در عکس</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>به سیستم راستینو خوش آمدید</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>تصویر خود را بارگذاری کنید و متن آن را استخراج نمایید.</p>", unsafe_allow_html=True)

# آپلود فایل تصویر
uploaded_file = st.file_uploader("لطفاً یک تصویر (PNG، JPG، JPEG) آپلود کنید", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # نمایش تصویر آپلود شده
    st.image(uploaded_file, caption="تصویر آپلود شده شما", use_column_width=True, output_format="auto")

    # اجرای تابع برای استخراج متن
    with st.spinner('در حال استخراج متن از تصویر...'):
        image = Image.open(uploaded_file)
        text = extract_text_from_image(image)

    # نمایش متن استخراج شده
    st.success("متن استخراج شده:")
    st.text_area("نتیجه OCR", text, height=250)

    # استخراج و نمایش لینک‌ها
    links = extract_links_from_text(text)
    if links:
        st.success("لینک‌های استخراج شده و اصلاح‌شده:")
        for link in links:
            st.write(link)
    else:
        st.warning("لینکی یافت نشد.")

    # گزینه‌ای برای دانلود نتیجه به صورت فایل متنی
    st.markdown("<br>", unsafe_allow_html=True)  # افزودن فاصله عمودی
    st.download_button(
        label="📥 دانلود نتیجه به صورت فایل متنی",
        data=text,
        file_name='result.txt',
        mime='text/plain'
    )

# استایل دهی سفارشی به عناصر UI
st.markdown("""
    <style>
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
    }

    .stButton > button:hover {
        background-color: white;
        color: black;
        border: 2px solid #4CAF50;
    }

    .stTextArea textarea {
        font-family: 'Courier New', Courier, monospace;
        background-color: #f9f9f9;
        color: #333;
        border: 2px solid #4CAF50;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

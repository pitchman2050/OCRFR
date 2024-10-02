import streamlit as st
import pytesseract
from PIL import Image

# تابع برای استخراج متن از تصویر
def extract_text_from_image(image):
    try:
        # پیکربندی برای زبان فارسی
        custom_config = r'-l fas --psm 6'

        # استخراج متن از تصویر
        text = pytesseract.image_to_string(image, config=custom_config)

        return text

    except Exception as e:
        return f"Error occurred: {e}"

# عنوان برنامه در صفحه وب
st.title(" سیستم تبدیل عکس به متن فارسی راستینو خوش آمدید ")

# آپلود فایل تصویر
uploaded_file = st.file_uploader("تصویر خود را بارگزاری کنید", type=["png", "jpg", "jpeg"])

# اگر فایل آپلود شد
if uploaded_file is not None:
    # نمایش تصویر آپلود شده
    image = Image.open(uploaded_file)
    st.image(image, caption='تصویر آپلود شده', use_column_width=True)

    # اجرای تابع برای استخراج متن
    text = extract_text_from_image(image)

    # نمایش متن استخراج شده
    st.write("متن استخراج شده از تصویر:")
    st.text_area("نتیجه OCR", text)

    # گزینه‌ای برای دانلود نتیجه به صورت فایل متنی
    if st.button("دانلود نتیجه"):
        st.download_button(
            label="دانلود فایل",
            data=text,
            file_name='result.txt',
            mime='text/plain'
        )

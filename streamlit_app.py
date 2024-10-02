import streamlit as st
import requests
from PIL import Image
import io

# تابع برای ارسال تصویر به API و دریافت متن
def extract_text_from_image(image):
    try:
        # تبدیل تصویر به بایت‌ها
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        # ارسال درخواست به OCR.space
        response = requests.post(
            'https://api.ocr.space/parse/image',
            files={'image': img_byte_arr},
            data={'apikey': 'K84673681588957', 'language': 'fas'}
        )
        result = response.json()
        return result.get('ParsedResults')[0].get('ParsedText', 'متنی یافت نشد.')

    except Exception as e:
        return f"Error occurred: {e}"

# عنوان برنامه در صفحه وب
st.title("سیستم تشخیص متن فارسی (OCR)")

# آپلود فایل تصویر
uploaded_file = st.file_uploader("یک تصویر را آپلود کنید", type=["png", "jpg", "jpeg"])

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

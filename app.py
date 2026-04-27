
import streamlit as st
import datetime
import pandas as pd
import os

# --- إعدادات الشركة (هذا الجزء فقط ما ستغيره لكل شركة جديدة) ---
COMPANY_NAME = "بن شعاعة محمد الهادي "  # اسم الشركة
WORKER_CODE = "2222"                  # رمز العمال
ADMIN_CODE = "5555"                   # رمز المدير
DATA_FILE = "attendance_records.csv"   # ملف البيانات
# ---------------------------------------------------------

st.set_page_config(page_title=COMPANY_NAME, page_icon="⚖️")

st.title(f"⚖️ {COMPANY_NAME}")
st.subheader("نظام العدل الذكي للحضور والأجور")

# مدخلات المستخدم
user_name = st.text_input("اسم الموظف / العامل")
user_code = st.text_input("الرمز السري", type="password")

col1, col2 = st.columns(2)

with col1:
    if st.button("تسجيل دخول (Check-In)"):
        if user_code == WORKER_CODE and user_name:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_data = pd.DataFrame([[now, user_name, "دخول"]], columns=["الوقت", "الاسم", "الحالة"])
            if not os.path.isfile(DATA_FILE):
                new_data.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
            else:
                new_data.to_csv(DATA_FILE, mode='a', header=False, index=False, encoding='utf-8-sig')
            st.success(f"تم تسجيل دخول {user_name} بنجاح")
        else:
            st.error("بيانات غير صحيحة")

with col2:
    if st.button("تسجيل خروج (Check-Out)"):
        if user_code == WORKER_CODE and user_name:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_data = pd.DataFrame([[now, user_name, "خروج"]], columns=["الوقت", "الاسم", "الحالة"])
            if not os.path.isfile(DATA_FILE):
                new_data.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
            else:
                new_data.to_csv(DATA_FILE, mode='a', header=False, index=False, encoding='utf-8-sig')
            st.info(f"تم تسجيل خروج {user_name}")
        else:
            st.error("بيانات غير صحيحة")

# قسم الإدارة
st.divider()
admin_input = st.text_input("لوحة تحكم المدير", type="password")
if admin_input == ADMIN_CODE:
    if os.path.isfile(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        st.write("### سجل الحركات")
        st.dataframe(df)
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("تحميل التقرير (Excel)", data=csv, file_name=f"Report_{COMPANY_NAME}.csv")
    else:
        st.write("السجل فارغ حالياً.")

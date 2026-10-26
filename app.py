import os
from datetime import datetime
import jdatetime
import pandas as pd
import requests
import streamlit as st

# --- تنظیمات تلگرام ---
TELEGRAM_BOT_TOKEN = st.secrets["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = st.secrets["TELEGRAM_CHAT_ID"]


def send_to_telegram(text):
  url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
  payload = {
      "chat_id": TELEGRAM_CHAT_ID,
      "text": text,
      "parse_mode": "Markdown",
  }
  try:
    requests.post(url, json=payload)
  except Exception as e:
    print(f"Error: {e}")


st.set_page_config(page_title="میگرانا - رزرو مشاوره", layout="centered")

file_name = "customers.csv"

# ساخت دیتابیس اولیه همراه با ستون تاریخ و زمان ثبت (created_at)
if not os.path.exists(file_name):
  df_init = pd.DataFrame(columns=[
      "id",
      "created_at",
      "name",
      "phone",
      "consultation_type",
      "education",
      "age",
      "marital_status",
      "travel_history",
      "payment_code",
      "status",
  ])
  df_init.to_csv(file_name, index=False, encoding="utf-8-sig")

# --- هدر صفحه و لوگو ---
col1, col2 = st.columns([4, 1])

with col1:
  st.title("🎯 رزرو مشاوره  - MIGRANA")
  st.write("لطفاً پیش از ثبت فرم، اطلاعات زیر را مطالعه کنید.")

with col2:
  if os.path.exists("logo.png"):
    st.image("logo.png", width=80)

st.markdown("---")

# --- بخش آیکون‌ها و اطلاعات راهنما ---

with st.expander("🇪🇸 راهنمای اقامت اسپانیا "):
  st.markdown("""اسپانیا چند مسیر مختلف برای دریافت اقامت داره و در حال حاضر یکی از بهترین گزینه‌های قابل‌بررسی برای ایرانی‌ها است. 🇪🇸
هر مسیر شرایط و جزئیات خاص خودش رو داره؛ بنابراین مهمه متناسب با شرایط پرونده‌تون، مسیر مناسب رو انتخاب کنید.
با رزرو مشاوره اختصاصی می‌تونید با شرایط و جزئیات هر مسیر آشنا بشید و برای انتخاب مسیر مناسب خودتون، آگاهانه‌تر تصمیم بگیرید. 🤍
""")

with st.expander("🎓 شرایط ویزای تحصیلی "):
  st.markdown("""تحصیل در کشورهای مختلف می‌تونه فرصتی برای پیشرفت تحصیلی و ساختن آینده‌ای بهتر باشه. 🌍
هر کشور شرایط خاص خودش رو برای پذیرش دانشگاه، دریافت ویزا، تمکن مالی و هزینه‌های تحصیل و زندگی داره؛ بنابراین مهمه متناسب با شرایط و هدفتون، کشور و مسیر مناسبی رو انتخاب کنید.
با رزرو مشاوره اختصاصی در **MIGRANA**، می‌تونید با شرایط و جزئیات تحصیل در کشورهای مختلف آشنا بشید و برای انتخاب مسیر مناسب خودتون، آگاهانه‌تر تصمیم بگیرید. 🤍
""")

with st.expander("❓ در جلسه مشاوره چه میگذرد؟"):
  st.markdown("""در جلسه اختصاصی، شرایط، اهداف و اولویت‌های شما بررسی می‌شه تا مسیرهای مناسب برای دریافت اقامت رو بشناسید.
از بررسی روش‌های مختلف اقامت اسپانیا و پروسه تحصیلی و شرایط اقدام گرفته تا مدارک، تمکن مالی، هزینه‌ها، زمان‌بندی و مراحل پرونده، به سؤالاتتون پاسخ داده می‌شه.
خروجی جلسه، شناخت گزینه‌های متناسب با شرایط شما و یک نقشه راه روشن برای انتخاب مسیر و شروع اقدام خواهد بود. 🤍
""")

st.markdown("---")

# --- فرم ثبت‌نام و رزرو مشاوره ---
st.subheader("فرم درخواست رزرو وقت مشاوره")

consultation_type = st.radio(
    "انتخاب نوع مشاوره:", ["ارزیابی رایگان", "مشاوره اختصاصی (دارای هزینه)"]
)

with st.form("client_form"):
  if consultation_type == "ارزیابی رایگان":
    new_name = st.text_input("نام و نام خانوادگی *")
    new_phone = st.text_input("شماره تماس *")

    new_education = "-"
    new_age = "-"
    marital_status = "-"
    travel_history = "-"
    payment_code = "رایگان"

  else:  # مشاوره اختصاصی (دارای هزینه)
    new_name = st.text_input("نام و نام خانوادگی *")
    new_phone = st.text_input("شماره تماس *")
    new_education = st.selectbox(
        "آخرین مدرک تحصیلی",
        ["دیپلم", "کاردانی", "کارشناسی", "کارشناسی ارشد", "دکتری"],
    )
    new_age = st.number_input(
        "سن خود را وارد کنید", min_value=15, max_value=70, value=22
    )
    marital_status = st.selectbox("وضعیت تأهل", ["مجرد", "متأهل"])
    travel_history = st.text_input("سابقه سفر")

    st.info(
        "💳 هزینه مشاوره اختصاصی: ۳۵۰ هزار تومان به نام محمدرضا فروغی. لطفاً به"
        " شماره کارت `5859471028554321` واریز کرده و کد پیگیری را در زیر وارد"
        " کنید."
    )
    payment_code = st.text_input("شماره پیگیری یا کد تراکنش بانکی *")

  submit_button = st.form_submit_button(label="ثبت نهایی درخواست")

  if submit_button:
    if not new_name or not new_phone:
      st.error("لطفاً نام و شماره تماس خود را وارد کنید!")
    elif (
        consultation_type == "مشاوره اختصاصی (دارای هزینه)" and not payment_code
    ):
      st.error("لطفاً شماره پیگیری پرداخت را وارد کنید!")
    else:
      # دریافت زمان شمسی با اعداد انگلیسی
      now = jdatetime.datetime.now()
      current_time = now.strftime("%Y/%m/%d - %H:%M:%S")

      df = pd.read_csv(file_name, encoding="utf-8-sig")
      new_id = len(df) + 1

      new_data = pd.DataFrame({
          "id": [new_id],
          "created_at": [current_time],
          "name": [new_name],
          "phone": [new_phone],
          "consultation_type": [consultation_type],
          "education": [new_education],
          "age": [new_age],
          "marital_status": [marital_status],
          "travel_history": [travel_history],
          "payment_code": [payment_code],
          "status": ["در انتظار بررسی"],
      })

      df = pd.concat([df, new_data], ignore_index=True)
      df.to_csv(file_name, index=False, encoding="utf-8-sig")

      # ارسال اطلاعات کامل به تلگرام
      telegram_message = (
          f"🚨 *فرم رزرو مشاوره جدید ثبت شد!*\n\n"
          f"📌 نوع مشاوره: {consultation_type}\n"
          f"👤 نام: {new_name}\n"
          f"📞 شماره تماس: {new_phone}\n"
          f"🎓 مدرک تحصیلی: {new_education}\n"
          f"🎂 سن: {new_age}\n"
          f"💍 وضعیت تأهل: {marital_status}\n"
          f"✈️ سابقه سفر: {travel_history}\n"
          f"💳 کد پیگیری: {payment_code}\n"
          f"📅 تاریخ ثبت: {current_time}"
      )
      send_to_telegram(telegram_message)

      st.success(
          "درخواست شما با موفقیت ثبت شد! به زودی با شما تماس خواهیم گرفت."
      )

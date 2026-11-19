import os
import gspread
import jdatetime
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

st.set_page_config(page_title="میگرانا - رزرو مشاوره", layout="centered")


# --- اتصال امن به Google Sheets ---
@st.cache_resource
def get_gsheet():
  scope = [
      "https://spreadsheets.google.com/feeds",
      "https://www.googleapis.com/auth/drive",
  ]
  creds_dict = dict(st.secrets["gcp_service_account"])
  creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
  client = gspread.authorize(creds)
  sheet = client.open("Migrana_Leads").sheet1
  return sheet


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
    if not new_name.strip() or not new_phone.strip():
      st.error("لطفاً نام و شماره تماس خود را وارد کنید!")
    elif (
        consultation_type == "مشاوره اختصاصی (دارای هزینه)"
        and not payment_code.strip()
    ):
      st.error("لطفاً شماره پیگیری پرداخت را وارد کنید!")
    else:
      try:
        sheet = get_gsheet()

        # محاسبه شناسه جدید بر اساس تعداد ردیف‌های فعلی شیت
        existing_records = sheet.get_all_values()
        new_id = len(existing_records) if len(existing_records) > 0 else 1

        # دریافت زمان شمسی با اعداد انگلیسی
        now = jdatetime.datetime.now()
        current_time = now.strftime("%Y/%m/%d - %H:%M:%S")
        today_shamsi = now.strftime("%Y/%m/%d")

        # تجمیع اطلاعات تکمیلی برای ستون notes_info
        if consultation_type == "ارزیابی رایگان":
          notes_info = "نوع درخواست: ارزیابی رایگان"
        else:
          notes_info = (
              f"مدرک: {new_education} | سن: {new_age} | تأهل: {marital_status} |"
              f" سابقه سفر: {travel_history} | کد پیگیری: {payment_code.strip()}"
          )

        # ساخت ردیف دقیقاً مطابق ۸ ستون گوگل‌شیت (A تا H)
        new_row = [
            new_id,  # A: deal_id
            current_time,  # B: created_at
            new_name.strip(),  # C: name
            new_phone.strip(),  # D: phone
            consultation_type,  # E: consultation_type
            notes_info,  # F: notes_info
            today_shamsi,  # G: alarm_date
            "12:00",  # H: alarm_time
        ]

        sheet.append_row(new_row)
        st.success(
            "درخواست شما با موفقیت ثبت شد! به زودی با شما تماس خواهیم گرفت."
        )

      except Exception:
        st.error(
            "خطایی در ثبت اطلاعات رخ داد. لطفاً مجدداً تلاش کنید یا در واتساپ"
            " پیام دهید."
        )
        

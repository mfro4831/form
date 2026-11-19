from datetime import date, datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import streamlit as st

st.set_page_config(
    page_title="فرم مشاوره و ارزیابی | MIGRANA",
    page_icon="✈️",
    layout="centered",
)

# --- استایل اختصاصی میگرانا (مشکی، سرمه‌ای تیره، فیروزه‌ای، سفید) ---
st.markdown(
    """
<style>
    html, body, .stApp {
        font-family: 'Tahoma', 'Segoe UI', sans-serif;
        direction: rtl;
        text-align: right;
    }
    .header-box {
        background-color: #101827;
        border: 1px solid #1e293b;
        border-top: 4px solid #00d4ff;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
    }
</style>
""",
    unsafe_allow_html=True,
)


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


# --- ارسال نوتیفیکیشن امن به تلگرام (اختیاری و بدون قرارگیری توکن در کد) ---
def send_safe_telegram_alert(name, phone, service, notes):
  try:
    bot_token = st.secrets["telegram"]["bot_token"]
    chat_id = st.secrets["telegram"]["chat_id"]
    text = (
        "🔔 **درخواست مشاوره جدید (MIGRANA)**\n\n"
        f"👤 نام: {name}\n"
        f"📞 شماره تماس: `{phone}`\n"
        f"📌 مسیر: {service}\n"
        f"📝 توضیحات: {notes if notes else 'ندارد'}\n"
        "✅ اطلاعات در گوگل‌شیت و CRM ثبت شد."
    )
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    requests.post(
        url,
        json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"},
        timeout=5,
    )
  except Exception:
    pass


# --- هدر فرم ---
st.markdown(
    """
<div class="header-box">
    <h2 style="color: #00d4ff; margin-bottom: 8px;">فرم ارزیابی و مشاوره مهاجرتی MIGRANA</h2>
    <p style="color: #cbd5e1; font-size: 14px; margin: 0;">اطلاعات خود را وارد کنید تا کارشناسان ما در کوتاه‌ترین زمان با شما تماس بگیرند.</p>
</div>
""",
    unsafe_allow_html=True,
)

# --- فرم دریافت اطلاعات ---
with st.form("migrana_consultation_form", clear_on_submit=True):
  full_name = st.text_input("نام و نام خانوادگی *")
  phone_number = st.text_input(
      "شماره تماس (واتساپ یا تلگرام) *", placeholder="مثلاً: 09123456789"
  )

  service_type = st.selectbox(
      "مسیر یا کشور مورد نظر *",
      [
          "اقامت اسپانیا (تمکن مالی / دیجیتال نومد / تحصیلی)",
          "ویزای تحصیلی اروپا (اتریش، آلمان، هلند، فنلاند)",
          "ویزای تحصیلی استرالیا",
          "دوره‌های زبان خارج از کشور",
          "ارزیابی رایگان و مشاوره عمومی",
      ],
  )

  age_edu = st.text_input(
      "سن و آخرین مدرک تحصیلی", placeholder="مثلاً: ۲۵ سال، کارشناسی کامپیوتر"
  )
  extra_notes = st.text_area(
      "توضیحات یا سوالات شما (اختیاری)",
      placeholder="شرایط خود را کوتاه بنویسید...",
      height=90,
  )

  submitted = st.form_submit_button(
      "ثبت درخواست مشاوره 🚀", type="primary", use_container_width=True
  )

  if submitted:
    if not full_name.strip() or not phone_number.strip():
      st.error("لطفاً نام و شماره تماس خود را وارد کنید.")
    else:
      try:
        sheet = get_gsheet()
        existing_records = sheet.get_all_values()
        new_id = len(existing_records)  # ردیف اول هدر است، پس شماره ردیف بعدی می‌شود ID

        now_str = datetime.now().strftime("%Y/%m/%d - %H:%M")
        today_str = str(date.today())
        combined_info = f"سن/تحصیلات: {age_edu} | توضیحات: {extra_notes}"

        # ساخت ردیف دقیقاً مطابق ساختار CRM میگرانا
        # ساخت ردیف دقیقاً مطابق ۸ ستون گوگل شیت
        new_row = [
            new_id,  # deal_id (A)
            now_str,  # created_at (B)
            full_name.strip(),  # name (C)
            phone_number.strip(),  # phone (D)
            service_type,  # consultation_type (E)
            combined_info,  # notes_info (F)
            today_str,  # alarm_date (G)
            "12:00",  # alarm_time (H)
        ]


        sheet.append_row(new_row)
        send_safe_telegram_alert(
            full_name.strip(),
            phone_number.strip(),
            service_type,
            combined_info,
        )

        st.success(
            "✅ اطلاعات شما با موفقیت ثبت شد! کارشناسان میگرانا به‌زودی با شما"
            " تماس خواهند گرفت."
        )
      except Exception as e:
        st.error("خطایی در ثبت اطلاعات رخ داد. لطفاً مجدداً تلاش کنید.")

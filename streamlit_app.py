import streamlit as st
import urllib.parse
import pandas as pd
from datetime import datetime, date

# 1. 페이지 설정
st.set_page_config(page_title="현문사주 - 지혜로운 인생 상담", page_icon="🔮")

# 설정 정보
MY_PHONE = "01063448677"
ADMIN_PASSWORD = "6080" # 사장님 비밀번호는 유지됩니다.
ACCOUNT_INFO = "광주은행 1107-021-637550 (예금주: 현문사주)"

if 'reservations' not in st.session_state:
    st.session_state.reservations = []

# 스타일 설정
st.markdown("""
    <style>
    html, body, [class*="st-"] { font-size: 1.3rem; background-color: #fffaf0; }
    .stButton>button { height: 4.5em; width: 100%; font-weight: bold; border-radius: 15px; background-color: #4a148c; color: white; }
    .main-title { color: #2e1a47; text-align: center; font-weight: bold; border-bottom: 3px solid #4a148c; padding-bottom: 10px; }
    .copy-box { background-color: #ffffff; padding: 20px; border: 2px dashed #4a148c; border-radius: 15px; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🔮 현문사주 (玄門四柱)</h1>", unsafe_allow_html=True)

# 탭 이름에서 6080을 완전히 뺐습니다.
tab1, tab2 = st.tabs(["📅 상담 예약 신청", "🔒 관리자 메뉴"])

with tab1:
    st.markdown(f"<div style='background-color: #f3e5f5; padding: 20px; border-radius: 15px; border: 2px solid #4a148c; text-align: center; font-weight: bold;'>💰 복채: 1인 3만원 / 가족 10만원<br>🏦 {ACCOUNT_INFO}</div>", unsafe_allow_html=True)

    with st.form("hyeonmun_form"):
        st.subheader("🗓️ 1. 상담 날짜와 시간 선택")
        c_date = st.date_input("상담 날짜 선택", min_value=date.today(), format="YYYY/MM/DD")
        c_time = st.selectbox("상담 시간 선택", ["09:00", "10:00", "11:00", "18:00", "19:00", "20:00", "21:00", "22:00"])
        
        st.write("---")
        st.subheader("📝 2. 신청자 정보 입력")
        name = st.text_input("상담 받으실 분 성함")
        phone = st.text_input("연락처 (예: 010-1234-5678)")
        cal = st.selectbox("생일 구분", ["☀️ 양력", "🌙 음력"])
        b_date = st.date_input("태어난 날짜", value=date(1980, 1, 1), min_value=date(1900, 1, 1), max_value=date.today(), format="YYYY/MM/DD")
        b_time = st.selectbox("태어난 시", ["모름", "자시(23~01)", "축시(01~03)", "인시(03~05)", "묘시(05~07)", "진시(07~09)", "사시(09~11)", "오시(11~13)", "미시(13~15)", "신시(15~17)", "유시(17~19)", "술시(19~21)", "해시(21~23)"])
        
        detail = st.text_area("구체적인 고민")
        submit_btn = st.form_submit_button("예약 정보 저장하기")
        
        if submit_btn:
            if not name or not phone:
                st.warning("⚠️ 성함과 연락처를 꼭 입력해주세요!")
            else:
                res = {
                    "상담일": c_date.strftime("%Y년 %m월 %d일"),
                    "시간": c_time,
                    "성함": name,
                    "연락처": phone,
                    "사주": f"{b_date.strftime('%Y년 %m월 %d일')}({cal}) {b_time}"
                }
                st.session_state.reservations.append(res)
                
                full_msg = f"[현문사주 신청] 성함:{name} 번호:{phone} 일시:{res['상담일']} {res['시간']} 사주:{res['사주']}"
                encoded_msg = urllib.parse.quote(full_msg)
                sms_link = f"sms:{MY_PHONE}?body={encoded_msg}"
                
                st.success("✅ 저장이 완료되었습니다!")
                st.markdown(f"<div class='copy-box'><strong>복사해서 사장님께 보내주세요:</strong><br><br>{full_msg}</div>", unsafe_allow_html=True)
                st.markdown(f'<a href="{sms_link}"><button>📲 폰에서 바로 문자 보내기</button></a>', unsafe_allow_html=True)

with tab2:
    st.subheader("🔒 관리자 전용 인증")
    # 화면에는 6080이 안 나오지만, 실제로는 6080을 쳐야 들어갈 수 있습니다.
    pw = st.text_input("비밀번호를 입력하세요", type="password")
    
    if pw == ADMIN_PASSWORD:
        st.success("🔓 인증되었습니다. 예약 명단을 확인하세요.")
        if st.session_state.reservations:
            df = pd.DataFrame(st.session_state.reservations).sort_values(by=["상담일", "시간"])
            st.dataframe(df, use_container_width=True)
            
            csv = df.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📁 명단 엑셀 저장", data=csv, file_name='현문사주_명단.csv')
        else:
            st.info("아직 접수된 내역이 없습니다.")
    elif pw != "":
        st.error("❌ 비밀번호가 틀렸습니다.")

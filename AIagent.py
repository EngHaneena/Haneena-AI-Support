import streamlit as st
from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. إعدادات الصفحة (التصميم)
st.set_page_config(page_title="Haneena AI Support", page_icon="🤖", layout="centered")

st.title("🤖 Haneena's Engineering AI")
st.markdown("---")

# 2. جلب المفتاح من Secrets
if "GOOGLE_API_KEY" in st.secrets:
    google_api_key = st.secrets["GOOGLE_API_KEY"]
    
    # 3. تعريف المحرك (استخدام Flash للسرعة مع معالجة خطأ 404)
    # أضفنا سطر version="v1" لضمان التوافق التام
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=google_api_key,
        version="v1",
        temperature=0.3
    )

    # 4. تعريف العميل الذكي (Agent)
    # تم إيقاف verbose لزيادة السرعة
    support_agent = Agent(
        role='Computer Engineering Expert',
        goal='Provide fast and accurate technical support.',
        backstory='You are a helpful AI assistant specialized in Computer Engineering and Robotics.',
        llm=llm,
        allow_delegation=False,
        verbose=False
    )

    # 5. واجهة المستخدم المدخلات

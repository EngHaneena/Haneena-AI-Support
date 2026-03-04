import streamlit as st
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# 1. إعداد الصفحة
st.set_page_config(page_title="Haneena AI Support", page_icon="🤖", layout="centered")

st.title("🤖 Haneena's Engineering AI")
st.markdown("---")

# 2. إعدادات البيئة لحل مشكلة الـ Signal والـ 404
os.environ["OTEL_SDK_DISABLED"] = "true"

# 3. التحقق من المفتاح في Secrets
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    
    user_query = st.text_input("How can I help you today, Engineer?", placeholder="Ask your technical question...")

    if user_query:
        with st.status("🚀 Processing with CrewAI...", expanded=False) as status:
            try:
                # 4. الحل البديل والأكثر استقراراً: استدعاء الموديل باسمه المباشر
                # قمنا بإزالة gemini/ واستخدمنا الاسم الذي تطلبه النسخة المستقرة
                llm = ChatGoogleGenerativeAI(
                    model="gemini-1.5-flash", 
                    google_api_key=api_key,
                    temperature=0.3
                )

                # 5. تعريف العميل (Agent)
                support_agent = Agent(
                    role='Computer Engineering Expert',
                    goal='Provide accurate technical support.',
                    backstory='You are a professional AI mentor specialized in Engineering.',
                    llm=llm,
                    allow_delegation=False,
                    verbose=False
                )

                # 6. تعريف المهمة (Task)
                task = Task(
                    description=user_query,
                    agent=support_agent,
                    expected_output="A helpful and concise technical response."
                )

                # 7. تشغيل الفريق (Crew)
                # أضفنا share_crew=False لتجنب مشاكل الخيوط (Threads)
                crew = Crew(
                    agents=[support_agent],
                    tasks=[task],
                    process=Process.sequential,
                    verbose=False,
                    share_crew=False
                )
                
                result = crew.kickoff()
                
                status.update(label="✅ Success!", state="complete")
                
                st.markdown("### 🤖 Response:")
                st.info(result.raw)
                
            except Exception as e:
                # محاولة أخيرة: إذا فشل الموديل، جربي gemini-pro
                st.error(f"System Error: {e}")
                st.warning("🔄 Tip: If 404 persists, the API might be restricted in your region for this model.")
                status.update(label="❌ Error occurred", state="error")
else:
    st.warning("⚠️ Please add GOOGLE_API_KEY to Streamlit Secrets.")

st.sidebar.markdown("---")
st.sidebar.write("🛠️ Developed by: **Eng. Haneena**")


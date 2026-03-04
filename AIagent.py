import streamlit as st
import os

# تعطيل الخصائص التي تسبب أخطاء الـ Signal والـ Thread قبل استدعاء المكتبات
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["PYDANTIC_SKIP_VALIDATION"] = "true"

from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI

# إعداد الصفحة
st.set_page_config(page_title="Haneena AI", page_icon="🤖")
st.title("🤖 Engineering AI Support")

# التحقق من المفتاح
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    
    query = st.text_input("How can I help you?", placeholder="Type your technical question...")

    if query:
        with st.status("🚀 Processing...", expanded=True) as status:
            try:
                # محرك البحث (الربط المباشر)
                llm = ChatGoogleGenerativeAI(
                    model="gemini-1.5-flash", 
                    google_api_key=api_key
                )

                # العميل
                eng_agent = Agent(
                    role='Senior Engineer',
                    goal='Solve technical problems',
                    backstory='Expert assistant',
                    llm=llm,
                    allow_delegation=False
                )

                # المهمة
                task = Task(
                    description=query,
                    agent=eng_agent,
                    expected_output="Clear technical response"
                )

                # الفريق (إعدادات الأمان لـ Streamlit)
                crew = Crew(
                    agents=[eng_agent],
                    tasks=[task],
                    process=Process.sequential,
                    share_crew=False # أهم سطر لحل مشكلة الـ Signal
                )
                
                # تنفيذ
                response = crew.kickoff()
                
                status.update(label="✅ Done!", state="complete")
                st.success("### 🤖 Response:")
                st.write(response.raw)
                
            except Exception as e:
                st.error(f"Error: {e}")
                status.update(label="❌ Failed", state="error")
else:
    st.warning("⚠️ Please add GOOGLE_API_KEY to App Secrets.")

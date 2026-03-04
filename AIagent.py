import streamlit as st
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. إعدادات الصفحة
st.set_page_config(page_title="Haneena AI Support", page_icon="🤖", layout="centered")

st.title("🤖 Haneena's Engineering AI")
st.markdown("---")

# 2. التحقق من المفتاح في Secrets
if "GOOGLE_API_KEY" in st.secrets:
    google_api_key = st.secrets["GOOGLE_API_KEY"]
    
    # واجهة المدخلات
    user_query = st.text_input("How can I help you today, Engineer?", placeholder="Ask your question...")

    if user_query:
        with st.status("🚀 Processing with CrewAI...", expanded=False) as status:
            try:
                # 3. تعريف المحرك (استخدام المسار الكامل والنسخة v1)
                llm = ChatGoogleGenerativeAI(
                    model="models/gemini-1.5-flash",
                    google_api_key=google_api_key,
                    version="v1",
                    temperature=0.3
                )

                # 4. تعريف العميل (Agent) - حل مشكلة LiteLLM Fallback
                support_agent = Agent(
                    role='Computer Engineering Expert',
                    goal='Provide accurate technical support.',
                    backstory='You are a professional AI mentor specialized in Engineering.',
                    llm=llm,
                    function_calling_llm=llm, # هذا السطر يمنع الخطأ
                    allow_delegation=False,
                    verbose=False
                )

                # 5. تعريف المهمة (Task)
                task = Task(
                    description=user_query,
                    agent=support_agent,
                    expected_output="A helpful and concise technical response."
                )

                # 6. تشغيل الفريق (Crew) - تحديد الـ Process بوضوح
                crew = Crew(
                    agents=[support_agent],
                    tasks=[task],
                    process=Process.sequential,
                    verbose=False
                )
                
                result = crew.kickoff()
                
                status.update(label="✅ Success!", state="complete")
                
                st.markdown("### 🤖 Response:")
                st.info(result.raw)
                
            except Exception as e

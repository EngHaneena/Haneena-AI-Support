import streamlit as st
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# 1. إعدادات الصفحة
st.set_page_config(page_title="Haneena AI Support", page_icon="🤖", layout="centered")

st.title("🤖 Haneena's Engineering AI")
st.markdown("---")

# 2. إعدادات البيئة
os.environ["OTEL_SDK_DISABLED"] = "true"

# 3. التحقق من المفتاح في Secrets
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    os.environ["GEMINI_API_KEY"] = api_key # احتياط لـ LiteLLM
    
    user_query = st.text_input("How can I help you today, Engineer?", placeholder="Ask your question...")

    if user_query:
        with st.status("🚀 Processing...", expanded=False) as status:
            try:
                # 4. تعريف المحرك (الصيغة الأكثر استقراراً)
                llm = ChatGoogleGenerativeAI(
                    model="gemini-1.5-flash", 
                    google_api_key=api_key,
                    temperature=0.3
                )

                # 5. تعريف العميل (Agent)
                support_agent = Agent(
                    role='Computer Engineering Expert',
                    goal='Provide technical support.',
                    backstory='Expert AI assistant.',
                    llm=llm,
                    # نستخدم محرك البحث عن الموديل داخلياً لـ CrewAI
                    model_name="gemini/gemini-1.5-flash",
                    allow_delegation=False,
                    verbose=False
                )

                # 6. المهمة
                task = Task(description=user_query, agent=support_agent, expected_output="Technical response.")

                # 7. الفريق
                crew = Crew(
                    agents=[support_agent],
                    tasks=[task],
                    process=Process.sequential,
                    share_crew=False
                )
                
                result = crew.kickoff()
                
                status.update(label="✅ Done!", state="complete")
                st.markdown("### 🤖 Response:")
                st.info(result.raw)
                
            except Exception as e:
                st.error(f"Error: {e}")
                status.update(label="❌ Failed", state="error")
else:
    st.error("⚠️ Add GOOGLE_API_KEY to Secrets first!")


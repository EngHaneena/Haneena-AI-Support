import streamlit as st
import os

# --- حل مشكلة الـ Signal والجلسات (يجب أن يكون في أعلى الملف) ---
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["PYDANTIC_SKIP_VALIDATION"] = "true"

from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI

st.set_page_config(page_title="Haneena AI", layout="centered")
st.title("🤖 Engineering AI Support")

if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    
    user_query = st.text_input("Ask me anything:", placeholder="Type here...")

    if user_query:
        with st.status("🚀 Engine starting...", expanded=False) as status:
            try:
                # تعريف الموديل
                llm = ChatGoogleGenerativeAI(
                    model="gemini-1.5-flash", 
                    google_api_key=api_key
                )

                # تعريف العميل
                engineer_agent = Agent(
                    role='Senior Engineer',
                    goal='Provide technical solutions',
                    backstory='Expert assistant',
                    llm=llm,
                    allow_delegation=False,
                    verbose=False
                )

                # المهمة
                tech_task = Task(
                    description=user_query,
                    agent=engineer_agent,
                    expected_output="Direct technical answer"
                )

                # الفريق - الحل هنا بوضع الاختصارات المطلوبة
                crew = Crew(
                    agents=[engineer_agent],
                    tasks=[tech_task],
                    process=Process.sequential,
                    share_crew=False # منع مشاركة البيانات وحل مشاكل الخيوط
                )
                
                # تنفيذ المهمة
                result = crew.kickoff()
                
                status.update(label="✅ Success!", state="complete")
                st.markdown("### 🤖 Response:")
                st.info(result.raw)
                
            except Exception as e:
                st.error(f"Error: {e}")
                status.update(label="❌ Failed", state="error")
else:
    st.error("Please add the API Key to Streamlit Secrets!")

import streamlit as st
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# 1. إعدادات الصفحة
st.set_page_config(page_title="Haneena AI Support", page_icon="🤖", layout="centered")

st.title("🤖 Haneena's Engineering AI")
st.markdown("---")

# 2. إعدادات البيئة (مهمة جداً لتعريف المزود لـ LiteLLM)
os.environ["OTEL_SDK_DISABLED"] = "true"
# هذا السطر يخبر CrewAI أن يستخدم Google Gemini مباشرة
os.environ["GEMINI_API_KEY"] = st.secrets.get("GOOGLE_API_KEY", "")

# 3. التحقق من المفتاح في Secrets
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    
    user_query = st.text_input("How can I help you today, Engineer?", placeholder="Ask your technical question...")

    if user_query:
        with st.status("🚀 Processing with CrewAI...", expanded=False) as status:
            try:
                # 4. تعريف المحرك بصيغة "google_generative_ai" لضمان التوافق
                llm = ChatGoogleGenerativeAI(
                    model="gemini-1.5-flash", 
                    google_api_key=api_key,
                    temperature=0.3
                )

                # 5. تعريف العميل (Agent)
                # أضفنا سطر الموديل بالصيغة التي تحبها مكتبة LiteLLM
                support_agent = Agent(
                    role='Computer Engineering Expert',
                    goal='Provide accurate technical support.',
                    backstory='You are a professional AI mentor specialized in Engineering.',
                    llm=llm,
                    model_name="gemini/gemini-1.5-flash", # هذه الصيغة تحل مشكلة الـ Provider
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
                st.error(f"System Error: {e}")
                status.update(label="❌ Error occurred", state="error")
else:
    st.warning("⚠️ Please add GOOGLE_API_KEY to Streamlit Secrets.")

st.sidebar.markdown("---")
st.sidebar.write("🛠️ Developed by: **Eng. Haneena**")
st.sidebar.markdown("---")
st.sidebar.write("🛠️ Developed by: **Eng. Haneena**")



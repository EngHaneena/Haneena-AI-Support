import streamlit as st
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# 1. إعداد الصفحة
st.set_page_config(page_title="Haneena AI Support", page_icon="🤖")

st.title("🤖 Haneena's Engineering AI")

# 2. حل مشكلة الـ Signal والـ API
os.environ["OTEL_SDK_DISABLED"] = "true"

if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    
    user_query = st.text_input("How can I help you?", placeholder="Ask me anything...")

    if user_query:
        with st.status("🚀 Working...", expanded=False) as status:
            try:
                # 3. تعريف المحرك (تغيير الاسم ليصبح مباشر)
                llm = ChatGoogleGenerativeAI(
                    model="gemini-1.5-flash", # لا تكتبي models/ ولا gemini/ هنا
                    google_api_key=api_key,
                    temperature=0.3
                )

                # 4. تعريف العميل
                agent = Agent(
                    role='Expert Engineer',
                    goal='Technical support',
                    backstory='Helpful assistant.',
                    llm=llm,
                    verbose=False,
                    allow_delegation=False
                )

                # 5. المهمة
                task = Task(description=user_query, agent=agent, expected_output="Technical answer.")

                # 6. التشغيل
                crew = Crew(
                    agents=[agent],
                    tasks=[task],
                    verbose=False,
                    share_crew=False
                )
                
                result = crew.kickoff()
                
                status.update(label="✅ Success!", state="complete")
                st.info(result.raw)
                
            except Exception as e:
                # إذا استمر الـ 404، جربي تغيير الموديل لـ gemini-pro يدوياً هنا
                st.error(f"Error: {e}")
                status.update(label="❌ Failed", state="error")
else:
    st.error("Add GOOGLE_API_KEY to Secrets!")

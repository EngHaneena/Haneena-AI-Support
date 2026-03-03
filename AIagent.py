import streamlit as st
from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# إعداد الصفحة
st.set_page_config(page_title="Haneena AI Support", page_icon="🤖")

st.title("🤖 Haneena's AI Computer Engineering Support")
st.markdown("---")

# جلب المفتاح من Secrets
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("❌ GOOGLE_API_KEY missing in Streamlit Secrets!")
    st.stop()

# تعريف المحرك (Gemini) - تم تعديل المسار لضمان عدم ظهور خطأ 404
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", 
    google_api_key=st.secrets["GOOGLE_API_KEY"],
    temperature=0.5
)

# تعريف العميل (Agent)
engineer_agent = Agent(
    role='Computer Engineering Expert',
    goal='Provide clear and technical advice for computer engineering students.',
    backstory='You are an expert engineer and mentor. You are helpful, precise, and love AI and Robotics.',
    allow_delegation=False,
    verbose=True,
    llm=llm
)

# واجهة المستخدم
user_query = st.text_input("Ask your question, Engineer:", placeholder="e.g. Tell me about Computer Architecture")

if user_query:
    with st.spinner('Engineer AI is processing...'):
        try:
            # تعريف المهمة
            task = Task(
                description=f"Provide a structured and professional answer for: {user_query}",
                agent=engineer_agent,
                expected_output="A helpful technical response in the same language as the query."
            )

            # تشغيل الفريق
            crew = Crew(agents=[engineer_agent], tasks=[task])
            result = crew.kickoff()
            
            # عرض النتيجة
            st.success("Done!")
            st.markdown("### 🤖 Response:")
            st.info(result.raw) # استخدام .raw لضمان ظهور النص بشكل صحيح
            
        except Exception as e:
            st.error(f"Error: {e}")

st.sidebar.write("🛠️ Developed by: **Eng. Haneena**")
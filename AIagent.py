import streamlit as st
from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# إعداد واجهة Streamlit
st.set_page_config(page_title="AI Computer Engineer Support", layout="wide")
st.title("🤖 Haneena's AI Agent Support")
st.subheader("Powered by Gemini 1.5 Flash")

# الحصول على المفتاح من Secrets
google_api_key = st.secrets["GOOGLE_API_KEY"]

# تعريف محرك Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=google_api_key
)

# 1. تعريف العميل (Agent)
support_agent = Agent(
    role='Technical Support Specialist',
    goal='Provide accurate and helpful technical advice to computer engineering students',
    backstory='You are an expert computer engineer with deep knowledge in AI, Robotics, and Software.',
    allow_delegation=False,
    verbose=True,
    llm=llm
)

# واجهة المستخدم لإدخال السؤال
user_input = st.text_input("How can I help you today, Engineer?")

if user_input:
    with st.spinner('Thinking...'):
        # 2. تعريف المهمة (Task)
        task = Task(
            description=f"Answer the following user query professionally: {user_input}",
            agent=support_agent,
            expected_output="A concise and helpful technical response."
        )

        # 3. تشغيل الفريق (Crew)
        crew = Crew(
            agents=[support_agent],
            tasks=[task]
        )
        
        result = crew.kickoff()
        
        # عرض النتيجة
        st.success("Analysis Complete!")
        st.markdown(f"### 🤖 AI Response:\n{result}")

st.sidebar.markdown("---")
st.sidebar.write("🛠️ Created by: **Eng. Haneena**")
st.sidebar.write("📚 Computer Engineering Project")
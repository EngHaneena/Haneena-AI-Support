import streamlit as st
from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# 1. إعداد واجهة التطبيق
st.set_page_config(page_title="Haneena AI Support", page_icon="🤖", layout="wide")

st.title("🤖 Haneena's AI Computer Engineering Support")
st.markdown("---")

# 2. جلب المفتاح من Secrets (تأكدي أن الاسم في Streamlit هو GOOGLE_API_KEY)
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Please add GOOGLE_API_KEY to your Streamlit Secrets!")
    st.stop()

google_api_key = st.secrets["GOOGLE_API_KEY"]

# 3. إعداد نموذج Gemini (المحرك)
# أضفنا إعدادات الأمان (safety_settings) لتجنب أخطاء الحجب
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=google_api_key,
    temperature=0.7
)

# 4. تعريف العميل الذكي (Agent)
support_agent = Agent(
    role='Computer Engineering Specialist',
    goal='Provide expert advice on AI, Robotics, and Computer Engineering topics.',
    backstory="""You are a brilliant computer engineer. You help students understand 
    complex concepts in robotics and AI with simple, clear explanations.""",
    allow_delegation=False,
    verbose=True,
    llm=llm
)

# 5. واجهة المستخدم لإدخال السؤال
user_query = st.text_input("What is your question, Engineer?", placeholder="e.g., How do I start with Robotics?")

if user_query:
    with st.spinner('Engineer AI is thinking... 🧠'):
        try:
            # 6. تعريف المهمة
            task = Task(
                description=f"Answer this question accurately and professionally: {user_query}",
                agent=support_agent,
                expected_output="A helpful and structured technical response in the same language as the question."
            )

            # 7. تشغيل الفريق
            crew = Crew(
                agents=[support_agent],
                tasks=[task]
            )
            
            result = crew.kickoff()
            
            # 8. عرض النتيجة
            st.success("Analysis Complete!")
            st.markdown("### 🤖 Response:")
            st.write(str(result))
            
        except Exception as e:
            st.error(f"An error occurred: {e}")

# إضافة تذييل الصفحة
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1998/1998614.png", width=100)
st.sidebar.title("Project Info")
st.sidebar.info("This is a Multi-Agent system built by Eng. Haneena using CrewAI and Gemini.")
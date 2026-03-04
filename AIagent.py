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
                # 3. تعريف المحرك (إضافة gemini/ لحل مشكلة Provider NOT provided)
                llm = ChatGoogleGenerativeAI(
                    model="gemini/gemini-1.5-flash",
                    google_api_key=google_api_key,
                    version="v1",
                    temperature=0.3
                )

                # 4. تعريف العميل (Agent) - ربط الـ LLM لضمان عدم حدوث Fallback
                support_agent = Agent(
                    role='Computer Engineering Expert',
                    goal='Provide accurate technical support.',
                    backstory='You are a professional AI mentor specialized in Engineering.',
                    llm=llm,
                    function_calling_llm=llm,
                    allow_delegation=False,
                    verbose=False
                )

                # 5. تعريف المهمة (Task)
                task = Task(
                    description=user_query,
                    agent=support_agent,
                    expected_output="A helpful and concise technical response."
                )

                # 6. تشغيل الفريق (Crew)
                crew = Crew(
                    agents=[support_agent],
                    tasks=[task],
                    process=Process.sequential,
                    verbose=False
                )
                
                result = crew.kickoff()
                
                status.update(label="✅ Success!", state="complete")
                
                # 8. عرض النتيجة
                st.markdown("### 🤖 Response:")
                st.info(result.raw)
                
            except Exception as e:
                # التأكد من وجود النقطتين الرأسيتين هنا لإصلاح الـ SyntaxError السابق
                st.error(f"System Error: {e}")
                status.update(label="❌ Error occurred", state="error")
else:
    st.warning("⚠️ Please add GOOGLE_API_KEY to Streamlit Secrets.")

# تذييل الصفحة
st.sidebar.markdown("---")
st.sidebar.write("🛠️ Developed by: **Eng. Haneena**")
st.sidebar.info("Framework: CrewAI + Gemini 1.5")
st.sidebar.markdown("---")
st.sidebar.write("🛠️ Developed by: **Eng. Haneena**")



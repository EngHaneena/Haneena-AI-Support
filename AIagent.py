import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# 1. إعداد الصفحة
st.set_page_config(page_title="Haneena AI Support", page_icon="🤖")
st.title("🤖 Haneena's Engineering AI")
st.markdown("---")

# 2. التحقق من المفتاح في Secrets
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    
    user_query = st.text_input("How can I help you today, Engineer?", placeholder="Ask your technical question...")

    if user_query:
        with st.spinner("🚀 Thinking..."):
            try:
                # 3. استخدام الموديل المستقر gemini-pro لحل مشكلة الـ 404
                llm = ChatGoogleGenerativeAI(
                    model="gemini-pro", # تم التغيير من flash إلى pro للاستقرار
                    google_api_key=api_key,
                    temperature=0.3
                )

                # 4. إرسال السؤال والحصول على الإجابة
                response = llm.invoke([HumanMessage(content=user_query)])
                
                # 5. عرض النتيجة
                st.success("### 🤖 Response:")
                st.write(response.content)
                
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("⚠️ Note: If this persists, please double-check your API key in Streamlit Secrets.")
else:
    st.warning("⚠️ Please add GOOGLE_API_KEY to Streamlit Secrets.")

st.sidebar.markdown("---")
st.sidebar.write("🛠️ Developed by: **Eng. Haneena**")

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
                # 3. الاتصال المباشر والمستقر بـ Gemini
                llm = ChatGoogleGenerativeAI(
                    model="gemini-1.5-flash",
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
                st.info("Tip: If you see 404, try changing the model to 'gemini-pro' in the code.")
else:
    st.warning("⚠️ Please add GOOGLE_API_KEY to Streamlit Secrets.")

st.sidebar.markdown("---")
st.sidebar.write("🛠️ Developed by: **Eng. Haneena**")

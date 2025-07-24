"""Streamlit UI for Vietnamese Tax Law Chatbot."""

import streamlit as st
from llm import generate
import time

# Page configuration
st.set_page_config(
    page_title="Tư vấn Luật Thuế Việt Nam",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        border-bottom: 2px solid #f0f2f6;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .stTextInput > div > div > input {
        border-radius: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🏛️ Chatbot Tư vấn Luật Thuế Việt Nam</h1>
    <p>Hỏi đáp về các quy định thuế hiện hành tại Việt Nam</p>
</div>
""", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add welcome message
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Xin chào! Tôi là chatbot chuyên tư vấn về luật thuế Việt Nam. Bạn có thể hỏi tôi về các quy định thuế, mức thuế suất, thủ tục khai thuế và các vấn đề pháp lý liên quan đến thuế. Hãy đặt câu hỏi của bạn!"
    })

# Create two columns for layout
col1, col2 = st.columns([3, 1])

with col1:
    # Display chat messages
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Nhập câu hỏi về luật thuế của bạn..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Đang tìm kiếm thông tin pháp luật..."):
                try:
                    result = generate(prompt)
                    response_text = result["response"]
                    functions_used = result["functions"]
                    
                    # Display the main response
                    st.markdown(response_text)
                    
                    # Show function calls info if any
                    if functions_used:
                        with st.expander("🔍 Chi tiết tìm kiếm", expanded=False):
                            for func in functions_used:
                                st.write(f"**Chức năng:** {func['function']}")
                                if func['result']:
                                    st.text_area("Kết quả tìm kiếm:", func['result'], height=100)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                    
                except Exception as e:
                    error_msg = f"Xin lỗi, đã có lỗi xảy ra: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

with col2:
    # Sidebar with information and controls
    st.markdown("### 📋 Thông tin hữu ích")
    
    with st.expander("💡 Gợi ý câu hỏi"):
        st.markdown("""
        - Thuế VAT cho dịch vụ tư vấn là bao nhiêu?
        - Mức thuế thu nhập cá nhân hiện tại?
        - Thủ tục khai thuế doanh nghiệp?
        - Các khoản được miễn thuế thu nhập?
        - Thuế xuất nhập khẩu mới nhất?
        """)
    
    with st.expander("⚠️ Lưu ý quan trọng"):
        st.markdown("""
        - Thông tin chỉ mang tính tham khảo
        - Không thay thế tư vấn pháp lý chuyên nghiệp
        - Luôn kiểm tra với cơ quan thuế
        - Quy định có thể thay đổi theo thời gian
        """)
    
    # Clear chat button
    if st.button("🗑️ Xóa lịch sử chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "Lịch sử chat đã được xóa. Bạn có thể bắt đầu cuộc trò chuyện mới!"
        })
        st.rerun()
    
    # Statistics
    if len(st.session_state.messages) > 1:
        user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
        st.metric("Số câu hỏi đã hỏi", user_messages)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.8em;">
    <p>Được phát triển với ❤️ sử dụng Streamlit và Google Gemini AI</p>
    <p><em>Lưu ý: Đây là công cụ hỗ trợ tham khảo, không thay thế tư vấn pháp lý chuyên nghiệp</em></p>
</div>
""", unsafe_allow_html=True)
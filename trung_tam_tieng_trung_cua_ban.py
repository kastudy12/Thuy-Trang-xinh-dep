import streamlit as st
import google.generativeai as genai
import os

# --- CÀI ĐẶT BAN ĐẦU ---

# Thiết lập tiêu đề và icon cho trang web
st.set_page_config(page_title="Gia sư Tiếng Trung AI", page_icon="📖")

# Thiết lập tiêu đề chính của ứng dụng
st.title("📖 Gia sư Tiếng Trung AI")
st.caption("Chatbot được hỗ trợ bởi Google Gemini")

# Lấy API key từ Streamlit Secrets
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
except Exception:
    st.error("Lỗi: Vui lòng thiết lập GOOGLE_API_KEY trong file secrets.toml!")
    st.stop()


# --- ĐỊNH NGHĨA PROMPT CHO CHATBOT ---

SYSTEM_INSTRUCTION = """
BẠN LÀ MỘT GIA SƯ TIẾNG TRUNG.
Tên của bạn là "Minh Lão sư" (明老师).

## VAI TRÒ & TÍNH CÁCH:
- Thân thiện, kiên nhẫn, và luôn khuyến khích người học.
- Sử dụng ngôn ngữ tiếng Việt để giải thích, trừ khi người dùng yêu cầu dùng tiếng Trung.
- Có thể sử dụng các emoji 😊👍📖 để cuộc trò chuyện thêm sinh động.

## BỘ QUY TẮC & CHỨC NĂNG:
1.  **Sửa lỗi chi tiết:** Khi người dùng mắc lỗi (ngữ pháp, từ vựng, pinyin), bạn phải:
    - Chỉ ra lỗi sai.
    - Giải thích TẠI SAO nó sai một cách dễ hiểu.
    - Cung cấp câu đúng.
    - Đưa ra 1-2 ví dụ khác để củng cố kiến thức.

2.  **Định dạng Pinyin và Dịch nghĩa:** Khi cung cấp từ vựng hoặc câu tiếng Trung, luôn tuân theo định dạng:
    Chữ Hán (Pinyin với thanh điệu) - Dịch nghĩa tiếng Việt.
    Ví dụ: 我爱学习 (wǒ ài xuéxí) - Tôi yêu việc học.

3.  **Luyện giao tiếp theo kịch bản:** Nếu người dùng yêu cầu "luyện giao tiếp chủ đề X", hãy bắt đầu một cuộc hội thoại thực tế về chủ đề đó và dẫn dắt họ.

4.  **Giải thích ngữ pháp:** Khi được hỏi về ngữ pháp, hãy giải thích lý thuyết, sau đó cho ít nhất 3 ví dụ từ dễ đến khó.

5.  **Duy trì cuộc trò chuyện:** Luôn kết thúc câu trả lời bằng một câu hỏi mở để khuyến khích người dùng tiếp tục học và tương tác.
"""

# --- KHỞI TẠO CHATBOT ---

# Khởi tạo mô hình Gemini
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    system_instruction=SYSTEM_INSTRUCTION
)

# Sử dụng st.session_state để lưu trữ lịch sử chat
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# --- HIỂN THỊ LỊCH SỬ CHAT ---

# Lặp qua lịch sử chat đã lưu và hiển thị
for message in st.session_state.chat.history:
    # Phân biệt vai trò của người dùng và model
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# --- NHẬN INPUT TỪ NGƯỜI DÙNG ---

if prompt := st.chat_input("Hỏi Minh Lão sư điều gì đó về tiếng Trung..."):
    # Hiển thị tin nhắn của người dùng ngay lập tức
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gửi yêu cầu đến Gemini và nhận phản hồi
    with st.spinner("Minh Lão sư đang soạn câu trả lời..."):
        response = st.session_state.chat.send_message(prompt)

    # Hiển thị phản hồi của chatbot
    with st.chat_message("assistant"):
        st.markdown(response.text)
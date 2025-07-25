import streamlit as st
import google.generativeai as genai
import os

# --- CÀI ĐẶT BAN ĐẦU ---

st.set_page_config(page_title="Gia sư Tiếng Trung AI", page_icon="👨‍🏫")

st.title("👨‍🏫 Gia sư Tiếng Trung AI")
st.caption("Trợ lý ngôn ngữ cá nhân bởi Google Gemini")

# --- KẾT NỐI VỚI GEMINI API ---

# Lấy API key từ Streamlit Secrets
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
except Exception:
    st.error("Lỗi: Vui lòng thiết lập GOOGLE_API_KEY trong phần Secrets của ứng dụng!")
    st.stop()


# --- BỘ NÃO CỦA GIA SƯ AI (SYSTEM PROMPT) ---

# Đây là phần quan trọng nhất, đã được tùy chỉnh cho bạn
SYSTEM_INSTRUCTION = """
BẠN LÀ MỘT GIA SƯ TIẾNG TRUNG CÁ NHÂN, TÊN LÀ "THẦY KHUYẾN".
NHIỆM VỤ CỦA BẠN LÀ DẠY TIẾNG TRUNG CHO MỘT NGƯỜI MỚI BẮT ĐẦU HỌC, VÌ VẬY HÃY GIỮ MỌI THỨ THẬT ĐƠN GIẢN, THÂN THIỆN VÀ KIÊN NHẪN.

## QUY TẮC VÀNG (BẮT BUỘC TUÂN THEO):
1.  **DÀNH CHO NGƯỜI MỚI HỌC:**
    - Luôn nhớ rằng người dùng là người mới. Hãy dùng từ ngữ đơn giản, giải thích chậm và kỹ.
    - Bắt đầu với các chủ đề cơ bản nhất như: Chào hỏi, Giới thiệu bản thân, Số đếm, Hỏi đường, Mua sắm đơn giản.

2.  **PHÂN TÍCH LỊCH SỬ & CHỦ ĐỘNG BẮT ĐẦU:**
    - Nhiệm vụ ĐẦU TIÊN của bạn trong mỗi phiên làm việc là xem lại các tin nhắn cũ trong lịch sử.
    - DỰA VÀO LỊCH SỬ, hãy bắt đầu bằng việc chào hỏi và tóm tắt ngắn gọn những gì người dùng đã học trong lần trước (ví dụ: "Chào bạn, lần trước chúng ta đã học cách đếm số từ 1 đến 10...").
    - NGAY SAU ĐÓ, hãy CHỦ ĐỘNG đề xuất một bài học tiếp theo hợp lý (ví dụ: "Hôm nay chúng ta học cách hỏi giá tiền nhé?").
    - Nếu lịch sử trống (lần đầu tiên sử dụng), hãy chào mừng và đề xuất bài học đầu tiên là "Chào hỏi cơ bản".

3.  **LỘ TRÌNH HỌC BÀI BẢN:**
    - Luôn cố gắng dẫn dắt người dùng theo một lộ trình có cấu trúc:
      a. **Dạy Từ vựng:** Dạy một nhóm nhỏ (3-5 từ) về một chủ đề.
      b. **Thực hành Câu:** Khuyến khích người dùng đặt những câu thật đơn giản với các từ vừa học.
      c. **Thực hành Hội thoại:** Tạo ra một kịch bản hội thoại ngắn và dễ hiểu.

4.  **SỬA LỖI ĐỘNG VIÊN:**
    - Khi người dùng mắc lỗi, hãy sửa một cách nhẹ nhàng.
    - Hãy nói: "Gần đúng rồi! Chỗ này chỉ cần sửa một chút là hoàn hảo. Lẽ ra phải là [...] vì [...]. Bạn thử lại xem sao nhé!".

5.  **TỔNG KẾT BUỔI HỌC:**
    - Khi kết thúc một chủ đề, hãy đưa ra một tóm tắt ngắn gọn.
    - Ví dụ: "Rất tốt! Vậy là hôm nay chúng ta đã học được cách chào hỏi và cảm ơn. Bạn làm tốt lắm!".

6.  **ĐỊNH DẠNG CHUẨN:**
    - Luôn dùng định dạng: `Chữ Hán (pīnyīn với thanh điệu) - Nghĩa Tiếng Việt`.
    - Sử dụng emoji một cách tinh tế để tạo cảm giác thân thiện 😊👍.

## NGÔN NGỮ GIAO TIẾP:
- Luôn luôn sử dụng Tiếng Việt để giải thích.
"""

# --- KHỞI TẠO CHATBOT VÀ LỊCH SỬ ---

# Khởi tạo mô hình Gemini
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    system_instruction=SYSTEM_INSTRUCTION
)

# Thiết lập lịch sử chat trong session_state
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# --- HIỂN THỊ LỊCH SỬ CHAT TRÊN GIAO DIỆN ---

# Lặp qua lịch sử chat đã lưu và hiển thị
for message in st.session_state.chat.history:
    # Bỏ qua các tin nhắn system instruction ban đầu để giao diện sạch sẽ
    if message.role != "model" or "BẠN LÀ MỘT GIA SƯ" not in message.parts[0].text:
        role = "user" if message.role == "user" else "assistant"
        with st.chat_message(role):
            st.markdown(message.parts[0].text)


# --- XỬ LÝ INPUT CỦA NGƯỜI DÙNG ---

if prompt := st.chat_input("Hỏi Thầy Khuyến điều gì đó..."):
    # Hiển thị tin nhắn của người dùng ngay lập tức
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gửi yêu cầu đến Gemini và nhận phản hồi
    with st.spinner("Thầy Khuyến đang suy nghĩ..."):
        response = st.session_state.chat.send_message(prompt)

    # Hiển thị phản hồi của chatbot
    with st.chat_message("assistant"):
        st.markdown(response.text)

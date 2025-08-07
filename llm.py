"""LLM module for generating responses using Gemini 2.5 Flash."""

import google.genai as genai
from google.genai import types
import os
from typing import Optional
from dotenv import load_dotenv
from lookup import search_law

# Load environment variables from .env file
load_dotenv()


class LLMGenerator:
    """Generator class for LLM responses using Gemini 2.5 Flash."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the LLM generator.
        
        Args:
            api_key: Google AI API key. If not provided, will try to get from environment.
        """
        self.api_key = api_key or os.getenv("GOOGLE_AI_API_KEY")
        if not self.api_key:
            raise ValueError("Google AI API key is required. Set GOOGLE_AI_API_KEY environment variable or pass api_key parameter.")
        
        self.client = genai.Client(api_key=self.api_key)
        
        self.system_prompt = """Bạn là một chuyên gia pháp luật thuế tại Việt Nam. Nhiệm vụ của bạn là cung cấp thông tin chính xác, khách quan và cập nhật về luật thuế Việt Nam dựa trên các văn bản pháp luật hiện hành.

Khi người dùng đặt câu hỏi, bạn sẽ:
1. Xác định vấn đề pháp lý thuế mà người dùng muốn tìm hiểu.
2. **Trước khi đưa ra câu trả lời, hãy trình bày ngắn gọn các bước bạn sẽ thực hiện để tìm kiếm và tổng hợp thông tin, ví dụ: "Để trả lời câu hỏi của bạn, tôi sẽ thực hiện các bước sau: [liệt kê các bước].**
3. Tìm kiếm các quy định pháp luật, thông tư, nghị định, luật và dự thảo luật liên quan đến vấn đề đó. Nếu có hãy trích dẫn đường dẫn tới nguồn thông tin. 
4. Trích dẫn chính xác các điều, khoản, điểm của văn bản pháp luật nếu có thể.
5. Giải thích nội dung của quy định đó một cách rõ ràng, dễ hiểu.
6. Luôn ưu tiên các nguồn luật chính thức và mới nhất.
7. Nếu câu hỏi liên quan đến tình huống cụ thể cần tư vấn chuyên sâu, hãy khuyến nghị người dùng tìm kiếm sự tư vấn từ luật sư hoặc chuyên gia thuế có kinh nghiệm.
8. Trả lời bằng tiếng Việt."""

    def generate(self, question: str, system_prompt: Optional[str] = None) -> dict:
        """Generate a response to a tax law question.
        
        Args:
            question: The user's question about Vietnamese tax law.
            system_prompt: Optional custom system prompt to override default.
            
        Returns:
            dict: Contains 'response' (model response) and 'functions' (list of function calls).
        """
        try:
            model = "gemini-2.5-flash"
            
            # Function calls disabled - tools removed
            
            # Create initial content
            contents = [
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text=question),
                    ],
                ),
            ]
            tools = [
                types.Tool(googleSearch=types.GoogleSearch(
                )),
            ]
            
            # Use custom system prompt if provided, otherwise use default
            prompt_to_use = system_prompt if system_prompt is not None else self.system_prompt
            
            # Create generate content config
            generate_content_config = types.GenerateContentConfig(
                response_mime_type="text/plain",
                system_instruction=[
                    types.Part.from_text(text=prompt_to_use),
                ],
                tools=tools,
            )
            
            # Generate initial response
            response = self.client.models.generate_content(
                model=model,
                contents=contents,
                config=generate_content_config,
            )
            # Function calls disabled - return direct response
            return {
                "response": response.text,
                "functions": []
            }
            
        except Exception as e:
            return {
                "response": f"Lỗi khi tạo phản hồi: {str(e)}",
                "functions": []
            }



def generate(question: str, api_key: Optional[str] = None, system_prompt: Optional[str] = None) -> dict:
    """Convenience function to generate a response.
    
    Args:
        question: The user's question about Vietnamese tax law.
        api_key: Optional Google AI API key.
        system_prompt: Optional custom system prompt to override default.
        
    Returns:
        dict: Contains 'response' (model response) and 'functions' (list of function calls).
    """
    generator = LLMGenerator(api_key=api_key)
    return generator.generate(question, system_prompt=system_prompt)
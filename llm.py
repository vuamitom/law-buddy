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
3. Tìm kiếm các quy định pháp luật, thông tư, nghị định, luật liên quan đến vấn đề đó.
4. Trích dẫn chính xác các điều, khoản, điểm của văn bản pháp luật nếu có thể.
5. Giải thích nội dung của quy định đó một cách rõ ràng, dễ hiểu.
6. Luôn ưu tiên các nguồn luật chính thức và mới nhất.
7. Nếu câu hỏi liên quan đến tình huống cụ thể cần tư vấn chuyên sâu, hãy khuyến nghị người dùng tìm kiếm sự tư vấn từ luật sư hoặc chuyên gia thuế có kinh nghiệm.
8. Trả lời bằng tiếng Việt.
9. KHÔNG đưa ra lời khuyên pháp lý cụ thể hoặc tư vấn cá nhân hóa. Chỉ cung cấp thông tin dựa trên luật."""

    def generate(self, question: str) -> str:
        """Generate a response to a tax law question.
        
        Args:
            question: The user's question about Vietnamese tax law.
            
        Returns:
            Generated response from the LLM.
        """
        try:
            model = "gemini-2.5-flash"
            
            # Define tools with function declarations
            tools = [
                types.Tool(
                    function_declarations=[
                        types.FunctionDeclaration(
                            name="lawLookup",
                            description="Tra cứu luật việt nam hiện hành với từ khóa keywords",
                            parameters=genai.types.Schema(
                                type=genai.types.Type.OBJECT,
                                properties={
                                    "keywords": genai.types.Schema(
                                        type=genai.types.Type.STRING,
                                    ),
                                },
                            ),
                        ),
                    ]
                )
            ]
            
            # Create initial content
            contents = [
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text=question),
                    ],
                ),
            ]
            
            # Create generate content config
            generate_content_config = types.GenerateContentConfig(
                tools=tools,
                response_mime_type="text/plain",
                system_instruction=[
                    types.Part.from_text(text=self.system_prompt),
                ],
            )
            
            # Generate initial response
            response = self.client.models.generate_content(
                model=model,
                contents=contents,
                config=generate_content_config,
            )
            # Check if there are function calls
            if response.function_calls:
                function_call = response.function_calls[0]
                
                if function_call.name == "lawLookup":
                    # Extract keywords from function call
                    keywords = function_call.args.get("keywords", "")
                    
                    # Call the search_law function
                    law_results = search_law(keywords)
                    # Create new contents with function response
                    contents_with_function = contents + [
                        types.Content(
                            role="model",
                            parts=[
                                types.Part.from_function_call(
                                    name="lawLookup",
                                    args=function_call.args
                                ),
                            ],
                        ),
                        types.Content(
                            role="function",
                            parts=[
                                types.Part.from_function_response(
                                    name="lawLookup",
                                    response={"output": str(law_results)},
                                ),
                            ],
                        ),
                    ]
                    
                    # Generate final response with function results
                    final_response = self.client.models.generate_content(
                        model=model,
                        contents=contents_with_function,
                        config=generate_content_config,
                    )
                    
                    return final_response.text
            
            return response.text
            
        except Exception as e:
            return f"Lỗi khi tạo phản hồi: {str(e)}"



def generate(question: str, api_key: Optional[str] = None) -> str:
    """Convenience function to generate a response.
    
    Args:
        question: The user's question about Vietnamese tax law.
        api_key: Optional Google AI API key.
        
    Returns:
        Generated response from the LLM.
    """
    generator = LLMGenerator(api_key=api_key)
    return generator.generate(question)
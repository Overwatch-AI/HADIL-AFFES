import io
from PIL import Image
import google.generativeai as genai
from typing import List, Dict, Any, Optional
from src.config import GEMINI_API_KEY

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def generate_answer(question: str, context: str, visual_parts: List[Dict[str, Any]]) -> str:
    """
    Generates an answer using the Gemini model based on text context and visual parts.

    Args:
        question: The user's question.
        context: The concatenated text from relevant chunks.
        visual_parts: A list of chunks that contain images.

    Returns:
        The generated answer as a string.
    """
    try:
        model = genai.GenerativeModel('gemini-2.5-pro')

        if visual_parts:
            parts = [
                f"""Answer this question about the Boeing 737 Operations Manual.

                CRITICAL INSTRUCTIONS FOR READING TABLES:
                - Look at the VISUAL table image carefully.
                - Locate the EXACT row and column specified in the question.
                - Read the value at the intersection VERY carefully.
                - Tables may have multiple sub-columns - make sure you're in the right one.
                - If the table has poor quality text extraction, RELY ON THE IMAGE.

                Question: {question}

                Text context:
                {context}

                IMPORTANT: Visual tables below are the PRIMARY source. Read them carefully:
                """
            ]
            for vp in visual_parts:
                img = Image.open(io.BytesIO(vp["page_image"]))
                parts.append(f"\n[Page {vp['page_number']}]")
                parts.append(img)
                parts.append(f"\nExtracted text (may have OCR errors, use image if unclear):\n{vp['content'][:1000]}")
            response = model.generate_content(parts)
            return response.text
        else:
            prompt = f"""Answer this question about the Boeing 737 Operations Manual.

            CRITICAL FOR TABLES:
            - Find the EXACT row mentioned (e.g., "1600 meters").
            - Find the EXACT column mentioned (e.g., "1000 FT", "WET").
            - Read the value at that specific intersection.
            - Be extremely precise - one cell off gives the wrong answer.

            Question: {question}

            Context:
            {context}

            Read the table precisely and provide the exact value:"""
            response = model.generate_content(prompt)
            return response.text
    except Exception as e:
        return f"Error generating answer: {str(e)}"
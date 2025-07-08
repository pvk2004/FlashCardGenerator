import fitz  # PyMuPDF
from typing import Tuple, Optional, List, Dict
import subprocess
import json
import sys


def extract_text_from_pdf(pdf_file, page_range: Optional[Tuple[int, int]] = None) -> str:
    """
    Extract text from a PDF file using PyMuPDF.
    Args:
        pdf_file: A file-like object containing the PDF.
        page_range: Optional tuple (start_page, end_page), 1-indexed inclusive.
    Returns:
        Extracted text as a string.
    """
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    num_pages = doc.page_count
    if page_range:
        start, end = page_range
        # Clamp values to valid range
        start = max(1, start)
        end = min(num_pages, end)
    else:
        start, end = 1, num_pages
    text = ""
    for page_num in range(start - 1, end):
        page = doc.load_page(page_num)
        text += page.get_text()
    doc.close()
    return text


def generate_flashcards_local(text: str, num_cards: int = 5) -> List[Dict[str, str]]:
    """
    Generate comprehensive flashcards suitable for 10-mark questions using local processing.
    Args:
        text: Extracted text from PDF
        num_cards: Number of flashcards to generate
    Returns:
        List of dictionaries with 'question' and 'answer' keys
    """
    try:
        flashcards = []
        paragraphs = text.split('\n\n')
        
        # Look for comprehensive content patterns
        comprehensive_patterns = [
            'discuss', 'explain', 'describe', 'analyze', 'compare', 'contrast',
            'evaluate', 'examine', 'investigate', 'explore', 'outline', 'summarize',
            'define', 'characterize', 'illustrate', 'demonstrate', 'elaborate'
        ]
        
        # Extract paragraphs that contain substantial content
        substantial_paragraphs = []
        for para in paragraphs:
            para = para.strip()
            if len(para) > 100 and any(pattern in para.lower() for pattern in comprehensive_patterns):
                substantial_paragraphs.append(para)
        
        # Create comprehensive questions from substantial content
        for i, paragraph in enumerate(substantial_paragraphs[:num_cards]):
            # Extract key concepts from the paragraph
            import re
            sentences = re.split(r'[.!?]+', paragraph)
            
            # Find the main topic (usually in the first sentence)
            main_topic = ""
            if sentences:
                first_sentence = sentences[0].strip()
                # Extract capitalized terms as potential main topics
                topics = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', first_sentence)
                if topics:
                    main_topic = topics[0]
            
            # Create comprehensive question
            if main_topic:
                question = f"Discuss in detail about {main_topic}. Explain its significance, characteristics, and applications with relevant examples."
            else:
                # Fallback question
                question = f"Provide a comprehensive explanation of the concepts discussed in the following text: {paragraph[:100]}..."
            
            # Create detailed answer
            answer = f"{paragraph}\n\nKey Points:\n"
            
            # Extract key points from the paragraph
            key_points = []
            for sentence in sentences[1:4]:  # Take next few sentences as key points
                sentence = sentence.strip()
                if len(sentence) > 20:
                    key_points.append(f"• {sentence}")
            
            answer += "\n".join(key_points[:3])  # Limit to 3 key points
            
            flashcards.append({
                "question": question,
                "answer": answer
            })
        
        # If we don't have enough flashcards, create some from general content
        if len(flashcards) < num_cards:
            remaining_cards = num_cards - len(flashcards)
            
            # Create comprehensive questions from remaining content
            for i in range(remaining_cards):
                # Extract a substantial portion of text
                start_idx = i * 500
                end_idx = start_idx + 500
                content_chunk = text[start_idx:end_idx]
                
                if len(content_chunk) > 100:
                    # Create a comprehensive question
                    question = f"Analyze and explain the key concepts and principles discussed in the following content. Provide detailed explanations with examples and applications."
                    
                    # Create a detailed answer
                    answer = f"Content Analysis:\n\n{content_chunk}\n\nComprehensive Explanation:\n"
                    answer += "This content discusses important concepts that require detailed understanding. "
                    answer += "The key aspects include fundamental principles, practical applications, and theoretical foundations. "
                    answer += "Understanding these concepts is crucial for comprehensive knowledge in this field."
                    
                    flashcards.append({
                        "question": question,
                        "answer": answer
                    })
        
        return flashcards[:num_cards]
        
    except Exception as e:
        print(f"Error generating flashcards: {e}")
        # Return comprehensive fallback flashcards
        return [
            {
                "question": "Discuss in detail the main topics and concepts covered in the uploaded document. Provide comprehensive explanations with examples.",
                "answer": "The document covers various important topics that require detailed analysis. Key concepts include fundamental principles, theoretical frameworks, and practical applications. Understanding these topics is essential for comprehensive knowledge in this subject area."
            },
            {
                "question": "Analyze the significance and implications of the content discussed in the document. Explain how these concepts relate to real-world applications.",
                "answer": "The content has significant implications for understanding complex concepts and their practical applications. These concepts form the foundation for advanced studies and real-world problem-solving approaches."
            },
            {
                "question": "Provide a detailed explanation of the key principles and methodologies discussed in the document. Include examples and applications.",
                "answer": "The document outlines important principles and methodologies that are fundamental to this field of study. These principles provide the theoretical framework for understanding complex phenomena and developing practical solutions."
            }
        ]


def generate_flashcards_with_ollama(text: str, model_name: str = "llama2", num_cards: int = 5) -> List[Dict[str, str]]:
    """
    Generate comprehensive flashcards using Ollama (if available) via subprocess.
    Args:
        text: Extracted text from PDF
        model_name: Ollama model to use (default: llama2)
        num_cards: Number of flashcards to generate
    Returns:
        List of dictionaries with 'question' and 'answer' keys
    """
    try:
        prompt = f"""From the following content, generate {num_cards} comprehensive flashcards suitable for 10-mark questions. 
        Create detailed questions that require thorough explanations and detailed answers that cover multiple aspects.
        
        Content:
        {text[:3000]}
        
        Format each flashcard as:
        Q: [Comprehensive question requiring detailed explanation]
        A: [Detailed answer covering multiple points, examples, and applications]
        
        Questions should be like:
        - "Discuss in detail about..."
        - "Analyze and explain..."
        - "Provide a comprehensive explanation of..."
        - "Evaluate and describe..."
        
        Answers should be detailed and cover:
        - Main concepts and definitions
        - Key characteristics and features
        - Examples and applications
        - Significance and implications
        
        Return only the Q&A pairs. Answers should be comprehensive and detailed."""
        
        # Try to use Ollama if available
        result = subprocess.run(
            ['ollama', 'run', model_name, prompt],
            capture_output=True,
            text=True,
            timeout=60  # Increased timeout for comprehensive generation
        )
        
        if result.returncode == 0:
            content = result.stdout
            flashcards = []
            
            lines = content.split('\n')
            current_question = None
            
            for line in lines:
                line = line.strip()
                if line.startswith('Q:'):
                    current_question = line[2:].strip()
                elif line.startswith('A:') and current_question:
                    answer = line[2:].strip()
                    flashcards.append({
                        "question": current_question,
                        "answer": answer
                    })
                    current_question = None
            
            if flashcards:
                return flashcards[:num_cards]
        
        # Fallback to local generation if Ollama fails
        return generate_flashcards_local(text, num_cards)
        
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
        # If Ollama is not available or fails, use local generation
        return generate_flashcards_local(text, num_cards)
    except Exception as e:
        print(f"Error with Ollama: {e}")
        return generate_flashcards_local(text, num_cards)

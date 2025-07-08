---
title: AI Comprehensive Question Generator
emoji: 📚
colorFrom: blue
colorTo: indigo
sdk: docker
sdk_version: "latest"
app_file: app.py
pinned: false
---

# AI Comprehensive Question Generator

🎓 **Generate detailed 10-mark questions and answers from PDF content using AI**

A powerful Streamlit application that extracts text from PDFs and generates comprehensive academic questions suitable for university-level examinations. No API keys required - works completely offline!

## ✨ Features

### 📄 PDF Processing

- **PDF Upload**: Upload any textbook, research paper, or notes
- **Page Range Selection**: Extract text from specific pages
- **Text Extraction**: Clean text extraction using PyMuPDF
- **Real-time Preview**: View extracted text before generating questions

### 🧠 Question Generation

- **10-Mark Questions**: Generate comprehensive questions suitable for university exams
- **Detailed Answers**: Multi-paragraph answers with examples and applications
- **Academic Style**: Questions like "Discuss in detail...", "Analyze and explain..."
- **Multiple Formats**: Both flip-style and list-style display options

### 🔧 Technical Features

- **Offline Processing**: No internet connection required
- **No API Costs**: Completely free to use
- **Local Generation**: Rule-based pattern matching for question creation
- **Ollama Support**: Optional local LLM integration
- **Privacy-Friendly**: All processing happens locally

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project**

   ```bash
   git clone <repository-url>
   cd FlashCardGenerator
   ```
2. **Create a virtual environment (recommended)**

   ```bash
   python -m venv .venv
   ```
3. **Activate the virtual environment**

   - **Windows:**
     ```bash
     .venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source .venv/bin/activate
     ```
4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```
5. **Run the application**

   ```bash
   streamlit run app.py
   ```
6. **Open your browser**

   - Navigate to `http://localhost:8501`
   - The app will open automatically

## 📖 How to Use

### Step 1: Upload PDF

- Click "Browse files" to upload your PDF
- Supported formats: PDF only
- The app will automatically detect the number of pages

### Step 2: Select Page Range

- Choose start and end pages for text extraction
- Default: All pages
- Recommended: Select specific chapters or sections for better results

### Step 3: Extract Text

- Click "Extract Text" to process the selected pages
- Review the extracted text in the preview area
- Make sure the content looks correct before proceeding

### Step 4: Generate Questions

- Choose generation method:
  - **Local (Rule-based)**: Fast, works offline, uses pattern matching
  - **Ollama (if available)**: Better quality, requires Ollama installation
- Select number of questions (3-15)
- Click "Generate Comprehensive Questions"

### Step 5: Review Results

- Questions appear in your chosen display style:
  - **Flip Style**: Click to reveal answers
  - **List Style**: All Q&A visible at once
- Each question is suitable for 10-mark university exams

## 🛠️ Generation Methods

### Local (Rule-based)

- **Pros**: Fast, works offline, no setup required
- **Cons**: Basic pattern matching, limited creativity
- **Best for**: Quick generation, basic content

### Ollama (if available)

- **Pros**: Higher quality questions, more creative
- **Cons**: Requires Ollama installation, slower
- **Best for**: Professional use, complex content

## 📁 Project Structure

```
FlashCardGenerator/
├── app.py              # Main Streamlit application
├── utils.py            # PDF processing & question generation logic
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── .venv/              # Virtual environment (created during setup)
```

## 🔧 Technical Details

### Dependencies

- **streamlit**: Web application framework
- **PyMuPDF**: PDF text extraction
- **python-dotenv**: Environment variable management (optional)

### Key Functions

#### `extract_text_from_pdf()`

- Extracts text from PDF files
- Supports page range selection
- Handles various PDF formats

#### `generate_flashcards_local()`

- Creates comprehensive questions using pattern matching
- Identifies key concepts and definitions
- Generates detailed answers with examples

#### `generate_flashcards_with_ollama()`

- Uses local LLM for question generation
- Provides higher quality results
- Falls back to local generation if Ollama unavailable

## 🎯 Use Cases

### Academic

- **University Exams**: Generate 10-mark questions for study
- **Research Papers**: Create comprehensive analysis questions
- **Textbook Review**: Extract key concepts for revision

### Professional

- **Training Materials**: Create assessment questions
- **Documentation**: Generate comprehension questions
- **Content Analysis**: Extract important topics

### Personal

- **Study Aid**: Create flashcards from notes
- **Knowledge Testing**: Self-assessment questions
- **Content Summarization**: Identify key points

## 🚀 Advanced Usage

### Customizing Question Types

The app generates various question types:

- **Discussion Questions**: "Discuss in detail about..."
- **Analysis Questions**: "Analyze and explain..."
- **Comprehensive Explanations**: "Provide a detailed explanation of..."
- **Evaluation Questions**: "Evaluate and describe..."

### Optimizing Results

- **Select Relevant Pages**: Choose specific chapters for focused questions
- **Review Extracted Text**: Ensure content quality before generation
- **Adjust Question Count**: More questions = more variety
- **Try Both Methods**: Compare local vs Ollama results

## 🔒 Privacy & Security

- **No Data Upload**: All processing happens locally
- **No API Calls**: No external services contacted
- **No Data Storage**: No personal data saved
- **Offline Operation**: Works without internet connection

## 🐛 Troubleshooting

### Common Issues

**PDF Upload Fails**

- Ensure file is a valid PDF
- Check file size (recommended < 50MB)
- Try a different PDF file

**Text Extraction Issues**

- Some PDFs may have image-based text
- Try different page ranges
- Check if PDF is password-protected

**Question Generation Fails**

- Ensure sufficient text was extracted
- Try reducing page range
- Check console for error messages

**App Won't Start**

- Verify Python version (3.8+)
- Check virtual environment activation
- Ensure all dependencies installed

### Getting Help

- Check the console output for error messages
- Verify all dependencies are installed correctly
- Try restarting the application

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report Bugs**: Open an issue with detailed description
2. **Suggest Features**: Propose new functionality
3. **Improve Code**: Submit pull requests
4. **Update Documentation**: Help improve this README

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **Streamlit**: For the amazing web app framework
- **PyMuPDF**: For robust PDF processing
- **Open Source Community**: For inspiration and tools

---

**Made with ❤️ for students and educators**

*Transform your PDFs into comprehensive study materials!*

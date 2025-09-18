# Financial Document Q&A Assistant

## 🎯 Project Overview

An AI-powered web application that processes financial documents (PDF and Excel formats) and provides an interactive question-answering system for querying financial data using natural language. Built with Streamlit and integrated with local Ollama AI models for intelligent document analysis.

## ✨ Features

- **📄 Document Processing**: Upload and process PDF and Excel financial statements (income statements, balance sheets, cash flow statements)
- **🤖 AI-Powered Q&A**: Natural language question answering using local Ollama models (qwen2:0.5b)
- **🔄 Dual System**: AI responses with pattern-matching fallback for reliability
- **🎨 Clean Interface**: Professional Streamlit web interface with intuitive navigation
- **📊 Data Extraction**: Automatic extraction of financial metrics and key data points
- **⚡ Real-time Analysis**: Interactive document analysis with instant feedback
- **🛡️ Error Handling**: Comprehensive validation and error management
- **🔒 Local Deployment**: No cloud dependencies - runs entirely on local machine

## 📋 Requirements

- **Operating System**: Windows 10+ (recommended)
- **Python**: Version 3.8 or higher
- **Storage**: Minimum 4GB free disk space (for AI model)
- **Memory**: 8GB RAM recommended
- **Ollama**: Local AI platform installed and configured

## 🚀 Installation

### 1. Clone the Repository
git clone https://github.com/Its-Skb/Financial_qa_app.git
cd financial-qa-app

text

### 2. Set Up Python Environment
Create virtual environment
python -m venv venv

Activate virtual environment (Windows)
venv\Scripts\activate

For Linux/Mac
source venv/bin/activate

text

### 3. Install Dependencies
pip install -r requirements.txt

text

### 4. Install and Configure Ollama
Download Ollama from https://ollama.com/download
Install the Windows version
Pull the required AI model
ollama pull qwen2:0.5b

text

## 🏃‍♂️ Usage

### 1. Start Ollama Service
ollama serve

text
*Keep this terminal open - Ollama service needs to run continuously*

### 2. Launch the Application
In a new terminal, navigate to project directory
cd financial-qa-app
venv\Scripts\activate
streamlit run app.py

text

### 3. Using the Web Interface

1. **Upload Document**: Navigate to "Document Upload" and select your financial PDF or Excel file
2. **Process Document**: Click "Process Document" to extract financial data
3. **Analyze Data**: View extracted information in "Document Analysis" section
4. **Ask Questions**: Go to "AI Q&A Chat" to interact with your financial data
5. **Debug (Optional)**: Use "Debug Test" section to troubleshoot processing issues

## 💬 Sample Questions

Try asking these questions about your financial documents:

**Revenue & Sales:**
- "What is the total sales revenue?"
- "How much revenue did the company generate?"
- "What were the sales figures for this period?"

**Profitability:**
- "What is the gross profit?"
- "How much profit did the company make?"
- "What is the net income?"

**Expenses:**
- "What are the main expense categories?"
- "How much was spent on advertising?"
- "What are the total operating expenses?"

**Assets & Liabilities:**
- "What are the total assets?"
- "Show me information about company liabilities?"
- "What is the company's net worth?"

## 📁 Project Structure

financial-qa-app/
│
├── app.py # Main Streamlit application
├── requirements.txt # Python dependencies
├── README.md # Project documentation
│
├── utils/ # Core utility modules
│ ├── init.py
│ ├── ai_qa.py # AI integration and prompt engineering
│ ├── document_processor.py # PDF/Excel processing and data extraction
│ ├── file_handler.py # File upload validation and handling
│ └── simple_qa.py # Pattern-matching fallback system
│
└── sample_documents/ # Example financial documents for testing
├── sample_balance_sheet.xlsx
├── sample_income_statement.pdf
└── financial_template.xlsx

text

## ⚙️ Technical Architecture

### Core Components:
- **Frontend**: Streamlit web interface with multi-page navigation
- **AI Engine**: Ollama local deployment with qwen2:0.5b model
- **Document Processing**: pandas (Excel) + pypdf (PDF) extraction
- **Q&A System**: Dual-mode (AI + pattern matching) for reliability
- **Validation**: Response verification against source documents

### Key Features:
- **Prompt Engineering**: Optimized prompts to prevent AI hallucination
- **Response Cleaning**: Post-processing to ensure readable output
- **Session Management**: Streamlit session state for conversation history
- **Error Recovery**: Graceful fallbacks when AI or processing fails

## ⚠️ Known Limitations

- **Storage Requirements**: AI model requires ~4GB disk space
- **PDF Quality**: Text extraction depends on document scan quality and format
- **AI Accuracy**: Responses validated but may occasionally require verification
- **Processing Speed**: Large documents may take 10-30 seconds to process
- **Language Support**: Optimized for English financial documents

## 🐛 Troubleshooting

### Common Issues:

**"Ollama command not recognized"**
- Ensure Ollama is installed and added to system PATH
- Try using full path: `C:\Users\USERNAME\AppData\Local\Programs\Ollama\ollama.exe serve`

**"AI Model Not Available"**
- Verify Ollama service is running: `ollama serve`
- Check model is downloaded: `ollama list`
- Application will fallback to pattern matching if AI unavailable

**"Document processing failed"**
- Verify file format is supported (PDF, Excel)
- Check file size is under 50MB
- Ensure file is not corrupted or password-protected

**"Insufficient disk space"**
- Use smaller model: `ollama pull qwen2:0.5b` (395MB vs 2GB)
- Clear temporary files and restart application

### Performance Optimization:
- **Close unused applications** to free RAM during processing
- **Use SSD storage** for faster model loading
- **Restart Ollama service** if responses become slow

## 🎯 Assignment Compliance

### ✅ Requirements Met:

**Document Processing:**
- ✅ PDF and Excel file upload support
- ✅ Financial data extraction and parsing
- ✅ Support for income statements, balance sheets, cash flow statements
- ✅ Various document layout handling

**Question-Answering System:**
- ✅ Natural language processing for user questions
- ✅ Accurate responses based on document content
- ✅ Conversational interactions with follow-up questions
- ✅ Specific financial metric extraction

**Technical Implementation:**
- ✅ Streamlit web application interface
- ✅ Ollama local Small Language Model deployment
- ✅ Local hosting without cloud dependencies
- ✅ Comprehensive error handling and user feedback

**User Interface:**
- ✅ Clean, intuitive document upload interface
- ✅ Interactive chat interface for questions
- ✅ Readable financial information display
- ✅ Clear processing status and result feedback

### 🏆 Success Criteria Achieved:
- ✅ **Upload financial documents** - Working with validation
- ✅ **Extract meaningful data** - Comprehensive PDF/Excel processing  
- ✅ **Answer basic questions** - AI + pattern-matching dual system

## 🤝 Contributing

Contributions are welcome! Please feel free to:
- Report bugs or issues
- Suggest new features or improvements
- Submit pull requests
- Share sample financial documents for testing

## 📄 License

This project is developed as part of the Financial Document Q&A Assignment. Feel free to use and modify for educational purposes.

## 👨‍💻 Developer Notes

**Development Environment:**
- Built and tested on Windows 11
- Python 3.10.x with virtual environment
- Streamlit 1.28+, Ollama 0.11+

**Future Enhancements:**
- Support for additional document formats
- Multi-language document processing
- Advanced financial ratio calculations
- Export functionality for analysis results
- Integration with external financial APIs

---

**🎉 Project completed as part of the Financial Document Q&A Assignment**

*For technical support or questions, please open an issue in the GitHub repository.*

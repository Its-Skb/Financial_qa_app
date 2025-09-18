import streamlit as st
import os
from utils.file_handler import FileHandler
from utils.document_processor import DocumentProcessor
from utils.ai_qa import AIQuestionAnswering
from utils.simple_qa import SimpleQA

# Page configuration
st.set_page_config(
    page_title="Financial Document Q&A Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("📊 Financial Document Q&A Assistant")
    st.markdown("### AI-Powered Financial Document Analysis")
    st.markdown("---")
    
    # Initialize session state
    if 'processed_data' not in st.session_state:
        st.session_state.processed_data = None
    if 'document_processor' not in st.session_state:
        st.session_state.document_processor = DocumentProcessor()
    if 'ai_qa' not in st.session_state:
        st.session_state.ai_qa = AIQuestionAnswering()
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Sidebar
    with st.sidebar:
        st.header("🚀 Navigation")
        page = st.selectbox("Choose a section:", 
                           ["Document Upload", "Document Analysis", "AI Q&A Chat", "Settings"])
        
        # AI Status indicator
        st.markdown("---")
        st.subheader("🤖 AI Status")
        if st.session_state.ai_qa.is_model_available():
            st.success("✅ AI Model Ready")
            st.write("Model: qwen2:0.5b")
        else:
            st.warning("⚠️ AI Model Not Available")
            st.write("Using pattern-matching backup")
    
    if page == "Document Upload":
        handle_document_upload()
    elif page == "Document Analysis":
        handle_document_analysis()
    elif page == "AI Q&A Chat":
        handle_ai_qa_chat()
    elif page == "🧪 Debug Test":
        test_document_processing()
    elif page == "Settings":
        handle_settings()

def handle_document_upload():
    st.header("📄 Document Upload")
    st.info("Upload your financial documents (PDF or Excel) to get started")
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['pdf', 'xlsx', 'xls', 'xlsm'],
        help="Supported formats: PDF, Excel (xlsx, xls, xlsm)"
    )
    
    if uploaded_file is not None:
        # Validate file
        validation_result = FileHandler.validate_file(uploaded_file)
        
        if not validation_result["valid"]:
            st.error(f"❌ {validation_result['error']}")
            return
        
        # Display file info
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("File Size", f"{validation_result['size'] / 1024:.1f} KB")
        with col2:
            st.metric("File Type", validation_result['file_type'].title())
        with col3:
            st.metric("Extension", f".{validation_result['extension']}")
        
        # Process document
        if st.button("🚀 Process Document", type="primary"):
            with st.spinner("Processing document..."):
                # Save temporary file
                temp_path = FileHandler.save_temp_file(uploaded_file)
                
                # Process document
                processor = DocumentProcessor()
                result = processor.process_document(temp_path, validation_result['file_type'])
                
                if result["success"]:
                    st.success("✅ Document processed successfully!")
                    st.session_state.processed_data = result
                    st.session_state.document_processor = processor
                    
                    # Display processing results
                    if validation_result['file_type'] == 'excel':
                        st.write(f"📊 Found {result['total_sheets']} sheets")
                        st.write(f"💰 Found {result['financial_tables_found']} financial tables")
                    elif validation_result['file_type'] == 'pdf':
                        st.write(f"📄 Processed {result['pages']} pages")
                        st.write(f"📝 Extracted {result['text_length']} characters")
                    
                    st.info("👉 Go to 'Document Analysis' to view data or 'AI Q&A Chat' to ask questions")
                else:
                    st.error(f"❌ Processing failed: {result['error']}")
                
                # Cleanup temp file
                try:
                    os.unlink(temp_path)
                except:
                    pass

def handle_document_analysis():
    st.header("📊 Document Analysis")
    
    if st.session_state.processed_data is None:
        st.warning("📄 Please upload and process a document first!")
        return
    
    data = st.session_state.processed_data
    processor = st.session_state.document_processor
    
    st.success("✅ Document data loaded successfully")
    
    # Display analysis based on file type
    if 'sheets' in data:  # Excel file
        st.subheader("📋 Excel Sheets Analysis")
        
        for sheet_name in data['sheets']:
            with st.expander(f"📄 Sheet: {sheet_name}"):
                sheet_data = data['data'][sheet_name]
                st.dataframe(sheet_data.head(10))
                st.write(f"**Dimensions:** {len(sheet_data)} rows × {len(sheet_data.columns)} columns")
        
        # Financial tables
        if processor.financial_tables:
            st.subheader("💰 Financial Tables Found")
            for table in processor.financial_tables:
                st.write(f"**{table['type']}** (Sheet: {table['sheet_name']})")
                st.dataframe(table['data'].head())
    
    elif 'full_text' in data:  # PDF file
        st.subheader("📄 PDF Content Analysis")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Pages", data['pages'])
        with col2:
            st.metric("Text Length", f"{data['text_length']:,} chars")
        
        # Financial metrics
        if processor.financial_metrics:
            st.subheader("💰 Extracted Financial Metrics")
            for metric, value in processor.financial_metrics.items():
                st.metric(metric.replace('_', ' ').title(), f"${value}")
        
        st.subheader("📖 Document Preview")
        st.text_area("Text Content (First 500 characters)", data['text_preview'], height=300, disabled=True)

def handle_ai_qa_chat():
    st.header("🤖 AI-Powered Q&A Chat")
    
    if st.session_state.processed_data is None:
        st.warning("📄 Please upload and process a document first!")
        return
    
    processor = st.session_state.document_processor
    ai_qa = st.session_state.ai_qa
    
    # Check AI availability
    ai_available = ai_qa.is_model_available()
    
    if ai_available:
        st.success("🤖 AI Model Ready - Advanced natural language processing available!")
    else:
        st.warning("⚠️ AI Model not available - Using pattern-matching backup system")
    
    st.info("💡 Ask questions about revenue, profit, expenses, assets, or any financial metrics from your document")
    
    # Question input
    user_question = st.text_input(
        "Ask a question about your financial document:", 
        placeholder="e.g., What is the total revenue? How much profit did the company make? What are the main expenses?"
    )
    
    if st.button("💬 Ask Question", type="primary") and user_question:
        with st.spinner("🧠 Analyzing your question..."):
            
            # 🔍 DEBUG: Get and display document context
            document_context = processor.get_context_for_ai()
            
            # Add debug expander - THIS IS THE NEW DEBUGGING CODE
            with st.expander("🔍 DEBUG: Document Context Sent to AI"):
                st.write("**Context Length:**", len(document_context), "characters")
                st.text_area("Context Preview (first 2000 chars):", document_context[:2000], height=300)
                
                # Show extracted financial metrics
                if hasattr(processor, 'financial_metrics'):
                    st.write("**Extracted Financial Metrics:**")
                    st.json(processor.financial_metrics)
                
                # Show raw document text length
                st.write("**Raw Document Text Length:**", len(processor.document_text), "characters")
            
            if ai_available:
                # Use AI for advanced Q&A
                answer = ai_qa.answer_question(user_question, document_context)
            else:
                # Use pattern matching backup
                from utils.simple_qa import SimpleQA
                simple_qa = SimpleQA(processor.document_text)
                answer = simple_qa.answer_question(user_question)
            
            # Add to chat history
            st.session_state.chat_history.append({
                'question': user_question,
                'answer': answer,
                'ai_powered': ai_available
            })
    
    # Display chat history
    if st.session_state.chat_history:
        st.subheader("💬 Chat History")
        
        for i, chat in enumerate(reversed(st.session_state.chat_history)):
            with st.expander(f"Q{len(st.session_state.chat_history)-i}: {chat['question'][:50]}..."):
                st.write(f"**❓ Question:** {chat['question']}")
                ai_badge = "🤖 AI" if chat.get('ai_powered', False) else "🔍 Pattern"
                st.write(f"**{ai_badge} Answer:** {chat['answer']}")
        
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            ai_qa.clear_history()
            st.rerun()
    
    # Sample questions
    st.subheader("💡 Sample Questions")
    sample_questions = [
        "What is the total revenue for this period?",
        "How much profit did the company make?",
        "What are the main expenses listed?",
        "Show me information about company assets",
        "What is the cash flow situation?",
        "Compare revenue to expenses"
    ]
    
    cols = st.columns(2)
    for i, question in enumerate(sample_questions):
        if cols[i%2].button(f"📝 {question}", key=f"sample_{i}"):
            st.session_state.sample_question = question
            st.rerun()

def handle_settings():
    st.header("⚙️ Application Settings")
    
    st.subheader("🤖 AI Configuration")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.ai_qa.is_model_available():
            st.success("✅ AI Model: qwen2:0.5b")
            st.write("Status: Running")
        else:
            st.error("❌ AI Model: Not Available")
            st.write("Status: Using backup system")
    
    with col2:
        st.metric("Questions Asked", len(st.session_state.chat_history))
        st.metric("Documents Processed", 1 if st.session_state.processed_data else 0)
    
    st.subheader("📊 Processing Settings")
    max_file_size = st.slider("Max File Size (MB):", 1, 100, 50)
    
    st.subheader("📈 System Information")
    st.write("- **Frontend**: Streamlit")
    st.write("- **AI Engine**: Ollama (Local deployment)")
    st.write("- **Document Processing**: pandas, pypdf")
    st.write("- **Storage**: Local file system")

def test_document_processing():
    """Debug function to verify document processing is working correctly"""
    st.subheader("🧪 Document Processing Test")
    
    if st.session_state.processed_data is None:
        st.warning("📄 Please upload and process a document first!")
        return
    
    processor = st.session_state.document_processor
    
    # Show extracted text preview
    st.write("**📝 Extracted Text Preview:**")
    if hasattr(processor, 'document_text') and processor.document_text:
        st.text_area("Raw Text (first 1000 chars):", processor.document_text[:1000], height=200)
        st.write(f"**Total text length:** {len(processor.document_text)} characters")
    else:
        st.error("❌ No document text found!")
    
    # Show financial metrics
    st.write("**💰 Extracted Financial Metrics:**")
    if hasattr(processor, 'financial_metrics') and processor.financial_metrics:
        st.json(processor.financial_metrics)
    else:
        st.warning("⚠️ No financial metrics extracted")
    
    # Show financial tables (for Excel files)
    if hasattr(processor, 'financial_tables') and processor.financial_tables:
        st.write("**📊 Financial Tables Found:**")
        for i, table in enumerate(processor.financial_tables):
            st.write(f"Table {i+1}: {table['type']} (Sheet: {table['sheet_name']})")
            st.dataframe(table['data'].head(3))
    
    # Show AI context
    st.write("**🤖 AI Context Preview:**")
    context = processor.get_context_for_ai()
    st.write(f"**Context length:** {len(context)} characters")
    st.text_area("Context Preview (first 1500 chars):", context[:1500], height=300)
    
    # Look for Joe's specific data
    st.write("**🔍 Joe's Motorbike Tyres Data Check:**")
    if "joe" in context.lower():
        st.success("✅ Found 'Joe' in context")
    else:
        st.error("❌ 'Joe' not found in context")
    
    if "52000" in context or "52,000" in context:
        st.success("✅ Found sales figure (52000) in context")
    else:
        st.error("❌ Sales figure (52000) not found in context")
    
    if "sales" in context.lower():
        st.success("✅ Found 'sales' keyword in context")
    else:
        st.error("❌ 'sales' keyword not found in context")

if __name__ == "__main__":
    main()

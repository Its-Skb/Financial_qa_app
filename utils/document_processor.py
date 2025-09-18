import pandas as pd
import streamlit as st
from typing import Dict, List, Any, Optional
import tempfile
import os
import re

# PDF processing imports
try:
    import pypdf as PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    try:
        import PyPDF2
        PDF_AVAILABLE = True
    except ImportError:
        PDF_AVAILABLE = False

class DocumentProcessor:
    """Process financial documents and extract relevant information"""
    
    def __init__(self):
        self.extracted_data = {}
        self.document_text = ""
        self.financial_tables = []
        self.financial_metrics = {}
    
    def process_document(self, file_path: str, file_type: str) -> Dict[str, Any]:
        """Main method to process different document types"""
        try:
            if file_type == "excel":
                return self._process_excel(file_path)
            elif file_type == "pdf":
                return self._process_pdf(file_path)
            else:
                return {"success": False, "error": f"Unsupported file type: {file_type}"}
        except Exception as e:
            return {"success": False, "error": f"Processing failed: {str(e)}"}
    
    def _process_excel(self, file_path: str) -> Dict[str, Any]:
        """Process Excel files and extract financial data"""
        try:
            excel_file = pd.ExcelFile(file_path)
            sheets_data = {}
            
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                sheets_data[sheet_name] = df
                
                # Look for financial keywords
                if self._contains_financial_keywords(df):
                    self.financial_tables.append({
                        'sheet_name': sheet_name,
                        'data': df,
                        'type': self._identify_statement_type(df)
                    })
                
                # Convert dataframe to text for AI processing
                self.document_text += f"\n\n--- Sheet: {sheet_name} ---\n"
                self.document_text += df.to_string()
            
            # Extract financial metrics from Excel data
            self.financial_metrics = self._extract_excel_metrics(sheets_data)
            
            return {
                "success": True,
                "sheets": list(sheets_data.keys()),
                "total_sheets": len(sheets_data),
                "financial_tables_found": len(self.financial_tables),
                "data": sheets_data,
                "text_for_ai": self.document_text
            }
            
        except Exception as e:
            return {"success": False, "error": f"Excel processing failed: {str(e)}"}
    
    def _process_pdf(self, file_path: str) -> Dict[str, Any]:
        """Process PDF files and extract text"""
        if not PDF_AVAILABLE:
            return {"success": False, "error": "PDF processing library not available. Install pypdf."}
        
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text_content = []
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    text_content.append(text)
                
                self.document_text = "\n".join(text_content)
                
                # Extract financial metrics from text
                self.financial_metrics = self._extract_text_metrics(self.document_text)
                
                return {
                    "success": True,
                    "pages": len(pdf_reader.pages),
                    "text_length": len(self.document_text),
                    "text_preview": self.document_text[:500] + "..." if len(self.document_text) > 500 else self.document_text,
                    "full_text": self.document_text,
                    "text_for_ai": self.document_text
                }
                
        except Exception as e:
            return {"success": False, "error": f"PDF processing failed: {str(e)}"}
    
    def _contains_financial_keywords(self, df: pd.DataFrame) -> bool:
        """Check if dataframe contains financial keywords"""
        financial_keywords = [
            'revenue', 'income', 'profit', 'loss', 'expense', 'cost',
            'sales', 'earnings', 'ebitda', 'assets', 'liabilities',
            'equity', 'cash', 'debt', 'balance', 'statement'
        ]
        
        df_text = df.to_string().lower()
        return any(keyword in df_text for keyword in financial_keywords)
    
    def _identify_statement_type(self, df: pd.DataFrame) -> str:
        """Identify the type of financial statement"""
        df_text = df.to_string().lower()
        
        if any(word in df_text for word in ['balance sheet', 'assets', 'liabilities']):
            return 'Balance Sheet'
        elif any(word in df_text for word in ['income statement', 'revenue', 'profit', 'loss']):
            return 'Income Statement'
        elif any(word in df_text for word in ['cash flow', 'operating', 'investing', 'financing']):
            return 'Cash Flow Statement'
        else:
            return 'Financial Statement'
    
    def _extract_excel_metrics(self, sheets_data: Dict) -> Dict[str, Any]:
        """Extract financial metrics from Excel data"""
        metrics = {}
        
        for sheet_name, df in sheets_data.items():
            df_text = df.to_string().lower()
            
            # Look for revenue patterns
            if 'revenue' in df_text or 'sales' in df_text:
                metrics['revenue_sheet'] = sheet_name
            
            # Look for profit patterns
            if 'profit' in df_text or 'net income' in df_text:
                metrics['profit_sheet'] = sheet_name
                
        return metrics
    
    def _extract_text_metrics(self, text: str) -> Dict[str, Any]:
        """Extract specific financial metrics from text"""
        metrics = {}
        text_lower = text.lower()
        
        # Revenue patterns
        revenue_patterns = [
            r'revenue[:\s]+\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            r'total revenue[:\s]+\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            r'sales[:\s]+\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
        ]
        
        for pattern in revenue_patterns:
            match = re.search(pattern, text_lower)
            if match:
                metrics['revenue'] = match.group(1)
                break
        
        # Profit patterns
        profit_patterns = [
            r'net income[:\s]+\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            r'profit[:\s]+\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
        ]
        
        for pattern in profit_patterns:
            match = re.search(pattern, text_lower)
            if match:
                metrics['profit'] = match.group(1)
                break
        
        return metrics
    
    def get_context_for_ai(self) -> str:
        """Get formatted text for AI processing"""
        context = "Financial Document Content:\n\n"
        context += self.document_text
        
        if self.financial_metrics:
            context += "\n\nExtracted Financial Metrics:\n"
            for metric, value in self.financial_metrics.items():
                context += f"- {metric}: {value}\n"
        
        return context

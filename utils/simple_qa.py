import re
from typing import Dict, List, Any

class SimpleQA:
    """Backup Q&A system using pattern matching"""
    
    def __init__(self, document_text: str = ""):
        self.document_text = document_text.lower()
    
    def answer_question(self, question: str) -> str:
        """Answer questions using pattern matching"""
        question = question.lower()
        
        if any(word in question for word in ['revenue', 'sales', 'income']):
            return self._find_revenue_info()
        elif any(word in question for word in ['profit', 'net income']):
            return self._find_profit_info()
        elif any(word in question for word in ['expense', 'cost']):
            return self._find_expense_info()
        elif any(word in question for word in ['assets']):
            return self._find_assets_info()
        else:
            return self._general_search(question)
    
    def _find_revenue_info(self) -> str:
        """Find revenue information"""
        patterns = [r'revenue[:\s]+\$?([\d,]+)', r'sales[:\s]+\$?([\d,]+)']
        
        for pattern in patterns:
            match = re.search(pattern, self.document_text)
            if match:
                return f"💰 Found revenue: ${match.group(1)}"
        
        if 'revenue' in self.document_text:
            return "📊 Revenue information found in the document. Please check the income statement."
        return "❓ No specific revenue information found."
    
    def _find_profit_info(self) -> str:
        """Find profit information"""
        patterns = [r'profit[:\s]+\$?([\d,]+)', r'net income[:\s]+\$?([\d,]+)']
        
        for pattern in patterns:
            match = re.search(pattern, self.document_text)
            if match:
                return f"💵 Found profit: ${match.group(1)}"
        
        return "❓ No specific profit information found."
    
    def _find_expense_info(self) -> str:
        """Find expense information"""
        if 'expense' in self.document_text:
            return "💸 Expense information found in the document."
        return "❓ No expense information found."
    
    def _find_assets_info(self) -> str:
        """Find assets information"""
        if 'assets' in self.document_text:
            return "🏢 Assets information found in the document."
        return "❓ No assets information found."
    
    def _general_search(self, question: str) -> str:
        """General search"""
        words = [w for w in question.split() if len(w) > 3]
        found = [w for w in words if w in self.document_text]
        
        if found:
            return f"🔍 Found references to: {', '.join(found)}"
        return "❓ No specific information found for your question."

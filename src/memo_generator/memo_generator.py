from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, List, Optional
import json

from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from .config import Config

@dataclass
class FinancialData:
    """Structure for financial data input."""
    revenue: float
    costs: float
    ebitda: float
    growth_rate: float
    market_size: float
    competitors: List[str]
    key_metrics: Dict[str, Any]

class MemoGenerator:
    """Main class for generating investment memorandums."""
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize the memo generator with configuration."""
        self.config = Config(config_path)
        self.llm = self._setup_llm()
        self.vector_store = self._setup_vector_store()
        
    def _setup_llm(self) -> ChatOpenAI:
        """Initialize the language model."""
        llm_config = self.config.llm_config
        return ChatOpenAI(
            model_name=llm_config.get("model", "gpt-4"),
            temperature=llm_config.get("temperature", 0.7)
        )
    
    def _setup_vector_store(self) -> Chroma:
        """Initialize the vector store for document retrieval."""
        embeddings = OpenAIEmbeddings()
        return Chroma(
            persist_directory="data/vectordb",
            embedding_function=embeddings
        )
    
    def load_financial_data(self, data_path: Path) -> FinancialData:
        """Load financial data from JSON file."""
        with open(data_path) as f:
            data = json.load(f)
        return FinancialData(**data)
    
    def generate_memo(self, financial_data: FinancialData) -> str:
        """Generate investment memorandum from financial data."""
        # Get memo template
        template = self._load_template()
        
        # Generate sections
        sections = {
            "executive_summary": self._generate_executive_summary(financial_data),
            "financial_analysis": self._generate_financial_analysis(financial_data),
            "market_analysis": self._generate_market_analysis(financial_data),
            "recommendation": self._generate_recommendation(financial_data)
        }
        
        # Combine sections using template
        return template.format(**sections)
    
    def _load_template(self) -> str:
        """Load memo template from file."""
        template_path = Path(self.config.template_config.get("path", "templates/memo.txt"))
        with open(template_path) as f:
            return f.read()
    
    def _generate_executive_summary(self, data: FinancialData) -> str:
        """Generate executive summary section."""
        prompt = f"""
        Generate an executive summary for an investment memo with the following metrics:
        - Revenue: ${data.revenue:,.2f}
        - EBITDA: ${data.ebitda:,.2f}
        - Growth Rate: {data.growth_rate:.1f}%
        - Market Size: ${data.market_size:,.2f}
        
        Format as a professional, concise paragraph.
        """
        response = self.llm.predict(prompt)
        return response
    
    def _generate_financial_analysis(self, data: FinancialData) -> str:
        """Generate financial analysis section."""
        metrics = "\n".join([f"- {k}: {v}" for k, v in data.key_metrics.items()])
        prompt = f"""
        Create a detailed financial analysis section with these metrics:
        {metrics}
        
        Include:
        1. Key performance indicators
        2. Growth trends
        3. Margin analysis
        4. Comparison to industry standards
        """
        response = self.llm.predict(prompt)
        return response
    
    def _generate_market_analysis(self, data: FinancialData) -> str:
        """Generate market analysis section."""
        competitors = ", ".join(data.competitors)
        prompt = f"""
        Generate a market analysis with:
        - Market Size: ${data.market_size:,.2f}
        - Key Competitors: {competitors}
        
        Include:
        1. Market dynamics
        2. Competitive positioning
        3. Growth opportunities
        4. Potential risks
        """
        response = self.llm.predict(prompt)
        return response
    
    def _generate_recommendation(self, data: FinancialData) -> str:
        """Generate investment recommendation."""
        prompt = f"""
        Based on:
        - Revenue: ${data.revenue:,.2f}
        - EBITDA: ${data.ebitda:,.2f}
        - Growth: {data.growth_rate:.1f}%
        
        Provide an investment recommendation including:
        1. Clear recommendation (invest/pass)
        2. Key supporting factors
        3. Risk factors to monitor
        4. Suggested next steps
        """
        response = self.llm.predict(prompt)
        return response
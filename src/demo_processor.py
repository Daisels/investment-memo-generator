from pathlib import Path
import pandas as pd
import pdfplumber
from typing import Dict, Any, Union
from dataclasses import dataclass
from datetime import datetime
from langdetect import detect

@dataclass
class ProcessedData:
    """Container for processed document data."""
    filename: str
    language: str
    date_processed: datetime
    content: Union[str, Dict[str, Any]]
    financial_metrics: Dict[str, Any]
    is_financial: bool

class SimpleDocumentProcessor:
    """Simple but complete document processor for testing."""
    
    # Financial terms we're looking for
    FINANCIAL_TERMS = {
        'dutch': ['omzet', 'ebitda', 'winst', 'kosten', 'marge'],
        'english': ['revenue', 'ebitda', 'profit', 'costs', 'margin']
    }
    
    def __init__(self, input_dir: str = "input", output_dir: str = "output"):
        """Initialize processor with input/output directories."""
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Create necessary directories if they don't exist."""
        self.input_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
    
    def process_file(self, filename: str) -> ProcessedData:
        """Process a single file and return structured data."""
        file_path = self.input_dir / filename
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Handle different file types
        if file_path.suffix.lower() == '.pdf':
            return self._process_pdf(file_path)
        elif file_path.suffix.lower() in ['.xlsx', '.xls']:
            return self._process_excel(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_path.suffix}")
    
    def _process_pdf(self, file_path: Path) -> ProcessedData:
        """Process PDF file."""
        text_content = []
        financial_metrics = {}
        
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_content.append(text)
            
            full_text = "\n".join(text_content)
            language = detect(full_text)
            
            # Look for financial metrics in the text
            financial_metrics = self._extract_financial_metrics(full_text, language)
            
            return ProcessedData(
                filename=file_path.name,
                language='dutch' if language == 'nl' else 'english',
                date_processed=datetime.now(),
                content=full_text,
                financial_metrics=financial_metrics,
                is_financial=bool(financial_metrics)
            )
            
        except Exception as e:
            print(f"Error processing PDF {file_path}: {str(e)}")
            raise
    
    def _process_excel(self, file_path: Path) -> ProcessedData:
        """Process Excel file."""
        try:
            df = pd.read_excel(file_path)
            columns_text = " ".join(df.columns.astype(str))
            language = detect(columns_text)
            
            # Check if this is financial data
            financial_metrics = {}
            if self._is_financial_data(df, language):
                financial_metrics = self._extract_financial_metrics_from_df(df)
            
            return ProcessedData(
                filename=file_path.name,
                language='dutch' if language == 'nl' else 'english',
                date_processed=datetime.now(),
                content=df.to_dict(),
                financial_metrics=financial_metrics,
                is_financial=bool(financial_metrics)
            )
            
        except Exception as e:
            print(f"Error processing Excel {file_path}: {str(e)}")
            raise
    
    def _is_financial_data(self, df: pd.DataFrame, language: str) -> bool:
        """Check if DataFrame contains financial data."""
        terms = self.FINANCIAL_TERMS['dutch' if language == 'nl' else 'english']
        columns = df.columns.astype(str).str.lower()
        return any(term in " ".join(columns) for term in terms)
    
    def _extract_financial_metrics(self, text: str, language: str) -> Dict[str, Any]:
        """Extract financial metrics from text."""
        metrics = {}
        terms = self.FINANCIAL_TERMS['dutch' if language == 'nl' else 'english']
        
        # Simple pattern matching - could be enhanced with regex
        lines = text.lower().split('\n')
        for line in lines:
            for term in terms:
                if term in line:
                    # Try to find a number in the line
                    numbers = [word for word in line.split() 
                             if any(c.isdigit() for c in word)]
                    if numbers:
                        metrics[term] = numbers[0]
        
        return metrics
    
    def _extract_financial_metrics_from_df(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Extract financial metrics from DataFrame."""
        metrics = {}
        
        # Look for columns containing financial terms
        for term in self.FINANCIAL_TERMS['english']:  # We'll standardize to English
            matching_cols = [col for col in df.columns 
                           if term.lower() in str(col).lower()]
            
            if matching_cols:
                # Get the last (most recent) non-null value
                col = matching_cols[0]
                values = df[col].dropna()
                if not values.empty:
                    metrics[term] = values.iloc[-1]
        
        return metrics

def main():
    """Example usage."""
    # Initialize processor
    processor = SimpleDocumentProcessor()
    
    # Process a file
    try:
        result = processor.process_file("example.pdf")  # or example.xlsx
        
        # Print results
        print(f"\nProcessed: {result.filename}")
        print(f"Language: {result.language}")
        print(f"Processed at: {result.date_processed}")
        print("\nFinancial Metrics Found:")
        for metric, value in result.financial_metrics.items():
            print(f"{metric}: {value}")
            
        # Save structured data
        output_file = Path("output") / f"processed_{result.filename}.json"
        with open(output_file, "w") as f:
            json.dump({
                "filename": result.filename,
                "language": result.language,
                "date_processed": result.date_processed.isoformat(),
                "financial_metrics": result.financial_metrics,
                "is_financial": result.is_financial
            }, f, indent=2)
            
    except Exception as e:
        print(f"Error processing file: {str(e)}")

if __name__ == "__main__":
    main()
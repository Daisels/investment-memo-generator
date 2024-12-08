from typing import List, Dict, Any, Optional
from pathlib import Path
import pandas as pd
from langdetect import detect

class MultilingualDocumentProcessor:
    """Handles processing of multiple document types in Dutch and English."""
    
    SUPPORTED_EXTENSIONS = {
        '.pdf': 'PDFPlumberLoader',
        '.xlsx': 'UnstructuredExcelLoader',
        '.xls': 'UnstructuredExcelLoader',
        '.docx': 'Docx2txtLoader',
        '.doc': 'Docx2txtLoader',
        '.csv': 'CSVLoader'
    }

    # Common financial terms in both languages
    FINANCIAL_TERMS = {
        'dutch': {
            'revenue': ['omzet', 'inkomsten', 'opbrengsten'],
            'profit': ['winst', 'resultaat', 'netto resultaat'],
            'ebitda': ['ebitda', 'bedrijfsresultaat'],
            'margin': ['marge', 'winstmarge'],
            'costs': ['kosten', 'uitgaven'],
            'balance': ['balans', 'balanstotaal']
        },
        'english': {
            'revenue': ['revenue', 'sales', 'turnover'],
            'profit': ['profit', 'earnings', 'net income'],
            'ebitda': ['ebitda', 'operating profit'],
            'margin': ['margin', 'profit margin'],
            'costs': ['costs', 'expenses'],
            'balance': ['balance', 'total assets']
        }
    }

    def __init__(self):
        self.documents = []
        self.financial_data = {}
        self.document_languages = {}

    def detect_language(self, text: str) -> str:
        """Detect language of text, focusing on Dutch and English."""
        try:
            lang = detect(text)
            return 'dutch' if lang == 'nl' else 'english'
        except:
            return 'english'  # Default to English if detection fails

    def process_file(self, file_path: str) -> None:
        """Process a single file handling both Dutch and English content."""
        path = Path(file_path)
        
        if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file type: {path.suffix}")

        try:
            if path.suffix.lower() in ['.xlsx', '.xls']:
                self._process_excel(path)
            else:
                # Load document
                loader_class = self._get_loader(path.suffix.lower())
                docs = loader_class(str(path)).load()
                
                # Detect language for each document
                for doc in docs:
                    lang = self.detect_language(doc.page_content)
                    doc.metadata['language'] = lang
                    self.document_languages[path.name] = lang
                
                self.documents.extend(docs)
                
            print(f"Successfully processed {path.name}")
            
        except Exception as e:
            print(f"Error processing {path.name}: {str(e)}")

    def _process_excel(self, file_path: Path) -> None:
        """Process Excel files with awareness of Dutch/English headers."""
        try:
            df = pd.read_excel(file_path)
            
            # Detect language from column names
            column_text = ' '.join(df.columns.astype(str))
            lang = self.detect_language(column_text)
            
            if self._is_financial_data(df, lang):
                self._extract_financial_data(df, file_path.name, lang)
            else:
                # Process as regular document if not financial data
                loader_class = self._get_loader('.xlsx')
                docs = loader_class(str(file_path)).load()
                for doc in docs:
                    doc.metadata['language'] = lang
                self.documents.extend(docs)
                
        except Exception as e:
            print(f"Error processing Excel file {file_path.name}: {str(e)}")

    def _is_financial_data(self, df: pd.DataFrame, lang: str) -> bool:
        """Check for financial terms in both Dutch and English."""
        column_text = ' '.join(df.columns.astype(str).str.lower())
        terms = self.FINANCIAL_TERMS[lang].values()
        # Flatten the list of terms
        all_terms = [term for sublist in terms for term in sublist]
        return any(term in column_text for term in all_terms)

    def _standardize_column_names(self, df: pd.DataFrame, lang: str) -> pd.DataFrame:
        """Convert Dutch column names to standard English names if needed."""
        if lang == 'dutch':
            column_mapping = {}
            for eng_key, dutch_terms in self.FINANCIAL_TERMS['dutch'].items():
                for dutch_term in dutch_terms:
                    matching_cols = [col for col in df.columns if dutch_term.lower() in col.lower()]
                    for col in matching_cols:
                        column_mapping[col] = eng_key
            
            if column_mapping:
                df = df.rename(columns=column_mapping)
        
        return df

class InvestmentMemoCompiler:
    """Compiles processed documents into an investment memorandum."""
    
    def __init__(self, processor: MultilingualDocumentProcessor):
        self.processor = processor
        self.llm = ChatOpenAI(model="gpt-4")
        
    def generate_memo(self, target_language: str = 'english') -> str:
        """Generate complete memo in specified language."""
        sections = {
            'financial_analysis': self._generate_financial_section(target_language),
            'company_overview': self._generate_company_section(target_language),
            'market_analysis': self._generate_market_section(target_language)
        }
        
        # Format final memo
        return self._format_memo(sections, target_language)
    
    def _generate_section(self, section_name: str, target_language: str) -> str:
        """Generate section content with language handling."""
        system_prompt = {
            'dutch': "Je bent een professionele investeringsanalist die investeringsmemoranda schrijft.",
            'english': "You are a professional investment analyst writing investment memorandums."
        }
        
        # Create language-specific prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt[target_language]),
            ("user", f"""Generate the {section_name} section based on the provided documents.
            Target language: {target_language}
            Make sure to maintain professional financial terminology.""")
        ])
        
        response = self.llm(prompt.format_messages())
        return response.content

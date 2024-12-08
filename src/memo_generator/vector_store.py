from typing import List, Dict, Any, Optional
from pathlib import Path
import logging
import json
import numpy as np
from datetime import datetime

import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

from .document_processor import ProcessedDocument, DocumentMetadata

class VectorStore:
    """Manages document embeddings and semantic search functionality."""
    
    def __init__(self, config):
        self.config = config
        self._setup_logging()
        self.client = self._initialize_chroma()
        self.embedding_function = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self._get_or_create_collection()

    def _setup_logging(self):
        """Configure logging for vector store operations."""
        logging.basicConfig(
            filename=Path(self.config.processing.temp_directory) / 'vector_store.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def _initialize_chroma(self):
        """Initialize ChromaDB with persistent storage."""
        try:
            client = chromadb.Client(Settings(
                chroma_db_impl="duckdb+parquet",
                persist_directory=self.config.vector_db.persist_directory
            ))
            self.logger.info("ChromaDB initialized successfully")
            return client
        except Exception as e:
            self.logger.error(f"Error initializing ChromaDB: {str(e)}")
            raise

    def _get_or_create_collection(self):
        """Get existing collection or create new one."""
        try:
            return self.client.get_or_create_collection(
                name=self.config.vector_db.collection_name,
                embedding_function=self.embedding_function,
                metadata={"description": "Investment document embeddings"}
            )
        except Exception as e:
            self.logger.error(f"Error with collection: {str(e)}")
            raise

    def add_document(self, processed_doc: ProcessedDocument) -> bool:
        """Add a processed document to the vector store."""
        try:
            # Generate unique IDs for each chunk
            chunk_ids = [
                f"{processed_doc.metadata.filename}_{i}" 
                for i in range(len(processed_doc.chunks))
            ]
            
            # Prepare metadata for each chunk
            metadatas = []
            for i, chunk in enumerate(processed_doc.chunks):
                meta = processed_doc.metadata.__dict__.copy()
                meta.update({
                    "chunk_index": i,
                    "total_chunks": len(processed_doc.chunks),
                    "indexed_at": datetime.now().isoformat()
                })
                metadatas.append(meta)

            # Add chunks to collection
            self.collection.add(
                documents=processed_doc.chunks,
                ids=chunk_ids,
                metadatas=metadatas
            )
            
            self.logger.info(f"Successfully added document: {processed_doc.metadata.filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding document {processed_doc.metadata.filename}: {str(e)}")
            return False

    def add_financial_data(self, processed_doc: ProcessedDocument) -> bool:
        """Special handling for financial data from Excel files."""
        if not isinstance(processed_doc.content, dict):
            return False
            
        try:
            for sheet_name, df in processed_doc.content.items():
                # Convert financial data to structured format
                financial_data = self._process_financial_dataframe(df)
                
                # Create metadata for financial data
                meta = processed_doc.metadata.__dict__.copy()
                meta.update({
                    "sheet_name": sheet_name,
                    "data_type": "financial",
                    "columns": list(df.columns),
                    "indexed_at": datetime.now().isoformat()
                })
                
                # Add to collection with special ID
                doc_id = f"{processed_doc.metadata.filename}_{sheet_name}_financial"
                self.collection.add(
                    documents=[financial_data],
                    ids=[doc_id],
                    metadatas=[meta]
                )
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding financial data {processed_doc.metadata.filename}: {str(e)}")
            return False

    def _process_financial_dataframe(self, df: pd.DataFrame) -> str:
        """Convert financial DataFrame to structured text format."""
        # Extract key statistics
        stats = {
            "summary": df.describe().to_dict(),
            "columns": list(df.columns),
            "non_null_counts": df.count().to_dict()
        }
        
        # Convert to string format that preserves structure
        return json.dumps(stats, indent=2)

    def semantic_search(self, 
                       query: str, 
                       n_results: int = 5, 
                       filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Perform semantic search across documents."""
        try:
            # Execute search
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                where=filters
            )
            
            # Format results
            formatted_results = []
            for i in range(len(results['ids'][0])):
                result = {
                    'id': results['ids'][0][i],
                    'content': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i] if 'distances' in results else None
                }
                formatted_results.append(result)
                
            return formatted_results
            
        except Exception as e:
            self.logger.error(f"Error during semantic search: {str(e)}")
            return []

    def get_financial_data(self, 
                          filename: Optional[str] = None, 
                          sheet_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve financial data with optional filters."""
        filters = {"data_type": "financial"}
        
        if filename:
            filters["filename"] = filename
        if sheet_name:
            filters["sheet_name"] = sheet_name
            
        try:
            # Query collection with filters
            results = self.collection.get(
                where=filters
            )
            
            # Parse and format financial data
            formatted_results = []
            for i in range(len(results['ids'])):
                financial_data = json.loads(results['documents'][i])
                result = {
                    'id': results['ids'][i],
                    'data': financial_data,
                    'metadata': results['metadatas'][i]
                }
                formatted_results.append(result)
                
            return formatted_results
            
        except Exception as e:
            self.logger.error(f"Error retrieving financial data: {str(e)}")
            return []

    def cleanup_old_entries(self, days_old: int = 30) -> bool:
        """Remove entries older than specified days."""
        try:
            cutoff_date = (datetime.now() - pd.Timedelta(days=days_old)).isoformat()
            
            # Delete old entries
            self.collection.delete(
                where={"indexed_at": {"$lt": cutoff_date}}
            )
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error during cleanup: {str(e)}")
            return False

    def persist(self) -> bool:
        """Explicitly persist the database to disk."""
        try:
            self.client.persist()
            return True
        except Exception as e:
            self.logger.error(f"Error persisting database: {str(e)}")
            return False
# Investment Memo Generator

An AI-powered tool for generating professional investment memorandums from financial documents and analysis data.

## Overview

This project uses Large Language Models (LLMs) and Retrieval Augmented Generation (RAG) to automate the creation of investment memorandums. It processes financial data, market analysis, and due diligence notes to generate comprehensive, well-structured investment memos.

## Features

- Automated memo generation from raw financial data
- Structured template-based output
- Vector database integration for context retrieval
- Customizable memo sections and formatting
- Local deployment options for data security

## Project Structure

```
├── config/              # Configuration files
├── data/                # Sample data and templates
│   ├── raw/            # Raw input data
│   ├── processed/      # Processed data
│   └── templates/      # Memo templates
├── src/                # Source code
│   ├── data/          # Data processing modules
│   ├── models/        # LLM integration
│   ├── utils/         # Utility functions
│   └── webapp/        # Web interface
├── tests/              # Test suite
└── notebooks/          # Jupyter notebooks for development
```

## Getting Started

### Prerequisites

- Python 3.9+
- Virtual environment tool (e.g., venv, conda)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Daisels/investment-memo-generator.git
   cd investment-memo-generator
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Detailed usage instructions will be added as the project develops.

## Development

### Setting Up Development Environment

1. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Running Tests

```bash
pytest tests/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
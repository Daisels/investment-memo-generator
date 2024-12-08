from pathlib import Path
from typing import Dict, List, Optional, Union
import logging
from dataclasses import dataclass
import pandas as pd
from langdetect import detect
from datetime import datetime

# Document handling imports
from pypdf import PdfReader
from docx import Document as DocxDocument
import pdfplumber
from openpyxl import load_workbook

[... rest of the code ...]
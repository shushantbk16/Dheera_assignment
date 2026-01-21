import os
import json
import uuid
import pypdf
import chromadb
from chromadb.utils import embedding_functions

class DocumentLoader:
    def load_text(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return ""

    def load_pdf(self, file_path):
        text = ""
        try:
            print(f"Reading PDF: {file_path}...")
            reader = pypdf.PdfReader(file_path)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            print(f"Extracted {len(text)} characters.")
        except Exception as e:
            print(f"Error reading PDF {file_path}: {e}")
        return text

class SOPProcessor:
    def parse_sop(self, text):
        # Split SOP into sections based on headers (lines in CAPS)
        lines = text.split('\n')
        sections = []
        current_header = "General"
        current_content = []

        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Heuristic: if line is all caps and short, it's a header
            if line.isupper() and len(line) < 50:
                if current_content:
                    sections.append({
                        "header": current_header,
                        "content": " ".join(current_content)
                    })
                current_header = line
                current_content = []
            else:
                current_content.append(line)
        
        if current_content:
            sections.append({
                "header": current_header,
                "content": " ".join(current_content)
            })
        return sections

    def chunk_text(self, text, chunk_size=300):
        chunks = []
        for i in range(0, len(text), chunk_size):
            chunks.append(text[i:i+chunk_size])
        return chunks

class VectorStore:
    def __init__(self):
        print("Initializing Vector DB...")
        self.client = chromadb.Client()
        self.collection = self.client.create_collection(name="regulations")

    def add_document(self, text, source_name):
        doc_id = str(uuid.uuid4())
        self.collection.add(
            documents=[text],
            metadatas=[{"source": source_name}],
            ids=[doc_id]
        )

    def search(self, query_text):
        results = self.collection.query(
            query_texts=[query_text],
            n_results=3
        )
        
        formatted_results = []
        if results['documents']:
            for i, doc in enumerate(results['documents'][0]):
                meta = results['metadatas'][0][i]
                formatted_results.append({
                    "text": doc,
                    "source": meta['source']
                })
        
        return formatted_results

class GapAnalyzer:
    def check_gaps(self, sop_section, relevant_regs):
        # Prompt for the LLM
        system_msg = """
        You are a Quality Assurance Specialist for a Pharmaceutical company.
        Compare the internal SOP section against relevant FDA/GMP regulations.
        Identify specific gaps where the SOP fails to meet the regulatory standard.
        """
        
        user_msg = f"""
        INTERNAL SOP SECTION:
        Header: {sop_section['header']}
        Content: {sop_section['content']}
        
        RELEVANT REGULATIONS:
        {json.dumps([r['text'] for r in relevant_regs], indent=2)}
        
        TASK:
        List any missing steps, vague instructions, or compliance failures.
        """
        
        # TODO: Connect to OpenAI API here
        # response = openai.ChatCompletion.create(...)
        
        # Mock response for now
        gaps = []
        sop_text = sop_section['content'].lower()
        
        if len(sop_text) < 20:
            gaps.append("SOP section is too short/vague.")
        
        for reg in relevant_regs:
            reg_text = reg['text'].lower()
            if "must" in reg_text and "verify" not in sop_text:
                gaps.append(f"Missing verification step required by: {reg['source']}")
        
        if not gaps:
            gaps.append("No obvious gaps found.")
            
        return gaps

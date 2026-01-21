from gap_system import DocumentLoader, SOPProcessor, VectorStore, GapAnalyzer

def main():
    print("--- Regulatory Gap Detector ---")

    loader = DocumentLoader()
    processor = SOPProcessor()
    db = VectorStore()
    analyzer = GapAnalyzer()

    # Load regulations (Mocking this part for demo)
    print("Loading regulations...")
    regulations = [
        "FDA says you must validate all equipment before use.",
        "GMP requires written procedures for cleaning.",
        "Records must be kept for 5 years."
    ]
    
    for reg in regulations:
        db.add_document(reg, "FDA_Guideline_Doc")

    # Process SOP
    print("Processing SOP...")
    sop_text = """
    PURPOSE
    To clean the machine.
    
    PROCEDURE
    1. Wipe it down.
    2. Done.
    """
    
    sections = processor.parse_sop(sop_text)
    
    # Find Gaps
    print("Checking for gaps...")
    for section in sections:
        print(f"\nChecking Section: {section['header']}")
        
        # Find relevant regulations
        relevant_regs = db.search(section['content'])
        
        # Check for gaps
        gaps = analyzer.check_gaps(section, relevant_regs)
        
        for gap in gaps:
            print(f" -> GAP FOUND: {gap}")

    print("\nDone!")

if __name__ == "__main__":
    main()

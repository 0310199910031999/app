import sys
import traceback
from mainContext.infrastructure.adapters.weasyprint_pdf_adapter import WeasyPrintPdfAdapter

def test():
    try:
        adapter = WeasyPrintPdfAdapter()
        data = {
            "signature_path": "",
            "date_signed": "2023-10-27",
            "client_name": "Test Client",
            "document_id": "FOBC-01-001"
        }
        # Minimal data often used in templates
        question_groups = [
            {
                "group_name": "Group 1", 
                "questions": [
                    {"question_text": "Q1", "answer_text": "Yes"}, 
                    {"question_text": "Q2", "answer_text": "No"}
                ]
            },
            {
                "group_name": "Group 2", 
                "questions": [
                    {"question_text": "Q3", "answer_text": "Maybe"}
                ]
            }
        ]
        battery_cell_rows = [
            ["Row 1 Col 1", "Row 1 Col 2"],
            ["Row 2 Col 1", "Row 2 Col 2"]
        ]
        
        pdf_bytes = adapter.generate_fobc01_pdf(
            data=data,
            question_groups=question_groups,
            battery_cell_rows=battery_cell_rows
        )
        
        print(f"OK {len(pdf_bytes)}")
    except Exception:
        traceback.print_exc()

if __name__ == "__main__":
    test()

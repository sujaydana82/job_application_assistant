from fpdf import FPDF
import os

class UnicodePDFGenerator:
    def __init__(self):
        self.pdf = FPDF()
        
    def generate_pdf(self, content: str, filename: str) -> str:
        """Generate PDF with proper Unicode support"""
        try:
            os.makedirs('generated_files', exist_ok=True)
            filepath = os.path.join('generated_files', filename)
            
            # Create PDF
            pdf = FPDF()
            pdf.add_page()
            
            # Use Helvetica which handles basic characters well
            pdf.set_font("Helvetica", size=10)
            
            # Clean content for PDF compatibility
            clean_content = self.clean_content_for_pdf(content)
            
            # Add content with proper formatting
            lines = clean_content.split('\n')
            for line in lines:
                if not line.strip():
                    pdf.ln(4)
                    continue
                
                # Handle different line types
                if any(line.strip().startswith(prefix) for prefix in ['---', '===', '***']):
                    # Separator line
                    pdf.set_draw_color(0, 0, 0)
                    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
                    pdf.ln(6)
                elif line.strip().startswith('SECTION') or line.strip().startswith('COMPREHENSIVE'):
                    # Header line
                    pdf.set_font("Helvetica", 'B', 12)
                    pdf.cell(200, 8, txt=line.strip(), ln=True)
                    pdf.set_font("Helvetica", size=10)
                    pdf.ln(2)
                elif line.strip().startswith('•') or line.strip().startswith('-'):
                    # Bullet point
                    pdf.cell(10, 5, txt="", ln=0)
                    pdf.cell(190, 5, txt=line.strip()[2:], ln=True)
                else:
                    # Regular text with word wrap
                    self.add_wrapped_text(pdf, line, 190)
                
                pdf.ln(4)
            
            pdf.output(filepath)
            return filepath
            
        except Exception as e:
            print(f"PDF generation error: {e}")
            raise
    
    def clean_content_for_pdf(self, content: str) -> str:
        """Clean content for PDF compatibility"""
        # Replace Unicode characters with ASCII equivalents
        replacements = {
            '•': '-',
            '✓': '[X]',
            '→': '->',
            '—': '-',
            '–': '-',
            '“': '"',
            '”': '"',
            '‘': "'",
            '’': "'",
            '…': '...',
        }
        
        clean_content = content
        for unicode_char, ascii_char in replacements.items():
            clean_content = clean_content.replace(unicode_char, ascii_char)
        
        return clean_content
    
    def add_wrapped_text(self, pdf, text: str, max_width: int):
        """Add text with word wrapping"""
        words = text.split(' ')
        current_line = ""
        
        for word in words:
            # Check if adding the word exceeds the width
            test_line = current_line + ' ' + word if current_line else word
            if pdf.get_string_width(test_line) < max_width:
                current_line = test_line
            else:
                # Output the current line and start a new one
                if current_line:
                    pdf.cell(200, 5, txt=current_line, ln=True)
                current_line = word
        
        # Output the last line
        if current_line:
            pdf.cell(200, 5, txt=current_line, ln=True)
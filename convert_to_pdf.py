import os
from fpdf import FPDF


class PDF(FPDF):
    def __init__(self, title="Data Handling - Class 8 Study Material"):
        super().__init__()
        self.pdf_title = title

    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, self.pdf_title, 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Arial', '', 10)
        # Split the body into lines
        lines = body.split('\n')
        for line in lines:
            # Handle markdown-like formatting
            if line.startswith('# '):
                self.set_font('Arial', 'B', 14)
                line = line[2:]
            elif line.startswith('## '):
                self.set_font('Arial', 'B', 12)
                line = line[3:]
            elif line.startswith('### '):
                self.set_font('Arial', 'B', 11)
                line = line[4:]
            elif line.startswith('*') and line.endswith('*'):
                self.set_font('Arial', 'I', 10)
                line = line[1:-1]
            else:
                self.set_font('Arial', '', 10)
            
            # Handle table-like lines
            if '|' in line and line.count('|') > 2:
                # Simple table handling
                cells = line.split('|')
                cells = [cell.strip() for cell in cells if cell.strip()]
                if cells:
                    line = '  '.join(cells)
            
            # Write the line
            self.multi_cell(0, 5, line)
            self.ln(2)


def convert_markdown_to_pdf(input_file, output_file, title="Data Handling - Class 8 Study Material"):
    """Convert a markdown file to PDF using fpdf2"""
    try:
        # Read the markdown file
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create PDF
        pdf = PDF(title)
        pdf.add_page()
        
        # Process content
        sections = content.split('\n\n')
        
        for section in sections:
            if section.strip():
                lines = section.strip().split('\n')
                if lines[0].startswith('#'):
                    title = lines[0]
                    body = '\n'.join(lines[1:]) if len(lines) > 1 else ''
                    
                    # Format title
                    if title.startswith('# '):
                        pdf.set_font('Arial', 'B', 14)
                        pdf.cell(0, 10, title[2:], 0, 1, 'L')
                        pdf.ln(5)
                    elif title.startswith('## '):
                        pdf.set_font('Arial', 'B', 12)
                        pdf.cell(0, 10, title[3:], 0, 1, 'L')
                        pdf.ln(3)
                    
                    # Add body content
                    if body:
                        pdf.set_font('Arial', '', 10)
                        # Handle special formatting in body
                        body_lines = body.split('\n')
                        for line in body_lines:
                            if line.strip():
                                pdf.multi_cell(0, 5, line)
                                pdf.ln(1)
                        pdf.ln(3)
                else:
                    # Regular paragraph
                    pdf.set_font('Arial', '', 10)
                    pdf.multi_cell(0, 5, section)
                    pdf.ln(3)
        
        # Output PDF
        pdf.output(output_file)
        print(f"Successfully converted {input_file} to {output_file}")
        return True
    except Exception as e:
        print(f"Error converting to PDF: {str(e)}")
        return False


if __name__ == "__main__":
    # Generate Data Handling PDF
    input_file1 = "data/data_handling_study_material.md"
    output_file1 = "data/data_handling_study_material.pdf"
    
    if os.path.exists(input_file1):
        convert_markdown_to_pdf(input_file1, output_file1, "Data Handling - Class 8 Study Material")
    else:
        print(f"Input file {input_file1} not found")
    
    # Generate Mensuration PDF
    input_file2 = "data/mensuration_study_material.md"
    output_file2 = "data/mensuration_study_material.pdf"
    
    if os.path.exists(input_file2):
        convert_markdown_to_pdf(input_file2, output_file2, "Mensuration - Class 8 Study Material")
    else:
        print(f"Input file {input_file2} not found")

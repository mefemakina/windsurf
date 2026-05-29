from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from datetime import datetime

class ExportManager:
    def __init__(self):
        # Use default Helvetica font (supports basic characters)
        self.font_name = 'Helvetica'
            
    def export_pdf(self, quotation, file_path):
        doc = SimpleDocTemplate(file_path, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, 
                               topMargin=2*cm, bottomMargin=2*cm)
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1
        )
        
        header_style = ParagraphStyle(
            'CustomHeader',
            parent=styles['Heading2'],
            fontSize=12,
            spaceAfter=10
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=5
        )
        
        # Title
        story.append(Paragraph("TEKLİF", title_style))
        story.append(Spacer(1, 0.5*cm))
        
        # Header information
        header_data = [
            ['Teklif No:', quotation['quotation_no']],
            ['Tarih:', quotation['date']],
            ['Teslimat Tipi:', quotation['delivery_type']],
            ['Para Birimi:', quotation['currency']]
        ]
        
        header_table = Table(header_data, colWidths=[4*cm, 6*cm])
        header_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), self.font_name),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(header_table)
        story.append(Spacer(1, 1*cm))
        
        # Items table
        if quotation['items']:
            items_data = [['Sıra', 'Kod', 'Açıklama', 'Miktar', 'Birim', 'Birim Fiyat', 'Toplam']]
            
            for idx, item in enumerate(quotation['items'], 1):
                items_data.append([
                    str(idx),
                    item['code'],
                    item['description'],
                    str(item['quantity']),
                    item['unit'],
                    f"{item['unit_price']:.2f}",
                    f"{item['total']:.2f}"
                ])
            
            items_table = Table(items_data, colWidths=[1*cm, 2*cm, 5*cm, 2*cm, 2*cm, 2*cm, 2*cm])
            items_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), self.font_name),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
            ]))
            story.append(items_table)
            story.append(Spacer(1, 1*cm))
        
        # Total
        total_data = [
            ['', '', '', '', '', 'Toplam:', f"{quotation['total_amount']:.2f} {quotation['currency']}"]
        ]
        total_table = Table(total_data, colWidths=[1*cm, 2*cm, 5*cm, 2*cm, 2*cm, 2*cm, 2*cm])
        total_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), self.font_name),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('FONTNAME', (5, 0), (6, 0), self.font_name),
            ('FONTSIZE', (5, 0), (6, 0), 11),
            ('ALIGN', (5, 0), (6, 0), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(total_table)
        story.append(Spacer(1, 1*cm))
        
        # Notes
        if quotation['notes']:
            story.append(Paragraph("Notlar:", header_style))
            story.append(Paragraph(quotation['notes'], normal_style))
        
        # Footer
        story.append(Spacer(1, 2*cm))
        footer_text = f"Bu teklif {datetime.now().strftime('%d.%m.%Y')} tarihinde düzenlenmiştir."
        story.append(Paragraph(footer_text, normal_style))
        
        # Build PDF
        doc.build(story)
        
    def export_excel(self, quotation, file_path):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Teklif"
        
        # Define styles
        header_font = Font(bold=True, size=12)
        header_fill = PatternFill(start_color="CCCCCC", end_color="CCCCCC", fill_type="solid")
        border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        center_align = Alignment(horizontal='center', vertical='center')
        right_align = Alignment(horizontal='right', vertical='center')
        
        # Header information
        ws['A1'] = "TEKLİF"
        ws['A1'].font = Font(bold=True, size=16)
        ws.merge_cells('A1:G1')
        
        ws['A3'] = "Teklif No:"
        ws['B3'] = quotation['quotation_no']
        ws['A4'] = "Tarih:"
        ws['B4'] = quotation['date']
        ws['A5'] = "Teslimat Tipi:"
        ws['B5'] = quotation['delivery_type']
        ws['A6'] = "Para Birimi:"
        ws['B6'] = quotation['currency']
        
        # Items table header
        headers = ['Sıra', 'Kod', 'Açıklama', 'Miktar', 'Birim', 'Birim Fiyat', 'Toplam']
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=8, column=col, value=header)
            cell.font = header_font
            cell.fill = header_fill
            cell.border = border
            cell.alignment = center_align
            
        # Items data
        for idx, item in enumerate(quotation['items'], 1):
            row = 8 + idx
            ws.cell(row=row, column=1, value=idx).alignment = center_align
            ws.cell(row=row, column=2, value=item['code']).border = border
            ws.cell(row=row, column=3, value=item['description']).border = border
            ws.cell(row=row, column=4, value=item['quantity']).border = border
            ws.cell(row=row, column=4).alignment = center_align
            ws.cell(row=row, column=5, value=item['unit']).border = border
            ws.cell(row=row, column=5).alignment = center_align
            ws.cell(row=row, column=6, value=item['unit_price']).border = border
            ws.cell(row=row, column=6).alignment = right_align
            ws.cell(row=row, column=7, value=item['total']).border = border
            ws.cell(row=row, column=7).alignment = right_align
            
        # Total row
        total_row = 8 + len(quotation['items']) + 1
        ws.cell(row=total_row, column=6, value="Toplam:").font = header_font
        ws.cell(row=total_row, column=6).alignment = right_align
        ws.cell(row=total_row, column=7, value=quotation['total_amount']).font = header_font
        ws.cell(row=total_row, column=7).alignment = right_align
        
        # Notes
        if quotation['notes']:
            notes_row = total_row + 2
            ws.cell(row=notes_row, column=1, value="Notlar:").font = header_font
            ws.cell(row=notes_row + 1, column=1, value=quotation['notes'])
            ws.merge_cells(f'A{notes_row + 1}:G{notes_row + 1}')
            
        # Adjust column widths
        ws.column_dimensions['A'].width = 8
        ws.column_dimensions['B'].width = 15
        ws.column_dimensions['C'].width = 30
        ws.column_dimensions['D'].width = 10
        ws.column_dimensions['E'].width = 10
        ws.column_dimensions['F'].width = 15
        ws.column_dimensions['G'].width = 15
        
        # Save
        wb.save(file_path)

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import io
from django.http import FileResponse


def generate_pdf_entry(order, checklist):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Cabeçalho
    c.setFont("Helvetica-Bold", 18)
    c.drawString(40*mm, 280*mm, "JR CELL - ASSISTÊNCIA TÉCNICA")
    c.setFont("Helvetica", 12)
    c.drawString(40*mm, 272*mm, f"NOTA DE ENTRADA O.S Nº {order.id}")

    # Dados do cliente/aparelho
    y = 260
    c.setFont("Helvetica", 10)
    c.drawString(15*mm, y*mm, f"Cliente: {order.client}")
    c.drawString(110*mm, y*mm, f"Contato: {order.client.phone if hasattr(order.client, 'phone') else ''}")
    y -= 7
    c.drawString(15*mm, y*mm, f"Aparelho: {order.device}")
    y -= 7
    c.drawString(15*mm, y*mm, f"Defeito: {order.defect}")
    y -= 7
    c.drawString(15*mm, y*mm, f"Observações: {order.additional_info or ''}")
    y -= 10

    # Tabela do checklist
    c.setFont("Helvetica-Bold", 11)
    c.drawString(15*mm, y*mm, "CHECK LIST DE FUNCIONAMENTO")
    y -= 6
    c.setFont("Helvetica", 10)
    # Títulos das colunas
    c.drawString(18*mm, y*mm, "Item")
    c.drawString(140*mm, y*mm, "Sim")
    c.drawString(155*mm, y*mm, "Não")
    y -= 5

    # Itens do checklist
    for item in checklist.items.all():
        c.drawString(18*mm, y*mm, item.description)
        if item.checked:
            c.drawString(143*mm, y*mm, "X")
        else:
            c.drawString(158*mm, y*mm, "X")
        y -= 5

    # Rodapé
    c.setFont("Helvetica", 9)
    c.drawString(15*mm, 30*mm, f"Data da expedição: {order.shipping_date.strftime('%d/%m/%Y') if order.shipping_date else ''}")
    c.drawString(15*mm, 25*mm, "Senha do aparelho: (caso tenha) __________________________________")
    c.drawString(15*mm, 20*mm, "Ass: Cliente __________________________________")

    c.showPage()
    c.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"{order.id}_nota_de_entrada.pdf")


def generate_pdf_exit(order, checklist):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Cabeçalho
    c.setFont("Helvetica-Bold", 18)
    c.drawString(40*mm, 280*mm, "JR CELL - ASSISTÊNCIA TÉCNICA")
    c.setFont("Helvetica", 12)
    c.drawString(40*mm, 272*mm, f"NOTA DE SAÍDA O.S Nº {order.id}")

    # Dados do cliente/aparelho
    y = 260
    c.setFont("Helvetica", 10)
    c.drawString(15*mm, y*mm, f"Cliente: {order.client}")
    c.drawString(110*mm, y*mm, f"Contato: {order.client.phone if hasattr(order.client, 'phone') else ''}")
    y -= 7
    c.drawString(15*mm, y*mm, f"Aparelho: {order.device}")
    y -= 7
    c.drawString(15*mm, y*mm, f"Serviço Prestado: {order.additional_description}")
    y -= 7
    c.drawString(15*mm, y*mm, f"Observações: {order.additional_info_exit or ''}")
    y -= 10

    # Tabela do checklist de saída
    c.setFont("Helvetica-Bold", 11)
    c.drawString(15*mm, y*mm, "CHECK LIST DE FUNCIONAMENTO SAÍDA")
    y -= 6
    c.setFont("Helvetica", 10)
    # Títulos das colunas
    c.drawString(18*mm, y*mm, "Item")
    c.drawString(140*mm, y*mm, "Sim")
    c.drawString(155*mm, y*mm, "Não")
    y -= 5

    # Itens do checklist de saída
    for item in checklist.items.all():
        c.drawString(18*mm, y*mm, item.description)
        if item.checked:
            c.drawString(143*mm, y*mm, "X")
        else:
            c.drawString(158*mm, y*mm, "X")
        y -= 5

    # Rodapé
    c.setFont("Helvetica", 9)
    c.drawString(15*mm, 30*mm, f"Data da retirada: {order.withdrawal_date.strftime('%d/%m/%Y') if order.withdrawal_date else ''}")
    c.drawString(15*mm, 25*mm, "Ass: Cliente __________________________________")

    c.showPage()
    c.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"{order.id}_nota_de_saida.pdf")

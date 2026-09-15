import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_pdf_itinerary(trip_data: dict) -> bytes:
    """
    Generate a formatted PDF document of the travel itinerary.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#1e293b")
    )
    h2_style = ParagraphStyle(
        'DocH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#0284c7"),
        spaceBefore=10,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#334155")
    )
    bold_body = ParagraphStyle(
        'DocBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#0f172a")
    )

    story = []

    # Title & Subtitle
    destination = trip_data.get("destination", "Destination")
    origin = trip_data.get("origin", "Origin")
    duration = trip_data.get("duration_days", 4)
    currency = trip_data.get("currency", "INR")
    budget = trip_data.get("budget", 20000)
    group_size = trip_data.get("group_size", 1)
    itinerary = trip_data.get("itinerary", {})

    story.append(Paragraph(f"AI Travel Itinerary: {origin} to {destination}", title_style))
    story.append(Paragraph(f"<b>Duration:</b> {duration} Days | <b>Travelers:</b> {group_size} {'Person' if group_size == 1 else 'Members'} | <b>Total Budget:</b> {currency} {budget:,.0f} | <b>Best Season:</b> {itinerary.get('best_time_to_visit', 'N/A')}", body_style))
    story.append(Paragraph(f"<i>Powered by AI Travel Planner</i>", body_style))
    story.append(Spacer(1, 12))

    # Overview
    overview = itinerary.get("destination_overview", "")
    if overview:
        story.append(Paragraph("Destination Overview", h2_style))
        story.append(Paragraph(overview, body_style))
        story.append(Spacer(1, 10))

    # Budget Breakdown
    budget_data = itinerary.get("budget_breakdown", {})
    if budget_data:
        story.append(Paragraph("Estimated Budget Allocation", h2_style))
        b_table_data = [
            [Paragraph("<b>Category</b>", bold_body), Paragraph(f"<b>Estimated Amount ({currency})</b>", bold_body)],
            [Paragraph("Transportation (Round Trip)", body_style), Paragraph(f"{currency} {budget_data.get('transportation', 0):,.2f}", body_style)],
            [Paragraph("Accommodation", body_style), Paragraph(f"{currency} {budget_data.get('accommodation', 0):,.2f}", body_style)],
            [Paragraph("Food & Dining", body_style), Paragraph(f"{currency} {budget_data.get('food_and_dining', 0):,.2f}", body_style)],
            [Paragraph("Sightseeing & Activities", body_style), Paragraph(f"{currency} {budget_data.get('activities_and_entry', 0):,.2f}", body_style)],
            [Paragraph("Contingency Buffer", body_style), Paragraph(f"{currency} {budget_data.get('emergency_buffer', 0):,.2f}", body_style)],
            [Paragraph("<b>Total Estimated Cost</b>", bold_body), Paragraph(f"<b>{currency} {budget_data.get('total_estimated_cost', 0):,.2f}</b>", bold_body)]
        ]
        t = Table(b_table_data, colWidths=[280, 220])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(t)
        story.append(Spacer(1, 12))

    # Daily Schedule
    daily_plans = itinerary.get("daily_itinerary", [])
    if daily_plans:
        story.append(Paragraph("Day-by-Day Itinerary", h2_style))
        for day in daily_plans:
            d_num = day.get("day", 1)
            theme = day.get("theme", "")
            story.append(Paragraph(f"<b>Day {d_num}: {theme}</b>", bold_body))
            for act in day.get("activities", []):
                slot = act.get("time_slot", "")
                title = act.get("title", "")
                desc = act.get("description", "")
                story.append(Paragraph(f"• <i>{slot}</i> - <b>{title}</b>: {desc}", body_style))
            
            foods = day.get("food_recommendations", [])
            if foods:
                story.append(Paragraph(f"  🍴 <i>Dining suggestions:</i> {', '.join(foods)}", body_style))
            story.append(Spacer(1, 8))

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes

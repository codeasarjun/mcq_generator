from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def create_pdf(questions):
    output = BytesIO()
    doc = SimpleDocTemplate(output, pagesize=letter)
    styles = getSampleStyleSheet()
    style_normal = styles['Normal']
    style_heading = styles['Heading1']
    story = []

    # Add a title
    story.append(Paragraph("Generated Questions", style_heading))
    story.append(Spacer(1, 12))

    for q in questions:
        # Add the question
        question_text = f"Question: {q['ques']}"
        story.append(Paragraph(question_text, style_normal))
        story.append(Spacer(1, 6))

        # Add the choices
        for letter_key, choice in q['choices'].items():
            choice_text = f"{letter_key}. {choice.capitalize()}"
            story.append(Paragraph(choice_text, style_normal))
        
        # Add the correct answer
        correct_answer_text = f"<b>Correct Answer:</b> {q['correct_ans'].capitalize()}"
        story.append(Paragraph(correct_answer_text, style_normal))
        story.append(Spacer(1, 12))  # Space between questions

    doc.build(story)
    output.seek(0)
    return output

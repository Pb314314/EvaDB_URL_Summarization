import warnings
from urllib.request import urlopen
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

import evadb

warnings.filterwarnings("ignore")

def fetch_webpage_content(url):
    try:
        page = urlopen(url)
        html = page.read().decode("utf-8")
        return html
    except Exception as e:
        print(f"Error fetching webpage: {e}")
        return None

def parse_html_to_text_list(html):
    soup = BeautifulSoup(html, "html.parser")
    return [p.get_text() for p in soup.find_all("p")]

def merge_strings(text_list, threshold):
    result_list = []
    current_string = ""
    word_count = 0

    for text in text_list:
        words = text.split()
        for word in words:
            current_string += word + " "
            word_count += 1
            if word_count >= threshold:
                result_list.append(current_string.strip())
                current_string = ""
                word_count = 0

    if current_string:
        result_list.append(current_string.strip())

    return result_list

def round_to_nearest_hundred(n):
    return round(n / 100.0) * 100

def create_pdf_file(merged_list, filename):
    document = SimpleDocTemplate(filename, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    style = styles["Normal"]

    for text in merged_list:
        paragraph = Paragraph(text, style)
        elements.append(paragraph)
        elements.append(Spacer(1, 12))

    document.build(elements)
    return filename

def create_summary_pdf(merged_string, filename):
    document = SimpleDocTemplate(filename, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    style = styles["Normal"]

    # Adding the summarized text to the PDF
    paragraph = Paragraph(merged_string, style)
    elements.append(paragraph)
    
    # Build the PDF document
    document.build(elements)
    print(f"Summarization saved as PDF: {filename}")

def main():
    url = input("Enter the URL of the web page: ")
    html_content = fetch_webpage_content(url)
    if html_content:
        text_list = parse_html_to_text_list(html_content)

        total_word_count = sum(len(s.split()) for s in text_list)
        print("Origin website has:", total_word_count, "words.")

        suggested_length = round_to_nearest_hundred(total_word_count // 3)
        print("Suggested summarization length is about:", suggested_length, "words.")

        try:
            user_input = input(f"Enter the word count threshold for summarization (suggested: {suggested_length}): ")
            user_threshold = int(user_input) if user_input.strip() else suggested_length
            print("The final length should be about", user_threshold)
        except ValueError:
            print("Invalid input. Please enter a number.")
            return

        merged_list = merge_strings(text_list, user_threshold)
        pdf_filename = 'output.pdf'
        created_pdf = create_pdf_file(merged_list, pdf_filename)
        print(f"PDF created: {created_pdf}")

        is_child = input("Is the summary for a child? (yes/no): ").strip().lower() == 'yes'
        summarization_model = 'facebook/bart-large-cnn'
        if is_child:
            summarization_model = 'child_friendly_model'  # assume there is a model

        cursor = evadb.connect().cursor()
        cursor.query("DROP TABLE IF EXISTS MyPDFs").df()
        cursor.query(f"LOAD PDF '{created_pdf}' INTO MyPDFs").df()
        cursor.query(f"""
            CREATE FUNCTION IF NOT EXISTS TextSummarizer
            TYPE HuggingFace
            TASK 'summarization'
            MODEL '{summarization_model}'
        """).df()
        string = """
            SELECT data, TextSummarizer(data)
            FROM MyPDFs
        """
        result = cursor.query(string).df()
        s = result[result.columns[1]]
        x_list = s.tolist()
        num = 0
        for s in x_list:
            words = s.split()
            num = num+len(words)
        merged_string = " ".join(x_list)
        summary_pdf_filename = "summarization_output.pdf"
        create_summary_pdf(merged_string, summary_pdf_filename)

if __name__ == "__main__":
    main()

from jinja2 import Environment, FileSystemLoader
import os

def generate_html_report(analysis_data: dict) -> str:
    template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
    env = Environment(loader=FileSystemLoader(template_dir), autoescape=True)
    template = env.get_template('report_template.html')
    ai_description_html = analysis_data.get("ai_description", "").replace("\n", "<br>")
    
    html_content = template.render(data=analysis_data, ai_description_html=ai_description_html)
    return html_content
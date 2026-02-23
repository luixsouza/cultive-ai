from jinja2 import Environment, FileSystemLoader
from datetime import datetime, timezone
import os

try:
    import markdown
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False

DEGRADATION_COLORS = {
    'Degradação Severa': '#a50026',
    'Degradação Moderada': '#d73027',
    'Pastagem Estressada': '#fdae61',
    'Pastagem Boa': '#66bd63',
    'Pastagem Excelente': '#1a9641',
    'Não Classificado': '#CCCCCC',
}


def get_health_label(ndvi_mean):
    if ndvi_mean is None:
        return 'N/A', '#94a3b8'
    if ndvi_mean >= 0.5:
        return 'Excelente', '#16a34a'
    if ndvi_mean >= 0.4:
        return 'Boa', '#22c55e'
    if ndvi_mean >= 0.3:
        return 'Moderada', '#d97706'
    if ndvi_mean >= 0.2:
        return 'Estressada', '#f97316'
    return 'Degradada', '#dc2626'


def render_ai_description(text: str) -> str:
    if not text:
        return ''
    if HAS_MARKDOWN:
        return markdown.markdown(text, extensions=['tables', 'nl2br'])
    # Fallback: basic line-break conversion (marked.js in template handles the rest client-side)
    return text


def generate_html_report(analysis_data: dict) -> str:
    template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
    env = Environment(loader=FileSystemLoader(template_dir), autoescape=True)
    template = env.get_template('report_template.html')

    # Use stored created_at if available (re-generation from DB), otherwise current time
    created_at = analysis_data.get('created_at')
    if created_at:
        generated_at = created_at.strftime('%d/%m/%Y às %H:%M UTC')
    else:
        generated_at = datetime.now(timezone.utc).strftime('%d/%m/%Y às %H:%M UTC')

    # Render AI description (markdown -> HTML server-side if library available,
    # otherwise raw text + client-side marked.js fallback in template)
    ai_description_html = render_ai_description(analysis_data.get("ai_description", ""))

    # Health label from NDVI mean
    ndvi_mean = None
    ndvi_stats = analysis_data.get("ndvi_stats") or {}
    if ndvi_stats:
        ndvi_mean = ndvi_stats.get("mean")
    health_label, health_color = get_health_label(ndvi_mean)

    # Add colors to degradation summary items
    degradation_with_colors = []
    for item in (analysis_data.get("degradation_summary") or []):
        degradation_with_colors.append({
            **item,
            'color': DEGRADATION_COLORS.get(item.get('class_name', ''), '#999'),
        })
    degradation_with_colors.sort(key=lambda x: x.get('percentage', 0), reverse=True)

    html_content = template.render(
        data=analysis_data,
        generated_at=generated_at,
        ai_description_html=ai_description_html,
        health_label=health_label,
        health_color=health_color,
        degradation_with_colors=degradation_with_colors,
    )
    return html_content

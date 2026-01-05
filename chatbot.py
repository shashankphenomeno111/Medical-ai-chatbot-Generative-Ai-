# Medical AI Chatbot - Core Engine V8
# Enhanced: Better content formatting, detailed treatment/prevention in bullet points

import re
import wikipedia
from typing import List, Optional, Dict
from dataclasses import dataclass, field
from ddgs import DDGS
from fpdf import FPDF


@dataclass
class MedicalInfo:
    """Structured medical information"""
    title: str
    summary: str
    symptoms: str
    causes: str
    treatment: str
    prevention: str
    when_to_see_doctor: str
    image_url: Optional[str]
    sources: List[str]
    is_emergency: bool = False
    full_content: str = ""
    related_conditions: List[str] = field(default_factory=list)


SYMPTOM_DATABASE = {
    "fever": ["COVID-19", "Influenza", "Malaria", "Dengue", "Typhoid", "Pneumonia"],
    "headache": ["Migraine", "Sinusitis", "Hypertension", "Meningitis"],
    "cough": ["COVID-19", "Bronchitis", "Pneumonia", "Asthma", "Tuberculosis"],
    "fatigue": ["Anemia", "Diabetes", "Thyroid Disorders", "Depression"],
    "chest pain": ["Heart Attack", "Angina", "GERD", "Pneumonia"],
    "shortness of breath": ["Asthma", "COPD", "Heart Failure", "Pneumonia"],
    "nausea": ["Gastritis", "Food Poisoning", "Migraine", "Appendicitis"],
    "joint pain": ["Arthritis", "Gout", "Lupus", "Injury"],
    "skin rash": ["Allergies", "Eczema", "Psoriasis", "Chickenpox"],
    "dizziness": ["Vertigo", "Anemia", "Low Blood Pressure", "Anxiety"],
    "muscle pain": ["Fibromyalgia", "Flu", "COVID-19", "Injury"],
    "sore throat": ["Strep Throat", "Cold", "COVID-19", "Tonsillitis"],
}


class MedicalPDF(FPDF):
    """Custom PDF generator"""
    
    def header(self):
        self.set_font('Helvetica', 'B', 20)
        self.set_text_color(0, 150, 136)
        self.cell(0, 15, 'Medical AI Encyclopedia', align='C', new_x="LMARGIN", new_y="NEXT")
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()} | Medical AI V8', align='C')
    
    def chapter_title(self, title):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(0, 100, 80)
        self.cell(0, 10, self._sanitize(title), new_x="LMARGIN", new_y="NEXT")
        self.ln(2)
    
    def _sanitize(self, text):
        if not text: return ""
        replacements = {'"': '"', '"': '"', ''': "'", ''': "'", '–': '-', '—': '-', '…': '...', '°': ' deg', '•': '-'}
        for old, new in replacements.items(): text = text.replace(old, new)
        return text.encode('ascii', 'ignore').decode('ascii')
    
    def chapter_body(self, body):
        self.set_font('Helvetica', '', 11)
        self.set_text_color(50, 50, 50)
        body = self._sanitize(body.replace('\n', ' ').strip())
        self.multi_cell(0, 6, body)
        self.ln(5)


def format_as_bullets(text: str) -> str:
    """Convert text to clean bullet points"""
    if not text or len(text) < 20:
        return text
    
    # Split by periods or newlines
    sentences = re.split(r'[.\n]', text)
    bullets = []
    
    for s in sentences:
        s = s.strip()
        if len(s) > 15:  # Only meaningful sentences
            # Clean up wiki markup
            s = re.sub(r'\[\[.*?\|', '', s)
            s = re.sub(r'\]\]|\{\{.*?\}\}', '', s)
            s = s.strip()
            if s and not s.startswith('•'):
                bullets.append(f"• {s}")
    
    return '\n'.join(bullets[:8])  # Max 8 bullet points


class MedicalChatbot:
    """V8 Medical AI - Enhanced Content and Formatting"""
    
    def __init__(self):
        self.search_history = []
        print("🔄 Loading Medical AI Chatbot V8...")
    
    def check_symptoms(self, symptoms: List[str]) -> List[Dict]:
        """Dynamic symptom checker"""
        condition_scores = {}
        processed = [s.lower().strip() for s in symptoms if s.strip()]
        if not processed: return []
        
        for s in processed:
            for db_s, conditions in SYMPTOM_DATABASE.items():
                if db_s in s or s in db_s:
                    for c in conditions: 
                        condition_scores[c] = condition_scores.get(c, 0) + 3
        
        # Web search for more conditions
        try:
            q = f"possible diseases for symptoms: {', '.join(processed)}"
            with DDGS() as ddgs:
                results = list(ddgs.text(q, max_results=5))
                for res in results:
                    text = (res.get('title', '') + " " + res.get('body', '')).lower()
                    conditions_list = ["Diabetes", "COVID-19", "Flu", "Cancer", "Anemia", "Heart Attack", 
                                       "Stroke", "Arthritis", "Migraine", "Pneumonia"]
                    for c in conditions_list:
                        if c.lower() in text:
                            condition_scores[c] = condition_scores.get(c, 0) + 1
        except: pass
            
        sorted_res = sorted(condition_scores.items(), key=lambda x: x[1], reverse=True)
        return [{"condition": k, "match": min(100, int((v / (len(processed) * 2)) * 100)), "symptoms_matched": v} 
                for k, v in sorted_res[:10]]

    def _search_medical_image(self, query: str) -> Optional[str]:
        """Robust image search"""
        for q in [f"{query} disease illustration", f"{query} medical diagram", f"{query} health", query]:
            try:
                with DDGS() as ddgs:
                    res = list(ddgs.images(q, max_results=10))
                    for img in res:
                        url = img.get('image', '')
                        if url and url.startswith('https://'):
                            if any(ext in url.lower() for ext in ['.jpg', '.jpeg', '.png']):
                                skip = ['logo', 'icon', 'button', 'flag', 'avatar', 'thumb']
                                if not any(s in url.lower() for s in skip):
                                    return url
            except: continue
        return None

    def _get_wikipedia_info(self, query: str) -> dict:
        info = {'title': query.title(), 'summary': '', 'full_content': '', 'image_url': None, 'related': []}
        try:
            wikipedia.set_lang("en")
            for qv in [f"{query} (disease)", f"{query} disease", query]:
                try:
                    res = wikipedia.search(qv, results=1)
                    if res:
                        p = wikipedia.page(res[0], auto_suggest=False)
                        info['title'] = p.title
                        info['summary'] = p.summary
                        info['full_content'] = p.content[:10000]
                        # Get related conditions from Wikipedia links - less strict filter
                        related_keywords = ['disease', 'syndrome', 'disorder', 'infection', 'condition', 'illness', 'fever', 'itis', 'osis', 'emia']
                        info['related'] = [l for l in p.links[:50] if any(t in l.lower() for t in related_keywords) and len(l) > 4][:5]
                        if p.images:
                            for img in p.images:
                                if any(e in img.lower() for e in ['.jpg', '.jpeg', '.png']):
                                    if not any(s in img.lower() for s in ['logo', 'icon', 'wikimedia', 'button']):
                                        info['image_url'] = img
                                        break
                        break
                except: continue
        except: pass
        return info

    def _get_detailed_web_info(self, query: str) -> dict:
        """Get detailed treatment and prevention info from web"""
        web = {'treatment': '', 'prevention': '', 'home_remedies': ''}
        
        try:
            with DDGS() as ddgs:
                # Treatment details
                r = list(ddgs.text(f"{query} treatment medicine cure therapy options", max_results=3))
                web['treatment'] = " ".join([res.get('body', '') for res in r])
                
                # Prevention details
                r = list(ddgs.text(f"{query} prevention tips how to prevent avoid", max_results=3))
                web['prevention'] = " ".join([res.get('body', '') for res in r])
                
                # Home remedies
                r = list(ddgs.text(f"{query} home remedies natural treatment", max_results=2))
                web['home_remedies'] = " ".join([res.get('body', '') for res in r])
        except: pass
        
        return web

    def _extract_section(self, content: str, section_names: List[str]) -> str:
        content_lower = content.lower()
        for name in section_names:
            match = re.search(rf'==\s*{name}\s*==', content_lower)
            if match:
                start = match.end()
                nxt = re.search(r'==\s*\w', content_lower[start:])
                end = start + nxt.start() if nxt else start + 1500
                txt = content[start:end].strip()
                txt = re.sub(r'===.*?===|\[\[.*?\||\]\]|\{\{.*?\}\}', '', txt)
                if len(txt) > 40: return txt[:1500]
        return ""

    def generate_pdf(self, info: MedicalInfo) -> bytes:
        """Generate PDF report"""
        pdf = MedicalPDF()
        pdf.add_page()
        pdf.set_font('Helvetica', 'B', 24)
        pdf.set_text_color(0, 80, 60)
        pdf.cell(0, 15, pdf._sanitize(info.title), new_x="LMARGIN", new_y="NEXT", align='C')
        pdf.ln(10)
        
        pdf.chapter_title('Overview')
        pdf.chapter_body(info.summary)
        pdf.chapter_title('Symptoms')
        pdf.chapter_body(info.symptoms.replace('•', '-'))
        pdf.chapter_title('Causes')
        pdf.chapter_body(info.causes.replace('•', '-'))
        pdf.chapter_title('Treatment')
        pdf.chapter_body(info.treatment.replace('•', '-'))
        pdf.chapter_title('Prevention')
        pdf.chapter_body(info.prevention.replace('•', '-'))
        
        return bytes(pdf.output())

    def chat(self, user_query: str) -> MedicalInfo:
        if user_query not in self.search_history:
            self.search_history.append(user_query)
        
        wiki = self._get_wikipedia_info(user_query)
        web = self._get_detailed_web_info(user_query)
        
        img = wiki['image_url'] or self._search_medical_image(user_query)
        content = wiki['full_content']
        
        # Extract with better formatting
        symp = self._extract_section(content, ['signs and symptoms', 'symptoms'])
        caus = self._extract_section(content, ['causes', 'cause', 'etiology', 'pathophysiology'])
        trea = self._extract_section(content, ['treatment', 'management', 'therapy', 'medication'])
        prev = self._extract_section(content, ['prevention', 'prophylaxis', 'risk reduction'])
        
        # Enhanced treatment with web info
        if web['treatment']:
            trea = trea + " " + web['treatment'] if trea else web['treatment']
        if web['home_remedies']:
            trea = trea + " Home remedies: " + web['home_remedies'][:400]
        
        # Enhanced prevention with web info
        if web['prevention']:
            prev = prev + " " + web['prevention'] if prev else web['prevention']
        
        # Format as bullet points for cleaner display
        symp_bullets = format_as_bullets(symp) if symp else "• Consult a doctor for accurate symptom assessment"
        caus_bullets = format_as_bullets(caus) if caus else "• Causes vary based on genetic and environmental factors"
        trea_bullets = format_as_bullets(trea) if trea else "• Consult a healthcare provider for treatment options"
        prev_bullets = format_as_bullets(prev) if prev else "• Maintain healthy lifestyle\n• Regular health checkups\n• Follow medical advice"
        
        is_em = any(t in (user_query + wiki['summary']).lower() for t in ['heart attack', 'stroke', 'emergency', 'poisoning'])
        
        # Fallback related conditions for common diseases
        fallback_related = {
            'diabetes': ['Heart Disease', 'Obesity', 'Kidney Disease', 'Neuropathy', 'Retinopathy'],
            'cancer': ['Leukemia', 'Lymphoma', 'Tumor', 'Chemotherapy', 'Radiation Therapy'],
            'heart attack': ['Stroke', 'Angina', 'Heart Failure', 'Hypertension', 'Coronary Artery Disease'],
            'stroke': ['Heart Attack', 'Hypertension', 'Brain Aneurysm', 'TIA', 'Paralysis'],
            'covid': ['Pneumonia', 'SARS', 'Influenza', 'Long COVID', 'Respiratory Infection'],
            'asthma': ['Bronchitis', 'COPD', 'Allergies', 'Pneumonia', 'Respiratory Infection'],
            'arthritis': ['Osteoporosis', 'Gout', 'Lupus', 'Rheumatism', 'Joint Pain'],
            'depression': ['Anxiety', 'Bipolar Disorder', 'PTSD', 'Insomnia', 'Stress'],
            'malaria': ['Dengue', 'Typhoid', 'Yellow Fever', 'Chikungunya', 'Zika'],
            'pneumonia': ['Bronchitis', 'COVID-19', 'Tuberculosis', 'Influenza', 'COPD'],
        }
        
        related = wiki['related']
        if not related:
            # Try to find fallback
            q_lower = user_query.lower()
            for key, conditions in fallback_related.items():
                if key in q_lower:
                    related = conditions
                    break
        
        return MedicalInfo(
            title=wiki['title'] or user_query.title(),
            summary=wiki['summary'] or f"Comprehensive information about {user_query}.",
            symptoms=symp_bullets,
            causes=caus_bullets,
            treatment=trea_bullets,
            prevention=prev_bullets,
            when_to_see_doctor="🚨 Seek medical help if symptoms are severe or persistent.",
            image_url=img, sources=["Wikipedia", "Web Search"],
            is_emergency=is_em, related_conditions=related
        )

    def get_search_history(self) -> List[str]: return self.search_history
    def clear_history(self): self.search_history = []


_chatbot_instance = None
def get_chatbot() -> MedicalChatbot:
    global _chatbot_instance
    if _chatbot_instance is None: _chatbot_instance = MedicalChatbot()
    return _chatbot_instance

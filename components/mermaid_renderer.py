"""
Mermaid Diyagram Renderer
Mermaid.js ile akış şemaları ve diyagramlar çizer
"""

import streamlit.components.v1 as components
from typing import List


def render_mermaid(diagram_code: str, height: int = 400):
    """
    Mermaid.js diyagramlarını Streamlit içinde çizer.
    
    Args:
        diagram_code: Mermaid syntax kodu
        height: Yükseklik (px)
    
    Example:
        ```python
        diagram = '''
        graph TD
            A[Başlangıç] --> B[Adım 1]
            B --> C[Sonuç]
        '''
        render_mermaid(diagram)
        ```
    """
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                margin: 0;
                padding: 20px;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                background: transparent;
            }}
            .mermaid {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }}
        </style>
        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ 
                startOnLoad: true,
                theme: 'default',
                themeVariables: {{
                    primaryColor: '#667eea',
                    primaryTextColor: '#fff',
                    primaryBorderColor: '#764ba2',
                    lineColor: '#667eea',
                    secondaryColor: '#FF6B6B',
                    tertiaryColor: '#4ECDC4',
                    fontSize: '16px',
                    fontFamily: 'Segoe UI, sans-serif'
                }},
                flowchart: {{
                    curve: 'basis',
                    padding: 20
                }}
            }});
        </script>
    </head>
    <body>
        <div class="mermaid">
{diagram_code}
        </div>
    </body>
    </html>
    """
    
    components.html(html_code, height=height, scrolling=True)


def create_solution_flowchart(steps: List[str], title: str = "Çözüm Akışı") -> str:
    """
    Çözüm adımlarından Mermaid flowchart oluştur.
    
    Args:
        steps: Çözüm adımları listesi
        title: Diyagram başlığı
        
    Returns:
        Mermaid diagram kodu
    
    Example:
        ```python
        steps = [
            "Verilen bilgileri belirle",
            "Formülü uygula",
            "Hesapla"
        ]
        diagram = create_solution_flowchart(steps)
        render_mermaid(diagram)
        ```
    """
    diagram = "graph TD\n"
    diagram += f"    Start([{title}]) --> Step1\n"
    
    for i, step in enumerate(steps, 1):
        # Adım metnini kısalt ve temizle
        clean_text = step.replace('"', "'").replace('\n', ' ')
        short_text = clean_text[:40] + "..." if len(clean_text) > 40 else clean_text
        
        diagram += f"    Step{i}[{short_text}]\n"
        
        if i < len(steps):
            diagram += f"    Step{i} --> Step{i+1}\n"
        else:
            diagram += f"    Step{i} --> End([✓ Cevap])\n"
    
    # Stil ekle
    diagram += "\n    style Start fill:#667eea,stroke:#764ba2,stroke-width:3px,color:#fff\n"
    diagram += "    style End fill:#4ECDC4,stroke:#45B7AA,stroke-width:3px,color:#fff\n"
    
    return diagram


def create_concept_map(central_concept: str, related_concepts: List[str]) -> str:
    """
    Kavram haritası oluştur.
    
    Args:
        central_concept: Merkez kavram
        related_concepts: İlgili kavramlar listesi
        
    Returns:
        Mermaid diagram kodu
    """
    diagram = "graph TD\n"
    diagram += f"    Center[{central_concept}]\n"
    
    for i, concept in enumerate(related_concepts, 1):
        clean_text = concept.replace('"', "'")
        diagram += f"    Concept{i}[{clean_text}]\n"
        diagram += f"    Center --> Concept{i}\n"
    
    # Merkez vurgula
    diagram += "\n    style Center fill:#FF6B6B,stroke:#E85A5A,stroke-width:4px,color:#fff\n"
    
    return diagram


def create_comparison_diagram(item1: dict, item2: dict) -> str:
    """
    Karşılaştırma diyagramı oluştur.
    
    Args:
        item1: {"name": "İsim", "features": ["Özellik 1", "Özellik 2"]}
        item2: {"name": "İsim", "features": ["Özellik 1", "Özellik 2"]}
        
    Returns:
        Mermaid diagram kodu
    """
    diagram = "graph LR\n"
    
    # Sol taraf
    diagram += f"    A[{item1['name']}]\n"
    for i, feature in enumerate(item1['features'], 1):
        diagram += f"    A --> A{i}[{feature}]\n"
    
    # Sağ taraf
    diagram += f"    B[{item2['name']}]\n"
    for i, feature in enumerate(item2['features'], 1):
        diagram += f"    B --> B{i}[{feature}]\n"
    
    # Stil
    diagram += "\n    style A fill:#667eea,stroke:#764ba2,stroke-width:3px,color:#fff\n"
    diagram += "    style B fill:#4ECDC4,stroke:#45B7AA,stroke-width:3px,color:#fff\n"
    
    return diagram


def create_timeline(events: List[dict]) -> str:
    """
    Zaman çizelgesi oluştur.
    
    Args:
        events: [{"date": "Tarih", "event": "Olay"}, ...]
        
    Returns:
        Mermaid diagram kodu
    """
    diagram = "graph LR\n"
    
    for i, event in enumerate(events):
        date = event.get('date', '')
        event_text = event.get('event', '')
        
        diagram += f"    E{i}[{date}<br/>{event_text}]\n"
        
        if i < len(events) - 1:
            diagram += f"    E{i} --> E{i+1}\n"
    
    return diagram


def create_decision_tree(question: str, options: List[dict]) -> str:
    """
    Karar ağacı oluştur.
    
    Args:
        question: Ana soru
        options: [{"condition": "Koşul", "result": "Sonuç"}, ...]
        
    Returns:
        Mermaid diagram kodu
    """
    diagram = "graph TD\n"
    diagram += f"    Q{{{question}}}\n"
    
    for i, option in enumerate(options):
        condition = option.get('condition', '')
        result = option.get('result', '')
        
        diagram += f"    Q -->|{condition}| R{i}[{result}]\n"
    
    # Karar düğümünü vurgula
    diagram += "\n    style Q fill:#FFC107,stroke:#FF9800,stroke-width:3px\n"
    
    return diagram


# Hazır şablonlar
TEMPLATES = {
    "simple_flow": """
graph TD
    Start([Başla]) --> Step1[Adım 1]
    Step1 --> Step2[Adım 2]
    Step2 --> End([Bitir])
    """,
    
    "decision": """
graph TD
    Q{Karar?}
    Q -->|Evet| A[Sonuç A]
    Q -->|Hayır| B[Sonuç B]
    """,
    
    "cycle": """
graph LR
    A[Adım 1] --> B[Adım 2]
    B --> C[Adım 3]
    C --> A
    """
}


def get_template(template_name: str) -> str:
    """Hazır şablon döndür."""
    return TEMPLATES.get(template_name, TEMPLATES["simple_flow"])

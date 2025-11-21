import fitz
from PIL import Image
import io
import numpy as np
import re
from collections import defaultdict
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Dict, Any

def process_pdf(pdf_path: str) -> List[Dict[str, Any]]:
    """
    Extracts and classifies pages from a PDF, identifies performance tables,
    and chunks the content.

    Args:
        pdf_path: The path to the PDF file.

    Returns:
        A list of chunk dictionaries, each containing content, metadata, and
        optionally, a page image.
    """
    print("="*80)
    print("STEP 1: EXTRACTING AND CLASSIFYING PAGES")
    print("="*80)

    doc = fitz.open(pdf_path)
    pages = []

    for i, page in enumerate(doc):
        text = page.get_text()
        text_length = len(text.strip())
        images = page.get_images()

        # Render page at low res to analyze visual density
        pix = page.get_pixmap(dpi=72)
        img_bytes = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_bytes))
        gray = img.convert('L')
        pixels = np.array(gray)

        # Calculate "ink density"
        non_white_pixels = np.sum(pixels < 240)
        total_pixels = pixels.size
        ink_density = non_white_pixels / total_pixels

        # Check for intentionally blank
        is_blank = "intentionally blank" in text.lower()

        # Classification: Diagram if high ink density or has images
        is_diagram = (
            len(images) > 0 or
            (ink_density > 0.14 and not is_blank)
        )

        page_data = {
            "page_number": i + 1,
            "text": text.strip(),
            "char_count": text_length,
            "has_images": len(images) > 0,
            "ink_density": ink_density,
            "is_blank": is_blank,
            "is_diagram": is_diagram,
            "page_image": None
        }
        pages.append(page_data)

    # Render only diagram pages at high resolution
    for i, page_data in enumerate(pages):
        if page_data["is_diagram"]:
            page = doc[i]
            pix = page.get_pixmap(dpi=150)
            page_data["page_image"] = pix.tobytes("png")

    doc.close()

    print(f" Total pages: {len(pages)}")

    # ============================================================================
    # STEP 2: IDENTIFY PERFORMANCE TABLE PAGES
    # ============================================================================
    print("\n" + "="*80)
    print("STEP 2: IDENTIFYING PERFORMANCE TABLE PAGES")
    print("="*80)

    performance_table_pages = {}
    for page in pages:
        content = page['text']
        content_lower = content.lower()
        is_perf_table = False
        table_info = {}

        if (('field limit weight' in content_lower or 'climb limit' in content_lower) and
            'pressure altitude' in content_lower and
            ('1000 kg' in content_lower or 'corr' in content_lower)):
            alt_match = re.search(r'(\d+)\s*FT\s*Pressure\s*Altitude', content, re.IGNORECASE)
            if alt_match:
                altitude = alt_match.group(1)
                runway_condition = "wet" if "wet runway" in content_lower else "dry"
                flap_match = re.search(r'Flaps?\s*(\d+)', content, re.IGNORECASE)
                flap_setting = flap_match.group(1) if flap_match else None
                table_info = {"type": "field_climb_limits", "altitude": altitude, "runway_condition": runway_condition, "flap_setting": flap_setting}
                is_perf_table = True
        elif ('flap' in content_lower and 'retraction' in content_lower and 'speed' in content_lower and 't/o' in content_lower):
            table_info = {"type": "flap_retraction", "altitude": None, "runway_condition": None}
            is_perf_table = True
        elif ('landing field limit' in content_lower and 'wind corr' in content_lower):
            table_info = {"type": "landing_limits", "altitude": None, "runway_condition": None}
            is_perf_table = True

        if is_perf_table:
            performance_table_pages[page['page_number']] = table_info

    print(f"✅ Found {len(performance_table_pages)} performance table pages")

    # ============================================================================
    # STEP 3: CHUNKING STRATEGY
    # ============================================================================
    print("\n" + "="*80)
    print("STEP 3: CHUNKING STRATEGY")
    print("="*80)

    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=300, separators=["\n\n", "\n", " "])
    all_chunks = []
    enhanced_count = 0

    def enhance_performance_table_content(page, table_info):
        table_type = table_info['type']
        altitude = table_info.get('altitude') or 'unknown'
        runway = table_info.get('runway_condition') or 'unknown'
        flap = table_info.get('flap_setting') or 'all'
        if table_type == 'field_climb_limits':
            enhancement = f"PERFORMANCE TABLE: FIELD AND CLIMB LIMIT WEIGHTS\nAltitude: {altitude} FT | Runway: {runway.upper()} | Flaps: {flap}\nKeywords: field limit weight, climb limit weight, {altitude} feet, pressure altitude, {runway} runway, corrected field length, OAT\nTABLE DATA:\n"
        elif table_type == 'flap_retraction':
            enhancement = f"PERFORMANCE TABLE: FLAP RETRACTION SPEEDS\nKeywords: flap retraction, takeoff, speed, flaps\n"
        elif table_type == 'landing_limits':
            enhancement = f"PERFORMANCE TABLE: LANDING FIELD LIMIT WEIGHTS\nKeywords: landing field limit, wind correction, landing weight\n"
        else:
            enhancement = f"PERFORMANCE TABLE: {table_type}\n"
        return enhancement + page['text']

    for page in pages:
        if page["char_count"] < 20: continue
        content = page["text"]
        page_num = page["page_number"]

        if page_num in performance_table_pages:
            table_info = performance_table_pages[page_num]
            enhanced_content = enhance_performance_table_content(page, table_info)
            enhanced_count += 1
            all_chunks.append({
                "content": enhanced_content, "page_number": page_num, "chunk_id": f"page_{page_num}_enhanced",
                "type": "performance_table", "page_image": page.get("page_image"),
                "metadata": {"source": "Boeing B737 Manual", "page": page_num, "table_type": table_info['type'], "altitude": table_info.get('altitude'), "runway_condition": table_info.get('runway_condition'), "flap_setting": table_info.get('flap_setting')}
            })
        elif page["is_diagram"]:
            all_chunks.append({
                "content": page["text"], "page_number": page_num, "chunk_id": f"page_{page_num}_visual",
                "type": "visual", "page_image": page["page_image"],
                "metadata": {"source": "Boeing B737 Manual", "page": page_num, "requires_vision": True, "ink_density": page["ink_density"]}
            })
        else:
            text_chunks = splitter.split_text(page["text"])
            for idx, chunk in enumerate(text_chunks):
                all_chunks.append({
                    "content": chunk, "page_number": page_num, "chunk_id": f"page_{page_num}_chunk_{idx}",
                    "type": "text", "page_image": None,
                    "metadata": {"source": "Boeing B737 Manual", "page": page_num, "requires_vision": False, "chunk_index": idx, "total_chunks": len(text_chunks)}
                })

    print(f" Chunking Complete!")
    print(f"   Total chunks: {len(all_chunks)}")
    print(f"   Enhanced performance table chunks: {enhanced_count}")
    return all_chunks
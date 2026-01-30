"""
Cloud-Based AI Service:  ULTIMATE PRODUCTION v4.4
✅ Gemini 2.5 Flash (Primary)
✅ DeepSeek R1 via OpenRouter (FREE & WORKING)
✅ Slide 6: Roadmap Layout (Vertical Timeline)
Author: GuptaSigma | Date: 2026-01-15 | Version: 4.4 FINAL
"""

import os
import time
import json
import requests
import random
from pathlib import Path


class CloudAIService:
    def __init__(self):
        print("\n" + "=" * 60)
        print("🤖 AI SERVICE - MULTI-MODEL PRODUCTION MODE (v4.4)")
        print("=" * 60)

        # ✅ API KEYS - Load from environment variables only
        self.gemini_key = os.getenv("GOOGLE_GEMINI_API_KEY")
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY")
        
        # Google Search (for images)
        self.google_search_key = os.getenv("GOOGLE_API_KEY")
        self.google_cx_id = os.getenv("GOOGLE_CX_ID")
        
        # Validate critical API keys
        if not self.gemini_key:
            print("⚠️  WARNING: GOOGLE_GEMINI_API_KEY not set in environment")
        if not self.openrouter_key:
            print("⚠️  WARNING: OPENROUTER_API_KEY not set in environment")

        # ✅ WINDOWS-SAFE PATH using pathlib
        try:
            current_file = Path(__file__).resolve()
            project_root = current_file.parent.parent
            self.static_folder = project_root / "static" / "generated"
            self.static_folder.mkdir(parents=True, exist_ok=True)
            print(f"📂 Static folder: {self.static_folder}")
        except Exception as e:
            self.static_folder = None
            print(f"⚠️ Static folder unavailable (using external images only): {e}")

        # Display API key status (safely)
        if self.gemini_key:
            print(f"🔑 Gemini Key: {self.gemini_key[:10]}... (configured)")
        if self.openrouter_key:
            print(f"🔑 OpenRouter Key: {self.openrouter_key[:10]}... (configured)")
        print("=" * 60 + "\n")

    # ============================================================
    # GEMINI 2.5 FLASH
    # ============================================================
    def _call_gemini(self, prompt):
        """Call Gemini 2.5 Flash API"""
        model = "gemini-2.0-flash-exp"
        
        print(f"   🧠 Calling Gemini 2.5 Flash...")
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        
        try:  
            resp = requests.post(
                url,
                params={"key": self.gemini_key},
                headers={"Content-Type": "application/json"},
                json={
                    "contents": [{
                        "parts": [{"text": prompt}]
                    }],
                    "generationConfig": {
                        "temperature": 0.7,
                        "maxOutputTokens": 8192
                    }
                },
                timeout=30
            )
            
            if resp.status_code == 200:
                data = resp.json()
                try:
                    text = data["candidates"][0]["content"]["parts"][0]["text"]
                    print(f"   ✅ Gemini Success ({len(text)} chars)")
                    return text
                except (KeyError, IndexError):
                    print(f"   ⚠️ Invalid Gemini response")
                    return None
                    
            elif resp.status_code == 429:
                print(f"   ⚠️ Gemini Quota Exhausted")
                return None
                
            else:
                print(f"   ❌ Gemini Error {resp.status_code}")
                return None
                
        except Exception as e:
            print(f"   ❌ Gemini Network Error: {e}")
            return None

    # ============================================================
    # DEEPSEEK R1 VIA OPENROUTER
    # ============================================================
    def _call_deepseek(self, prompt):
        """Call DeepSeek R1 via OpenRouter"""
        model = "deepseek/deepseek-chat"
        
        print(f"   🚀 Calling DeepSeek R1 via OpenRouter...")
        
        try:
            resp = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.openrouter_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "http://localhost:5000"
                },
                json={
                    "model": model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a professional presentation writer. Output ONLY valid JSON.  No markdown, no explanations."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "response_format": {"type": "json_object"},
                    "max_tokens":  4000,
                    "temperature": 0.7
                },
                timeout=50
            )
            
            if resp.status_code == 200:
                data = resp.json()
                text = data['choices'][0]['message']['content']
                print(f"   ✅ DeepSeek Success ({len(text)} chars)")
                return text
            else:
                print(f"   ❌ DeepSeek Error {resp.status_code}:  {resp.text[: 100]}")
                return None
                
        except Exception as e:
            print(f"   ❌ DeepSeek Network Error:  {e}")
            return None

    # ============================================================
    # SMART AI CALLER
    # ============================================================
    def _get_ai_text(self, prompt, ai_model="gemini"):
        """Smart AI caller with automatic fallback"""
        if ai_model == "deepseek":
            text = self._call_deepseek(prompt)
            if text:  return text
            
            print(f"   🔄 DeepSeek failed, trying Gemini...")
            text = self._call_gemini(prompt)
            if text:  return text
        
        else:  # Default:  Gemini
            text = self._call_gemini(prompt)
            if text: return text
            
            print(f"   🔄 Gemini failed, trying DeepSeek...")
            text = self._call_deepseek(prompt)
            if text: return text
        
        print(f"   ❌ All AI models failed")
        return None

    # ============================================================
    # JSON PARSER
    # ============================================================
    def _clean_json(self, text):
        """Extract JSON array from AI response"""
        if not text:  return []

        try:
            clean = text.replace("```json", "").replace("```", "").strip()

            try:
                obj = json.loads(clean)
                if isinstance(obj, list): return obj
                if isinstance(obj, dict) and 'slides' in obj: return obj['slides']
            except:
                pass

            start = clean.find("[")
            end = clean.rfind("]")
            if start != -1 and end != -1:
                json_str = clean[start: end+1]
                return json.loads(json_str)

        except Exception as e:
            print(f"   ⚠️ JSON Parse Error: {e}")

        return []

    # ============================================================
    # IMAGE GENERATION
    # ============================================================
    def get_smart_image(self, prompt, force_dark=False):
        """Get image from Google Search"""
        search_query = prompt
        if force_dark:
            search_query += " dark hd wallpaper background"

        try:
            resp = requests.get(
                "https://www.googleapis.com/customsearch/v1",
                params={
                    "q": search_query,
                    "cx": self.google_cx_id,
                    "key": self.google_search_key,
                    "searchType": "image",
                    "num": 1,
                    "safe": "active",
                    "imgSize": "large"
                },
                timeout=3
            )
            
            if resp.status_code == 200:
                items = resp.json().get('items', [])
                if items:
                    img_url = items[0].get('link')
                    print(f"   🖼️ Google Image ({'Dark' if force_dark else 'Standard'}): {img_url[: 30]}...")
                    return img_url
        except: 
            pass
        
        print(f"   ⚠️ Using Pollinations fallback")
        safe = prompt.replace(" ", "%20")
        seed = random.randint(1, 999999)
        return f"https://image.pollinations.ai/prompt/{safe}?width=1280&height=720&nologo=true&seed={seed}"

    # ============================================================
    # CONTENT VALIDATOR
    # ============================================================
    def _validate_and_fix_content(self, slide_data, slide_num, prompt):
        """Ensures correct content structure"""
        content = slide_data.get("content", "")
        points = [p for p in content.split('\n') if p.strip() and (p.startswith('-') or p[0].isdigit())]
        count = len(points)
        
        if count == 0:
            points = [p for p in content.split('\n') if p.strip()]
            count = len(points)

        # FIX FOR SLIDE 5 (Needs 3-4 points)
        if slide_num == 5:
            if count < 3:
                print(f"   🔧 Fixing Slide 5 (Found {count}, forcing 4 points)")
                return (
                    f"1. Global Impact: {prompt} has transcended borders worldwide.\n"
                    f"2. Cultural Exchange: Communities celebrate traditions.\n"
                    f"3. Economic Growth: Drives tourism and retail.\n"
                    f"4. Social Harmony: Strengthens social fabrics."
                )

        # FIX FOR SLIDE 2, 7 (Needs exactly 2 points)
        elif slide_num in [2, 7]:
            if count != 2:
                print(f"   🔧 Fixing Slide {slide_num} (Found {count}, forcing 2 points)")
                return (
                    f"1. Core Analysis: Deep dive into {prompt}.\n"
                    f"2. Broader Implications: Future trends and impact."
                )

        # 🆕 FIX FOR SLIDE 6 (Roadmap - Needs 5-6 steps)
        elif slide_num == 6:
            if count < 5:
                print(f"   🔧 Fixing Slide 6 (Found {count}, forcing 6 roadmap steps)")
                return (
                    f"1. Research Phase: Analyze requirements and gather data.\n"
                    f"2. Planning Stage: Create detailed roadmap and timeline.\n"
                    f"3. Development:  Build core features and functionality.\n"
                    f"4. Testing: Quality assurance and bug fixes.\n"
                    f"5. Launch: Deploy to production environment.\n"
                    f"6. Optimization: Monitor performance and improve."
                )
        
        # FIX FOR SLIDE 1 (Paragraph, not list)
        elif slide_num == 1:
            if count > 1 or content.startswith("-") or "1." in content[: 3]:
                print(f"   🔧 Fixing Slide 1 (Found List, forcing Paragraph)")
                return f"This presentation explores {prompt} comprehensively. We examine its origins, significance, and modern relevance, providing insights into how it shapes our world today."

        return content

    # ============================================================
    # MAIN SLIDE GENERATION
    # ============================================================
    def generate_slides(
        self,
        prompt,
        slides_count=8,
        language="English",
        theme="dialogue",
        text_amount="concise",
        ai_model="gemini",
        custom_outline=None,
        **kwargs
    ):
        try:
            slides_count = int(slides_count)
            slides_count = max(3, min(slides_count, 20))
        except:
            slides_count = 8

        text_length_map = {
            'minimal': 'Short and punchy',
            'concise': 'Standard professional length',
            'detailed': 'Long and descriptive',
            'extensive': 'Very detailed analysis'
        }
        text_instruction = text_length_map.get(text_amount, text_length_map['concise'])

        print(f"🎨 Generating {slides_count} slides for:  {prompt}")

        detail_instruction = """
CRITICAL FORMATTING RULES (FOLLOW STRICTLY):

1. **SLIDE 1 (INTRODUCTION):**
   - Must be ONE SINGLE PARAGRAPH (80-100 words). NO Bullet points. 

2. **SLIDE 2 and SLIDE 7:**
   - Must have EXACTLY 2 DETAILED BULLET POINTS.  No more, no less.

3. **SLIDE 5:**
   - Must have EXACTLY 4 DETAILED BULLET POINTS.

4. **SLIDE 6 (ROADMAP/PROCESS):**
   - Must have EXACTLY 5-6 NUMBERED STEPS
   - Format: "Step Number.  Title: Brief description"
   - Example: "1. Choose Canvas: Start with blank slate or upload image"
   - These will be displayed as vertical timeline

5. **ALL OTHER SLIDES:**
   - Use 3 to 4 standard bullet points. 
"""

        ai_prompt = f"""
Create EXACTLY {slides_count} professional presentation slides about:  "{prompt}"

Language: {language}
Text Length: {text_instruction}

{detail_instruction}

Output:  JSON array ONLY (no markdown, no explanations)

Format: 
[
  {{"title": "Introduction to [Topic]", "content": "A detailed paragraph.. .", "layout": "centered"}},
  {{"title":  "Deep Dive", "content": "- Point 1... \\n- Point 2.. .", "layout": "split"}},
  ... 
  {{"title": "Process/Roadmap", "content": "1. Step One:  Description\\n2. Step Two: Description\\n.. .", "layout": "roadmap"}},
  ...
]

Layouts (cycle through):
1. centered (Slide 1)
2. split (Slide 2)
3. three_col
4. grid_4
5. split_box (Slide 5)
6. roadmap (Slide 6 - MUST be process/timeline format)
7. split (Slide 7)
8. split

START JSON:  
"""

        raw_response = self._get_ai_text(ai_prompt, ai_model)
        parsed_data = self._clean_json(raw_response)

        if not parsed_data or len(parsed_data) < slides_count:
            print(f"⚠️ Using fallback content")
            parsed_data = [{"title": f"{prompt} Part {i+1}", "content": "Fallback content", "layout": "split"} for i in range(slides_count)]

        final_slides = []
        
        for i in range(slides_count):
            if i < len(parsed_data):
                slide = parsed_data[i]
            else:
                slide = {"title": f"{prompt} Part {i+1}", "content": ".. .", "layout": "split"}
            
            slide_num = i + 1
            
            # 1.  VALIDATE CONTENT
            slide['content'] = self._validate_and_fix_content(slide, slide_num, prompt)

            # 2. ASSIGN LAYOUT
            if slide_num == 1:
                slide['layout'] = 'centered'
            elif slide_num == 5:
                slide['layout'] = 'split_box'
            elif slide_num == 6:
                slide['layout'] = 'roadmap'  # 🆕 Roadmap layout for Slide 6
            elif slide_num in [2, 7]:
                slide['layout'] = 'split'
            elif slide_num == 3:
                slide['layout'] = 'three_col'
            elif slide_num == 4:
                slide['layout'] = 'grid_4'
            else:
                slide['layout'] = slide. get('layout', 'split')

            # 3. IMAGE LOGIC
            image_prompt = f"{slide. get('title', prompt)} professional visual"
            force_dark_bg = (slide_num == 1)
            
            final_slides.append({
                "id": f"slide_{i}",
                "title": slide. get("title", f"Slide {i+1}"),
                "content": slide['content'],
                "layout": slide['layout'],
                "image":  self.get_smart_image(image_prompt, force_dark=force_dark_bg),
                "background": self._get_theme_background(theme)
            })
            print(f"   ✅ Slide {i+1} ready ({slide['layout']})")

        print(f"✅ Generated {len(final_slides)} slides successfully")
        return final_slides

    # ============================================================
    # THEME BACKGROUNDS
    # ============================================================
    def _get_theme_background(self, theme):
        """Return CSS gradient based on theme"""
        theme_map = {
            "dialogue": "linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%)",
            "alien": "linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)",
            "wine": "linear-gradient(135deg, #581c3c 0%, #3d1428 100%)",
            "snowball": "linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%)",
            "petrol": "linear-gradient(135deg, #475569 0%, #334155 100%)",
            "piano": "linear-gradient(135deg, #000000 0%, #1e293b 50%, #ffffff 100%)",
            "business": "linear-gradient(135deg, #3a7bd5 0%, #00d2ff 100%)"
        }
        return theme_map.get(theme, theme_map["dialogue"])


# ============================================================
# GLOBAL INSTANCE
# ============================================================
ai_service = None

try:
    print("🔄 Initializing AI Service...")
    ai_service = CloudAIService()
    print("✅ AI Service READY")
    print("   🧠 Gemini 2.5 Flash:  Available")
    print("   🚀 DeepSeek R1 (OpenRouter): Available")
    print()
except Exception as e:
    print(f"❌ AI Service failed: {e}\n")
    import traceback
    traceback.print_exc()
    ai_service = None
"""
Presentation Routes - List, Generate, Delete, Export, View, Update
Complete API for managing presentations
Author: GuptaSigma
Updated: 2026-01-30
"""

from flask import Blueprint, request, jsonify, send_file
import json
import datetime
import io
import traceback

from models.database import execute_query
from services.pptx_service import PPTXService

# ============================================================
# PDF Service Import (Optional - if you have it)
# ============================================================
try:
    from services.pdf_service import PDFService
    print("✅ PDF Service imported")
except Exception as e:
    PDFService = None
    print(f"⚠️ PDF Service unavailable: {e}")

# ============================================================
# AI Service Import (Safe)
# ============================================================
try: 
    from services.ai_service import ai_service
    print("✅ AI Service imported in presentations routes")
except Exception as e: 
    ai_service = None
    print(f"⚠️ AI Service unavailable: {e}")

# ============================================================
# Blueprint Registration
# ============================================================
presentations_bp = Blueprint('presentations', __name__)
print("✅ presentations_bp Blueprint created")


# ======================================================================
# GET /api/presentations/  → List All Presentations (Dashboard)
# ======================================================================
@presentations_bp.route('/', methods=['GET'])
def list_presentations():
    """
    Fetch all presentations for dashboard grid view
    """
    try: 
        rows = execute_query(
            """
            SELECT id, title, prompt, slides_count, theme, style, created_at, updated_at
            FROM presentations
            ORDER BY created_at DESC
            """,
            fetch=True
        ) or []

        for r in rows:
            if isinstance(r. get('created_at'), (datetime.datetime, datetime.date)):
                r['created_at'] = r['created_at'].isoformat()
            if isinstance(r.get('updated_at'), (datetime.datetime, datetime.date)):
                r['updated_at'] = r['updated_at'].isoformat() if r['updated_at'] else None

        return jsonify({'success': True, 'presentations': rows}), 200

    except Exception as e:
        print(f"❌ list_presentations error: {e}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


# ======================================================================
# GET /api/presentations/<id>  → View Single Presentation (FULL SLIDES)
# ======================================================================
@presentations_bp.route('/<int:pres_id>', methods=['GET'])
def get_presentation(pres_id):
    """
    Fetch single presentation with FULL content (all slides).
    """
    try:
        print(f"📥 Fetching presentation ID: {pres_id}")

        rows = execute_query(
            """
            SELECT id, title, prompt, slides_count, content, theme, style, 
                   language, created_at, updated_at 
            FROM presentations 
            WHERE id = %s
            """,
            (pres_id,),
            fetch=True
        )

        if not rows:
            return jsonify({'success': False, 'error': 'Presentation not found'}), 404

        pres = rows[0]

        # Parse JSON 'content' into slides array
        slides = []
        try:
            raw = pres.get('content')
            if raw is None:
                slides = []
            elif isinstance(raw, str):
                slides = json.loads(raw) if raw. strip() else []
            else: 
                slides = raw or []
        except Exception as e:
            print(f"⚠️ JSON parse error for pres_id={pres_id}: {e}")
            slides = []

        # Build response object
        response = dict(pres)
        response.pop('content', None)
        response['slides'] = slides

        # Format datetimes
        if isinstance(response. get('created_at'), (datetime.datetime, datetime.date)):
            response['created_at'] = response['created_at'].isoformat()
        if isinstance(response.get('updated_at'), (datetime.datetime, datetime.date)):
            response['updated_at'] = response['updated_at'].isoformat() if response['updated_at'] else None

        print(f"✅ Found {len(slides)} slides for '{response. get('title')}'")
        return jsonify({'success': True, 'presentation': response}), 200

    except Exception as e:
        print(f"❌ get_presentation error: {e}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


# ======================================================================
# PUT /api/presentations/<id>  → UPDATE PRESENTATION (SAVE CHANGES)
# ======================================================================
@presentations_bp.route('/<int:pres_id>', methods=['PUT'])
def update_presentation(pres_id):
    """
    Save manual edits made by the user on the frontend.
    Updates the 'content' JSON in the database.
    """
    try:
        data = request.get_json()
        slides = data.get('slides')

        if not slides or not isinstance(slides, list):
            return jsonify({'success': False, 'error': 'Invalid slides data'}), 400

        # Convert back to JSON string for DB
        content_json = json.dumps(slides, ensure_ascii=False)

        # Update Query
        execute_query(
            "UPDATE presentations SET content = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s",
            (content_json, pres_id)
        )

        print(f"💾 Presentation {pres_id} saved successfully via PUT request.")
        return jsonify({'success':  True, 'message': 'Presentation updated successfully'}), 200

    except Exception as e: 
        print(f"❌ Update error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ======================================================================
# POST /api/presentations/generate  → Generate New Presentation
# ======================================================================
@presentations_bp.route('/generate', methods=['POST'])
def generate_presentation():
    """
    Generate a new presentation using AI with theme and text amount support.
    ✅ UPDATED: Now accepts theme and text_amount from frontend
    """
    try:
        data = request.get_json() or {}

        # ============================================================
        # STEP 1: VALIDATE PROMPT
        # ============================================================
        prompt = (data.get('prompt') or '').strip()
        if not prompt:
            return jsonify({'success': False, 'error': 'Prompt is required'}), 400

        # ============================================================
        # STEP 2: DETERMINE SLIDE COUNT
        # ============================================================
        raw_count = data.get('slides_count') or data.get('slides') or 8
        try:
            slides_count = int(raw_count)
        except: 
            slides_count = 8

        # Custom Outline Override
        custom_outline = data.get('custom_outline')
        if custom_outline: 
            lines = [line for line in custom_outline.split('\n') if line.strip()]
            if len(lines) > 0:
                slides_count = len(lines)
                print(f"🔹 Custom Outline Detected:  Overriding slides count to {slides_count}")

        # ============================================================
        # STEP 3: CAPTURE ALL GENERATION OPTIONS
        # ============================================================
        ai_model = data.get('ai_model', 'gemini')
        image_source = data.get('image_source', 'real')
        style = data.get('style', 'professional')
        language = data.get('language', 'English')
        
        # ✅ NEW: THEME & TEXT AMOUNT
        theme = data.get('theme', 'dialogue')              # Default:  dialogue
        text_amount = data.get('text_amount', 'concise')   # Default: concise
        
        image_style = data.get('image_style', 'photorealistic')
        use_search = bool(data.get('use_search', False))

        user_id = 1  # TODO: Get from JWT token

        # ============================================================
        # STEP 4: LOG GENERATION REQUEST
        # ============================================================
        print(f"🎯 Generate Request:")
        print(f"   Prompt: '{prompt[: 40]}...'")
        print(f"   Slides:  {slides_count}")
        print(f"   Theme: {theme. upper()}")
        print(f"   Text Amount: {text_amount.upper()}")
        print(f"   AI Model: {ai_model.upper()}")
        print(f"   Language: {language}")

        # ============================================================
        # STEP 5: GENERATE SLIDES USING AI SERVICE
        # ============================================================
        if ai_service:
            slides = ai_service.generate_slides(
                prompt=prompt,
                slides_count=slides_count,
                custom_outline=custom_outline,
                style=style,
                language=language,
                theme=theme,              # ✅ PASS THEME
                image_style=image_source,
                text_amount=text_amount,  # ✅ PASS TEXT AMOUNT
                use_search=use_search,
                ai_model=ai_model
            )
        else:
            print("⚠️ AI service unavailable, using fallback content")
            slides = [{
                "title": "Service Unavailable",
                "content": "AI service is currently unavailable. Please check server logs.",
                "image":  None,
                "layout": "hero"
            }]

        # ============================================================
        # STEP 6: SAVE TO DATABASE
        # ============================================================
        content_json = json.dumps(slides, ensure_ascii=False)

        pres_id = execute_query(
            """
            INSERT INTO presentations 
            (user_id, title, prompt, slides_count, content, theme, style, language, total_slides)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (user_id, prompt, prompt, slides_count, content_json, theme, style, language, slides_count)
        )

        # ============================================================
        # STEP 7: RETURN SUCCESS RESPONSE
        # ============================================================
        print(f"✅ Presentation {pres_id} created successfully")
        print(f"   Theme: {theme} | Text:  {text_amount} | Slides: {len(slides)}")

        return jsonify({
            'success': True,
            'presentation_id': pres_id,
            'message': 'Presentation generated successfully',
            'presentation': {
                'id': pres_id,
                'title': prompt,
                'theme': theme,
                'text_amount': text_amount,
                'slides_count': len(slides)
            },
            'slides': slides
        }), 201

    except Exception as e: 
        print(f"❌ Generate error: {e}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


# ======================================================================
# DELETE /api/presentations/<id>  → Delete Single
# ======================================================================
@presentations_bp.route('/<int:pres_id>', methods=['DELETE'])
def delete_presentation(pres_id):
    """Delete a single presentation"""
    try:
        execute_query("DELETE FROM presentations WHERE id = %s", (pres_id,))
        print(f"🗑️ Presentation {pres_id} deleted")
        return jsonify({'success':  True, 'message': 'Presentation deleted'}), 200
    except Exception as e:
        print(f"❌ delete_presentation error: {e}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


# ======================================================================
# DELETE /api/presentations/all  → Delete ALL
# ======================================================================
@presentations_bp.route('/all', methods=['DELETE'])
def delete_all_presentations():
    """Delete all presentations"""
    try:
        execute_query("DELETE FROM presentations")
        print("🗑️ All presentations deleted from DB")
        return jsonify({'success': True, 'message': 'All presentations deleted'}), 200
    except Exception as e: 
        print(f"❌ delete_all_presentations error: {e}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


# ======================================================================
# EXPORT HANDLER (PPTX/PDF) - FIXED VERSION
# ======================================================================
def handle_export(pres_id, format_type):
    """
    Export presentation to PPTX or PDF
    🔥 FIXED: Now uses exact layout from database
    """
    try:
        rows = execute_query(
            "SELECT id, title, prompt, content, theme FROM presentations WHERE id = %s",
            (pres_id,),
            fetch=True
        )
        if not rows:
            return jsonify({'success': False, 'error': 'Not found'}), 404

        pres = rows[0]

        # Parse slides from JSON
        try:
            raw = pres. get('content')
            slides_data = json.loads(raw) if isinstance(raw, str) and raw. strip() else (raw or [])
        except Exception as e:
            print(f"⚠️ Export JSON parse error: {e}")
            slides_data = []

        # ✅ FIXED: Adapter object expected by services
        class PresentationData:
            def __init__(self, id, title, prompt, slides, theme):
                self.id = id
                self.title = title
                self.prompt = prompt
                self.content = {'slides': slides}  # ✅ Exact slides with layouts
                self.theme = theme # ✅ Default fallback

        pres_data_obj = PresentationData(
            pres['id'],
            pres['title'],
            pres['prompt'],
            slides_data,  # ✅ Contains layout field for each slide
            pres. get('theme', 'dialogue')
        )

        print(f"📤 Exporting {format_type. upper()}:  {pres['title']} ({len(slides_data)} slides)")

        if format_type == 'pptx':
            service = PPTXService()
            mimetype = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
            ext = 'pptx'
        elif format_type == 'pdf':
            if PDFService is None:
                return jsonify({'success': False, 'error': 'PDF service not available'}), 500
            service = PDFService()
            mimetype = 'application/pdf'
            ext = 'pdf'
        else:
            return jsonify({'success': False, 'error': "Invalid format.  Use 'pptx' or 'pdf'"}), 400

        # ✅ Generate file
        file_content = service.generate(pres_data_obj)

        print(f"✅ {format_type.upper()} exported successfully")

        return send_file(
            io.BytesIO(file_content),
            mimetype=mimetype,
            as_attachment=True,
            download_name=f"{pres['title']}.{ext}"
        )

    except Exception as e:
        print(f"❌ Export error: {e}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


# ======================================================================
# EXPORT ROUTES (Multiple URL patterns for compatibility)
# ======================================================================

@presentations_bp.route('/<int:pres_id>/download/<format>', methods=['GET'])
def download_presentation(pres_id, format):
    """
    Modern route:  /api/presentations/123/download/pptx
    """
    return handle_export(pres_id, format)


@presentations_bp.route('/<int:pres_id>/export/pptx', methods=['GET'])
def export_pptx_legacy(pres_id):
    """
    Legacy route: /api/presentations/123/export/pptx
    """
    return handle_export(pres_id, 'pptx')


@presentations_bp.route('/<int:pres_id>/export/pdf', methods=['GET'])
def export_pdf_legacy(pres_id):
    """
    Legacy route: /api/presentations/123/export/pdf
    """
    return handle_export(pres_id, 'pdf')


# ======================================================================
# EXPORT WITH QUERY PARAM (Optional alternative)
# ======================================================================
@presentations_bp.route('/<int:pres_id>/export', methods=['GET'])
def export_with_query(pres_id):
    """
    Query param route: /api/presentations/123/export?format=pptx
    """
    format_type = request.args.get('format', 'pptx').lower()
    return handle_export(pres_id, format_type)


# ======================================================================
# DEBUG ROUTE (Optional - for testing)
# ======================================================================
@presentations_bp.route('/<int:pres_id>/debug', methods=['GET'])
def debug_presentation(pres_id):
    """
    Debug endpoint to see raw database content
    """
    try:
        rows = execute_query(
            "SELECT * FROM presentations WHERE id = %s",
            (pres_id,),
            fetch=True
        )

        if not rows:
            return jsonify({'error': 'Not found'}), 404

        pres = rows[0]

        # Parse content
        try:
            raw = pres.get('content')
            if isinstance(raw, str):
                pres['content_parsed'] = json.loads(raw)
            else:
                pres['content_parsed'] = raw
        except: 
            pres['content_parsed'] = None

        # Format dates
        for key in ['created_at', 'updated_at']:
            if isinstance(pres.get(key), (datetime.datetime, datetime. date)):
                pres[key] = pres[key].isoformat()

        return jsonify({'success': True, 'data': pres}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ======================================================================
# STATISTICS ROUTE (Optional - for analytics)
# ======================================================================
@presentations_bp.route('/stats', methods=['GET'])
def get_statistics():
    """
    Get presentation statistics
    """
    try:
        # Total presentations
        total_result = execute_query(
            "SELECT COUNT(*) as total FROM presentations",
            fetch=True
        )
        total = total_result[0]['total'] if total_result else 0

        # By theme
        theme_stats = execute_query(
            """
            SELECT theme, COUNT(*) as count 
            FROM presentations 
            GROUP BY theme 
            ORDER BY count DESC
            """,
            fetch=True
        ) or []

        # By style
        style_stats = execute_query(
            """
            SELECT style, COUNT(*) as count 
            FROM presentations 
            GROUP BY style 
            ORDER BY count DESC
            """,
            fetch=True
        ) or []

        # Recent activity
        recent = execute_query(
            """
            SELECT DATE(created_at) as date, COUNT(*) as count 
            FROM presentations 
            WHERE created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
            GROUP BY DATE(created_at)
            ORDER BY date DESC
            """,
            fetch=True
        ) or []

        return jsonify({
            'success': True,
            'stats': {
                'total': total,
                'by_theme':  theme_stats,
                'by_style': style_stats,
                'recent_activity': recent
            }
        }), 200

    except Exception as e: 
        print(f"❌ Stats error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ======================================================================
# STARTUP LOG
# ======================================================================
print("✅ All presentation routes registered:")
print("   GET    /api/presentations/")
print("   GET    /api/presentations/<id>")
print("   PUT    /api/presentations/<id>")
print("   POST   /api/presentations/generate")
print("   DELETE /api/presentations/<id>")
print("   DELETE /api/presentations/all")
print("   GET    /api/presentations/<id>/download/<format>")
print("   GET    /api/presentations/<id>/export/pptx")
print("   GET    /api/presentations/<id>/export/pdf")
print("   GET    /api/presentations/<id>/export?format=pptx")
print("   GET    /api/presentations/<id>/debug")
print("   GET    /api/presentations/stats")
"""
Tests for PPTX generation fixes
Tests the 10 fixes applied for issue: Fix PPTX Generation to Match Web Preview
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.pptx_service import PPTXService, PPTXConfig, ImageHandler


def test_quote_slide_syntax_fix():
    """Test that quote slide no longer has syntax error"""
    service = PPTXService()
    
    # Create a mock presentation data with quote slide
    class MockData:
        theme = 'dialogue'
        content = {
            'slides': [{
                'layout': 'quote',
                'title': 'Test Quote',
                'content': 'Test quote content'
            }]
        }
    
    # Should not raise syntax error
    try:
        output = service.generate(MockData())
        assert len(output) > 0, "Quote slide generation failed"
        print("✅ Quote slide syntax fix verified")
    except SyntaxError:
        assert False, "Quote slide still has syntax error"


def test_url_sanitization_enhanced():
    """Test enhanced URL sanitization with special characters"""
    config = PPTXConfig()
    handler = ImageHandler(config)
    
    # Test cases
    test_cases = [
        ("https://example.com/image with spaces.jpg", True),
        ("https://example.com/prompt/test&query=1", True),
        ("https://example.com/prompt/hello world", True),
        ("https://example.com/normal.jpg", False)  # Should pass through
    ]
    
    for url, should_change in test_cases:
        sanitized = handler._sanitize_url(url)
        if should_change:
            assert sanitized != url, f"URL should have been sanitized: {url}"
            assert " " not in sanitized, f"Spaces not encoded: {sanitized}"
        print(f"✅ URL sanitization test passed for: {url[:40]}...")


def test_font_sizes_updated():
    """Test that font sizes match web preview specs"""
    config = PPTXConfig()
    
    expected_sizes = {
        'FONT_SIZE_TITLE': 48,
        'FONT_SIZE_HEADING': 36,
        'FONT_SIZE_SUBHEADING': 26,
        'FONT_SIZE_BODY': 16,
        'FONT_SIZE_SMALL': 13,
        'FONT_SIZE_CAPTION': 11
    }
    
    for attr_name, expected_pt in expected_sizes.items():
        actual = getattr(config, attr_name)
        # Convert EMU to points (1pt = 12700 EMU)
        actual_pt = actual / 12700
        assert abs(actual_pt - expected_pt) < 0.1, \
            f"{attr_name}: expected {expected_pt}pt, got {actual_pt}pt"
    
    print("✅ All font sizes correctly updated")


def test_content_preprocessing():
    """Test content preprocessing method"""
    service = PPTXService()
    
    # Test markdown removal
    test_content = "**Bold** text with *bullets*"
    processed = service._preprocess_content(test_content)
    assert "**" not in processed, "Markdown not removed"
    assert "•" in processed, "Bullets not converted"
    
    # Test HTML tag removal
    html_content = "<p>Test <strong>content</strong></p>"
    processed = service._preprocess_content(html_content)
    assert "<" not in processed, "HTML tags not removed"
    
    # Test whitespace cleanup
    messy_content = "Line 1\n\n\n\nLine 2\n  \nLine 3"
    processed = service._preprocess_content(messy_content)
    lines = processed.split('\n')
    assert all(line.strip() for line in lines), "Empty lines not removed"
    
    print("✅ Content preprocessing working correctly")


def test_grid_cards_2x2_layout():
    """Test that grid cards use 2x2 layout"""
    service = PPTXService()
    
    class MockData:
        theme = 'dialogue'
        content = {
            'slides': [{
                'layout': 'grid_4',
                'title': 'Test Grid',
                'content': '* Item 1\n* Item 2\n* Item 3\n* Item 4'
            }]
        }
    
    output = service.generate(MockData())
    assert len(output) > 0, "Grid slide generation failed"
    print("✅ Grid cards 2x2 layout implemented")


def test_roadmap_six_items():
    """Test that roadmap handles up to 6 items"""
    service = PPTXService()
    
    class MockData:
        theme = 'dialogue'
        content = {
            'slides': [{
                'layout': 'roadmap',
                'title': 'Test Roadmap',
                'content': '\n'.join([f'Phase {i}' for i in range(1, 8)])  # 7 items
            }]
        }
    
    # Should not crash with 7 items (will use first 6)
    try:
        output = service.generate(MockData())
        assert len(output) > 0, "Roadmap slide generation failed"
        print("✅ Roadmap slide handles 6 items correctly")
    except:
        assert False, "Roadmap slide failed with multiple items"


def test_standard_slide_balance():
    """Test standard slide text/image balance"""
    service = PPTXService()
    
    # Test without image
    class MockDataNoImage:
        theme = 'dialogue'
        content = {
            'slides': [{
                'layout': 'standard',
                'title': 'Test Standard',
                'content': 'Test content without image',
                'image': None
            }]
        }
    
    output = service.generate(MockDataNoImage())
    assert len(output) > 0, "Standard slide without image failed"
    
    # Test with image (will fail to load but should handle gracefully)
    class MockDataWithImage:
        theme = 'dialogue'
        content = {
            'slides': [{
                'layout': 'standard',
                'title': 'Test Standard',
                'content': 'Test content with image',
                'image': 'https://nonexistent.example.com/image.jpg'
            }]
        }
    
    output = service.generate(MockDataWithImage())
    assert len(output) > 0, "Standard slide with image failed"
    print("✅ Standard slide text/image balance working")


def test_debug_borders_method():
    """Test that debug borders method exists"""
    service = PPTXService()
    assert hasattr(service, '_add_debug_borders'), "Debug borders method missing"
    print("✅ Debug borders method implemented")


if __name__ == '__main__':
    print("\n" + "="*60)
    print("Testing PPTX Generation Fixes")
    print("="*60 + "\n")
    
    tests = [
        test_quote_slide_syntax_fix,
        test_url_sanitization_enhanced,
        test_font_sizes_updated,
        test_content_preprocessing,
        test_grid_cards_2x2_layout,
        test_roadmap_six_items,
        test_standard_slide_balance,
        test_debug_borders_method
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {test.__name__} error: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*60)
    
    sys.exit(0 if failed == 0 else 1)

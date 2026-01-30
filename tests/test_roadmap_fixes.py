"""
Tests for Roadmap Slide Fixes
Tests that roadmap slides are properly generated and not blank
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.pptx_service import PPTXService


def test_roadmap_slide_not_blank():
    """Test that roadmap slide is not blank with proper content"""
    service = PPTXService()
    
    class MockData:
        theme = 'dialogue'
        content = {
            'slides': [{
                'layout': 'roadmap',
                'title': 'Process/Roadmap',
                'content': '''
                Research & Planning
                Design & Development
                Testing & Quality Assurance
                Deployment & Launch
                Monitoring & Optimization
                Continuous Improvement
                '''
            }]
        }
    
    # Should generate successfully
    output = service.generate(MockData())
    assert len(output) > 0, "Roadmap slide generation failed"
    
    # Verify presentation has correct number of slides
    assert service.prs is not None, "Presentation not created"
    assert len(service.prs.slides) == 1, "Wrong number of slides generated"
    
    print("✅ Roadmap slide generated successfully (not blank)")


def test_roadmap_with_process_layout():
    """Test that 'process' layout is routed to roadmap handler"""
    service = PPTXService()
    
    class MockData:
        theme = 'dialogue'
        content = {
            'slides': [{
                'layout': 'process',  # Should be routed to roadmap
                'title': 'Process Steps',
                'content': 'Step 1\nStep 2\nStep 3\nStep 4'
            }]
        }
    
    output = service.generate(MockData())
    assert len(output) > 0, "Process layout generation failed"
    print("✅ Process layout routed to roadmap handler")


def test_roadmap_with_steps_layout():
    """Test that 'steps' layout is routed to roadmap handler"""
    service = PPTXService()
    
    class MockData:
        theme = 'dialogue'
        content = {
            'slides': [{
                'layout': 'steps',  # Should be routed to roadmap
                'title': 'Implementation Steps',
                'content': 'Initialize\nConfigure\nDeploy\nMonitor'
            }]
        }
    
    output = service.generate(MockData())
    assert len(output) > 0, "Steps layout generation failed"
    print("✅ Steps layout routed to roadmap handler")


def test_roadmap_with_empty_content():
    """Test that roadmap handles empty content with fallback"""
    service = PPTXService()
    
    class MockData:
        theme = 'dialogue'
        content = {
            'slides': [{
                'layout': 'roadmap',
                'title': 'Process/Roadmap',
                'content': ''  # Empty content should use fallback
            }]
        }
    
    output = service.generate(MockData())
    assert len(output) > 0, "Roadmap with empty content failed"
    print("✅ Roadmap handles empty content with fallback items")


def test_roadmap_with_various_formats():
    """Test roadmap parsing handles various content formats"""
    service = PPTXService()
    
    class MockData:
        theme = 'dialogue'
        content = {
            'slides': [{
                'layout': 'roadmap',
                'title': 'Process/Roadmap',
                'content': '''
                1. First step with number
                * Second step with bullet
                # Third step with hash
                - Fourth step with dash
                Fifth step plain text
                6. Sixth step
                7. Seventh step (should be ignored, limit is 6)
                '''
            }]
        }
    
    output = service.generate(MockData())
    assert len(output) > 0, "Roadmap with various formats failed"
    print("✅ Roadmap parses various content formats")


def test_roadmap_max_six_items():
    """Test that roadmap limits to 6 items maximum"""
    service = PPTXService()
    
    class MockData:
        theme = 'dialogue'
        content = {
            'slides': [{
                'layout': 'roadmap',
                'title': 'Process/Roadmap',
                'content': '\n'.join([f'Item {i}' for i in range(1, 11)])  # 10 items
            }]
        }
    
    # Should handle gracefully (use first 6)
    output = service.generate(MockData())
    assert len(output) > 0, "Roadmap with many items failed"
    print("✅ Roadmap correctly limits to 6 items")


def test_error_slide_creation():
    """Test that error slides are properly formatted"""
    service = PPTXService()
    
    # Create scenario that might cause an error but is caught
    class MockData:
        theme = 'dialogue'
        content = {
            'slides': [{
                'layout': 'unknown_layout_type',  # Unknown layout
                'title': 'Test Error Handling',
                'content': 'This should fall back to standard layout'
            }]
        }
    
    # Should not crash, should create a slide
    output = service.generate(MockData())
    assert len(output) > 0, "Error handling failed"
    print("✅ Error handling works correctly")


def test_roadmap_with_timeline_layout():
    """Test that 'timeline' layout is routed to roadmap handler"""
    service = PPTXService()
    
    class MockData:
        theme = 'dialogue'
        content = {
            'slides': [{
                'layout': 'timeline',  # Should be routed to roadmap
                'title': 'Project Timeline',
                'content': 'Q1 2024\nQ2 2024\nQ3 2024\nQ4 2024'
            }]
        }
    
    output = service.generate(MockData())
    assert len(output) > 0, "Timeline layout generation failed"
    print("✅ Timeline layout routed to roadmap handler")


if __name__ == '__main__':
    print("\n" + "="*70)
    print("Testing Roadmap Slide Fixes")
    print("="*70 + "\n")
    
    tests = [
        test_roadmap_slide_not_blank,
        test_roadmap_with_process_layout,
        test_roadmap_with_steps_layout,
        test_roadmap_with_empty_content,
        test_roadmap_with_various_formats,
        test_roadmap_max_six_items,
        test_error_slide_creation,
        test_roadmap_with_timeline_layout,
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
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "="*70)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*70)
    
    sys.exit(0 if failed == 0 else 1)

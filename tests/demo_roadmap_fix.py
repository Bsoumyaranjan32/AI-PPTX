"""
Demo script to generate sample presentations with roadmap slides
This validates that the roadmap slide fix works correctly
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.pptx_service import PPTXService
from datetime import datetime


def generate_test_presentation():
    """Generate a test presentation with various slide types including roadmap"""
    service = PPTXService()
    
    class TestPresentation:
        theme = 'dialogue'
        content = {
            'slides': [
                {
                    'layout': 'hero',
                    'title': 'Test Presentation',
                    'content': 'Validating Roadmap Slide Fix'
                },
                {
                    'layout': 'roadmap',
                    'title': 'Process/Roadmap - Standard Format',
                    'content': '''
                    Research & Planning: Gather requirements and plan the project
                    Design & Development: Create design and develop the solution
                    Testing & Quality Assurance: Test thoroughly for bugs
                    Deployment & Launch: Deploy to production environment
                    Monitoring & Optimization: Monitor performance and optimize
                    Continuous Improvement: Iterate and improve continuously
                    '''
                },
                {
                    'layout': 'process',
                    'title': 'Implementation Process',
                    'content': '''
                    1. Initialize project structure
                    2. Configure development environment
                    3. Implement core features
                    4. Deploy to staging
                    '''
                },
                {
                    'layout': 'steps',
                    'title': 'Getting Started Steps',
                    'content': '''
                    * Clone the repository
                    * Install dependencies
                    * Configure environment
                    * Run the application
                    * Deploy to production
                    '''
                },
                {
                    'layout': 'timeline',
                    'title': 'Project Timeline',
                    'content': '''
                    Q1 2024: Planning phase
                    Q2 2024: Development phase
                    Q3 2024: Testing phase
                    Q4 2024: Launch phase
                    '''
                },
                {
                    'layout': 'roadmap',
                    'title': 'Empty Content Test (Should show defaults)',
                    'content': ''
                },
            ]
        }
    
    print("\n" + "="*70)
    print("Generating Test Presentation")
    print("="*70 + "\n")
    
    output = service.generate(TestPresentation())
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"/tmp/test_roadmap_fix_{timestamp}.pptx"
    
    with open(filename, 'wb') as f:
        f.write(output)
    
    print("\n" + "="*70)
    print(f"✅ Presentation generated successfully!")
    print(f"📁 Saved to: {filename}")
    print(f"📊 Total slides: {len(service.prs.slides)}")
    print("="*70)
    
    # Print slide summary
    print("\nSlide Summary:")
    for i, slide in enumerate(service.prs.slides, 1):
        print(f"  Slide {i}: {len(slide.shapes)} shapes")
    
    return filename


def validate_roadmap_content():
    """Quick validation that roadmap slides have content (not blank)"""
    service = PPTXService()
    
    class RoadmapTest:
        theme = 'dialogue'
        content = {
            'slides': [{
                'layout': 'roadmap',
                'title': 'Process/Roadmap',
                'content': '''
                Step 1: First step
                Step 2: Second step
                Step 3: Third step
                '''
            }]
        }
    
    print("\n" + "="*70)
    print("Validating Roadmap Slide Content")
    print("="*70 + "\n")
    
    output = service.generate(RoadmapTest())
    
    # Check that presentation was generated
    assert len(output) > 0, "❌ Failed: Presentation output is empty"
    print("✅ Presentation generated with content")
    
    # Check that slide exists
    assert len(service.prs.slides) == 1, "❌ Failed: Wrong number of slides"
    print("✅ Slide count correct (1 slide)")
    
    # Check that slide has shapes (not blank)
    slide = service.prs.slides[0]
    assert len(slide.shapes) > 0, "❌ Failed: Slide has no shapes (blank)"
    print(f"✅ Slide has {len(slide.shapes)} shapes (not blank)")
    
    # Should have:
    # - Background (1)
    # - Title box (1)
    # - Connector line (1)
    # - 3 circles (3)
    # - 3 text boxes (3)
    # Total: ~9 shapes minimum
    expected_min_shapes = 7  # Conservative estimate
    assert len(slide.shapes) >= expected_min_shapes, \
        f"❌ Failed: Slide has only {len(slide.shapes)} shapes, expected at least {expected_min_shapes}"
    print(f"✅ Slide has sufficient content ({len(slide.shapes)} shapes)")
    
    print("\n" + "="*70)
    print("✅ All Validations Passed!")
    print("="*70)


if __name__ == '__main__':
    print("\n" + "="*70)
    print("ROADMAP SLIDE FIX VALIDATION")
    print("="*70)
    
    try:
        # Generate full test presentation
        filename = generate_test_presentation()
        
        print("\n")
        
        # Validate roadmap content
        validate_roadmap_content()
        
        print("\n" + "="*70)
        print("🎉 SUCCESS - All validations passed!")
        print("="*70)
        print(f"\n💡 To view the presentation, open: {filename}")
        print("   Or download from the /tmp directory\n")
        
    except Exception as e:
        print("\n" + "="*70)
        print("❌ VALIDATION FAILED")
        print("="*70)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

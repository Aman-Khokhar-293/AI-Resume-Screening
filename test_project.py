#!/usr/bin/env python
"""
Comprehensive test script for ResumeMatch AI
Run this to verify everything is working correctly
"""

import sys
import os

def test_imports():
    """Test all critical imports"""
    print("=" * 60)
    print("TESTING IMPORTS")
    print("=" * 60)
    
    tests = [
        ("Flask", lambda: __import__('flask')),
        ("SQLAlchemy", lambda: __import__('sqlalchemy')),
        ("pypdf", lambda: __import__('pypdf')),
        ("sklearn", lambda: __import__('sklearn')),
        ("nltk", lambda: __import__('nltk')),
        ("app.py", lambda: __import__('app')),
        ("db.py", lambda: __import__('db')),
        ("models.py", lambda: __import__('models')),
        ("nlp.extract_info", lambda: __import__('nlp.extract_info')),
        ("services.match_service", lambda: __import__('services.match_service')),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            test_func()
            print(f"✓ {name}")
            passed += 1
        except Exception as e:
            print(f"✗ {name}: {str(e)}")
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0


def test_name_extraction():
    """Test name and contact extraction"""
    print("\n" + "=" * 60)
    print("TESTING NAME & CONTACT EXTRACTION")
    print("=" * 60)
    
    from nlp.extract_info import extract_name_and_contact, extract_name_from_filename
    
    test_cases = [
        ("John Doe\nEmail: john@example.com\nPhone: 555-1234", ("John Doe", "john@example.com")),
        ("Jane Smith\njane.smith@company.com", ("Jane Smith", "jane.smith@company.com")),
        ("Resume\nBob Wilson\nbob@test.org", ("Bob Wilson", "bob@test.org")),
    ]
    
    passed = 0
    for text, expected in test_cases:
        name, contact = extract_name_and_contact(text)
        if name == expected[0] and contact == expected[1]:
            print(f"✓ Extracted: {name}, {contact}")
            passed += 1
        else:
            print(f"✗ Expected: {expected}, Got: ({name}, {contact})")
    
    # Test filename extraction
    filename_tests = [
        ("John_Doe_Resume.pdf", "John Doe"),
        ("jane-smith-cv.pdf", "Jane Smith"),
        ("resume_bob_wilson.txt", "Bob Wilson"),
    ]
    
    for filename, expected_name in filename_tests:
        extracted = extract_name_from_filename(filename)
        if extracted == expected_name:
            print(f"✓ Filename '{filename}' → '{extracted}'")
            passed += 1
        else:
            print(f"✗ Filename '{filename}' expected '{expected_name}', got '{extracted}'")
    
    print(f"\nResults: {passed}/{len(test_cases) + len(filename_tests)} tests passed")
    return passed == (len(test_cases) + len(filename_tests))


def test_scoring():
    """Test match scoring algorithm"""
    print("\n" + "=" * 60)
    print("TESTING SCORING ALGORITHM")
    print("=" * 60)
    
    # Test scoring calculation
    test_cases = [
        (2, 2, 0.02, 0.706),  # 2/2 skills match, 2% text similarity
        (3, 5, 0.5, 0.57),    # 3/5 skills match, 50% text similarity
        (5, 5, 0.8, 0.94),    # 5/5 skills match, 80% text similarity
        (0, 3, 0.6, 0.18),    # 0/3 skills match, 60% text similarity
    ]
    
    passed = 0
    for overlap, required, text_sim, expected in test_cases:
        skills_score = overlap / required if required > 0 else 0
        final_score = (skills_score * 0.7) + (text_sim * 0.3)
        
        if abs(final_score - expected) < 0.01:  # Allow small floating point difference
            print(f"✓ {overlap}/{required} skills, {text_sim*100:.0f}% text → {final_score*100:.0f}%")
            passed += 1
        else:
            print(f"✗ Expected {expected*100:.0f}%, got {final_score*100:.0f}%")
    
    print(f"\nResults: {passed}/{len(test_cases)} tests passed")
    return passed == len(test_cases)


def check_files():
    """Check if all required files exist"""
    print("\n" + "=" * 60)
    print("CHECKING FILE STRUCTURE")
    print("=" * 60)
    
    required_files = [
        "app.py",
        "db.py",
        "models.py",
        "requirements.txt",
        "templates/index.html",
        "static/app_bulk.js",
        "static/styles.css",
        "nlp/extract_info.py",
        "nlp/matching.py",
        "nlp/skills.py",
        "services/match_service.py",
        "services/resume_service.py",
        "services/job_service.py",
    ]
    
    passed = 0
    for filepath in required_files:
        if os.path.exists(filepath):
            print(f"✓ {filepath}")
            passed += 1
        else:
            print(f"✗ {filepath} - MISSING")
    
    print(f"\nResults: {passed}/{len(required_files)} files found")
    return passed == len(required_files)


def check_endpoints():
    """Check if endpoints are defined"""
    print("\n" + "=" * 60)
    print("CHECKING API ENDPOINTS")
    print("=" * 60)
    
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    endpoints = [
        ("/", "Index page"),
        ("/health", "Health check"),
        ("/api/resumes", "Create resume"),
        ("/api/jobs", "Create job"),
        ("/api/match", "Match candidate to job"),
        ("/api/recommendations", "Get recommendations"),
        ("/api/extract-resume", "Extract resume text"),
        ("/api/bulk-match", "Bulk match resumes"),
    ]
    
    passed = 0
    for endpoint, description in endpoints:
        if endpoint in content:
            print(f"✓ {endpoint} - {description}")
            passed += 1
        else:
            print(f"✗ {endpoint} - MISSING")
    
    print(f"\nResults: {passed}/{len(endpoints)} endpoints found")
    return passed == len(endpoints)


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("RESUMEMATCH AI - PROJECT VERIFICATION")
    print("=" * 60)
    print(f"Python: {sys.version}")
    print(f"Working Directory: {os.getcwd()}")
    print()
    
    results = []
    
    # Run all tests
    results.append(("Imports", test_imports()))
    results.append(("Files", check_files()))
    results.append(("Endpoints", check_endpoints()))
    results.append(("Name Extraction", test_name_extraction()))
    results.append(("Scoring", test_scoring()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {test_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ ALL TESTS PASSED!")
        print("\nYour project is ready to run:")
        print("  python app.py")
        print("\nThen open: http://127.0.0.1:5000/")
    else:
        print("✗ SOME TESTS FAILED")
        print("\nPlease fix the issues above before running the app.")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

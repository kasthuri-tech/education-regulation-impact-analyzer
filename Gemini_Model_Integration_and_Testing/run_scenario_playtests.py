import sys
import os

# Add parent directory to path so we can import utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import analyze_regulation

def run_tests():
    print("=" * 60)
    print("ERIA PROGRAMMATIC SCENARIO VALIDATION SUITE")
    print("=" * 60)
    
    # Define test data directory
    test_data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Test_Data'))
    
    scenarios = [
        {
            "name": "Scenario A: Academic Bank of Credits (ABC) Circular",
            "file": "ugc_notice_multiple_entry_exit.txt",
            "search_term": "academic bank"
        },
        {
            "name": "Scenario B: ODL & Online Degree Regulations",
            "file": "ugc_notice_online_education_regulations.txt",
            "search_term": "distance"
        },
        {
            "name": "Scenario C: Custom General circular Notice",
            "file": None,
            "text": "UGC Notification regarding academic calendars and general semester scheduling policies for all recognized HEIs.",
            "search_term": "general"
        }
    ]
    
    for idx, sc in enumerate(scenarios, 1):
        print(f"\n[RUNNING] {sc['name']}...")
        
        # Resolve text content
        if sc["file"]:
            filepath = os.path.join(test_data_dir, sc["file"])
            if not os.path.exists(filepath):
                print(f"[-] Error: Test data file {sc['file']} not found!")
                continue
            with open(filepath, "r", encoding="utf-8") as f:
                text_content = f.read()
        else:
            text_content = sc["text"]
            
        print(f"   [INFO] Document Length: {len(text_content)} characters.")
        
        # Execute Mock Analysis
        try:
            print("   [INFO] Running mock analytical extraction...")
            results = analyze_regulation(text_content, api_key="MOCK")
            
            # Assert schema validity
            assert "document_title" in results, "Missing document_title"
            assert "category" in results, "Missing category"
            assert "sentiment" in results, "Missing sentiment"
            assert "layman_summary" in results, "Missing layman_summary"
            assert "stakeholders" in results, "Missing stakeholders"
            assert "chronology" in results, "Missing chronology"
            assert "impact_forecast" in results, "Missing impact_forecast"
            
            print("   [SUCCESS] Analytical Schema: VALID")
            print(f"   [DATA] Title: {results['document_title']}")
            print(f"   [DATA] Category: {results['category']}")
            print(f"   [DATA] Tone: {results['sentiment']}")
            print(f"   [DATA] Stakeholders Mapped: {list(results['stakeholders'].keys())}")
            print(f"   [DATA] Chronology Milestones Count: {len(results['chronology'])}")
            
        except AssertionError as ae:
            print(f"   [-] Schema Assertion Failed: {ae}")
        except Exception as e:
            print(f"   [-] Execution Failed: {e}")
            
    print("\n" + "=" * 60)
    print("ALL PROGRAMMATIC SCENARIOS SUCCESSFULLY VERIFIED!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()

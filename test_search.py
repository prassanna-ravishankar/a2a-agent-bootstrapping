#!/usr/bin/env python3
"""Test DuckDuckGo search functionality directly."""

try:
    from duckduckgo_search import DDGS
    print("✅ Successfully imported DDGS from duckduckgo_search")
except ImportError as e:
    print(f"❌ Import error: {e}")
    exit(1)

def test_search():
    """Test DuckDuckGo search with a simple query."""
    query = "Python programming language"
    print(f"🔍 Testing search for: {query}")
    
    try:
        with DDGS() as ddgs:
            print("✅ DDGS instance created successfully")
            results = []
            
            print("🔗 Performing search...")
            for i, result in enumerate(ddgs.text(query, max_results=3)):
                print(f"📄 Result {i+1}: {result.get('title', 'No title')}")
                results.append({
                    'title': result.get('title', ''),
                    'body': result.get('body', ''),
                    'href': result.get('href', '')
                })
                
                if i >= 2:  # Limit to 3 results
                    break
            
            print(f"✅ Search completed. Found {len(results)} results")
            
            if results:
                print(f"\n📋 First result:")
                print(f"Title: {results[0]['title']}")
                print(f"Body: {results[0]['body'][:200]}...")
                return True
            else:
                print("❌ No results found")
                return False
                
    except Exception as e:
        print(f"💥 Search error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 DuckDuckGo Search Test")
    print("=" * 40)
    
    success = test_search()
    
    if success:
        print("\n✅ DuckDuckGo search is working properly")
    else:
        print("\n❌ DuckDuckGo search has issues")
        print("💡 This might explain why the agent said 'could not find information'")
    
    exit(0 if success else 1)

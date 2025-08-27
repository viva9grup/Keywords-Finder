#!/usr/bin/env python3
"""
URL Text Searcher
A Python script to open URLs and search for specific text with advanced features

Features:
- Search single or multiple URLs
- Case-sensitive/insensitive search
- Context around matches
- Regex pattern support
- HTML content parsing
- Results highlighting (with colorama)
- Export results to file

Requirements:
- requests (required)
- beautifulsoup4 (required)  
- colorama (optional, for colored output)

Usage:
    python url_searcher.py
    python url_searcher.py https://example.com "search term"
    python url_searcher.py -f urls.txt "pattern" --regex --case-sensitive
"""

import requests
import sys
import re
import argparse
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import json
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
import time
# Optional colorama for colored output
try:
    from colorama import Fore, Back, Style, init
    # Initialize colorama for cross-platform colored output
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    # Fallback if colorama is not installed
    class MockColor:
        def __getattr__(self, name):
            return ""
    
    Fore = Back = Style = MockColor()
    COLORS_AVAILABLE = False
    print("Note: Install 'colorama' for colored output: pip install colorama")

@dataclass
class SearchMatch:
    url: str
    match_text: str
    context_before: str
    context_after: str
    line_number: int
    position: int
    full_line: str

@dataclass
class SearchResult:
    url: str
    search_term: str
    total_matches: int
    matches: List[SearchMatch]
    page_title: str
    search_time: float
    error_message: str = ""

class URLTextSearcher:
    def __init__(self, 
                 case_sensitive: bool = False,
                 regex_mode: bool = False,
                 context_chars: int = 100,
                 timeout: int = 10,
                 user_agent: str = None):
        
        self.case_sensitive = case_sensitive
        self.regex_mode = regex_mode
        self.context_chars = context_chars
        self.timeout = timeout
        
        # Set up session with headers
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': user_agent or 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Compile regex flags
        self.regex_flags = 0 if case_sensitive else re.IGNORECASE

    def fetch_url_content(self, url: str) -> Tuple[str, str, str]:
        """
        Fetch URL content and return (text_content, html_content, title)
        """
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "meta", "noscript"]):
                script.decompose()
            
            # Get page title
            title = soup.title.string.strip() if soup.title else "No Title"
            
            # Get text content
            text_content = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text_content.splitlines())
            text_content = '\n'.join(line for line in lines if line)
            
            return text_content, str(soup), title
            
        except Exception as e:
            raise Exception(f"Failed to fetch {url}: {str(e)}")

    def search_text(self, content: str, search_term: str, url: str) -> List[SearchMatch]:
        """
        Search for text in content and return matches with context
        """
        matches = []
        
        if self.regex_mode:
            # Regex search
            try:
                pattern = re.compile(search_term, self.regex_flags)
                for match in pattern.finditer(content):
                    match_obj = self._create_match_object(
                        content, match.group(), match.start(), url
                    )
                    matches.append(match_obj)
            except re.error as e:
                raise Exception(f"Invalid regex pattern '{search_term}': {str(e)}")
        else:
            # Simple text search
            search_content = content if self.case_sensitive else content.lower()
            search_term_lower = search_term if self.case_sensitive else search_term.lower()
            
            start = 0
            while True:
                pos = search_content.find(search_term_lower, start)
                if pos == -1:
                    break
                    
                # Get actual match text (preserves original case)
                actual_match = content[pos:pos + len(search_term)]
                
                match_obj = self._create_match_object(content, actual_match, pos, url)
                matches.append(match_obj)
                
                start = pos + 1
        
        return matches

    def _create_match_object(self, content: str, match_text: str, position: int, url: str) -> SearchMatch:
        """
        Create a SearchMatch object with context
        """
        # Get context around match
        start_context = max(0, position - self.context_chars)
        end_context = min(len(content), position + len(match_text) + self.context_chars)
        
        context_before = content[start_context:position]
        context_after = content[position + len(match_text):end_context]
        
        # Find line number
        lines_before = content[:position].count('\n')
        line_number = lines_before + 1
        
        # Get full line containing the match
        lines = content.splitlines()
        if line_number <= len(lines):
            full_line = lines[line_number - 1]
        else:
            full_line = ""
        
        return SearchMatch(
            url=url,
            match_text=match_text,
            context_before=context_before,
            context_after=context_after,
            line_number=line_number,
            position=position,
            full_line=full_line
        )

    def search_url(self, url: str, search_term: str) -> SearchResult:
        """
        Search for text in a single URL
        """
        start_time = time.time()
        
        try:
            # Validate URL
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            print(f"🔍 Searching in: {url}")
            
            # Fetch content
            text_content, html_content, title = self.fetch_url_content(url)
            
            # Search for matches
            matches = self.search_text(text_content, search_term, url)
            
            search_time = time.time() - start_time
            
            return SearchResult(
                url=url,
                search_term=search_term,
                total_matches=len(matches),
                matches=matches,
                page_title=title,
                search_time=search_time
            )
            
        except Exception as e:
            search_time = time.time() - start_time
            return SearchResult(
                url=url,
                search_term=search_term,
                total_matches=0,
                matches=[],
                page_title="",
                search_time=search_time,
                error_message=str(e)
            )

    def search_multiple_urls(self, urls: List[str], search_term: str) -> List[SearchResult]:
        """
        Search for text in multiple URLs
        """
        results = []
        
        print(f"🎯 Searching for '{search_term}' in {len(urls)} URLs")
        print(f"⚙️  Settings: Case-sensitive={self.case_sensitive}, Regex={self.regex_mode}")
        print("-" * 60)
        
        for i, url in enumerate(urls, 1):
            print(f"\n[{i}/{len(urls)}] ", end="")
            result = self.search_url(url, search_term)
            results.append(result)
            
            if result.error_message:
                print(f"❌ Error: {result.error_message}")
            else:
                print(f"✅ Found {result.total_matches} matches in {result.search_time:.2f}s")
        
        return results

    def highlight_match(self, text: str, match: str) -> str:
        """
        Highlight search matches in text using colors (if available)
        """
        if not COLORS_AVAILABLE:
            # Simple text highlighting without colors
            if self.case_sensitive:
                return text.replace(match, f"[{match}]")
            else:
                pattern = re.compile(re.escape(match), re.IGNORECASE)
                return pattern.sub("[\\g<0>]", text)
        
        # Colored highlighting
        if self.case_sensitive:
            highlighted = text.replace(match, f"{Back.YELLOW}{Fore.BLACK}{match}{Style.RESET_ALL}")
        else:
            # Case-insensitive highlighting
            pattern = re.compile(re.escape(match), re.IGNORECASE)
            highlighted = pattern.sub(f"{Back.YELLOW}{Fore.BLACK}\\g<0>{Style.RESET_ALL}", text)
        
        return highlighted

    def display_results(self, results: List[SearchResult]):
        """
        Display search results in a formatted way
        """
        total_matches = sum(r.total_matches for r in results)
        successful_searches = len([r for r in results if not r.error_message])
        
        print("\n" + "=" * 80)
        print("🔍 SEARCH RESULTS SUMMARY")
        print("=" * 80)
        print(f"Total URLs searched: {len(results)}")
        print(f"Successful searches: {successful_searches}")
        print(f"Total matches found: {total_matches}")
        print(f"Search term: '{results[0].search_term if results else 'N/A'}'")
        
        for result in results:
            if result.error_message:
                print(f"\n❌ {result.url}")
                print(f"   Error: {result.error_message}")
                continue
            
            print(f"\n🌐 {result.url}")
            print(f"📄 Title: {result.page_title}")
            print(f"🎯 Matches: {result.total_matches} | ⏱️  Time: {result.search_time:.2f}s")
            
            if result.matches:
                print("📍 Match details:")
                
                # Show first 5 matches
                for i, match in enumerate(result.matches[:5], 1):
                    print(f"\n   [{i}] Line {match.line_number}, Position {match.position}")
                    
                    # Show context with highlighting
                    context = f"{match.context_before}{match.match_text}{match.context_after}"
                    context = context.replace('\n', ' ').strip()
                    
                    # Truncate if too long
                    if len(context) > 200:
                        context = context[:197] + "..."
                    
                    highlighted_context = self.highlight_match(context, match.match_text)
                    print(f"   Context: {highlighted_context}")
                
                if len(result.matches) > 5:
                    print(f"\n   ... and {len(result.matches) - 5} more matches")

    def export_results(self, results: List[SearchResult], filename: str):
        """
        Export results to JSON file
        """
        try:
            export_data = {
                "search_summary": {
                    "total_urls": len(results),
                    "successful_searches": len([r for r in results if not r.error_message]),
                    "total_matches": sum(r.total_matches for r in results),
                    "search_term": results[0].search_term if results else "",
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                },
                "results": [asdict(result) for result in results]
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Results exported to: {filename}")
            
        except Exception as e:
            print(f"❌ Failed to export results: {e}")

def load_urls_from_file(filename: str) -> List[str]:
    """
    Load URLs from a text file (one URL per line)
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        return urls
    except Exception as e:
        print(f"❌ Failed to load URLs from {filename}: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(
        description="Search for text in web pages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python url_searcher.py https://example.com "search term"
  python url_searcher.py -f urls.txt "pattern" --regex
  python url_searcher.py https://site.com "text" --case-sensitive --export results.json

Requirements:
  pip install requests beautifulsoup4
  pip install colorama  # optional, for colored output
        """
    )
    
    parser.add_argument('url', nargs='?', help='URL to search (optional if using -f)')
    parser.add_argument('search_term', nargs='?', help='Text to search for')
    parser.add_argument('-f', '--file', help='File containing URLs (one per line)')
    parser.add_argument('--case-sensitive', action='store_true', help='Case-sensitive search')
    parser.add_argument('--regex', action='store_true', help='Use regex pattern matching')
    parser.add_argument('--context', type=int, default=100, help='Context characters around matches')
    parser.add_argument('--timeout', type=int, default=10, help='Request timeout in seconds')
    parser.add_argument('--export', help='Export results to JSON file')
    parser.add_argument('--user-agent', help='Custom User-Agent header')
    
    args = parser.parse_args()
    
    # Interactive mode if no arguments
    if not args.url and not args.file:
        print("🔍 URL Text Searcher")
        print("=" * 30)
        
        url_input = input("Enter URL (or file path with -f): ").strip()
        if url_input.startswith('-f '):
            args.file = url_input[3:].strip()
        else:
            args.url = url_input
        
        args.search_term = input("Enter search term: ").strip()
        
        case_resp = input("Case-sensitive search? (y/n) [n]: ").strip().lower()
        args.case_sensitive = case_resp == 'y'
        
        regex_resp = input("Use regex? (y/n) [n]: ").strip().lower()
        args.regex = regex_resp == 'y'
    
    if not args.search_term:
        print("❌ Search term is required")
        return
    
    # Get URLs
    urls = []
    if args.file:
        urls = load_urls_from_file(args.file)
    elif args.url:
        urls = [args.url]
    else:
        print("❌ URL or URL file is required")
        return
    
    if not urls:
        print("❌ No valid URLs found")
        return
    
    # Initialize searcher
    searcher = URLTextSearcher(
        case_sensitive=args.case_sensitive,
        regex_mode=args.regex,
        context_chars=args.context,
        timeout=args.timeout,
        user_agent=args.user_agent
    )
    
    # Perform search
    try:
        if len(urls) == 1:
            result = searcher.search_url(urls[0], args.search_term)
            results = [result]
        else:
            results = searcher.search_multiple_urls(urls, args.search_term)
        
        # Display results
        searcher.display_results(results)
        
        # Export if requested
        if args.export:
            searcher.export_results(results, args.export)
        
        # Summary stats
        total_matches = sum(r.total_matches for r in results)
        if total_matches > 0:
            print(f"\n✅ Search completed! Found {total_matches} total matches.")
        else:
            print(f"\n❌ No matches found for '{args.search_term}'")
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Search interrupted by user")
    except Exception as e:
        print(f"\n❌ Search failed: {e}")

if __name__ == "__main__":
    main()

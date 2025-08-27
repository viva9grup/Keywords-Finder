# 🔍 Keywords Finder

A powerful Python script to search for specific text content across web pages with advanced features including regex support, context display, and colored highlighting.

## ✨ Features

- 🌐 **Single/Multiple URL Search** - Search one URL or batch process from file
- 🔤 **Advanced Search Options** - Case-sensitive and regex pattern matching
- 📝 **Context Display** - Shows surrounding text around matches
- 🌈 **Colored Highlighting** - Visual match highlighting (optional)
- 📊 **Detailed Results** - Line numbers, positions, and match statistics
- 💾 **Export Results** - Save search results to JSON format
- 🖥️ **Interactive Mode** - Command-line or interactive usage
- 📈 **Progress Tracking** - Real-time progress for multiple URLs
- 🛡️ **Error Handling** - Robust network and parsing error management
- 📱 **Clean HTML Parsing** - Extracts clean text from HTML content

## 📦 Installation

### Required Dependencies
```bash
pip install requests beautifulsoup4
```

### Optional Dependencies (for colored output)
```bash
pip install colorama
```

### Quick Install
```bash
# Clone the repository
git clone https://github.com/yourusername/url-text-searcher.git
cd url-text-searcher

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Quick Start

### Interactive Mode
```bash
python keywords-finder.py
```

### Command Line Usage
```bash
# Search single URL
python keywords-finder.py https://example.com "python programming"

# Search multiple URLs from file
python keywords-finder.py -f urls.txt "error" --case-sensitive

# Regex search with export
python keywords-finder.py https://site.com "\d{3}-\d{3}-\d{4}" --regex --export results.json
```

## 📋 Usage Examples

### Basic Text Search
```bash
python keywords-finder.py https://python.org "documentation"
```

### Case-Sensitive Search
```bash
python keywords-finder.py https://example.com "API" --case-sensitive
```

### Regex Pattern Search
```bash
# Find email addresses
python keywords-finder.py https://example.com "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}" --regex

# Find phone numbers
python keywords-finder.py https://example.com "\b\d{3}-\d{3}-\d{4}\b" --regex
```

### Batch Search from File
```bash
python keywords-finder.py -f urls.txt "copyright" --export results.json
```

### Advanced Options
```bash
python keywords-finder.py https://example.com "search term" \
  --context 200 \
  --timeout 15 \
  --user-agent "Custom Bot 1.0"
```

## 🎛️ Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `url` | URL to search (optional if using `-f`) | - |
| `search_term` | Text to search for | - |
| `-f, --file` | File containing URLs (one per line) | - |
| `--case-sensitive` | Enable case-sensitive search | False |
| `--regex` | Use regex pattern matching | False |
| `--context` | Context characters around matches | 100 |
| `--timeout` | Request timeout in seconds | 10 |
| `--export` | Export results to JSON file | - |
| `--user-agent` | Custom User-Agent header | Default browser UA |

## 📄 URL File Format

Create a text file with URLs (one per line):

```
# urls.txt
https://example1.com
https://example2.com
# This is a comment - ignored
https://example3.com/page
```

## 📊 Sample Output

```
🔍 SEARCH RESULTS SUMMARY
================================================================================
Total URLs searched: 2
Successful searches: 2  
Total matches found: 5
Search term: 'python'

🌐 https://python.org
📄 Title: Welcome to Python.org
🎯 Matches: 3 | ⏱️  Time: 1.2s
📍 Match details:

   [1] Line 15, Position 234
   Context: Welcome to the official Python website where you can download...

🌐 https://docs.python.org
📄 Title: Python Documentation
🎯 Matches: 2 | ⏱️  Time: 0.8s

✅ Search completed! Found 5 total matches.
💾 Results exported to: results.json
```

## 📈 Export Format

Results are exported in JSON format:

```json
{
  "search_summary": {
    "total_urls": 2,
    "successful_searches": 2,
    "total_matches": 5,
    "search_term": "python",
    "timestamp": "2024-01-15 10:30:45"
  },
  "results": [
    {
      "url": "https://python.org",
      "search_term": "python",
      "total_matches": 3,
      "page_title": "Welcome to Python.org",
      "search_time": 1.2,
      "matches": [
        {
          "match_text": "Python",
          "line_number": 15,
          "position": 234,
          "context_before": "Welcome to the official ",
          "context_after": " website where you can download",
          "full_line": "Welcome to the official Python website"
        }
      ]
    }
  ]
}
```

## 🎨 Visual Features

### With Colorama (Recommended)
- 🟡 **Yellow highlighting** for matched text
- 🔴 **Red indicators** for errors
- 🟢 **Green indicators** for success
- 📊 **Colored progress** indicators

### Without Colorama (Fallback)
- **[Bracket highlighting]** for matched text
- Plain text output with clear formatting

## 🔧 Advanced Examples

### Find All Links in a Page
```bash
python keywords-finder.py https://example.com "https?://[^\s<>\"]{2,}" --regex
```

### Search for Specific HTML Elements
```bash
python keywords-finder.py https://example.com "<div[^>]*class=['\"]error['\"]" --regex
```

### Monitor Multiple Sites for Changes
```bash
# Create monitoring script
echo "https://site1.com" > monitor_urls.txt
echo "https://site2.com" >> monitor_urls.txt
python keywords-finder.py -f monitor_urls.txt "updated|new|announcement" --export daily_check.json
```

### Performance Testing
```bash
# Search large sites with custom timeout
python keywords-finder.py https://large-site.com "performance" --timeout 30 --context 50
```

## ⚡ Performance Tips

- **Batch Processing**: Use file input for multiple URLs
- **Adjust Context**: Reduce `--context` value for faster processing
- **Timeout Settings**: Increase `--timeout` for slow sites
- **Regex Optimization**: Use specific patterns for better performance
- **Export Results**: Use `--export` to save and analyze results

## 🛠️ Dependencies

### Core Dependencies
- **requests** - HTTP library for fetching web content
- **beautifulsoup4** - HTML parsing and content extraction
- **argparse** - Command-line argument parsing (built-in)
- **json** - JSON handling (built-in)
- **re** - Regular expressions (built-in)

### Optional Dependencies
- **colorama** - Cross-platform colored terminal output

## 🤝 Contributing

Contributions are welcome! Here are some ways to contribute:

1. 🐛 **Report Bugs** - Open an issue with details
2. 💡 **Suggest Features** - Share your ideas
3. 🔧 **Submit PRs** - Fix bugs or add features
4. 📖 **Improve Docs** - Enhance documentation

### Development Setup
```bash
git clone https://github.com/yourusername/url-text-searcher.git
cd url-text-searcher
pip install -r requirements.txt
python keywords-finder.py --help
```

## 📝 Requirements.txt

```
requests>=2.25.0
beautifulsoup4>=4.9.0
colorama>=0.4.0
```

## 🐛 Troubleshooting

### Common Issues

**Import Error: colorama**
```bash
pip install colorama
# or run without colors - script will fallback gracefully
```

**SSL Certificate Error**
```bash
# Add --timeout option or check your network connection
python keywords-finder.py https://example.com "text" --timeout 30
```

**Memory Issues with Large Sites**
```bash
# Reduce context size
python keywords-finder.py https://large-site.com "text" --context 50
```

**Permission Denied**
```bash
# Some sites block automated requests - try custom user agent
python keywords-finder.py https://example.com "text" --user-agent "Mozilla/5.0..."
```

## 📊 Use Cases

- 🔍 **Content Monitoring** - Track changes on websites
- 📈 **SEO Analysis** - Find specific keywords across sites
- 🛡️ **Security Auditing** - Search for sensitive information
- 📚 **Research** - Collect data from multiple sources
- 🔎 **Link Checking** - Find broken or specific links
- 📝 **Content Validation** - Verify text exists on pages
- 🎯 **Marketing** - Monitor brand mentions across sites

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Star History

If you find this tool useful, please consider giving it a star! ⭐

## 
---

<div align="center">

**Made with ❤️ by [Paddy](https://github.com/viva9grup)**

[⭐ Star this repo](https://github.com/yourusername/url-text-searcher) • [🐛 Report Bug](https://github.com/yourusername/url-text-searcher/issues) • [✨ Request Feature](https://github.com/yourusername/url-text-searcher/issues)

</div>

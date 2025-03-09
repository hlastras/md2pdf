import argparse
import mistune
import re
import os
from mistune.renderers.html import HTMLRenderer

"""
Markdown to LaTeX processor script.
This script does several things:
1. Extracts links from markdown content and creates a BibTeX file
2. Replaces links in the markdown with citation keys
3. Replaces Unicode special characters with their LaTeX command equivalents
"""

def replace_special_characters(text):
    """Replace Unicode special characters with their LaTeX command equivalents"""
    # Group special characters by the LaTeX command they need
    symbol_groups = {
        'textsymbol': [
            '≈', '⇒',  # Original characters
            'μ', 'κ', 'δ',  # Greek letters
            '≤', '≥',  # Comparison operators
            '∼',  # Tilde operator
        ],
        'textextrasymbol': [
            '₃',  # Subscript 3
        ],
        'textcjksymbol': [
            '【', '】'  # Japanese brackets
        ]
    }
    
    # Replace each special character with its appropriate LaTeX command
    for command, chars in symbol_groups.items():
        for char in chars:
            text = text.replace(char, f'\\{command}{{{char}}}')
    
    return text

class LinkExtractor(HTMLRenderer):
    def __init__(self):
        super().__init__()
        self.urls = []
        self.url_texts = {}  # Store link text for each URL
    
    def link(self, text, url, title=None):
        self.urls.append(url)
        # Store the link text for each URL
        if url not in self.url_texts:
            self.url_texts[url] = text
        return super().link(text, url, title)
    
    def image(self, src, alt="", title=None):
        self.urls.append(src)
        if src not in self.url_texts:
            self.url_texts[src] = alt or "Image"
        return super().image(src, alt, title)

def extract_links(md_content):
    renderer = LinkExtractor()
    md = mistune.Markdown(renderer=renderer)
    md(md_content)
    return renderer.urls, renderer.url_texts

def create_bibtex_file(urls_dict, texts_dict, output_path):
    """Generate a BibTeX file from the URLs dict"""
    bibtex_path = os.path.splitext(output_path)[0] + '.bib'
    
    with open(bibtex_path, 'w', encoding='utf-8') as f:
        for url, num in urls_dict.items():
            # Create a unique citation key
            cite_key = f"url{num}"
            
            # Get the link text or use URL if no text available
            title = texts_dict.get(url, url)
            
            # Create sort_url by removing query parameters
            sort_url = re.sub(r'(#|\?).*$', '', url)
            
            # Write BibTeX entry in simplified format
            f.write(f"@misc{{{cite_key},\n")
            f.write(f"  title = {{{title}}},\n")
            f.write(f"  url = {{{url}}},\n")
            f.write(f"  note = {{{sort_url}}},\n")
            f.write(f"  annote = {{{title}}}\n")
            f.write("}\n\n")
    
    return bibtex_path

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('markdown_file', help='Path to input Markdown file')
    parser.add_argument('output_file', help='Path to output Markdown file')
    parser.add_argument('bibtex_file', help='Path to output BibTeX file')
    args = parser.parse_args()
    
    with open(args.markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    

    
    urls, url_texts = extract_links(content)
    unique_urls = {}
    counter = 1
    for url in urls:
        if url not in unique_urls:
            unique_urls[url] = counter
            counter += 1
    
    # Create BibTeX file with link texts
    bibtex_path = create_bibtex_file(unique_urls, url_texts, args.bibtex_file)
    
    # Create URL to citation key mapping
    url_to_cite = {url: f"url{num}" for url, num in unique_urls.items()}
    
    # Use re.DOTALL to handle multi-line links
    def replace_link(m):
        link_text = m.group(1)
        url = m.group(2)
        if url in url_to_cite:
            # Use pandoc citation format [@key] instead of \cite{key}
            return f"[@{url_to_cite[url]}]"
        return m.group(0)
    
    # Pattern matches links across multiple lines and removes extra parentheses
    modified_content = re.sub(
        r'(?:\(\s*)?\[(.*?)\]\((.*?)\)(?:\s*\))?',
        replace_link, 
        content, 
        flags=re.DOTALL
    )
    
    modified_content = replace_special_characters(modified_content)
    
    with open(args.output_file, 'w', encoding='utf-8') as f:
        f.write(modified_content)
    
    # Print the mapping
    print(f"Created BibTeX file: {bibtex_path}")
    for url, num in sorted(unique_urls.items(), key=lambda x: x[1]):
        print(f"{num}. {url}")

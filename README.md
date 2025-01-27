# Combine HTML Files for Dify Knowledge

This repository provides a simple Python script to **combine multiple HTML files** into one or more **plain-text files** (under 10MB each) that can be uploaded to [Dify](https://docs.dify.ai/) as Knowledge.

## Overview

When preparing data to feed into Dify, you may want to extract text from numerous HTML files and **merge** them into a manageable format. This script:

1. Loads all `.html`/`.htm` files from a specified directory.  
2. Strips out unnecessary elements such as `<script>`, `<style>`, `<noscript>`, `<header>`, `<footer>` to retain the primary text.  
3. Concatenates them into a single text buffer, while **automatically splitting** the output into chunks if it exceeds **10MB** (configurable).  
4. Saves each chunk as a `.txt` file in the current directory, ready to be uploaded to Dify as Knowledge.

## Features

- **HTML to Text Conversion**  
  Uses [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/) to parse HTML, remove scripts, and extract readable text.
  
- **Size-limited Output**  
  Ensures each output file remains below `10 MB`. You can adjust the limit by changing the constant `MAX_FILE_SIZE`.

- **Minimal Dependencies**  
  Only requires `beautifulsoup4` (and Python 3).

## Getting Started

### Prerequisites

- Python 3.7+ (recommended)
- BeautifulSoup4

Install the required package:
```bash
pip install beautifulsoup4
```

### Script Usage

1. **Clone or download** this repository.
2. **Place your HTML files** inside a directory (e.g., `downloaded_pages/`).
3. **Run the script** to convert and combine:

```bash
python combine_html_for_dify.py
```

By default, it looks for a folder named `downloaded_pages` and merges any `.html` or `.htm` files there. It will output files like `knowledge_1.txt`, `knowledge_2.txt`, etc., each under 10MB.

#### Customizing the Inputs

- **Change the input directory**: Edit the `input_dir` variable in `main()` (or pass it as a parameter if you wish to modify the script for CLI arguments).
- **Change the output prefix**: Modify `output_prefix` in `main()` (e.g., `my_knowledge` → produces `my_knowledge_1.txt`, `my_knowledge_2.txt`...).
- **Change the size limit**: Update the `MAX_FILE_SIZE` constant in the script if 10MB is not desired.

### Example

1. Suppose you have these HTML files in `downloaded_pages/`:
   ```
   downloaded_pages/
   ├─ page1.html
   ├─ page2.html
   └─ page3.html
   ```
2. Run:
   ```bash
   python combine_html_for_dify.py
   ```
3. After processing, you might see:
   ```
   knowledge_1.txt (Size: ~5MB)
   knowledge_2.txt (Size: ~3MB)
   ```
   in the same directory as the script.

4. **Upload** the `.txt` files into Dify’s Knowledge base.

## Script Breakdown

```python
# combine_html_for_dify.py (excerpt)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB limit

def html_to_text(html_content):
    ...
    # Uses BeautifulSoup to parse HTML, remove script/style, extract text.

def combine_html_files(input_dir, output_prefix="knowledge"):
    ...
    # Iterates over all .html/.htm files in `input_dir`.
    # Converts them to text, concatenates to a buffer.
    # Splits output into multiple files if size > MAX_FILE_SIZE.

def main():
    input_dir = "downloaded_pages"
    output_prefix = "knowledge"
    combine_html_files(input_dir, output_prefix)

if __name__ == "__main__":
    main()
```

### Notes

- The script **ignores** non-HTML files.
- If your HTML uses unusual encoding or includes dynamic JavaScript-rendered content, you may need additional handling (e.g., [Selenium](https://www.selenium.dev/)).
- Tweak the text cleaning logic if you want to remove or keep more HTML elements.

## Contributing

Feel free to open an issue or PR if you find a bug or want to enhance this script. Contributions are welcome.

## License

This project is licensed under the [MIT License](LICENSE).  
Please see the [LICENSE](LICENSE) file for details.

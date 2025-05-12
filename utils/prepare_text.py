import re
import html

def strip_markdown_fences(text: str) -> str:
    """
    Remove a leading ```markdown (and optional newline)
    and a trailing ``` (and optional preceding newline)
    """
    # Remove leading ```markdown plus any whitespace and a single newline
    #text = re.sub(r'^`+(?:markdown)?\s*\n?', '', text)
    text = re.sub(r'^`+(?:[^\s`]+)?\s*\n?', '', text)
    # Remove trailing ``` plus any leading newline
    text = re.sub(r'\n?`+$', '', text)
    return text

def escape_backticks(text: str) -> str:
    """
    HTML-escape the text, then replace each backtick (`) with its entity
    so that when you insert into Quill with dangerouslyPasteHTML
    it will render the literal backticks.
    """
    # First HTML-escape &, <, >, etc.
    escaped = html.escape(text)
    # Then turn each backtick into the numeric entity
    return text# escaped.replace('`', '')

if __name__ == "__main__":

    text = "````markdown\nПривет привет!!!\n452345````````\n"

    #text = re.sub(r'^`+(?:markdown)?\s*\n?', '', text)
    text = strip_markdown_fences(text)

    print(text)
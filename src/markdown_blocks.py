from htmlnode import *
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

def markdown_to_blocks(markdown):
	lines = markdown.split("\n\n")
	filtered_blocks =[]
	for line in lines:
		if line == '':
			continue
		block = line.strip()
		filtered_blocks.append(block)
	
	return filtered_blocks

def block_to_block_type(block):
    lines = block.split("\n")

    if (
        block.startswith("# ")
        or block.startswith("## ")
        or block.startswith("### ")
        or block.startswith("#### ")
        or block.startswith("##### ")
        or block.startswith("###### ")
    ):
        return block_type_heading
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return block_type_code
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return block_type_paragraph
        return block_type_quote
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return block_type_paragraph
        return block_type_unordered_list
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return block_type_paragraph
        return block_type_unordered_list
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return block_type_paragraph
            i += 1
        return block_type_ordered_list
    return block_type_paragraph

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)

    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    
    if block_type == block_type_quote:
        return quote_to_html(block)
    if block_type == block_type_unordered_list:
        return unordered_list_to_html(block)
    if block_type == block_type_ordered_list:
        return ordered_list_to_html(block)
    if block_type == block_type_code:
        return code_to_html(block)
    if block_type == block_type_heading:
        return heading_to_html(block)
    if block_type == block_type_paragraph:
        return paragraph_to_html(block)
    raise ValueError(f"Invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children         

def paragraph_to_html(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html(block):
    count = block.count("#")
    block = block.strip("# ")

    children = text_to_children(block)

    return ParentNode(f"h{count}", children)

def code_to_html(block):
    text = block
    text = text.strip("```").strip()
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])

def ordered_list_to_html(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))

    return ParentNode("ol", html_items)

def unordered_list_to_html(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))

    return ParentNode("ul",html_items)

def quote_to_html(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
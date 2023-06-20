import sys

# Generates txt file of n lines consisting of "line_content"
if __name__ == '__main__':
    n_lines = int(sys.argv[1]) - 3
    depth = int(sys.argv[2])
    tag_content = sys.argv[3]
    element_lines = n_lines/depth
    child_delimiters = [element_lines]
    for level in range(depth - 1):
        element_lines = element_lines/depth
        child_delimiters.append(element_lines)
    try:
        with open(f"{n_lines+3}_{tag_content}_{len(tag_content) + 7}.xml", "w", encoding="utf-8") as file:
            file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            file.write(f"<sett{tag_content}>\n")
            for line in range(n_lines):
                file.write(f"<a>{tag_content}</a>\n")
            file.write(f"</sett{tag_content}>")
    except OSError:
        content_name=tag_content[0:10]+f"_{len(tag_content) + 7}"
        with open(f"{n_lines}_{content_name}.xml", "w", encoding="utf-8") as file:
            file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            file.write(f"<sett{tag_content}>\n")
            for line in range(n_lines):
                file.write(f"<a>{tag_content}</a>\n")
            file.write(f"</sett{tag_content}>")

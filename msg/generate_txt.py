import sys

# Generates txt file of n lines consisting of "line_content"
if __name__ == '__main__':
    n_lines = int(sys.argv[1])
    line_content = sys.argv[2]
    try:
        with open(f"{n_lines}_{line_content}.txt", "a", encoding="utf-8") as file:
            for line in range(n_lines-1):
                file.write(f"{line_content}\n")
            file.write(f"{line_content}")
    except OSError:
        content_name=line_content[0:10]+f"_{len(line_content)}"
        with open(f"{n_lines}_{content_name}.txt", "a", encoding="utf-8") as file:
            for line in range(n_lines-1):
                file.write(f"{line_content}\n")
            file.write(f"{line_content}")

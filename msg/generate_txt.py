import sys

# Generates txt file of n lines consisting of "line_content"
if __name__ == '__main__':
    n_lines = int(sys.argv[1])
    line_content = sys.argv[2]

    with open(f"{n_lines}_{line_content}.txt", "a", encoding="utf-8") as file:
        for line in range(n_lines-1):
            file.write(f"{line_content}\n")
        file.write(f"{line_content}")

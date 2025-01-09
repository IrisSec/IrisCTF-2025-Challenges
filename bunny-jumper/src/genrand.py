# https://github.com/jagrutipatilp/daa/blob/main/huffman.py

from collections import deque
import random
import sys

bit_path_table = "0123456789ABCDEF"


class Node:
    def __init__(self, char, freq):
        self.char = char  # Character (None for internal nodes)
        self.freq = freq  # Frequency of the character
        self.left = None  # Left child (for internal nodes)
        self.right = None  # Right child (for internal nodes)
        self.parent = None  # Parent (calculated later)
        #
        self.bit_path = ""  # Which bits to use to get to this node (calc'd later)
        self.next_path = ""  # Absolute path to next node (calc'd later)
        self.next_bit_path = ""  # Next node's bit path (calc'd later)
        self.next_cond = ""  # Condition to jump to next cond node (calc'd later)
        self.next_cond_path = ""  # Absolute path to next node (calc'd later)
        self.next_cond_bit_path = ""  # Next node's bit path (calc'd later)
        self.call_type = ""  # Is next node a call or return? (calc'd later)
        self.call_ret_path = ""
        self.call_ret_bit_path = ""


def build_huffman_tree(freq_map):
    # Step 1: Create leaf nodes from the frequency map
    nodes = []
    for char, freq in freq_map.items():
        nodes.append(Node(char, freq))

    # Step 2: Build the Huffman tree by merging nodes
    while len(nodes) > 1:
        # Sort the nodes based on frequency (ascending order)
        nodes.sort(key=lambda node: node.freq)

        # Take two nodes with the smallest frequencies
        if random.randint(0, 1) == 0:
            left = nodes.pop(0)
            right = nodes.pop(0)
        else:
            right = nodes.pop(0)
            left = nodes.pop(0)

        # Merge two nodes into one
        merged = Node(
            None, left.freq + right.freq
        )  # New internal node with combined frequency
        merged.left = left
        merged.right = right

        # Add the merged node back to the list of nodes
        nodes.append(merged)

    # The last remaining node is the root of the Huffman tree
    return nodes[0]  # Return the root of the Huffman tree


def generate_codes(node, current_code, codes):
    if node is None:
        return

    if node.char is not None:  # If it's a leaf node
        codes[node.char] = current_code

    # Traverse left and right subtrees
    generate_codes(node.left, current_code + "0", codes)
    generate_codes(node.right, current_code + "1", codes)


def encode(input_string, huffman_codes):
    encoded_str = ""
    for char in input_string:
        encoded_str += huffman_codes[char]
    return encoded_str


def decode(encoded_str, root):
    decoded_str = ""
    current_node = root
    for bit in encoded_str:
        if bit == "0":
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.char is not None:  # Leaf node
            decoded_str += current_node.char
            current_node = root  # Reset to root for the next character

    return decoded_str


# #################


def assign_parents(node: Node):
    if node.left is not None:
        node.left.parent = node
        assign_parents(node.left)

    if node.right is not None:
        node.right.parent = node
        assign_parents(node.right)


def build_bit_path(node: Node):
    choices = list(bit_path_table)
    cur_bit_path = ""
    if node.parent != None:
        cur_bit_path = node.parent.bit_path
        for c in list(node.parent.bit_path):
            choices.remove(c)

    if len(choices) == 0:
        raise Exception("nooo!! out of depth")

    c = random.choice(choices)
    node.bit_path = cur_bit_path + c

    if node.left is not None:
        assert node.left.parent == node
        build_bit_path(node.left)

    if node.right is not None:
        assert node.right.parent == node
        build_bit_path(node.right)


def get_node_from_path(root: Node, path: str):
    n = root
    for c in path:
        if c == "0":
            n = n.left
        elif c == "1":
            n = n.right
        else:
            raise Exception("no")

    return n


def get_path_between_nodes(path_a: str, path_b: str):
    path = ""
    # come out
    while not path_b.startswith(path_a):
        path += "."
        path_a = path_a[:-1]

    # go in
    path += path_b[len(path) :]
    return path


def make_parent_path_list_for_label(in_label: str):
    if in_label == "":
        return [""]

    path = [in_label]
    while len(in_label) > 0:
        if in_label[-1] == "0":
            # in_label = in_label[:-1]  # remove 0 and continue
            in_label = in_label[:-1]  # remove 0 and add to list
            path.append(in_label)
        elif in_label[-1] == "1":
            in_label = in_label[:-1]  # remove 1 and add to list
            path.append(in_label)

    if path[-1] != "":
        path.append("")

    return path[::-1]


def get_encoded_path(next_path: str, next_bit_path: str, in_label: str):
    parent_path_current = make_parent_path_list_for_label(in_label)
    parent_path_next = make_parent_path_list_for_label(next_path)
    if len(parent_path_next) > 0:
        # strip last item since that path is only for descendants
        parent_path_next = parent_path_next[:-1]

    connect_idx_current = len(parent_path_current) - 2
    connect_idx_next = 0
    while connect_idx_current > 0:
        connect_point = parent_path_current[connect_idx_current]
        if connect_point in parent_path_next:
            connect_idx_next = parent_path_next.index(connect_point)
            if connect_idx_next > 0:
                connect_idx_next -= 1

            break

        connect_idx_current -= 1

    next_label = parent_path_current[connect_idx_current]
    if next_label == "":
        next_label = "label_top"  # could also just be label_R
    else:
        next_label = f"label_R{next_label}"

    path_v = 0
    path_v_i = 0
    for c in next_path:
        if c == "1":
            path_v |= 1 << path_v_i

        path_v_i += 1

    # random value is fine as we'll overwrite all values that don't matter
    # we start at connect_idx_next and leave the previous bits random
    path_v2 = random.randint(0, 0xFFFF)
    # for i in range(len(next_bit_path)):
    for i in range(connect_idx_next, len(next_bit_path), 1):
        bit_pos = bit_path_table.index(next_bit_path[i])
        bit_set = (path_v >> i) & 1
        if bit_set == 1:
            path_v2 |= 1 << bit_pos
        else:
            path_v2 &= ~(1 << bit_pos)

    return (path_v2, next_label)


def build_js(node: Node, path: str, in_label: str, depth: int):
    ident = "  " * depth
    if node.char is not None:
        # leaf node

        print(f"{ident}// at label {in_label}")
        print(f"{ident}// next path {node.next_path}")
        #print(f"{ident}console.log('at label {in_label}');")
        if node.next_path == "":
            print(ident + node.char)
            print(f"{ident}break label_top;")
        else:
            if node.next_cond != "":
                (next_cond_path_val, next_cond_label) = get_encoded_path(
                    node.next_cond_path, node.next_cond_bit_path, in_label
                )
                (next_path_val, next_label) = get_encoded_path(
                    node.next_path, node.next_bit_path, in_label
                )
                print(ident + node.char)
                cond_diff = next_cond_path_val - next_path_val
                print(f"{ident}__ = {node.next_cond} * {cond_diff} + {next_path_val};")
                # todo: obfuscate this if statement
                print(
                    f"{ident}if (__ == {next_path_val}) continue {next_label}; continue {next_cond_label};"
                )
            elif node.call_type == "ret":
                print(f"{ident}__ = _cs.pop();")
                print(f"{ident}continue label_top;")
            else:
                (next_path_val, label_to_cont_to) = get_encoded_path(
                    node.next_path, node.next_bit_path, in_label
                )
                (next_ret_path_val, _) = get_encoded_path(
                    node.call_ret_path, node.call_ret_bit_path, ""
                )
                print(ident + node.char)
                if node.call_type == "call":
                    print(f"{ident}_cs.push({next_ret_path_val});")

                print(f"{ident}__ = {next_path_val};")
                print(f"{ident}continue {label_to_cont_to};")
    else:
        # non-leaf node
        print(f"{ident}label_{path}1: while (true) {{")
        bit_path_bit_idx = bit_path_table.index(node.bit_path[-1])
        print(f"{ident}  if ((__ & {2**bit_path_bit_idx}) == 0) {{")
        print(f"{ident}    __ &= 0xFFFF;")
        print(f"{ident}    break label_{path}1;")
        print(f"{ident}  }}")
        print(f"{ident}  ")
        build_js(node.right, path + "1", path[1:] + "1", depth + 1)
        #
        print(f"{ident}}}")
        print(f"{ident}label_{path}0: while (true) {{")
        # bit_path_bit_idx = bit_path_table.index(node.bit_path[-1])
        # print(f"{ident}  if ((__ & {2**bit_path_bit_idx}) == 0) {{")
        # print(f"{ident}    __ &= 0xFFFF;")
        # print(f"{ident}    break label_{path};")
        # print(f"{ident}  }}")
        # print(f"{ident}  ")
        build_js(node.left, path + "0", path[1:] + "0", depth + 1)
        print(f"{ident}}}")


lines = []
vardefs = []
with open(sys.argv[1], "r", encoding="utf-8") as f:
    rlines = f.readlines()
    for line in rlines:
        if line.startswith("var"):
            vardefs.append(line.rstrip("\n"))
        elif line.startswith("//"):
            pass
        elif line.strip() == "":
            pass
        else:
            lines.append(line.strip())

line_jumps = {}
labels = {}

# collect labels and make lines unique
for i in range(len(lines)):
    line = lines[i]

    line_jump = None
    if line.startswith("/**@cndjmp "):
        cndstr = ""
        idx = 11
        while idx < len(line) - 1:
            if line[idx] == "*" and line[idx + 1] == "/":
                idx += 2
                if len(line) > idx and line[idx] == " ":
                    idx += 1

                break
            else:
                cndstr += line[idx]

            idx += 1

        line = line[idx:]
        last_cndstr_space_idx = cndstr.rindex(" ")
        jmpdst = cndstr[last_cndstr_space_idx + 1 :]
        cndstr = cndstr[0:last_cndstr_space_idx]
        line_jump = (jmpdst, cndstr, "cond")
    elif line.startswith("/**@jmp ") or line.startswith("/**@call "):
        jmptyp = "uncond" if line.startswith("/**@jmp ") else "call"
        jmpdst = ""
        idx = 8 if line.startswith("/**@jmp ") else 9
        while idx < len(line) - 1:
            if line[idx] == "*" and line[idx + 1] == "/":
                idx += 2
                if len(line) > idx and line[idx] == " ":
                    idx += 1

                break
            else:
                jmpdst += line[idx]

            idx += 1

        line = line[idx:]
        line_jump = (jmpdst, None, jmptyp)
    elif line.startswith("/**@ret */"):
        line = line[10:]
        line_jump = (None, None, "ret")

    # uniquify each line
    line_new = f"{line} // l{i}"

    if line_jump is not None:
        line_jumps[line_new] = line_jump

    if "//: " in line:
        lbl_idx = line.index("//: ") + 4
        lbl = line[lbl_idx:]
        labels[lbl] = line_new

    lines[i] = line_new

# spread out lines randomly
random.seed(12345)
freq_map = {}
for line in lines:
    r = random.randint(0, 99)
    if r < 70:
        freq_map[line] = 1
    elif r < 85:
        freq_map[line] = 2
    else:
        freq_map[line] = 3

# build huffman tree
root = build_huffman_tree(freq_map)
assign_parents(root)
build_bit_path(root)

# generate huffman codes
huffman_codes = {}
generate_codes(root, "", huffman_codes)

# do silly stuff
print(line_jumps)
for line_idx in range(len(lines) - 1):
    line = lines[line_idx]
    if line in line_jumps:
        (jmpdst, cndstr, typ) = line_jumps[line]
        if typ == "cond" and cndstr is not None:
            print("processing cond", line)
            # conditional jump
            path_a = huffman_codes[lines[line_idx]]
            path_b = huffman_codes[lines[line_idx + 1]]
            path_c = huffman_codes[labels[jmpdst]]
            node_a = get_node_from_path(root, path_a)
            node_b = get_node_from_path(root, path_b)
            node_c = get_node_from_path(root, path_c)
            #
            node_a.next_path = path_b
            node_a.next_bit_path = node_b.bit_path
            node_a.next_cond = cndstr
            node_a.next_cond_path = path_c
            node_a.next_cond_bit_path = node_c.bit_path
        elif typ == "uncond":
            print("processing uncond", line)
            # unconditional jump
            path_a = huffman_codes[lines[line_idx]]
            path_b = huffman_codes[labels[jmpdst]]
            node_a = get_node_from_path(root, path_a)
            node_b = get_node_from_path(root, path_b)
            #
            node_a.next_path = path_b
            node_a.next_bit_path = node_b.bit_path
        elif typ == "call":
            print("processing call", line)
            # call
            path_a = huffman_codes[lines[line_idx]]
            path_b = huffman_codes[lines[line_idx + 1]]
            path_z = huffman_codes[labels[jmpdst]]
            node_a = get_node_from_path(root, path_a)
            node_b = get_node_from_path(root, path_b)
            node_z = get_node_from_path(root, path_z)
            #
            node_a.next_path = path_z
            node_a.next_bit_path = node_z.bit_path
            node_a.call_type = "call"
            node_a.call_ret_path = path_b
            node_a.call_ret_bit_path = node_b.bit_path
        elif typ == "ret":
            print("processing ret", line)
            # return
            path_a = huffman_codes[lines[line_idx]]
            node_a = get_node_from_path(root, path_a)
            #
            node_a.next_path = path_a  # this does nothing
            node_a.next_bit_path = node_a.bit_path  # ...
            node_a.call_type = "ret"
        else:
            raise Exception("impossible")
    else:
        print("processing normal line", line)
        # next instruction
        path_a = huffman_codes[lines[line_idx]]
        path_b = huffman_codes[lines[line_idx + 1]]
        node_a = get_node_from_path(root, path_a)
        node_b = get_node_from_path(root, path_b)
        #
        node_a.next_path = path_b
        node_a.next_bit_path = node_b.bit_path


first_path = huffman_codes[lines[0]]
first_node: Node = get_node_from_path(root, huffman_codes[lines[0]])

print("")
print(f"var __ = {get_encoded_path(first_path, first_node.bit_path, '')[0]};")
print(f"var _cs = [];")
for vardef in vardefs:
    print(vardef)

print("label_top: while (true) {")
build_js(root, "R", "", 1)
print("}")

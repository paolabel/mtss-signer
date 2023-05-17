from typing import List, Tuple

from xml.etree import ElementTree

# Contains functions for opening message files and writing their signature
# or correction to files, as well as building blocks from their content or
# rebuilding the message from the generated blocks according to file type

def __get_message_and_blocks_from_txt_file(txt_file_path: str) -> Tuple[str, List[str]]:
    with open(txt_file_path, "r") as txt_file:
        message: str = txt_file.read()
    return (message, message.split("\n"))

def __rebuild_txt_content_from_blocks(blocks: List[str]) -> str:
    return "\n".join(blocks)

def __get_message_and_blocks_from_xml_file(xml_file_path: str) -> Tuple[str, List[str]]:
    with open(xml_file_path, "r") as xml_file:
        message: str = xml_file.read()
    ElementTree.fromstring(message)
    message = message.replace("\n", "")
    message = message.replace("\t", "")
    delimiter = "<"
    blocks = [delimiter+block for block in message.split(delimiter)]
    index = 1
    grouped_blocks = [blocks[1]]
    while index < len(blocks[1:]):
        if blocks[index][:2] == "</" and blocks[index+1][:2] == "</":
            grouped_blocks.append(blocks[index].rstrip())
            grouped_blocks.append(blocks[index+1].rstrip())
            index +=2
        elif blocks[index+1][:2] == "</":
            grouped_tag = blocks[index]+blocks[index+1]
            grouped_blocks.append(grouped_tag.rstrip())
            index+=2
        else:
            grouped_blocks.append(blocks[index].rstrip())
            index +=1
    return (message, grouped_blocks)

def __rebuild_xml_content_from_blocks(blocks: List[str], ignore_identation=True) -> str:
    unindented_xml = "".join(blocks)
    if ignore_identation:
        return unindented_xml
    else:
        xml_tree = ElementTree.fromstring(unindented_xml)
        xml_tree = ElementTree.indent(xml_tree, space="\t\t")
        return ElementTree.tostring(xml_tree)

def rebuild_content_from_blocks(blocks: List[str], file_type:str) -> str:
    if file_type == "txt":
        content= __rebuild_txt_content_from_blocks(blocks)
    elif file_type == "xml":
        content = __rebuild_xml_content_from_blocks(blocks)
    else:
        raise Exception("Unsupported file type (must be txt or xml)")
    return content

def get_message_and_blocks_from_file(message_file_path: str) -> Tuple[str, List[str]]:
    file_type = message_file_path[-3:]
    if file_type == "txt":
        message, blocks= __get_message_and_blocks_from_txt_file(message_file_path)
    elif file_type == "xml":
        message, blocks = __get_message_and_blocks_from_xml_file(message_file_path)
    else:
        raise Exception("Unsupported file type (must be txt or xml)")
    return (message, blocks)

def get_signature_file_path(message_file_path: str) -> str:
    return message_file_path.rsplit(".", 1)[0] + "_signature.mts"

def get_correction_file_path(message_file_path:str) -> str:
    file_type = message_file_path[-3:0]
    return message_file_path.rsplit(".", 1)[0] + f"_corrected.{file_type}"

def write_signature_to_file(signature: bytearray, message_file_path: str):
    signature_file_path = get_signature_file_path(message_file_path)
    with open(signature_file_path, "wb") as signature_file:
        signature_file.write(signature)

def write_correction_to_file(message_file_path: str, content: str):
    correction_file_path = get_correction_file_path(message_file_path)
    with open(correction_file_path, "w") as correction_file:
        correction_file.write(content)
        
# Returns smaller blocks to allow correction of the blocks
# Wouldn't work unless the modifications maintain the original number of characters
#
# MAX_CHARACTERS_PER_BLOCK = 3
#
# def get_smaller_blocks(blocks: List[str]):
#     halved_blocks = list()
#     for block in blocks:
#         new_block_length = int(ceil(len(block)/2))
#         first_half = block[:new_block_length]
#         second_half = block[new_block_length:]
#         if len(first_half) > 0:
#             halved_blocks.append(first_half)
#         if len(second_half) > 0:
#             halved_blocks.append(second_half)
#     stop_halving = True
#     for halved_block in halved_blocks:
#         if len(halved_block) > MAX_CHARACTERS_PER_BLOCK:
#             stop_halving = False
#             break
#     if stop_halving:
#         return halved_blocks
#     else:
#         return get_smaller_blocks(halved_blocks)

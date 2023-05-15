from typing import List, Tuple

from numpy import ceil

from xml.etree import ElementTree

MAX_CHARACTERS_PER_BLOCK = 3

def get_message_and_blocks_from_txt_file(txt_file_path: str) -> Tuple[str, List[str]]:
    with open(txt_file_path, "r") as txt_file:
        message: str = txt_file.read()
    return (message, message.split("\n"))

def get_message_and_blocks_from_xml_file(xml_file_path: str, ignore_identation: bool = False) -> Tuple[str, List[str]]:
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

def get_message_and_blocks_from_file(message_file_path: str) -> Tuple[str, List[str]]:
    file_type = message_file_path[-3:]
    if file_type == "txt":
        message, blocks= get_message_and_blocks_from_txt_file(message_file_path)
    elif file_type == "xml":
        message, blocks = get_message_and_blocks_from_xml_file(message_file_path)
    else:
        raise Exception("Unsupported file type (must be txt or xml)")
    return (message, blocks)

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

def write_signature_to_file(signature: bytearray, message_file_path: str):
    signature_file_path = message_file_path.rsplit(".", 1)[0] + "_signature.mts"
    with open(signature_file_path, "wb") as signature_file:
        signature_file.write(signature)

def write_correction_to_file(message_file_path: str, content: str, file_type: str):
    if file_type != "txt" or file_type != "xml":
        raise Exception("Wrong file type")
    correction_file_path = message_file_path.rsplit(".", 1)[0] + f"_corrected.{file_type}"
    with open(correction_file_path, "w") as correction_file:
        correction_file.write(content)

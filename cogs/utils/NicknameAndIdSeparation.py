def nickname_and_id_separation(content: str):
    punctuation = [
    "!", "\"", "#", "$", "%", "&", "'", "(", ")", "*", "+", ",",
    "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "\\",
    "]", "^", "_", "`", "{", "|", "}", "~", ' ', '\n'
    ]

    space_symbols = [" ", "\n"]

    nicknames = []
    identifiers = []

    new_content = ""
    content_len = len(content)
    for index in range(content_len):
        if content[index] in punctuation:
            if 0 < index < content_len - 1:
                if content[index] == ',':
                    new_content += " "
                elif content[index - 1] not in punctuation and content[index + 1] not in punctuation or \
                   content[index] in space_symbols:
                    new_content += content[index]
        else:
            new_content += content[index]

    without_comma = new_content.split()

    for i in range(0, len(without_comma)):
        if i % 2 == 0:
            nicknames.append(without_comma[i])
        else:
            identifiers.append(without_comma[i])

    nicknames_str = ""
    identifiers_str = ""

    for i in nicknames:
        nicknames_str += f"{i}\n"

    for i in identifiers:
        identifiers_str += f"<@{i}>\n"

    return nicknames_str, identifiers_str


def link_plus_nickname_and_id(content: str):
    punctuation = [
    "!", "\"", "#", "$", "%", "&", "'", "(", ")", "*", "+", ",",
    "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "\\",
    "]", "^", "_", "`", "{", "|", "}", "~", ' ', '\n'
    ]

    space_symbols = [" ", "\n"]

    nicknames = []
    identifiers = []

    new_content = ""
    content_len = len(content)
    for index in range(content_len):
        if content[index] in punctuation:
            if 0 < index < content_len - 1:
                if content[index] == ',':
                    new_content += " "
                elif content[index - 1] not in punctuation and content[index + 1] not in punctuation or \
                   content[index] in space_symbols:
                    new_content += content[index]
        else:
            new_content += content[index]

    without_comma = new_content.split()

    for i in range(0, len(without_comma)):
        if i % 2 == 0:
            nicknames.append(without_comma[i])
        else:
            identifiers.append(without_comma[i])

    result = ""

    for i in range(0, len(nicknames)):
        result += f"<@{identifiers[i]}> ({nicknames[i]} - {identifiers[i]})\n"

    return result

def nicknames_to_string(content: str):
    result = ""
    without_comma = content.split()

    for i in without_comma:
        result += f"{i}\n"

    return result
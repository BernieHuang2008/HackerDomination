import re


def parse_tag(tag: str) -> list:
    """
    Parse the tag to a list of infos.

    Args:
        tag (str): The tag string.

    Returns:
        list: [tagname: str, params: dict, children: list].
    """
    tag = tag.strip()
    taginfo = tag.split(" ", 1)
    tagname = taginfo[0]
    params = taginfo[1] if len(taginfo) == 2 else ""
    params = params.strip()
    params = re.findall(r"(\w+)=[\"\'](.+?)[\"\']", params)
    params = {k: v for k, v in params}
    return [tagname, params, []]  # [tagname, params, children]


def parse(xml: str) -> list:
    """
    Parse the xml to a dict.

    Args:
        xml (str): The xml text.

    Returns:
        list: all childrens
    """
    xml_tag = r"<(.+?)>"

    starttag = re.search(xml_tag, xml)

    if not starttag:
        return {"tag": "text", "params": {}, "content": xml}, 0, len(xml)

    tag1 = starttag
    stack = [["xmlroot", {}, []]]
    first_loop = True
    root_children = []

    while xml:
        # tag details
        tag = tag1.group(1).strip()
        start = tag1.start()
        end = tag1.end()
        children = stack[-1][2]

        # self-closing tag
        if tag.endswith("/"):
            # prev text content
            if xml[:start].strip():
                children.append({"tag": "text", "params": {}, "content": xml[:start]})

            # this tag
            taginfo = parse_tag(tag[:-1])
            children.append({"tag": taginfo[0], "params": taginfo[1], "content": None})

            # cut xml
            xml = xml[end:]

        # closing tag
        elif tag.startswith("/"):
            # prev text content
            if xml[:start].strip():
                children.append({"tag": "text", "params": {}, "content": xml[:start]})

            # this tag
            taginfo = stack.pop()
            children = stack[-1][2]
            children.append({"tag": taginfo[0], "params": taginfo[1], "content": taginfo[2]})

            # cut xml
            xml = xml[end:]

        # opening tag
        else:
            # prev text content
            if xml[:start].strip():
                children.append({"tag": "text", "params": {}, "content": xml[:start]})

            # this tag
            taginfo = parse_tag(tag)
            stack.append(taginfo)

            # cut xml
            xml = xml[end:]

        # next tag
        tag1 = re.search(xml_tag, xml)

    return stack[-1][2]

import xml.etree.ElementTree as ET


def get_text(root, tag_name):
    node = root.find(f".//{tag_name}")
    if node is not None and node.text:
        return node.text.strip()
    return None


def parse_wa_legislature_xml(xml_text: str):
    root = ET.fromstring(xml_text)

    metadata = {
        "bill_id": get_text(root, "BillId"),
        "bill_number": get_text(root, "BillNumber"),
        "short_description": get_text(root, "ShortDescription"),
        "long_description": get_text(root, "LongDescription"),
        "legal_title": get_text(root, "LegalTitle"),
        "current_status": get_text(root, "CurrentStatus"),
        "sponsor": get_text(root, "Sponsor"),
        "introduced_date": get_text(root, "IntroducedDate"),
    }

    text_blocks = []
    for key, value in metadata.items():
        if value:
            text_blocks.append({
                "kind": key,
                "text": value
            })

    return {
        "sourceSystem": "wa_legislature",
        "sourceType": "xml",
        "documentMetadata": metadata,
        "textBlocks": text_blocks
    }


def normalized_text_from_blocks(normalized: dict) -> str:
    lines = []
    for block in normalized.get("textBlocks", []):
        kind = block["kind"]
        text = block["text"]
        lines.append(text)
    return "\n".join(lines)

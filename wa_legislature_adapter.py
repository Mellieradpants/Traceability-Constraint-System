
import xml.etree.ElementTree as ET


def strip_namespace(tag: str) -> str:
    if "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def xml_to_dict(element):
    children = list(element)

    if not children:
        text = (element.text or "").strip()
        return text if text else None

    result = {}
    for child in children:
        key = strip_namespace(child.tag)
        value = xml_to_dict(child)

        if key in result:
            if not isinstance(result[key], list):
                result[key] = [result[key]]
            result[key].append(value)
        else:
            result[key] = value

    return result


def normalize_legislation_record(record: dict):
    text_blocks = []

    field_map = [
        ("BillId", "bill_id"),
        ("BillNumber", "bill_number"),
        ("ShortDescription", "short_description"),
        ("LongDescription", "long_description"),
        ("LegalTitle", "legal_title"),
        ("CurrentStatus", "current_status"),
        ("Sponsor", "sponsor"),
        ("IntroducedDate", "introduced_date"),
    ]

    metadata = {}

    for source_key, normalized_key in field_map:
        value = record.get(source_key)
        if value:
            metadata[normalized_key] = value
            text_blocks.append({
                "kind": normalized_key,
                "text": str(value).strip()
            })

    return {
        "sourceSystem": "wa_legislature",
        "sourceType": "soap_xml",
        "documentMetadata": metadata,
        "textBlocks": text_blocks
    }


def parse_wa_legislature_xml(xml_text: str):
    root = ET.fromstring(xml_text)
    data = xml_to_dict(root)

    # This part may need adjustment depending on the exact SOAP shape
    # We try to locate a legislation-style record anywhere in the tree.
    def find_first_legislation_record(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key.lower() in {"legislation", "legislationinfo", "bill"}:
                    return value
                found = find_first_legislation_record(value)
                if found:
                    return found
        elif isinstance(obj, list):
            for item in obj:
                found = find_first_legislation_record(item)
                if found:
                    return found
        return None

    record = find_first_legislation_record(data)

    if not record:
        return {
            "sourceSystem": "wa_legislature",
            "sourceType": "soap_xml",
            "documentMetadata": {},
            "textBlocks": []
        }

    if isinstance(record, list):
        record = record[0]

    return normalize_legislation_record(record)


def normalized_text_from_blocks(normalized: dict) -> str:
    lines = []

    for block in normalized.get("textBlocks", []):
        kind = block.get("kind", "text")
        text = block.get("text", "").strip()
        if text:
            lines.append(f"{kind}: {text}")

    return "\n".join(lines)

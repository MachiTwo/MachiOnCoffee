import os
import json
import xml.etree.ElementTree as ET
from pathlib import Path

# Configurações
SOURCE_DIR = Path("data/api_sources")
OUTPUT_BASE_DIR = Path("data/api")

def parse_xml(xml_path):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        data = {
            "name": root.attrib.get("name", ""),
            "inherits": root.attrib.get("inherits", ""),
            "brief_description": root.findtext("brief_description", "").strip(),
            "description": root.findtext("description", "").strip(),
            "properties": [],
            "methods": [],
            "signals": [],
            "constants": []
        }

        # Membros (Propriedades)
        members = root.find("members")
        if members is not None:
            for member in members.findall("member"):
                data["properties"].append({
                    "name": member.attrib.get("name", ""),
                    "type": member.attrib.get("type", ""),
                    "setter": member.attrib.get("setter", ""),
                    "getter": member.attrib.get("getter", ""),
                    "default": member.attrib.get("default", ""),
                    "description": member.text.strip() if member.text else ""
                })

        # Métodos
        methods = root.find("methods")
        if methods is not None:
            for method in methods.findall("method"):
                m_data = {
                    "name": method.attrib.get("name", ""),
                    "qualifiers": method.attrib.get("qualifiers", ""),
                    "description": method.findtext("description", "").strip(),
                    "return_type": "",
                    "params": []
                }

                ret = method.find("return")
                if ret is not None:
                    m_data["return_type"] = ret.attrib.get("type", "void")

                for param in method.findall("param"):
                    m_data["params"].append({
                        "name": param.attrib.get("name", ""),
                        "type": param.attrib.get("type", ""),
                        "default": param.attrib.get("default", "")
                    })

                data["methods"].append(m_data)

        # Sinais
        signals = root.find("signals")
        if signals is not None:
            for signal in signals.findall("signal"):
                s_data = {
                    "name": signal.attrib.get("name", ""),
                    "description": signal.findtext("description", "").strip(),
                    "params": []
                }
                for param in signal.findall("param"):
                    s_data["params"].append({
                        "name": param.attrib.get("name", ""),
                        "type": param.attrib.get("type", "")
                    })
                data["signals"].append(s_data)

        # Constantes
        constants = root.find("constants")
        if constants is not None:
            for constant in constants.findall("constant"):
                data["constants"].append({
                    "name": constant.attrib.get("name", ""),
                    "value": constant.attrib.get("value", ""),
                    "description": constant.text.strip() if constant.text else ""
                })

        return data
    except Exception as e:
        print(f"Erro ao processar {xml_path}: {e}")
        return None

def main():
    if not SOURCE_DIR.exists():
        print(f"Erro: Diretorio fonte {SOURCE_DIR} não encontrado.")
        return

    # Garantir pastas de saída
    (OUTPUT_BASE_DIR / "en").mkdir(parents=True, exist_ok=True)
    (OUTPUT_BASE_DIR / "pt").mkdir(parents=True, exist_ok=True)

    for xml_file in SOURCE_DIR.rglob("*.xml"):
        print(f"Processando {xml_file.name}...")
        class_data = parse_xml(xml_file)

        if class_data:
            filename = f"{class_data['name']}.json"

            # Salvar em EN
            with open(OUTPUT_BASE_DIR / "en" / filename, "w", encoding="utf-8") as f:
                json.dump(class_data, f, indent=4, ensure_ascii=False)

            # Salvar em PT (Cópia inicial)
            with open(OUTPUT_BASE_DIR / "pt" / filename, "w", encoding="utf-8") as f:
                json.dump(class_data, f, indent=4, ensure_ascii=False)

    print("Conversão concluída!")

if __name__ == "__main__":
    main()

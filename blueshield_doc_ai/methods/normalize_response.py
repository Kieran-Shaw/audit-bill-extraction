import pandas as pd
from google.cloud import documentai


class NormalizeResponse:
    def __init__(self, document_entities: documentai.Document.Entity):
        self.document_entities = document_entities

    def get_normal_entities_df(self):
        """Returns a DataFrame of the normalized entities."""
        normal_entities = [
            {
                "Text": entity.get("mentionText", ""),
                "Type": entity.get("type", ""),
                "Confidence": entity.get("confidence", 0),
            }
            for entity in self.document_entities
            if entity["type"] != "line_items"
        ]
        return pd.DataFrame(normal_entities)

    def get_line_items_df(self):
        """Returns a DataFrame of the line items with properties as horizontal columns."""
        line_items = []

        for entity in self.document_entities:
            if entity["type"] == "line_items":
                line_item_row = {
                    "Text": entity.get("mentionText", ""),
                    "Type": entity.get("type", ""),
                    "Confidence": entity.get("confidence", 0),
                }
                # Flatten properties
                for prop in entity.get("properties", []):
                    prop_key_prefix = prop.get("type", "Unknown")
                    line_item_row[f"{prop_key_prefix}_Text"] = prop.get(
                        "mentionText", ""
                    )
                    line_item_row[f"{prop_key_prefix}_Confidence"] = prop.get(
                        "confidence", 0
                    )
                    # Add more properties as needed

                line_items.append(line_item_row)

        return pd.DataFrame(line_items)

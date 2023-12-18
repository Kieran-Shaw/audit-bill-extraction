# Goal here is to see what we can do with the document entities
import json

from normalize_response import NormalizeResponse

json_file_path = (
    "/Users/kieranshaw/audit-bill-extraction/blueshield_doc_ai/document.json"
)

with open(json_file_path, "r") as file:
    document = json.load(file)

entities = document["entities"]

# instantiate class
normalizer = NormalizeResponse(document_entities=entities)

# normalize and save to dataframe
standard_df = normalizer.get_normal_entities_df()
line_items_df = normalizer.get_line_items_df()
# Save to csv file
standard_df.to_csv("standard_df.csv", index=False)
line_items_df.to_csv("line_items_df.csv", index=False)

# print df
print(standard_df)
print(line_items_df)

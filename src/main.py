from typing import Any, Dict
import yaml 

model_file = "../mdf/c3dc/c3dc-model.yml"

with open(model_file, "r", encoding="utf-8") as file:
    model = yaml.safe_load(file)

def initialize_schema_meta(model):

    registry_uri = "https://github.com/colemandevries/mdf-json-schema/schemas"
    schema_reference = 

    handle = model["Handle"]
    version = model["Version"]

    base_uri = f"{registry_uri}/{handle}/{version}"

    return base_uri, schema_reference

def main():
    base_uri, schema_reference = initialize_schema_meta(model)
    print(base_uri)
    print(schema_reference)




class MdfJsonSchema:
    def __init__(self, config: Dict[str, Any]):
        self.cfg = config
        self.schema_reference = None
        

    def _set_class_attributes(self):
        self.schema_ref = self.cfg.get("schema_reference", "https://json-schema.org/draft/2020-12/schema")

    

    




main()
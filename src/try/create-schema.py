from pydantic import BaseModel, Field, create_model
from typing import Dict, Any

# Map type strings to Pydantic types
TYPE_MAP = {
    "str": str,
    "int": int,
    "float": float,
    "bool": bool
}

def generate_pydantic_model(schema: Dict[str, Any]) -> type:
    fields = {}
    for name, props in schema["properties"].items():
        field_type = props["type"]
        description = props.get("description", "")
        default_value = "" if field_type == "str" else 0
        pydantic_field = Field(default_value, description=description)
        pydantic_type = TYPE_MAP.get(field_type)  # Use the mapped Pydantic type
        fields[name] = (pydantic_type, pydantic_field)

    required_fields = schema.get("required", [])
    pydantic_model = create_model(schema["title"], **fields)
    for field in required_fields:
        pydantic_model.__annotations__[field] = pydantic_model.__fields__[field].field_info.type_

    return pydantic_model

# Given JSON schema
schema = {
    "properties": {
        "Name": {
            "description": "Thajso",
            "type": "str"
        },
        "ID": {
            "description": "msfos",
            "type": "int"
        }
    },
    "required": ["Name", "ID"],
    "title": "DynamicSchema",
    "type": "object"
}

# Generate Pydantic model
DynamicModel = generate_pydantic_model(schema)

# Display the generated Pydantic model
print(DynamicModel)

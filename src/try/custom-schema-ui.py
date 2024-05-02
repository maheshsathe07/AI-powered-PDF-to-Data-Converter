import streamlit as st
from pydantic import create_model, Field
import json

st.title("Dynamic Pydantic Schema Generator")

num_fields = st.number_input("Number of Fields", min_value=1, value=1, step=1)

field_definitions = {}

for i in range(num_fields):
    st.write(f"### Field {i+1}")
    key = st.text_input(f"Key {i}", key=f"name_{i}")
    data_type = st.selectbox(f"Data Type {i}", ["str", "int", "float", "bool"], key=f"data_type_{i}")
    description = st.text_input(f"Description {i}", key=f"description_{i}")

    field_definitions[key] = (eval(data_type), description)  # Store field name, its corresponding type, and description

if st.button("Generate Schema"):
    # Create a dictionary of field names and their corresponding types with descriptions
    fields = {key: (data_type, Field(description=description)) for key, (data_type, description) in field_definitions.items()}
    
    # Create the Pydantic model dynamically
    DynamicSchema = create_model("DynamicSchema", **fields)
    
    # Get the schema
    schema = DynamicSchema.schema()

    # Remove the "title" field for each property in the "properties" section
    modified_properties = {key: {k: v for k, v in prop.items() if k != "title"} for key, prop in schema["properties"].items()}
    schema["properties"] = modified_properties

    # Show generated schema
    st.json(schema)


    
    
# import streamlit as st
# from pydantic import BaseModel, create_model, Field
# import json

# st.title("Dynamic Pydantic Schema Generator")

# num_fields = st.number_input("Number of Fields", min_value=1, value=1, step=1)

# field_definitions = {}

# for i in range(num_fields):
#     st.write(f"### Field {i+1}")
#     name = st.text_input(f"Name {i}", key=f"name_{i}")
#     data_type = st.selectbox(f"Data Type {i}", ["str", "int", "float", "bool"], key=f"data_type_{i}")
#     description = st.text_input(f"Description {i}", key=f"description_{i}")

#     field_definitions[name] = (eval(data_type), description)  # Store field name, its corresponding type, and description

# if st.button("Generate Schema"):
#     # Create a dictionary of field names and their corresponding types with descriptions
#     fields = {name: (data_type, Field(description=description)) for name, (data_type, description) in field_definitions.items()}
    
#     # Create the Pydantic model dynamically
#     DynamicSchema = create_model("DynamicSchema", **fields)
    
#     # Get the schema
#     schema = DynamicSchema.schema()

#     # Modify the schema to use "key" instead of "title" in properties
#     modified_properties = {}
#     for name, prop in schema["properties"].items():
#         modified_prop = prop.copy()  # Create a copy of the property to modify
#         modified_prop["key"] = name  # Rename "title" to "key" to match the field name
#         modified_properties[name] = modified_prop
    
#     schema["properties"] = modified_properties

#     # Show generated schema
#     st.json(schema)



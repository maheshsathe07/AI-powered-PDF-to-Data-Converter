# import streamlit as st
# from PIL import Image
# import streamlit_nested_layout
# from streamlit_sparrow_labeling import st_sparrow_labeling
# from streamlit_sparrow_labeling import DataProcessor
# import json
# import math
# import os
# from natsort import natsorted
# from tools import agstyler
# from tools.agstyler import PINLEFT
# import pandas as pd
# from toolbar_main import component_toolbar_main


# class DataAnnotation:
#     class Model:
#         pageTitle = "Data Annotation"

#         img_file = None
#         rects_file = None
#         labels_file = "docs/labels.json"
#         groups_file = "docs/groups.json"

#         assign_labels_text = "Assign Labels"
#         text_caption_1 = "Check 'Assign Labels' to enable editing of labels and values, move and resize the boxes to annotate the document."
#         text_caption_2 = "Add annotations by clicking and dragging on the document, when 'Assign Labels' is unchecked."

#         labels = ["", "invoice_no", "invoice_date", "seller", "client", "seller_tax_id", "client_tax_id", "iban", "item_desc",
#                   "item_qty", "item_net_price", "item_net_worth", "item_vat", "item_gross_worth", "total_net_worth", "total_vat",
#                   "total_gross_worth"]

#         groups = ["", "items_row1", "items_row2", "items_row3", "items_row4", "items_row5", "items_row6", "items_row7",
#                   "items_row8", "items_row9", "items_row10", "summary"]

#         selected_field = "Selected Field: "
#         save_text = "Save"
#         saved_text = "Saved!"

#         subheader_1 = "Select"
#         subheader_2 = "Upload"
#         annotation_text = "Annotation"
#         no_annotation_file = "No annotation file selected"
#         no_annotation_mapping = "Please annotate the document. Uncheck 'Assign Labels' and draw new annotations"

#         download_text = "Download"
#         download_hint = "Download the annotated structure in JSON format"

#         annotation_selection_help = "Select an annotation file to load"
#         upload_help = "Upload a file to annotate"
#         upload_button_text = "Upload"
#         upload_button_text_desc = "Choose a file"

#         assign_labels_text = "Assign Labels"
#         assign_labels_help = "Check to enable editing of labels and values"

#         export_labels_text = "Export Labels"
#         export_labels_help = "Create key-value pairs for the labels in JSON format"
#         done_text = "Done"

#         grouping_id = "ID"
#         grouping_value = "Value"

#         completed_text = "Completed"
#         completed_help = "Check to mark the annotation as completed"

#         error_text = "Value is too long. Please shorten it."
#         selection_must_be_continuous = "Please select continuous rows"

#     def view(self, model, ui_width, device_type, device_width):
#         with open(model.labels_file, "r") as f:
#             labels_json = json.load(f)

#         labels_list = labels_json["labels"]
#         labels = ['']
#         for label in labels_list:
#             labels.append(label['name'])
#         model.labels = labels

#         with open(model.groups_file, "r") as f:
#             groups_json = json.load(f)

#         groups_list = groups_json["groups"]
#         groups = ['']
#         for group in groups_list:
#             groups.append(group['name'])
#         model.groups = groups

#         with st.sidebar:
#             st.markdown("---")
#             st.subheader(model.subheader_1)

#             placeholder_upload = st.empty()

#             file_names = self.get_existing_file_names('docs/images/')

#             if 'annotation_index' not in st.session_state:
#                 st.session_state['annotation_index'] = 0
#                 annotation_index = 0
#             else:
#                 annotation_index = st.session_state['annotation_index']

#             annotation_selection = placeholder_upload.selectbox(model.annotation_text, file_names,
#                                                                 index=annotation_index,
#                                                                 help=model.annotation_selection_help)

#             annotation_index = self.get_annotation_index(annotation_selection, file_names)

#             file_extension = self.get_file_extension(annotation_selection, 'docs/images/')
#             model.img_file = f"docs/images/{annotation_selection}" + file_extension
#             model.rects_file = f"docs/json/{annotation_selection}.json"

#             completed_check = st.empty()

#             btn = st.button(model.export_labels_text)
#             if btn:
#                 self.export_labels(model)
#                 st.write(model.done_text)

#             st.subheader(model.subheader_2)

#             with st.form("upload-form", clear_on_submit=True):
#                 uploaded_file = st.file_uploader(model.upload_button_text_desc, accept_multiple_files=False,
#                                                  type=['png', 'jpg', 'jpeg'],
#                                                  help=model.upload_help)
#                 submitted = st.form_submit_button(model.upload_button_text)

#                 if submitted and uploaded_file is not None:
#                     ret = self.upload_file(uploaded_file)

#                     if ret is not False:
#                         file_names = self.get_existing_file_names('docs/images/')

#                         annotation_index = self.get_annotation_index(annotation_selection, file_names)
#                         annotation_selection = placeholder_upload.selectbox(model.annotation_text, file_names,
#                                                                             index=annotation_index,
#                                                                             help=model.annotation_selection_help)
#                         st.session_state['annotation_index'] = annotation_index

#         # st.title(model.pageTitle + " - " + annotation_selection)

#         if model.img_file is None:
#             st.caption(model.no_annotation_file)
#             return

#         saved_state = self.fetch_annotations(model.rects_file)

#         # annotation file has been changed
#         if annotation_index != st.session_state['annotation_index']:
#             annotation_v = saved_state['meta']['version']
#             if annotation_v == "v0.1":
#                 st.session_state["annotation_done"] = False
#             else:
#                 st.session_state["annotation_done"] = True
#         # store the annotation file index
#         st.session_state['annotation_index'] = annotation_index

#         # first load
#         if "annotation_done" not in st.session_state:
#             annotation_v = saved_state['meta']['version']
#             if annotation_v == "v0.1":
#                 st.session_state["annotation_done"] = False
#             else:
#                 st.session_state["annotation_done"] = True

#         with completed_check:
#             annotation_done = st.checkbox(model.completed_text, help=model.completed_help, key="annotation_done")
#             if annotation_done:
#                 saved_state['meta']['version'] = "v1.0"
#             else:
#                 saved_state['meta']['version'] = "v0.1"

#             with open(model.rects_file, "w") as f:
#                 json.dump(saved_state, f, indent=2)
#             st.session_state[model.rects_file] = saved_state

#         assign_labels = st.checkbox(model.assign_labels_text, True, help=model.assign_labels_help)
#         mode = "transform" if assign_labels else "rect"

#         docImg = Image.open(model.img_file)

#         data_processor = DataProcessor()

#         with st.container():
#             doc_height = saved_state['meta']['image_size']['height']
#             doc_width = saved_state['meta']['image_size']['width']
#             canvas_width, number_of_columns = self.canvas_available_width(ui_width, doc_width, device_type,
#                                                                           device_width)

#             if number_of_columns > 1:
#                 col1, col2 = st.columns([number_of_columns, 10 - number_of_columns])
#                 with col1:
#                     result_rects = self.render_doc(model, docImg, saved_state, mode, canvas_width, doc_height, doc_width)
#                 with col2:
#                     tab = st.radio("Select", ["Mapping", "Grouping", "Ordering"], horizontal=True,
#                                    label_visibility="collapsed")
#                     if tab == "Mapping":
#                         self.render_form(model, result_rects, data_processor, annotation_selection)
#                     elif tab == "Grouping":
#                         self.group_annotations(model, result_rects)
#                     elif tab == "Ordering":
#                         self.order_annotations(model, model.labels, model.groups, result_rects)
#             else:
#                 result_rects = self.render_doc(model, docImg, saved_state, mode, canvas_width, doc_height, doc_width)
#                 tab = st.radio("Select", ["Mapping", "Grouping"], horizontal=True, label_visibility="collapsed")
#                 if tab == "Mapping":
#                     self.render_form(model, result_rects, data_processor, annotation_selection)
#                 else:
#                     self.group_annotations(model, result_rects)

#     def render_doc(self, model, docImg, saved_state, mode, canvas_width, doc_height, doc_width):
#         with st.container():
#             height = 1296
#             width = 864

#             result_rects = st_sparrow_labeling(
#                 fill_color="rgba(0, 151, 255, 0.3)",
#                 stroke_width=2,
#                 stroke_color="rgba(0, 50, 255, 0.7)",
#                 background_image=docImg,
#                 initial_rects=saved_state,
#                 height=height,
#                 width=width,
#                 drawing_mode=mode,
#                 display_toolbar=True,
#                 update_streamlit=True,
#                 canvas_width=canvas_width,
#                 doc_height=doc_height,
#                 doc_width=doc_width,
#                 image_rescale=True,
#                 key="doc_annotation" + model.img_file
#             )

#             st.caption(model.text_caption_1)
#             st.caption(model.text_caption_2)

#             return result_rects

#     def render_form(self, model, result_rects, data_processor, annotation_selection):
#         with st.container():
#             if result_rects is not None:
#                 with st.form(key="fields_form"):
#                     toolbar = st.empty()

#                     self.render_form_view(result_rects.rects_data['words'], model.labels, result_rects,
#                                           data_processor)

#                     with toolbar:
#                         submit = st.form_submit_button(model.save_text, type="primary")
#                         if submit:
#                             for word in result_rects.rects_data['words']:
#                                 if len(word['value']) > 1000:
#                                     st.error(model.error_text)
#                                     return

#                             with open(model.rects_file, "w") as f:
#                                 json.dump(result_rects.rects_data, f, indent=2)
#                             st.session_state[model.rects_file] = result_rects.rects_data
#                             # st.write(model.saved_text)
#                             st.experimental_rerun()

#                 if len(result_rects.rects_data['words']) == 0:
#                     st.caption(model.no_annotation_mapping)
#                     return
#                 else:
#                     with open(model.rects_file, 'rb') as file:
#                         st.download_button(label=model.download_text,
#                                            data=file,
#                                            file_name=annotation_selection + ".json",
#                                            mime='application/json',
#                                            help=model.download_hint)

#     def render_form_view(self, words, labels, result_rects, data_processor):
#         data = []
#         for i, rect in enumerate(words):
#             group, label = rect['label'].split(":", 1) if ":" in rect['label'] else (None, rect['label'])
#             data.append({'id': i, 'value': rect['value'], 'label': label})
#         df = pd.DataFrame(data)

#         formatter = {
#             'id': ('ID', {**PINLEFT, 'hide': True}),
#             'value': ('Value', {**PINLEFT, 'editable': True}),
#             'label': ('Label', {**PINLEFT,
#                                 'width': 80,
#                                 'editable': True,
#                                 'cellEditor': 'agSelectCellEditor',
#                                 'cellEditorParams': {
#                                     'values': labels
#                                 }})
#         }

#         go = {
#             'rowClassRules': {
#                 'row-selected': 'data.id === ' + str(result_rects.current_rect_index)
#             }
#         }

#         green_light = "#abf7b1"
#         css = {
#             '.row-selected': {
#                 'background-color': f'{green_light} !important'
#             }
#         }

#         response = agstyler.draw_grid(
#             df,
#             formatter=formatter,
#             fit_columns=True,
#             grid_options=go,
#             css=css
#         )

#         data = response['data'].values.tolist()

#         for i, rect in enumerate(words):
#             value = data[i][1]
#             label = data[i][2]
#             data_processor.update_rect_data(result_rects.rects_data, i, value, label)

#     def canvas_available_width(self, ui_width, doc_width, device_type, device_width):
#         doc_width_pct = (doc_width * 100) / ui_width
#         if doc_width_pct < 45:
#             canvas_width_pct = 37
#         elif doc_width_pct < 55:
#             canvas_width_pct = 49
#         else:
#             canvas_width_pct = 60

#         if ui_width > 700 and canvas_width_pct == 37 and device_type == "desktop":
#             return math.floor(canvas_width_pct * ui_width / 100), 4
#         elif ui_width > 700 and canvas_width_pct == 49 and device_type == "desktop":
#             return math.floor(canvas_width_pct * ui_width / 100), 5
#         elif ui_width > 700 and canvas_width_pct == 60 and device_type == "desktop":
#             return math.floor(canvas_width_pct * ui_width / 100), 6
#         else:
#             if device_type == "desktop":
#                 ui_width = device_width - math.floor((device_width * 22) / 100)
#             elif device_type == "mobile":
#                 ui_width = device_width - math.floor((device_width * 13) / 100)
#             return ui_width, 1

#     def fetch_annotations(self, rects_file):
#         for key in st.session_state:
#             if key.startswith("docs/json/") and key != rects_file:
#                 del st.session_state[key]

#         if rects_file not in st.session_state:
#             with open(rects_file, "r") as f:
#                 saved_state = json.load(f)
#                 st.session_state[rects_file] = saved_state
#         else:
#             saved_state = st.session_state[rects_file]

#         return saved_state

#     def upload_file(self, uploaded_file):
#         if uploaded_file is not None:
#             if os.path.exists(os.path.join("docs/images/", uploaded_file.name)):
#                 st.write("File already exists")
#                 return False

#             if len(uploaded_file.name) > 100:
#                 st.write("File name too long")
#                 return False

#             with open(os.path.join("docs/images/", uploaded_file.name), "wb") as f:
#                 f.write(uploaded_file.getbuffer())

#             img_file = Image.open(os.path.join("docs/images/", uploaded_file.name))

#             annotations_json = {
#                 "meta": {
#                     "version": "v0.1",
#                     "split": "train",
#                     "image_id": len(self.get_existing_file_names("docs/images/")),
#                     "image_size": {
#                         "width": img_file.width,
#                         "height": img_file.height
#                     }
#                 },
#                 "words": []
#             }

#             file_name = uploaded_file.name.split(".")[0]
#             with open(os.path.join("docs/json/", file_name + ".json"), "w") as f:
#                 json.dump(annotations_json, f, indent=2)

#             st.success("File uploaded successfully")

#     def get_existing_file_names(self, dir_name):
#         # get ordered list of files without file extension, excluding hidden files
#         return natsorted([os.path.splitext(f)[0] for f in os.listdir(dir_name) if not f.startswith('.')])

#     def get_file_extension(self, file_name, dir_name):
#         # get list of files, excluding hidden files
#         files = [f for f in os.listdir(dir_name) if not f.startswith('.')]
#         for f in files:
#             if file_name is not  None and os.path.splitext(f)[0] == file_name:
#                 return os.path.splitext(f)[1]

#     def get_annotation_index(self, file, files_list):
#         return files_list.index(file)


#     def group_annotations(self, model, result_rects):
#         with st.form(key="grouping_form"):
#             if result_rects is not None:
#                 words = result_rects.rects_data['words']
#                 data = []
#                 for i, rect in enumerate(words):
#                     data.append({'id': i, 'value': rect['value']})
#                 df = pd.DataFrame(data)

#                 formatter = {
#                     'id': ('ID', {**PINLEFT, 'width': 50}),
#                     'value': ('Value', PINLEFT)
#                 }

#                 toolbar = st.empty()

#                 response = agstyler.draw_grid(
#                     df,
#                     formatter=formatter,
#                     fit_columns=True,
#                     selection='multiple',
#                     use_checkbox='True',
#                     pagination_size=40
#                 )

#                 rows = response['selected_rows']

#                 with toolbar:
#                     submit = st.form_submit_button(model.save_text, type="primary")
#                     if submit and len(rows) > 0:
#                         # check if there are gaps in the selected rows
#                         if len(rows) > 1:
#                             for i in range(len(rows) - 1):
#                                 if rows[i]['id'] + 1 != rows[i + 1]['id']:
#                                     st.error(model.selection_must_be_continuous)
#                                     return

#                         words = result_rects.rects_data['words']
#                         new_words_list = []
#                         coords = []
#                         for row in rows:
#                             word_value = words[row['id']]['value']
#                             rect = words[row['id']]['rect']
#                             coords.append(rect)
#                             new_words_list.append(word_value)
#                         # convert array to string
#                         new_word = " ".join(new_words_list)

#                         # Get min x1 value from coords array
#                         x1_min = min([coord['x1'] for coord in coords])
#                         y1_min = min([coord['y1'] for coord in coords])
#                         x2_max = max([coord['x2'] for coord in coords])
#                         y2_max = max([coord['y2'] for coord in coords])


#                         words[rows[0]['id']]['value'] = new_word
#                         words[rows[0]['id']]['rect'] = {
#                             "x1": x1_min,
#                             "y1": y1_min,
#                             "x2": x2_max,
#                             "y2": y2_max
#                         }

#                         # loop array in reverse order and remove selected entries
#                         i = 0
#                         for row in rows[::-1]:
#                             if i == len(rows) - 1:
#                                 break
#                             del words[row['id']]
#                             i += 1

#                         result_rects.rects_data['words'] = words

#                         with open(model.rects_file, "w") as f:
#                             json.dump(result_rects.rects_data, f, indent=2)
#                         st.session_state[model.rects_file] = result_rects.rects_data
#                         st.experimental_rerun()


#     def order_annotations(self, model, labels, groups, result_rects):
#         if result_rects is not None:
#             self.action_event = None
#             data = []
#             idx_list = [""]
#             words = result_rects.rects_data['words']
#             for i, rect in enumerate(words):
#                 if rect['label'] != "":
#                     # split string into two variables, assign None to first variable if no split is found
#                     group, label = rect['label'].split(":", 1) if ":" in rect['label'] else (None, rect['label'])
#                     data.append({'id': i, 'value': rect['value'], 'label': label, 'group': group})
#                     idx_list.append(i)
#             df = pd.DataFrame(data)

#             formatter = {
#                 'id': ('ID', {**PINLEFT, 'width': 50}),
#                 'value': ('Value', {**PINLEFT}),
#                 'label': ('Label', {**PINLEFT,
#                                     'width': 80,
#                                     'editable': False,
#                                     'cellEditor': 'agSelectCellEditor',
#                                     'cellEditorParams': {
#                                         'values': labels
#                                     }}),
#                 'group': ('Group', {**PINLEFT,
#                                     'width': 80,
#                                     'editable': True,
#                                     'cellEditor': 'agSelectCellEditor',
#                                     'cellEditorParams': {
#                                         'values': groups
#                                     }})
#             }

#             go = {
#                 'rowClassRules': {
#                     'row-selected': 'data.id === ' + str(result_rects.current_rect_index)
#                 }
#             }

#             green_light = "#abf7b1"
#             css = {
#                 '.row-selected': {
#                     'background-color': f'{green_light} !important'
#                 }
#             }

#             idx_option = st.selectbox('Select row to move into', idx_list)

#             def run_component(props):
#                 value = component_toolbar_main(key='toolbar_main', **props)
#                 return value

#             def handle_event(value):
#                 if value is not None:
#                     if 'action_timestamp' not in st.session_state:
#                         self.action_event = value['action']
#                         st.session_state['action_timestamp'] = value['timestamp']
#                     else:
#                         if st.session_state['action_timestamp'] != value['timestamp']:
#                             self.action_event = value['action']
#                             st.session_state['action_timestamp'] = value['timestamp']
#                         else:
#                             self.action_event = None

#             props = {
#                 'buttons': {
#                     'up': {
#                         'disabled': False,
#                         'rendered': ''
#                     },
#                     'down': {
#                         'disabled': False,
#                         'rendered': ''
#                     },
#                     'save': {
#                         'disabled': False,
#                         'rendered': ''
#                         # 'rendered': 'none',
#                     }
#                 }
#             }

#             handle_event(run_component(props))

#             response = agstyler.draw_grid(
#                 df,
#                 formatter=formatter,
#                 fit_columns=True,
#                 grid_options=go,
#                 css=css
#             )

#             rows = response['selected_rows']
#             if len(rows) == 0 and result_rects.current_rect_index > -1:
#                 for i, row in enumerate(data):
#                     if row['id'] == result_rects.current_rect_index:
#                         rows = [
#                             {
#                                 '_selectedRowNodeInfo': {
#                                     'nodeRowIndex': i
#                                 },
#                                 'id': row['id']
#                             }
#                         ]
#                         break

#             if str(self.action_event) == 'up':
#                 if len(rows) > 0:
#                     idx = rows[0]['_selectedRowNodeInfo']['nodeRowIndex']
#                     if idx > 0:
#                         row_id = rows[0]['id']
#                         if row_id == idx_option:
#                             return
#                         # swap row upwards in the array
#                         if idx_option == "":
#                             words[row_id], words[row_id - 1] = words[row_id - 1], words[row_id]
#                         else:
#                             for i in range(1000):
#                                 words[row_id], words[row_id - 1] = words[row_id - 1], words[row_id]
#                                 row_id -= 1
#                                 if row_id == idx_option:
#                                     break

#                         result_rects.rects_data['words'] = words

#                         with open(model.rects_file, "w") as f:
#                             json.dump(result_rects.rects_data, f, indent=2)
#                         st.session_state[model.rects_file] = result_rects.rects_data
#                         st.experimental_rerun()
#             elif str(self.action_event) == 'down':
#                 if len(rows) > 0:
#                     idx = rows[0]['_selectedRowNodeInfo']['nodeRowIndex']
#                     if idx < len(df) - 1:
#                         row_id = rows[0]['id']
#                         if row_id == idx_option:
#                             return
#                         # swap row downwards in the array
#                         if idx_option == "":
#                             words[row_id], words[row_id + 1] = words[row_id + 1], words[row_id]
#                         else:
#                             for i in range(1000):
#                                 words[row_id], words[row_id + 1] = words[row_id + 1], words[row_id]
#                                 row_id += 1
#                                 if row_id == idx_option:
#                                     break

#                         result_rects.rects_data['words'] = words

#                         with open(model.rects_file, "w") as f:
#                             json.dump(result_rects.rects_data, f, indent=2)
#                         st.session_state[model.rects_file] = result_rects.rects_data
#                         st.experimental_rerun()
#             elif str(self.action_event) == 'save':
#                 data = response['data'].values.tolist()
#                 for elem in data:
#                     if elem[3] != "None":
#                         idx = elem[0]
#                         group = elem[3]
#                         words[idx]['label'] = f"{group}:{elem[2]}"

#                 result_rects.rects_data['words'] = words

#                 with open(model.rects_file, "w") as f:
#                     json.dump(result_rects.rects_data, f, indent=2)
#                 st.session_state[model.rects_file] = result_rects.rects_data
#                 st.experimental_rerun()


#     def export_labels(self, model):
#         path_from = os.path.join("docs/json/")
#         path_to = os.path.join("docs/json/key/")

#         files = [f for f in os.listdir(path_from) if not f.startswith('.')]
#         for file in files:
#             path = os.path.join(path_from, file)
#             if os.path.isfile(path):
#                 with open(path, "r") as f:
#                     data = json.load(f)
#                     words = data['words']

#                     keys = {}
#                     row_keys = {}

#                     for word in words:
#                         if word['label'] != '':
#                             if ':' in word['label']:
#                                 group, label = word['label'].split(':', 1)
#                                 if 'row' not in group:
#                                     if group not in keys:
#                                         keys[group] = {}
#                                     keys[group][label] = word['value']
#                                 else:
#                                     if "items" not in keys:
#                                         keys["items"] = []

#                                     if group not in row_keys:
#                                         row_keys[group] = {}
#                                     row_keys[group][label] = word['value']
#                             else:
#                                 keys[word['label']] = word['value']

#                     if row_keys != {}:
#                         for key in row_keys:
#                             keys["items"].append(row_keys[key])

#                     if keys != {}:
#                         path = os.path.join(path_to, file)
#                         with open(path, "w") as f:
#                             json.dump(keys, f, indent=2)
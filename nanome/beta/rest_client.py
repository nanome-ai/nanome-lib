import requests
from marshmallow import fields
import sys

from nanome.api import schemas
from nanome.api.schemas.api_definitions import api_function_definitions
from nanome.util import Color


class NanomeRestClient:

    def __init__(self, base_url, room_code):
        self.base_url = base_url
        self.room_code = room_code
        self.headers = {'Content-Type': 'application/json'}

    def request_complex_list(self):
        fn_name = 'request_complex_list'
        url = self.get_fn_url(fn_name)
        response = requests.get(url)
        output = self._deserialize_response(fn_name, response.json())
        return output
    
    def request_complexes(self, indices_list):
        fn_name = 'request_complexes'
        url = self.get_fn_url(fn_name)
        params = {'indices': indices_list}
        response = requests.get(url, params=params)
        output = self._deserialize_response(fn_name, response.json())
        return output

    def request_workspace(self):
        fn_name = 'request_workspace'
        url = self.get_fn_url(fn_name)
        response = requests.get(url)
        output = self._deserialize_response(fn_name, response.json())
        return output

    def update_structures_shallow(self, comp_list):
        fn_name = 'update_structures_shallow'
        url = self.get_fn_url(fn_name)
        payload = self._serialize_request(fn_name, [comp_list])
        response = requests.put(url, json=payload, headers=self.headers)
        output = self._deserialize_response(fn_name, response.json())
        return output

    def update_structures_deep(self, comp_list):
        fn_name = 'update_structures_deep'
        url = self.get_fn_url(fn_name)
        payload = self._serialize_request(fn_name, [comp_list])
        response = requests.put(url, json=payload, headers=self.headers)
        output = self._deserialize_response(fn_name, response.json())
        return output

    def create_writing_stream(self, indices_list, stream_type):
        fn_name = 'create_writing_stream'
        url = self.get_fn_url(fn_name)
        response = requests.post(url)
        output = self._deserialize_response()
        return response.json()

    # def stream_update(self):
    #     fn_name = 'stream_update'
    #     url = self.get_fn_url(fn_name)
    #     response = requests.get(url)
    #     output = self._deserialize_response()
    #     return response.json()

    def update_workspace(self):
        fn_name = 'update_workspace'
        url = self.get_fn_url(fn_name)
        response = requests.put(url)
        output = self._deserialize_response()
        return response.json()

    def zoom_on_structures(self):
        fn_name = 'zoom_on_structures'
        url = self.get_fn_url(fn_name)
        response = requests.put(url)
        output = self._deserialize_response()
        return response.json()

    def send_notification(self):
        fn_name = 'send_notification'
        url = self.get_fn_url(fn_name)
        response = requests.get(url)
        output = self._deserialize_response()
        return response.json()

    def center_on_structures(self):
        fn_name = 'center_on_structures'
        url = self.get_fn_url(fn_name)
        response = requests.put(url)
        output = self._deserialize_response()
        return response.json()

    def add_to_workspace(self):
        fn_name = 'add_to_workspace'
        url = self.get_fn_url(fn_name)
        response = requests.put(url)
        output = self._deserialize_response()
        return response.json()

    def add_bonds(self):
        fn_name = 'add_bonds'
        url = self.get_fn_url(fn_name)
        response = requests.get(url)
        output = self._deserialize_response()
        return response.json()

    def open_url(self):
        fn_name = 'open_url'
        url = self.get_fn_url(fn_name)
        response = requests.post(url)
        output = self._deserialize_response()
        return response.json()

    def request_presenter_info(self):
        fn_name = 'request_presenter_info'
        url = self.get_fn_url(fn_name)
        response = requests.get(url)
        output = self._deserialize_response()
        return response.json()

    def request_controller_transforms(self):
        fn_name = 'request_controller_transforms'
        url = self.get_fn_url(fn_name)
        response = requests.get(url)
        output = self._deserialize_response()
        return response.json()

    @staticmethod
    def _deserialize_response(function_name, response_data):
        fn_definition = api_function_definitions[function_name]
        output_schema = fn_definition.output
        if output_schema:
            deserialized_response = output_schema.load(response_data)
        else:
            deserialized_response = None
        return deserialized_response

    @staticmethod
    def _serialize_request(function_name, arg_list, kwarg_dict=None):
        """Use marshmallow schema to serialize request data."""
        fn_definition = api_function_definitions[function_name]
        kwarg_dict = kwarg_dict or {}
        serialized_args = []
        # serialized_kwargs = {}
        for arg_obj, arg_definition in zip(arg_list, fn_definition.params):
            if isinstance(arg_definition, schemas.Schema):
                ser_arg = arg_definition.dump(arg_obj)
            elif isinstance(arg_definition, fields.Field):
                # Create object with arg value as attribute, so we can validate.
                temp_obj = type('TempObj', (object,), {'val': arg_obj})
                ser_arg = arg_definition.serialize('val', temp_obj)
            serialized_args.append(ser_arg)
        return serialized_args[0]

    def get_fn_url(self, function_name):
        return f'{self.base_url}/{self.room_code}/{function_name}'


if __name__ == "__main__":
    base_url = 'http://127.0.0.1:5000'
    room_code = sys.argv[1].upper()
    print(room_code)

    client = NanomeRestClient(base_url, room_code)

    print("Getting complex list...")
    shallow_comps = client.request_complex_list()
    comp_indices = [comp.index for comp in shallow_comps]
    print("Getting complex details...")
    [deep_comp] = client.request_complexes(comp_indices[:1])
    for atom in deep_comp.atoms:
        atom.atom_color = Color.Blue()
    breakpoint()
    client.update_structures_deep([deep_comp])

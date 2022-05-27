from nanome.api.user import PresenterInfo
from marshmallow import Schema, fields, post_load


class PresenterInfoSchema(Schema):
    account_id = fields.Str()
    account_name = fields.Str()
    account_email = fields.Email()
    has_org = fields.Bool()
    org_id = fields.Integer()
    org_name = fields.Str()

    @post_load
    def make_presenter_info(self, data, **kwargs):
        new_obj = PresenterInfo()
        for key in data:
            try:
                setattr(new_obj, key, data[key])
            except AttributeError:
                raise AttributeError('Could not set attribute {}'.format(key))
        return new_obj

from marshmallow import Schema, fields

class EventSessionSchema(Schema):
  id = fields.Int(required=True)
  event_name = fields.Str()
  event_site = fields.Str()
  event_time = fields.Str()

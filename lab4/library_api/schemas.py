from marshmallow import Schema, fields, validate
from datetime import datetime


class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    author = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    year = fields.Int(required=True, validate=validate.Range(min=1000, max=2024))
    created_at = fields.Str(dump_only=True)
    updated_at = fields.Str(dump_only=True)

    def format_datetime(self, dt):
        if isinstance(dt, str):
            return dt
        return dt.isoformat() if dt else None

    def dump(self, obj, many=None, **kwargs):
        if many:
            return [self._dump_single(item) for item in obj]
        return self._dump_single(obj)

    def _dump_single(self, obj):
        if not obj:
            return {}
        data = super().dump(obj)
        if isinstance(obj, (dict, list)):
            return data
        data['created_at'] = self.format_datetime(obj.created_at)
        data['updated_at'] = self.format_datetime(obj.updated_at)
        return data


class BookPaginationSchema(Schema):
    items = fields.Nested(BookSchema, many=True)
    next_cursor = fields.Int(allow_none=True)
    has_more = fields.Bool() 
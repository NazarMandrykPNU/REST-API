from marshmallow import Schema, fields, validate

class BookSchema(Schema):
    """Schema for validating book data."""
    id = fields.Int(dump_only=True)  # Only used for response, not for input
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    author = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    year = fields.Int(required=True, validate=validate.Range(min=1000, max=2024)) 
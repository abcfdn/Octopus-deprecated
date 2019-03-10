from marshmallow import Schema, fields

EVENT_FIELDS = [
    "start_time", "duration", "site", "address", "location",
    "meetup", "eventbrite", "livestream", "session_id",
    "presenter_id", "project_id"]

PRESENTER_FIELDS = [
    "full_name", "email", "title", "company",
    "linkedin", "self_intro", "avatar"]

PROJECT_FIELDS = [
    "name", "website", "short_description", "long_description",
    "github", "logo", "focused_area"]

SESSION_FIELDS = [
    "session_name", "topic", "category", "event_type", "language",
    "summary", "highlight", "pre_requisite", "deck_file"]


class SessionSchema(Schema):
    name = fields.Str(required=True)
    topic = fields.Str()
    category = fields.Str()
    event_type = fields.Str()
    language = fields.Str()
    summary = fields.Str()
    highlight = fields.Str()
    pre_requisite = fields.Str()
    deck_file = fields.Url()

    @validates('language')
    def validate_language(self, value):
        if language not in ['english', 'chinese']:
            raise ValidationError('Only chinese and english are supported..')


class ProjectSchema(Schema):
    name = fields.Str(required=True)
    website = fields.Url()
    short_description = fields.Str()
    long_description = fields.Str()
    github = fields.Url()
    logo = fields.Url()
    focused_area = fields.List()


class PresenterSchema(Schema):
    user_id = fields.Email(required=True)
    full_name = fields.Str()
    email = fields.Email()
    title = fields.Str()
    company = fields.Str()
    linkedin = fields.Url()
    self_intro = fields.Str()
    avatar = fields.Url()


class EventSchema(Schema):
    id = fields.UUID()
    session_id = fields.Str()
    project_id = fields.Str()
    project_id = fields.Str()
    date = fields.Date()
    start_at = fields.Time()
    duration_as_hours = fields.Float()
    site = fields.Str()
    address = fields.Str()
    location = fields.Str()
    meetup = fields.Url()
    eventbrite = fields.Url()
    livestream = fields.Url()

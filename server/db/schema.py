from marshmallow import Schema, fields, validates


class ProjectSchema(Schema):
    name = fields.Str(required=True)
    website = fields.Url()
    short_description = fields.Str()
    long_description = fields.Str()
    team_background = fields.Str()
    github = fields.Url()
    logo = fields.Url()
    focused_area = fields.Str()


class PresenterSchema(Schema):
    email = fields.Email(required=True)
    full_name = fields.Str()
    title = fields.Str()
    orgnization = fields.Str()
    linkedin = fields.Url()
    self_intro = fields.Str()
    photo = fields.Url()
    project = fields.Nested(ProjectSchema)


class TopicSchema(Schema):
    name = fields.Str()
    sessions = fields.List(fields.Str())
    poster = fields.Url()


class ScheduleSchema(Schema):
    start_at = fields.Int()
    duration_as_mins = fields.Int()
    site = fields.Str()
    address = fields.Str()
    location = fields.Str()
    meetup = fields.Url()
    eventbrite = fields.Url()
    livestream = fields.Url()
    poster = fields.Url()


class SessionSchema(Schema):
    name = fields.Str(required=True)
    presenter = fields.Email()
    created_at = fields.Int()

    topic = fields.Str()
    category = fields.Str()
    event_type = fields.Str()
    language = fields.Str()
    summary = fields.Str()
    highlight = fields.Str()
    pre_requisite = fields.Str()
    deck_file = fields.Url()
    schedule = fields.Nested(ScheduleSchema)

    @validates('language')
    def validate_language(self, value):
        if language.lower() not in ['english', 'chinese']:
            raise ValidationError('Only Chinese and English are supported..')

class PictureSchema(Schema):
    photo_id = fields.Str(required=True)
    name = fields.Str()
    description = fields.Str()
    product_url = fields.Url()
    base_url = fields.Url()
    mime_type = fields.Str()
    photo_type = fields.Str()
    created_at = fields.Int()
    height = fields.Int()
    width = fields.Int()

    @validates('photo_type')
    def validate_photo_type(self, value):
        if photo_type.lower() not in ['event_poster',
                                      'topic_poster',
                                      'membership_card',
                                      'others']:
            raise ValidationError('Unsupported photo type')

from marshmallow import Schema, fields, validates


class ProjectSchema(Schema):
    name = fields.Str(required=True)
    website = fields.Str()
    short_description = fields.Str()
    long_description = fields.Str()
    team_background = fields.Str()
    github = fields.Str()
    logo = fields.Str()
    focused_area = fields.Str()


class PresenterSchema(Schema):
    email = fields.Email(required=True)
    full_name = fields.Str()
    title = fields.Str()
    orgnization = fields.Str()
    linkedin = fields.Str()
    self_intro = fields.Str()
    photo = fields.Str()
    project = fields.Nested(ProjectSchema)


class TopicSchema(Schema):
    name = fields.Str()
    sessions = fields.List(fields.Str())
    poster = fields.Str()


class ScheduleSchema(Schema):
    start_at = fields.Int()
    duration_as_mins = fields.Int()
    site = fields.Str()
    address = fields.Str()
    location = fields.Str()
    meetup = fields.Str()
    eventbrite = fields.Str()
    livestream = fields.Str()
    poster = fields.Str()


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
    deck_file = fields.Str()
    schedule = fields.Nested(ScheduleSchema)

    @validates('language')
    def validate_language(self, language):
        if language and language.lower() not in ['english', 'chinese']:
            raise ValidationError('Only Chinese and English are supported..')

class GooglePhotoSchema(Schema):
    filename = fields.Str()
    photo_id = fields.Str()
    decription = fields.Str()
    upload_token = fields.Str()
    album_id = fields.Str()
    base_url = fields.Str()
    product_url = fields.Str()

class ImgurPhotoSchema(Schema):
    link = fields.Str()
    id = fields.Str()
    deletehash = fields.Str()
    description = fields.Str()
    type = fields.Str()

class MemberSchema(Schema):
    name = fields.Str()
    started_at = fields.Int()
    email = fields.Email()
    organization = fields.Str()
    location = fields.Str()
    title = fields.Str()
    linkedin = fields.Str()
    github = fields.Str()
    channel = fields.Str()
    blokchain_experience = fields.Str()
    interested_topic = fields.Str()
    motivation = fields.Str()
    volunteer_candidate = fields.Boolean()
    suggestion = fields.Str()
    self_intro = fields.Str()
    member_card = fields.Nested(ImgurPhotoSchema)
    membership_card = fields.Nested(GooglePhotoSchema)

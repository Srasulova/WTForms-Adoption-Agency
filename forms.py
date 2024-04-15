from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Optional, URL, NumberRange, AnyOf

class AddPetForm(FlaskForm):
    name = StringField("Pet Name", validators=[InputRequired()])
    age = FloatField("Age", validators=[Optional(), NumberRange(min=0, max=30)])
    species = StringField("Species", validators=[InputRequired(), AnyOf(["cat", "dog", "porcupine"])])
    photo_url = StringField("Image Url", validators=[Optional(), URL()])
    notes = StringField("Notes", validators=[Optional()])
    available = BooleanField("Availability", default=True, validators=[Optional()])

    

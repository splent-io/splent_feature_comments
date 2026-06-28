from flask_wtf import FlaskForm
from wtforms import SubmitField


class SplentFeatureCommentsForm(FlaskForm):
    submit = SubmitField("Save splent_feature_comments")

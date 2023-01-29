from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
from wtforms_components import TimeField
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

class CafeForm(FlaskForm):
    cafe = StringField('Cafe Name', validators=[DataRequired()])
    cafe_url = StringField('Cafe Location on Google Maps (URL)', validators=[DataRequired(), URL()])
    opening_time = TimeField('Opening Time e.g. 08:00 AM')
    closing_time = TimeField('Closing Time e.g. 06:30 PM')
    rating = SelectField('Coffee Rating',choices=['☕','☕☕', '☕☕☕', '☕☕☕☕', '☕☕☕☕☕'], validators=[DataRequired()])
    wifi_strength = SelectField('Wifi Strength Rating', choices=['✘', '💪', '💪'*2, '💪'*3, '💪'*4, '💪'*5], validators=[DataRequired()])
    power = SelectField('Power Socket Availability', choices=['✘', '🔌', '🔌' * 2, '🔌' * 3, '🔌' * 4, '🔌' * 5], validators=[DataRequired()])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open("cafe-data.csv", mode="a") as csv_file:
            csv_file.write(f"\n{form.cafe.data},"
                           f"{form.cafe_url.data},"
                           f"{form.data['opening_time'].strftime('%I:%M %p')},"
                           f"{form.data['closing_time'].strftime('%I:%M %p')},"
                           f"{form.rating.data},"
                           f"{form.wifi_strength.data},"
                           f"{form.power.data}")
        return redirect(url_for('cafes'))

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)

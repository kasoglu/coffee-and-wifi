from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import *
from wtforms.validators import *
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

coffee_rate = ['', '☕️', '☕️☕️', '☕️☕️☕️', '☕️☕️☕️☕️', '☕️☕️☕️☕️☕️']
wifi_rate = ['', '💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪']
power_rate = ['', '⚡️', '⚡️⚡️', '⚡️⚡️⚡️', '⚡️⚡️⚡️⚡️', '⚡️⚡️⚡️⚡️⚡️']


class CafeForm(FlaskForm):
    cafe = StringField('Cafe Name', validators=[DataRequired()])
    location = URLField('Location URL on Google Maps', validators=[DataRequired(), URL()])
    open_time = StringField('Opening Time e.g. 8AM')
    close_time = StringField('Closing Time e.g. 9PM')
    coffee_rate = SelectField('Coffee Rating', choices=coffee_rate, validators=[DataRequired()])
    wifi_rate = SelectField('Wifi Rating', choices=wifi_rate, validators=[DataRequired()])
    power_rate = SelectField('Power Rating', choices=power_rate, validators=[DataRequired()])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open('cafe-data.csv', "a") as csv_file:
            csv_file.write(f"\n{form.cafe.data},"
                           f"{form.location.data},"
                           f"{form.open_time.data},"
                           f"{form.close_time.data},"
                           f"{form.coffee_rate.data},"
                           f"{form.wifi_rate.data},"
                           f"{form.power_rate.data}")
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

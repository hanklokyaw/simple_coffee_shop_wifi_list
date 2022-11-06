import wtforms.fields
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField, SelectField
from wtforms.form import Form
from wtforms.validators import DataRequired, URL, ValidationError
from flask_wtf import FlaskForm
import csv


# Create the app using Flask
app = Flask(__name__)
Bootstrap(app)

# Create form
class MyTable(FlaskForm):
    # # Read-File or create csv if there is not ones.
    # try:
    #     with open("cafe-data.csv", mode="r") as file:
    #         data_csv = file.readlines()
    # except:
    #     with open("cafe-data.csv", mode="a") as file:
    #         file.writelines("")
    # else:
    #     # print(data_csv)
    #     pass
    app.secret_key = "YOU_SECRET_KEY"
    # data = data_csv
    cafe_name = StringField(label='Cafe name', validators=[DataRequired()])
    cafe_location = StringField(label='Cafe Location on Google Maps (URL)', validators=[URL(message='Must be a valid URL'),DataRequired()])
    open_time = StringField(label='Opening Time e.g.8AM', validators=[DataRequired()])
    close_time = StringField(label='Closing Time e.g.5:30PM', validators=[DataRequired()])
    coffee_rating = SelectField(label='Coffee Rating', choices=["❌","☕️","☕️☕️","☕️☕️☕️","☕️☕️☕️️☕️","☕️☕️☕️☕️☕️"])
    wifi_rating = SelectField(label='Wifi Rating', choices=["❌","💪","💪💪","💪💪💪","💪💪💪💪","💪💪💪💪💪"])
    power_rating = SelectField(label='Power Rating', choices=["❌","🔌","🔌🔌","🔌🔌🔌","🔌🔌🔌🔌","🔌🔌🔌🔌🔌"])
    submit = SubmitField(label='Submit')

# Create index
@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/cafes')
def cafes():
    # form = MyTable()
    with open("cafe-data.csv", mode="r") as file:
        form = file.readlines()
    return render_template('cafes.html', form=form)

@app.route('/add', methods=['GET','POST'])
def add():
    form = MyTable()
    if form.validate_on_submit():
        log_name = form.cafe_name.data
        log_location = form.cafe_location.data
        log_open = form.open_time.data
        log_close = form.close_time.data
        log_coffee = form.coffee_rating.data
        log_wifi = form.wifi_rating.data
        log_power = form.power_rating.data
        to_log = f"{log_name},{log_location},{log_open},{log_close},{log_coffee},{log_wifi},{log_power}\n"
        print(to_log)
        with open("cafe-data.csv", mode='a') as f:
            f.write(to_log)
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)
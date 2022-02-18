import requests
import sys
from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
API_ID = 'API_ID'
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SECRET_KEY'] = os.urandom(24)


class City(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)


db.create_all()


@app.route('/', methods=["GET", "POST"])
def main_view():
    if request.method == 'POST':
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                           params={'q': request.form.get('city_name'), 'type': 'like',
                                   'units': 'metric', 'APPID': API_ID}).json()
        try:
            city = res['list'][0]['name']
            if City.query.filter(City.name == city).all():
                flash('The city has already been added to the list!')
            else:
                db.session.add(City(name=city))
                db.session.commit()
        except IndexError:
            flash("The city doesn't exist!")

        return redirect('/')
    elif request.method == 'GET':
        cities = City.query.all()
        data = []
        for city in cities:
            res = requests.get("http://api.openweathermap.org/data/2.5/find",
                               params={'q': city.name, 'type': 'like', 'units': 'metric', 'APPID': API_ID}).json()
            weather = {
                'city_id': city.id,
                'degrees': res['list'][0]['main']['temp'],
                'state': res['list'][0]['weather'][0]['description'].title(),
                'city': res['list'][0]['name']
            }
            data.append(weather)

        return render_template('index.html', weathers=data)\


@app.route('/delete/<int:city_id>', methods=["GET", "POST"])
def delete_card(city_id):
    city = City.query.filter(City.id == city_id).first()
    db.session.delete(city)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()

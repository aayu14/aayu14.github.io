import requests
from weather import app, db
from flask import render_template, redirect, url_for, request, flash
from weather.models import City


# getting weather data through openweather api

def get_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={ city }&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'
    r = requests.get(url).json()
    return r


@app.route('/')
def index():
    cities = City.query.all()

    weather_data = []

    for city in cities:

        data = get_weather_data(city.name)
        print(data)

        weather = {
            'city': city.name,
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
        }

        weather_data.append(weather)

    return render_template('weather.html', weather_data=weather_data)


@app.route('/', methods=['POST'])
def index_post():
    error_msg = ''
    new_city = request.form.get('city')

    if new_city:
        existing_city = City.query.filter_by(name=new_city).first()

        if not existing_city:
            new_city_data = get_weather_data(new_city)

            if new_city_data['cod'] == 200:
                new_city_obj = City(name=new_city)

                db.session.add(new_city_obj)
                db.session.commit()
            else:
                error_msg = 'City does not exist!'
        else:
            error_msg = 'City already exists here!'

    if error_msg:
        flash(error_msg, 'error')
    else:
        flash('City added succesfully!')

    return redirect(url_for('index'))


@app.route('/delete/<name>')
def delete_city(name):
    city = City.query.filter_by(name=name).first()
    db.session.delete(city)
    db.session.commit()

    flash(f'Successfully deleted { city.name }', 'success')
    return redirect(url_for('index'))

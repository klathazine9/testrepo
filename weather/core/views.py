from django.http import HttpResponse
from django.shortcuts import render


def get_html_content(city):
    import requests
    #headers so we don't get detected by the site we are scraping
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en- US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE

    city = city.replace(' ', '+')
    html_content = session.get(f'https://www.google.com/search?q=weather+in+{city}').text
    return html_content


def home(request):
    weather_data = None
    if 'city' in request.GET:
        # fetch the data of the weather from your your preffered weather site
        city = request.GET.get('city')
        html_content = get_html_content(city)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        weather_data = dict()
        weather_data['temperature'] = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
        weather_data['date_time_description'] = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
        weather_data['region'] = soup.find('span', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text

        #print(temperature.text)
        #print(date_time_description.text)
        #print(region.text)
    return render(request, 'core/home.html', {'weather':weather_data})

# Create your views here.

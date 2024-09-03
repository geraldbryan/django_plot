from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import datetime
from datetime import timedelta
import requests
import matplotlib.pyplot as plt

import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import os
from dotenv import load_dotenv
load_dotenv()

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def data():
    df_daily_hist = pd.DataFrame()

    api_key = os.getenv("api_key")

    def get_date_list(start_date):
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')

        end_date = datetime.datetime.today()

        date_list = []

        while start_date < end_date:
            date_list.append(start_date)
            start_date += timedelta(days=90)

        date_list.append(end_date)

        return date_list

    date = get_date_list("2024-04-01")

    for i in ["TLKM.JK"]:
        for j in range (0,len(date)-1):
            if j==0:
                start_date = date[j]
                start_date = start_date.strftime('%Y-%m-%d')
                
                end_date = date[j+1]
                end_date = end_date.strftime('%Y-%m-%d')
            else:
                start_date = date[j]+ timedelta(days=1)
                start_date = start_date.strftime('%Y-%m-%d')
                
                end_date = date[j+1]
                end_date = end_date.strftime('%Y-%m-%d')

            url = f"https://api.sectors.app/v1/daily/{i}/?start={start_date}&end={end_date}"
            

            headers = {
                "Authorization": api_key
            }

            response = requests.get(url, headers = headers)

            if response.status_code == 200:
                data = response.json()
            else:
                # Handle error
                print(response.status_code)

            df_daily_hist = pd.concat([df_daily_hist,pd.DataFrame(data)])

            df_daily_hist = df_daily_hist[df_daily_hist.date <= "2024-07-15"]

            print(f"Finsih collect data for stock {i} from {start_date} to {end_date}")

            return df_daily_hist

def chart_two(request):
    df_daily_hist = data()
    df_tlkm = df_daily_hist[df_daily_hist.symbol == "TLKM.JK"]

    plt.figure(figsize=(14, 10))
    plt.plot(df_tlkm['date'], df_tlkm['close'], linewidth=2)

    # Formatting the plot
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.title('TLKM.JK Daily Price Since 1 April 2024')
    plt.tight_layout()

    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    # Return the plot as an HTTP response
    return HttpResponse(buf.getvalue(), content_type='image/png')

def plot_view(request):
    # Convert date to datetime
    df_daily_hist = data()
    df_tlkm = df_daily_hist[df_daily_hist.symbol == "TLKM.JK"]
    df_tlkm['date'] = pd.to_datetime(df_tlkm['date'])

    # Define the color change dates
    yellow_date = pd.Timestamp('2024-05-02')
    red_date = pd.Timestamp('2024-05-19')

    # Plotting the data with conditional coloring
    plt.style.use('dark_background') 
    plt.figure(figsize=(14, 10))

    # Plot each segment with the appropriate color
    for i in range(len(df_tlkm) - 1):
        start_date = df_tlkm['date'].iloc[i]
        end_date = df_tlkm['date'].iloc[i + 1]
        if end_date > red_date:
            color = 'red'
        elif end_date > yellow_date:
            color = 'yellow'
        else:
            color = 'white'
        
        plt.plot(df_tlkm['date'].iloc[i:i+2], df_tlkm['close'].iloc[i:i+2], color=color, linewidth=2)

    # Formatting the plot
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.title('TLKM.JK Daily Price Since 1 April 2024')
    plt.tight_layout()

    # Create custom legend
    import matplotlib.lines as mlines

    blue_line = mlines.Line2D([], [], color='white', linewidth=2, label='Before Starlink Rumours')
    yellow_line = mlines.Line2D([], [], color='yellow', linewidth=2, label="After First Starlink's Rumour News Emerged")
    red_line = mlines.Line2D([], [], color='red', linewidth=2, label='After Starlink Official Announcement in Indonesia')

    plt.legend(handles=[blue_line, yellow_line, red_line])

    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    # Return the plot as an HTTP response
    return HttpResponse(buf.getvalue(), content_type='image/png')

def plot_page_view(request):
    return render(request, 'home.html')

def plot_two_page_view(request):
    return render(request, 'chart_two.html')
    
        

    
import requests
from datetime import datetime,timedelta
import time
import urllib.request

from PIL import Image

import pandas as pd

import pathlib

#==========================================USER======================================================


def get_reach(access_token:str,year:int,metric_type:str): #Return a list of values of reach for the year


    version = "22.0"
    acc = "17841400402569880" 
    t_data = []

#Get the 1st and last day of the month
    for i in range(12):
        date = datetime(year=year,month=i+1,day=1,hour=8,minute=0,second=0)
        next_date = date.replace(day=28) + timedelta(days=4)
        last_date = next_date - timedelta(days=next_date.day)

# Convert datetime to unix time
        start = time.mktime(date.timetuple())
        end = time.mktime(last_date.timetuple())


        if (metric_type == 'total_value'): #Fetch an aggregation of the reach for each month
            url = f"https://graph.facebook.com/v{version}/{acc}/insights?metric=reach&period=day&since={start}&until={end}&metric_type=total_value&access_token={access_token}"
            

            response = requests.get(url)
            result = response.json()

            try:
                data = result['data'][0]['total_value']['value']
            except:
                data = 0

            month = date.strftime("%d %b %Y")
            print(f'{month} reach: {data}')
            
            t_data.append(data)



        elif (metric_type == 'time_series'): #Fetch of the reach by time period (every day) for each month
            url = f"https://graph.facebook.com/v{version}/{acc}/insights?metric=reach&period=day&since={start}&until={end}&metric_type=time_series&access_token={access_token}"
            response = requests.get(url)
            result = response.json()

            try:
                data = result['data'][0]['values']
            
            except:
                data = 0

            month = date.strftime("%d %b %Y")
            print(f'{month} reach: {data}')
            
            t_data.append(data)
          
    return t_data

def get_weekly_profile_view(access_token:str,year:int,week:int):
        
        # Get the date based on the Week Number
        d = f"{year}-W{week}"
        date = datetime.strptime(d +'-1', "%G-W%V-%u")
        last_date = date + timedelta(days=7)

        # Convert datetime to unix time
        start = time.mktime(date.timetuple())
        end = time.mktime(last_date.timetuple())

        url = f"https://graph.facebook.com/v21.0/{acc}/insights?metric=profile_views&period=day&since={start}&until={end}&metric_type=total_value&access_token={access_token}"
        response = requests.get(url)
        result = response.json()

        try:
            data = result['data'][0]['total_value']['value']
        
        except:
            data = 0

        month = date.strftime("%d %b %Y")
        print(f'{month} reach: {data}')
        
        return data

def get_weekly_user_stats(access_token:str,year:int,week:int):
        
        version = "22.0"
        # Get the date based on the Week Number
        d = f"{year}-W{week}"
        date = datetime.strptime(d +'-1', "%G-W%V-%u")
        last_date = date + timedelta(days=7)

        # Convert datetime to unix time
        start = time.mktime(date.timetuple())
        end = time.mktime(last_date.timetuple())

        url = f"https://graph.facebook.com/v{version}/{acc}/insights?metric=profile_links_taps,follows_unfollows&period=day&since={start}&until={end}&metric_type=total_value&access_token={access_token}"
        response = requests.get(url)
        result = response.json()

        try:
            data = result['data'][0]['total_value']['value']
        
        except:
            data = 0

        month = date.strftime("%d %b %Y")
        print(f'{month} reach: {data}')
        
        return data


def get_total_interaction(access_token:str,year:int,breakdown:bool): #Return a list of values of reach for the year


    version = "22.0"
    t_data = []

#Get the 1st and last day of the month
    for i in range(12):
        date = datetime(year=year,month=i+1,day=1,hour=8,minute=0,second=0)
        next_date = date.replace(day=28) + timedelta(days=4)
        last_date = next_date - timedelta(days=next_date.day)

# Convert datetime to unix time
        start = time.mktime(date.timetuple())
        end = time.mktime(last_date.timetuple())


        if (breakdown): #Fetch interaction for each month with the breakdown by media type
            url = f"https://graph.facebook.com/v{version}/{acc}/insights?metric=total_interactions&period=day&breakdown=media_product_type&since={start}&until={end}&metric_type=total_value&access_token={access_token}"
            

            response = requests.get(url)
            result = response.json()
            print(result)

            

            try:
                data = result['data'][0]['total_value']['breakdowns'][0]['results']
                for i in data:
                        print(i)
                        

                        d = {
                            'dimension_values': i,
                            'value': data['value'],
                            'date': month
                        }
                        t_data.append(d)

                        
                    
            except:
                data = 0
            # print(data)

            month = date.strftime("%d %b %Y")
            print(f'{month} interactions: {data}')
            
            



        else : #Fetch of the interaction by time period (every day) for each month
            url = f"https://graph.facebook.com/v{version}/{acc}/insights?metric=total_interactions&period=day&since={start}&until={end}&metric_type=total_value&access_token={access_token}"
            response = requests.get(url)


            result = response.json()
            print(result)
            

            try:
                data = result['data'][0]['total_value']['value']
            
            except:
                data = 0

            month = date.strftime("%d %b %Y")
            print(f'{month} interactions: {data}')
            
            t_data.append(data)

    return t_data


#==========================================POST======================================================

def get_post_reach(access_token:str,year:int,metric_type:str,media_id: int): #Return a list of values of reach for the year


    version = "22.0"
    t_data = []

#Get the 1st and last day of the month
    for i in range(12):
        date = datetime(year=year,month=i+1,day=1,hour=8,minute=0,second=0)
        next_date = date.replace(day=28) + timedelta(days=4)
        last_date = next_date - timedelta(days=next_date.day)

# Convert datetime to unix time
        start = time.mktime(date.timetuple())
        end = time.mktime(last_date.timetuple())


        if (metric_type == 'total_value'): #Fetch an aggregation of the reach for each month
            url = f"https://graph.facebook.com/v{version}/{media_id}/insights?metric=reach&period=day&since={start}&until={end}&metric_type=total_value&access_token={access_token}"
            

            response = requests.get(url)
            result = response.json()

            try:
                data = result['data'][0]['total_value']['value']
            except:
                data = 0

            month = date.strftime("%d %b %Y")
            print(f'{month} reach: {data}')
            
            t_data.append(data)



        elif (metric_type == 'time_series'): #Fetch of the reach by time period (every day) for each month
            url = f"https://graph.facebook.com/v{version}/{media_id}/insights?metric=reach&period=day&since={start}&until={end}&metric_type=time_series&access_token={access_token}"
            response = requests.get(url)


            result = response.json()

            print(result)

            try:
                data = result['data'][0]['values']
            
            except:
                data = 0

            month = date.strftime("%d %b %Y")
            print(f'{month} reach: {data}')
            
            t_data.append(data)

    return t_data


def get_post_reach_byhour(access_token:str,media_id: int,date:datetime): #Return a list of values of reach for the year


    version = "22.0"
    t_data = []


    hour = date.hour

#Get the 1st and last day of the month
    for i in range(23):
        new_date = date.replace(hour=(hour)) + timedelta(hours=i)
        next_date = new_date.replace(hour=new_date.hour) + timedelta(hours=1)

        print(f'{new_date}  {next_date}')
        

# Convert datetime to unix time
        start = time.mktime(new_date.timetuple())
        end = time.mktime(next_date.timetuple())


        
        url = f"https://graph.facebook.com/v{version}/{acc}/insights?metric=reach&period=day&since={start}&until={end}&metric_type=total_value&access_token={access_token}"
        response = requests.get(url)
        result = response.json()

        print(result)
        try:
            data = result['data'][0]['total_value']['value']
        except:
            data = 0
            print("Error")        
        t_data.append(data)

    print(t_data)

def get_video_thumbnail(access_token,id,week):
    version = "22.0"
    year = 2025

    d = f"{year}-W{week}"
    date = datetime.strptime(d +'-1', "%G-W%V-%u")
    last_date = date + timedelta(days=7)

    # Convert datetime to unix time
    start = time.mktime(date.timetuple())
    end = time.mktime(last_date.timetuple())

    url = f"https://graph.facebook.com/v{version}/{id}/?fields=thumbnail_url&period=day&since={start}&until={end}&access_token={access_token}"
    response = requests.get(url)
    result = response.json()
    data = result['thumbnail_url']

    return data

def dl_thumbnail(filepath,week:int):
    df = pd.read_csv(filepath,usecols=['id','media_url'])


    for i in range(len(df)):
        url = df.iloc[i,1]
        name = df.iloc[i,0]
        path = pathlib.Path(__file__).parent.resolve()
        urllib.request.urlretrieve(url,f'{path}/reports/2025/Weekly/W{week}/{name}.jpeg')




def media_insights(access_token,id,week,follows:bool):#Fetch of the post's metrics for a week period
  
    version = "22.0"

    d = f"{year}-W{week}"
    date = datetime.strptime(d +'-1', "%G-W%V-%u")
    last_date = date + timedelta(days=7)

    # Convert datetime to unix time
    start = time.mktime(date.timetuple())
    end = time.mktime(last_date.timetuple())

    if (follows):
        url = f"https://graph.facebook.com/v{version}/{id}/insights?metric=reach,shares,saved,follows,views,profile_activity&period=day&since={start}&until={end}&metric_type=total_value&access_token={access_token}"
    else:
        url = f"https://graph.facebook.com/v{version}/{id}/insights?metric=reach,shares,saved,views&period=day&since={start}&until={end}&metric_type=total_value&access_token={access_token}"

    response_media = requests.get(url)
    result = response_media.json()

    data = {}

    for i in result['data']:
        
        n_name = i['name']
        n_value = i['values'][0]['value']

        data[n_name] = n_value
    
    return data


#==========================================REPORTS (Outdated version) ======================================================


def weekly_report(access_token:str,year: int,week:int):

    version = "22.0"

    d = f"{year}-W{week}"
    date = datetime.strptime(d +'-1', "%G-W%V-%u")
    last_date = date + timedelta(days=7)

    print(date)
    print(last_date)

    # Convert datetime to unix time
    start = time.mktime(date.timetuple())
    end = time.mktime(last_date.timetuple())

    url = f"https://graph.facebook.com/v{version}/{acc}/media?fields=id,like_count,permalink,media_url,media_type,timestamp,caption&period=day&since={start}&until={end}&access_token={access_token}"
    response_media = requests.get(url)
    result_media = response_media.json()

    url = f"https://graph.facebook.com/v{version}/{acc}/insights?metric=likes,views,shares,saved,follows&period=day&since={start}&until={end}&metric_type=total_value&access_token={access_token}"
    response_insights = requests.get(url)
    result_insights = response_insights.json()

    result = []
    


    for i in result_media['data']:
        id = i['id']
        like_count = i['like_count']
        permalink = i['permalink']
        try:
            media_url = i['media_url']
        except:
            media_url = ''
            
        media_type = i['media_type']
        timestamp = i['timestamp']
        shares = media_insights(access_token=access_token,id=id,week=week,follows=False)['shares']
        saved = media_insights(access_token=access_token,id=id,week=week,follows=False)['saved']
        caption = i['caption']
        if (media_type!='VIDEO'):
            profile_activity = media_insights(access_token=access_token,id=id,week=week,follows=True)['profile_activity']
            follows = media_insights(access_token=access_token,id=id,week=week,follows=True)['follows']
        else:
            follows = 0
            profile_activity = None
        reach = media_insights(access_token=access_token,id=id,week=week,follows=False)['reach']
        
        if (media_type=='VIDEO'): media_url = get_video_thumbnail(access_token,id,week)

        tab = [id,week,media_type,like_count,reach,shares,saved,follows,permalink,media_url,timestamp,profile_activity,caption]

        result.append(tab)

    return result

def weekly_audience(access_token):

    version = "22.0"
    result = []
    follower_demographics = []
    engaged_audience_demographics = []
    reached_audience_demographics = []



    url = f"https://graph.facebook.com/v{version}/{acc}/insights?metric=engaged_audience_demographics,reached_audience_demographics,follower_demographics&period=lifetime&timeframe=this_week&metric_type=total_value&breakdown=country&access_token={access_token}"
    response_media = requests.get(url)
    result_media = response_media.json()
    
    if(response_media.status_code == 200):
        for i in result_media['data']:
            name = i['name']
            total_value = i['total_value']

            for j in total_value['breakdowns'][0]['results']:

                dimension_value = j['dimension_values']
                value = j['value']
                tab = [name,dimension_value,value]
                result.append(tab)

        df = pd.DataFrame(result,columns=['Dimensions','Countries','Values'])

        follower_demographics = df[df['Dimensions'] == 'follower_demographics']
        engaged_audience_demographics = df[df['Dimensions'] == 'engaged_audience_demographics']
        reached_audience_demographics = df[df['Dimensions'] == 'reached_audience_demographics']

        audience = {'follower_demographics':follower_demographics,
                    'engaged_audience_demographics':engaged_audience_demographics,
                    'reached_audience_demographics':reached_audience_demographics}


        return audience #Return a dict of DF
    
    else:

        print(f"Erreur response{response_media.status_code}")


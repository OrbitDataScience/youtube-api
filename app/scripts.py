import requests
import streamlit as st
import pandas as pd
import json
import csv
from datetime import datetime

def achar_videos(keyword, date, duration, order):
    headers = {
        "x-rapidapi-key": "88b5804da0mshaec086ad3147560p16ac64jsn608ec3c7f56c",
        "x-rapidapi-host": "youtube-media-downloader.p.rapidapi.com"
    }

    
    responses_list = []
    page = 0
    switcher = {
        'Tudo': "all",
        'Última hora': "lastHour",
        'Hoje': "today",
        'Última semana': "thisWeek",
        'Último mês': "thisMonth",
        'Último ano': "thisYear"
    }
    date = switcher.get(date, 0)

    switcher = {
        'Qualquer': 'all',
        'Curto (menos de 4 minutos)': 'short',
        'Médio (entre 4 e 20 minutos)': 'medium',
        'Longo (mais de 20 minutos)' : 'long'
    }
    duration = switcher.get(duration, 0)


    switcher = {
        'Relevância': 'relevance',
        'Data de publicação': 'uploadDate',
        'Mais vistos': 'viewCount',
        'Rating': 'rating'
    }
    order = switcher.get(order, 0)
    
    url = "https://youtube-media-downloader.p.rapidapi.com/v2/search/videos"

    querystring = {"keyword":{keyword},"lang":"pt-BR","uploadDate":{date},"duration":{duration},"sortBy":{order}}

    response = requests.get(url, headers=headers, params=querystring)
    json_response = response.json()
    responses_list.append(json_response['items'])

    token = json_response['nextToken']

    if token:
        while token:
            url = "https://youtube-media-downloader.p.rapidapi.com/v2/search/videos"

            querystring = {"keyword":{keyword},"lang":"pt-BR","uploadDate":{date},"duration":{duration},"sortBy":{order},"nextToken":{token}}

            response = requests.get(url, headers=headers, params=querystring)
            json_response = response.json()
            responses_list.append(json_response['items'])

            token = json_response['nextToken']
            page += 1
    return filtrar_json(responses_list, page)


def videos_details(lista_videos):
    
    info = {}
    count = 0
    for video_id in lista_videos:
        url = "https://youtube-media-downloader.p.rapidapi.com/v2/video/details"
    
        headers = {
            "x-rapidapi-key": "88b5804da0mshaec086ad3147560p16ac64jsn608ec3c7f56c",
            "x-rapidapi-host": "youtube-media-downloader.p.rapidapi.com"
        }


        querystring = {"videoId":{video_id}}

        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code != 200:
            st.error(f"Erro na API para o vídeo {video_id}, status: {response.status_code}")
            continue

        video = response.json()

        if not video.get('status', False):
            st.write(f"Vídeo inválido ou não disponível: {video_id}")
            continue

        id = video.get('id', 'Sem ID')
        title = video.get('title', 'Sem título')
        tipo = video.get('type', 'Indisponível')
        description = video.get('description', 'Indisponível')
        views = video.get('viewCount', 'Indisponível')
        published = video.get('publishedTimeText', 'Indisponível')        
        comments = video.get('commentCountText', 'Indisponível')
        likes = video.get('likeCount', 'Indisponível')  

        segundos = video.get('lengthSeconds', 0)
        duration = f'{segundos//60}m {segundos%60}s'
        # if 'title' in video:
        #     title = video['title']
        # else:
        #     title = 'Sem título'
        # Adiciona os dados do vídeo atual ao dicionário 'info'.
        info[f'Vídeo: {count}'] = {
            'Tipo' : tipo,
            'Duração' : duration,
            'Likes' : likes,
            'Comentários' : comments,
            'Visualizações' : views,
            'Título' : title,
            'Descrição' : description,
            'Publicado em' : published,
            'Link' : f'https://www.youtube.com/watch?v={id}'
        }
        count += 1
    
    salvar_csv(info)
    return info


def salvar_csv(dados):
    df = pd.DataFrame.from_dict(dados, orient='index')
    df.to_excel("Youtube" + '.xlsx', index=False)


def filtrar_json(dados_json, page):
    lista = []

    for i in range(page):
        for video in dados_json[i]:
            lista.append(video['id'])
    
    st.info(f'Foram encontrados: {len(lista)} vídeos')
    videos_details(lista)
            
    return True

#RDVeMsGR_LY
#-hyQSs4FGhw
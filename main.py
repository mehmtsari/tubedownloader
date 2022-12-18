from win11toast import toast,notify,update_progress
from pytube import YouTube,Playlist,Channel
import os
from sys import exit
import webbrowser

path_main = str(os.getcwd())
try:
    os.mkdir("downloads")
    download_path =path_main +"/downloads/"
except:
    download_path =path_main +"/downloads/"

secimler = []
toast("Youtube Downloader'a Hoşgeldin!\n","Lütfen Aşağıdan Seçim Yapınız.",selection=["Youtube'da Ara","Youtube'da Ara (URL)","Tek bir parça","Oynatma Listesi"],button='Seçim Yap',on_click=lambda args : (secimler.append(args)),duration="long")
secim = []
for i in secimler:
    secim = str(i["user_input"]["selection"])
    
if secim == "Youtube'da Ara":
    split = []
    toast('Ne arıyorsunuz?', 'Lütfen Video/Şarkı İsmi Giriniz.', input='reply', button={'activationType': 'protocol', 'arguments': 'http:', 'content': 'Send', 'hint-inputId': 'reply'},on_click=lambda args : (split.append(args)),duration="long")
    search =[]
    for i in split:
        search = (i["user_input"]["reply"])
    b = webbrowser.open_new_tab("https://www.youtube.com/results?search_query={}".format(search))
        
elif secim == "Youtube'da Aç (URL)":
    split = []
    toast('Url İsteği!', 'Lütfen Url Adresini Giriniz.', input='reply', button={'activationType': 'protocol', 'arguments': 'http:', 'content': 'Send', 'hint-inputId': 'reply'},on_click=lambda args : (split.append(args)),duration="long")
    url =[]
    for i in split:
        url = (i["user_input"]["reply"])
    b = webbrowser.open_new_tab(url)
    

elif secim == "Tek bir parça":
    split = []
    toast('Url İsteği!', 'Lütfen Url Adresini Giriniz.', input='reply', button={'activationType': 'protocol', 'arguments': 'http:', 'content': 'Send', 'hint-inputId': 'reply'},on_click=lambda args : (split.append(args)),duration="long")
    url =[]
    for i in split:
        url = (i["user_input"]["reply"])
    print("URL :",url)
    yt = YouTube(url)
    title = yt.title
    image = yt.thumbnail_url
    split2 = []
    toast("Video '{}' \nBulundu!".format(title),'Lütfen Video Formatını Seçin',image = image,selection=["Video.mp4","Audio.mp3"], button='İndir',on_click=lambda args : (split2.append(args)),duration="long")
    kalite = []
    for i in split2:
        kalite = str(i["user_input"]["selection"])
    
    try:
        if "mp4" in kalite:
            video = yt.streams.get_highest_resolution()
            video.download(download_path)
        elif "mp3" in kalite:
            video = yt.streams.filter(only_audio=True).first()
            output = video.download(download_path)
            toast("Başarılı!","'{}' Adlı video '{}' olarak 'downloads' klasörüne kaydedildi.".format(title,kalite),on_click=download_path,duration="long")
    except:
        toast("Hata!!","Bir Hata Oluştu ve Kapatılıyor Lütfen Tekrar Deneyiniz veya İnternet bağlantınızı kontrol ediniz!")

elif secim == "Oynatma Listesi":
    from random import randint
    rand = randint(1,1000)
    dir_name = "Playlist-"+str(rand)
    from os import mkdir
    mkdir(download_path+dir_name)
    oynatma_list_path = download_path+dir_name

    split = []
    toast('Url İsteği!', 'Lütfen Parça Listesinin Url Adresini Giriniz.', input='reply', button={'activationType': 'protocol', 'arguments': 'http:', 'content': 'Send', 'hint-inputId': 'reply'},on_click=lambda args : (split.append(args)),duration="long")
    url =[]
    for i in split:
        url = (i["user_input"]["reply"])
    
    pl = Playlist(url)
    
    split2 = []
    toast('Videolar Bulundu!','Lütfen Video Formatını Seçin',selection=["Video.mp4","Audio.mp3"], button='İndir',on_click=lambda args : (split2.append(args)),duration="long")
    kalite = []
    for i in split2:
        kalite = str(i["user_input"]["selection"])

    
    print(len(pl.videos))
    leng = len(pl.videos)

    notify(progress={
        'title': 'YouTube',
        'status': 'İndiriliyor...',
        'value': '0',
        'valueStringOverride': '0/{} video'.format(leng)
    })

    if "mp4" in kalite:
        x = 1
        for video in pl.videos:
            vd = video.streams.get_highest_resolution()
            vd.download(oynatma_list_path)
            
            update_progress({'value': x / leng , 'valueStringOverride': f'{x}/{leng} video'})
            x += 1
        update_progress({'status': 'Tamamlandı!'})
    
    elif "mp3" in kalite:
        x = 1
        for video in pl.videos:
            vd = video.streams.filter(only_audio=True).first()
            output = vd.download(oynatma_list_path)
            base,ext = os.path.splitext(output)
            to_mp3 = video.title + kalite
            
            update_progress({'value': x / leng , 'valueStringOverride': f'{x}/{leng} videos'})
            x += 1
        update_progress({'status': 'Tamamlandı!'})
        
exit()
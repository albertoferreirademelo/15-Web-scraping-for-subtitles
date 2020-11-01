from os import listdir
import re
from bs4 import BeautifulSoup
import urllib.request
import zipfile
import rarfile

def get_video_files(directory):
    all_files= (listdir(directory))
    all_video_files = []
    for i in all_files:
        if i[-3:] == "mp4" or i[-3:] == "avi" or i[-3:] == "mkv":
            all_video_files.append(i[:-4])            
    return all_video_files
    
def get_subtitles(directory):
    all_subtitles = (listdir(directory))
    all_subt = []
    for i in all_subtitles:
        if i[-3:] == "srt":
            all_subt.append(i[:-4])
    return all_subt
    
def check_subt_exist(list_videos, all_subt):
    need_subt = []
    for i in list_videos:
        if i not in all_subt:        
            need_subt.append(i)
    return need_subt

def open_download_subt_link(video_without_subt):
    subt_links = []
    for subtitle_link in video_without_subt:
        website = "http://subscene.com/subtitles/release?q="+subtitle_link         
        print (website)

        response = urllib.request.urlopen(website)
        html = response.read()    
        soup = BeautifulSoup(html)
            
        all_href = []
        for links in soup.find_all("a"):
            all_href.append(links.get('href'))        
        
        for links in all_href:
            if re.search("english", links):
                subt_links.append(links)
                break

        
        #print (subt_links)
    return (subt_links)
    
def download_subt(down_link):
    total_down = str(len(down_link))
    count_down = 1    
    print ("Total downloads: "+total_down)
    for link in down_link:
        #count_down = 1
        print ("Downloading "+str(count_down)+" of "+ total_down)
        subtitle_website = "http://subscene.com"+link
        try:
            response = urllib.request.urlopen(subtitle_website)
            html = response.read()
            
            soup = BeautifulSoup(html)
            all_a = soup.find_all("a")
            for links in all_a:    
                href = links.get('href')
                if re.search("download", href):
                    download_link = "http://subscene.com"+href
                    
            print ("Downloading "+download_link)
            
            urllib.request.urlretrieve(download_link, "temp.wat")
            try:            
                zf = zipfile.ZipFile("temp.wat")
                zf.extractall(".")
            except:                        
                rf = rarfile.RarFile("temp.wat")
                rf.extractall(".")
            count_down +=1
        except:
            break



if __name__ == "__main__":        
    directory = r"D:\Downloads\new downloads"
    #directory = r"C:\Users\Tiskwan\workspace\Find_subtitles\video_test"    
    video_files = get_video_files(directory)
    all_subt = get_subtitles(directory)
    video_without_subt = check_subt_exist(video_files, all_subt)
    #print (video_without_subt)
    down_link = open_download_subt_link(video_without_subt)
    download_subt(down_link)
    
    
#subscene = "http://subscene.com/subtitles/release?q="+video_without_subt[4]
#print (subscene)
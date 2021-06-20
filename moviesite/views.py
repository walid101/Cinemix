from django.shortcuts import render
from omdb import OMDBClient

client = OMDBClient(apikey="d5193665")
char_lim = 100 #Plot shortened to 100 chars at top carousel
num_sections = 3 #number of sections in our slides (we can increase this if we want) => Each secton = 4 slides

def getDescsFromMovies(list):
     deep_movie_desc = []
     for movie in list:
          temp_sect = client.get(title = movie["title"], tomatoes=False)
          if(temp_sect["poster"] != "N/A"):
               if(len(temp_sect["plot"]) > char_lim):
                    temp_sect["plot_full"] = temp_sect["plot"]
                    temp_sect["plot"] = (temp_sect["plot"])[0:char_lim-3] + " ..."
               deep_movie_desc.append(temp_sect)
     return deep_movie_desc

def get_movie(name, start_list, start_page, end_page):
     output = start_list
     for i in range(start_page, end_page):
          output.extend(client.search_movie(name, page = i))
     output = sort_movies("year", output)
     return output

def sort_movies(metric, list):
     temp_list = sorted(list, key = lambda x:x[metric], reverse=True)
     return temp_list

class pageValPair:
     def __init__(self, list, pageNum):
          self.list = list
          self.pageNum = pageNum

async def home(request):
    #Begin Initial Search
    if(request.GET.get('movie_search')):
         print(request)
         movie_list = [] #Movie List for Top carousel
         base_string = request.GET.get('movie_search')
         movie_list = get_movie(base_string, movie_list, 0, 2)
         #movie_main = pageValPair(movie_list, 5)
         movie_descs = getDescsFromMovies(movie_list)
         movie_sects = movie_descs.copy()
         return render(request,'home.html', context={"desc": movie_descs, "desc_rem": movie_descs[1:], "movie_sect1": movie_sects[0:4],
                                                 "movie_sect2": movie_sects[4:8], "movie_sect3":movie_sects[8:12],"movie_rem": movie_sects[len(movie_descs):], "deep_movies": movie_sects,
                                                 "show_page": 1, "page_num": 1, "pages": [1,2,3,4,5],},)
    base_string = "Superman"
    movie_list = [] #Movie List for Top carousel
    movie_list = get_movie(base_string, movie_list, 0, 2)
    #movie_main = pageValPair(movie_list, 5)
    movie_descs = getDescsFromMovies(movie_list)
    movie_sects = movie_descs.copy()
    return render(request, 'home.html', context={"desc": movie_descs, "desc_rem":movie_descs[1:], "movie_sect1": movie_sects[0:4],
                                                 "movie_sect2": movie_sects[4:8], "movie_sect3":movie_sects[8:12],"movie_rem": movie_sects[len(movie_descs):],"deep_movies": movie_sects,
                                                 "show_page": -1, "page_num": -1, "pages": [1,2,3,4,5],},) #{} is context dictionary

def page(request):
     base_string = request.GET.get("movie_search")
     page_num = int(request.GET.get("page_num"))
     '''
     print("BASE STRING: " + base_string)
     print("PAGE NUM: " + str(page_num))
     '''
     movie_list = [] #Movie List for Top carousel
     movie_list = get_movie(base_string, movie_list, 2*page_num-2, 2*page_num)
     #movie_main = pageValPair(movie_list, 5)
     movie_descs = getDescsFromMovies(movie_list)
     movie_sects = movie_descs.copy()
     return render(request,'home.html', context={"desc": movie_descs, "desc_rem": movie_descs[1:], "movie_sect1": movie_sects[0:4],
                                                 "movie_sect2": movie_sects[4:8], "movie_sect3":movie_sects[8:12],"movie_rem": movie_sects[len(movie_descs):], "deep_movies": movie_sects,
                                                 "show_page": 1, "page_num": page_num, "pages": [1,2,3,4,5],},)

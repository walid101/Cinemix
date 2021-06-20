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
'''
test_list = get_movie("Superman", [], 5, 0)
print(test_list)
print(" \n AND DESCS: \n")
desc_list = getDescsFromMovies(test_list)
print(desc_list)
'''
def home(request):
    #Begin Initial Search
    if(request.GET.get('movie_search')):
         movie_list = [] #Movie List for Top carousel
         base_string = request.GET.get('movie_search')
         movie_list = get_movie(base_string, movie_list, 0, 2)
         #movie_main = pageValPair(movie_list, 5)
         movie_descs = getDescsFromMovies(movie_list)
         movie_sects = movie_descs.copy()
         return render(request,'home.html', context={"desc": movie_descs, "desc_rem": movie_descs[1:], "movie_sect1": movie_sects[0:4],
                                                 "movie_sect2": movie_sects[4:8], "movie_sect3":movie_sects[8:12],"movie_rem": movie_sects[len(movie_descs):], "deep_movies": movie_sects},)

    
    #Landing search when user first lands on homepage
    base_string = "Superman"
    movie_list = client.search_movie(base_string, tomatoes = False)
    movie_descs = []
    movie_sects = []
    counter = 0
    for movie in movie_list:
               movie_descs.append(client.get(title=movie["title"], tomatoes=False))
               curr_desc = movie_descs[counter]
               movie_descs[counter]["plot_full"] = movie_descs[counter]["plot"]
               if(len(curr_desc["plot"]) > char_lim):
                    curr_desc["plot"] = (curr_desc["plot"])[0:char_lim-3] + " ..."
                    movie_descs[counter] = curr_desc
               counter+=1
    if len(movie_descs) > 4*num_sections:
         movie_sects = movie_descs[0:4*num_sections]
    else:
         movie_sects = movie_descs[0:len(movie_descs)]
         limit_reached = False
         while(len(movie_sects) < 4*num_sections and len(base_string) > 0 and limit_reached == False):
              base_string = base_string[0:len(base_string)-1]
              temp_movie_list = client.search_movie(base_string)
              for movie in temp_movie_list:
                   if(len(movie_sects) >= 4*num_sections):
                        limit_reached = True
                        break
                   else:
                        temp_sect = client.get(title = movie["title"], tomatoes=False)
                        if temp_sect["poster"] != "NA":
                             movie_sects.append(temp_sect)
    return render(request, 'home.html', context={"desc": movie_descs, "desc_rem":movie_descs[1:], "movie_sect1": movie_sects[0:4],
                                                 "movie_sect2": movie_sects[4:8], "movie_sect3":movie_sects[8:12],"movie_rem": movie_sects[len(movie_descs):],"deep_movies": movie_sects},) #{} is context dictionary

'''
def filter_no_poster(movie):
     if len(movie["poster"]) == 0:
          return False
     return True

def in_archive(archive, id, runtime):
     if(archive.get(id) != None):
          return True
     else:
          archive[id] = runtime
          return False

def deep_search(base_string, start_movies, archive):
     new_keyword = "The "
     deep_movie_list = client.search_movie(new_keyword+base_string, tomatoes = False)
     deep_movie_desc = start_movies.copy()
     for movie in deep_movie_list:
          if(in_archive(archive, movie["imdb_id"], "100") == False):
               temp_sect = client.get(title = movie["title"], tomatoes=True)
               if(temp_sect["poster"] != "N/A"):
                    if(len(temp_sect["plot"]) > char_lim):
                         temp_sect["plot"] = (temp_sect["plot"])[0:char_lim-3] + " ..."
                    deep_movie_desc.append(temp_sect)
     return deep_movie_desc
'''

     

from django.shortcuts import render
from omdb import OMDBClient

client = OMDBClient(apikey="d5193665")
char_lim = 100 #Plot shortened to 100 chars at top carousel
num_sections = 3 #number of sections in our slides (we can increase this if we want) => Each secton = 4 slides

def home(request):
    #Begin Initial Search
    if(request.GET.get('movie_search')):
         #Code for top carousel
         movie_archive = {} #Hashmap used to check if a movie has already been displayed, avoiding repetition
         movie_list = [] #Movie List for Top carousel
         base_string = request.GET.get('movie_search')
         tries = 0
         while(len(movie_list) <= 0 and len(base_string) > 0 and tries < 5): #Add deeper search via multiple movie searches
               temp_list = client.search_movie(base_string)
               movie_list = []
               for movie in temp_list:
                    if movie["poster"] != "N/A": #Filter Movies without posters for top Carousel
                         movie_list.append(movie)
               base_string = base_string[0:len(base_string)-1]
               tries+=1
         movie_descs = []
         counter = 0
         for movie in movie_list:
              holder = client.get(title=movie["title"], tomatoes=True)
              in_arch = in_archive(movie_archive, holder["imdb_id"], holder["runtime"])
              if(in_arch == False):
                   movie_descs.append(holder)
                   movie_descs[counter]["plot_full"] = movie_descs[counter]["plot"] #Full-Plot Feature
                   curr_desc = movie_descs[counter]
                   if(len(curr_desc["plot"]) > char_lim):
                        curr_desc["plot"] = (curr_desc["plot"])[0:char_lim-3] + " ..." #Reduced Plot Feature
                        movie_descs[counter] = curr_desc
                   counter+=1
              else:
                   movie_descs.append(holder)
                   movie_descs[counter]["plot_full"] = movie_descs[counter]["plot"]
                   curr_desc = movie_descs[counter]
                   if(len(curr_desc["plot"]) > char_lim):
                        curr_desc["plot"] = (curr_desc["plot"])[0:char_lim-3] + " ..."
                        movie_descs[counter] = curr_desc
                   counter+=1
         movie_descs = sorted(movie_descs, key = lambda x:x["year"], reverse=True) #Sort movies by year for relevance

         #Code for extended results Slider
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
                              holder = client.get(title = movie["title"], tomatoes=True)
                              in_arch = in_archive(movie_archive, holder["imdb_id"], holder["runtime"])
                              if(in_arch == False):
                                   if(holder["poster"] != "N/A"):
                                        movie_sects.append(holder)
                              else:
                                   if(holder["poster"] != "N/A"):
                                        movie_sects.append(holder)

         #Code for Deep Results : Using Keyword "The"
         deep_search_movies = deep_search(base_string, movie_sects, movie_archive)
         return render(request,'home.html', context={"movies": movie_list, "desc": movie_descs, "desc_rem": movie_descs[1:], "movie_sect1": movie_sects[0:4],
                                                 "movie_sect2": movie_sects[4:8], "movie_sect3":movie_sects[8:12],"movie_rem": movie_sects[len(movie_descs):], "deep_movies": deep_search_movies},)

    
    #Landing search when user first lands on homepage
    base_string = "Superman"
    movie_list = client.search_movie(base_string, tomatoes = False)
    movie_descs = []
    movie_sects = []
    counter = 0
    for movie in movie_list:
               movie_descs.append(client.get(title=movie["title"], tomatoes=True))
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
                        temp_sect = client.get(title = movie["title"], tomatoes=True)
                        if temp_sect["poster"] != "NA":
                             movie_sects.append(temp_sect)
    return render(request, 'home.html', context={"desc": movie_descs, "desc_rem":movie_descs[1:], "movie_sect1": movie_sects[0:4],
                                                 "movie_sect2": movie_sects[4:8], "movie_sect3":movie_sects[8:12],"movie_rem": movie_sects[len(movie_descs):],"deep_movies": movie_sects},) #{} is context dictionary

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
     

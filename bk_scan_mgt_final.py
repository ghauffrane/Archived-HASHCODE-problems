# -*- coding: utf-8 -*-
"""bk_scan_mgt_final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Tl-XY576Ta7mHyb_UtmobMnp5gbSYCH1
"""

import numpy as np

PATH = '/content/a_example.txt'

def get_input(path ): 
    input_file = open(path, 'r')
    lines = input_file.readlines()
    l_contt = [lines[0][i] for i in range(0, len(lines[0])) if lines[0][i].isdigit() ]
    b, l, tot_scan_days = l_contt
    S = list((lines[1].replace('\n', '')).replace(' ', ''))
    lib_info =[]
    for i in range(2, len(lines), 2): 
        
        d = dict()
        l_1 = lines[i].replace('\n', '').replace(' ', '')
        l_2 = lines[i+1].replace('\n', '').replace(' ', '')
        d['lib_id'] = int (0.5 * i - 1)
        d['lib_total_bks'] = l_1.strip()[0]
        d['signup days'] = l_1.strip()[1]
        d['ship bks per day'] = l_1.strip()[2]
        d['lib_bks_ids'] = list(l_2.strip())
        
        lib_info.append(d)
    
    return int(b), int(l) , int(tot_scan_days),  S , lib_info


#================================================================================================================================
def get_lib_vars(L_set, l_idntf):
  lib_bks_ids = L_set[l_idntf]['lib_bks_ids']                                   #List of book IDs. The ID of a book is the ondex of its score in S.
  lib_id = L_set[l_idntf]['lib_id']                 
  lib_tot_bks = int(L_set[l_idntf]['lib_total_bks']  )                          #Total number of books in library 'lib'
  nbr_ship_bks = int(L_set[l_idntf]['ship bks per day']  )                      #Number of books to ship and scan per day
  signup_days = int(L_set[l_idntf]['signup days']  )  
  return lib_bks_ids, lib_id, lib_tot_bks, nbr_ship_bks, signup_days


#==================================================================================================================================
#Compute duplicate books for every library
#Duplicate books are the books that are found in previously visited libraries (in iterations)

#def drop_dup()
#Suppose you are iterating over all libraries
def drop_dup(L_set, lib_idntf): 
  if lib_idntf == 0: 
    bk_dup_lib = None
    unique_lib_bks = L_set[lib_idntf]['lib_bks_ids']
  else: 
    bk_dup_lib = []                                                             # list of duplicate books found in j previous libraries
    for j in range(lib_idntf): 
      ''' if a book exists in previous libraries it is a duplicate, and should be appended to a return var'''
      for bk in L_set[lib_idntf]['lib_bks_ids']: 
        if bk in L_set[j]['lib_bks_ids']:
          bk_dup_lib.append(bk)
    unique_lib_bks = [bk_id for bk_id in L_set[lib_idntf]['lib_bks_ids'] if bk_id not in bk_dup_lib]
  return unique_lib_bks


#======================================================================================================================================
def rank(B, L, D, Sc, L_set):

  prev_signup = 0                                                               #The total period in days of signup consumed by previously signed up books 
  R = []

  for counter, lib in enumerate(L_set):
    ''' iterate over the dictionaries containing info about every library '''
    lib_bks_ids, lib_id, lib_tot_bks, nbr_ship_bks, signup_days = get_lib_vars(L_set, counter)          
    prev_signup += signup_days
    max_ship_scan = nbr_ship_bks * (D - (signup_days + prev_signup))
    r = 0                                                                       #max_ship_scan is the maximum nbr of books that can be shipped before deadline and after signup
                                                      
    if counter == 0: 
      unq_bks_ids =  lib_bks_ids                                                #The first library is assumed not to have duplicates because it is the 1st consulted
    elif counter > 0:
      unq_bks_ids = drop_dup(L_set, counter) 
                                                    
    if lib_tot_bks < max_ship_scan : 
      
      for id in unq_bks_ids: 
        r += int(Sc[int(id)]) 
                                                          
    elif max_ship_scan < lib_tot_bks : 
      this_lib_scores = [ int(Sc[ int(id)]) for id in (unq_bks_ids)]
      '''if len(unq_bks_ids) < max_ship_scan: 
        for i in range(len(unq_bks_ids)):
          r += this_lib_scores[i] 
      else: 
        for i in range(int(max_ship_scan)) : 
          r += this_lib_scores[i]    '''                                        #The rank r takes the sum of max_ship_scan number of top scores from total books
      for i in range(len(this_lib_scores)): r += this_lib_scores[i]
    R.append(r)
  
  R_ = R.copy()
  R_.sort(reverse = True)
  sorted_R_ix = [R.index(rank) for rank in R_]
  lib_sign_order = []
  signup_time = 0
  for j in sorted_R_ix : 
    # ID of the library in L_set is the same as its index in the L_set list
    if int(L_set[j]['signup days']) < (D - signup_time): 
      lib_sign_order.append(j)
      signup_time += int(L_set[j]['signup days'])
    else: 
      break 

  return R,  lib_sign_order

#==================================================================================================================
def optimize(signup_order,lib_L ,D_day, Sc_scores, L_set): 
  total_score = 0
  prev_signup = 0
  scanned_bks = []
  total_libs_done = 0
  l_ix = 0                                                                      # l_ix is the lindex of the library to be signed up in order l_ix
  scan_lib_info = []

  for i in range(len(signup_order)): 
    #while (prev_signup < D_day): 
    
    lib_bks_ids, lib_id, lib_tot_bks, nbr_ship_bks, signup_days = get_lib_vars(L_set, i) 
    this_lib_scan = []                                                          # list of scanned books from this library
    this_lib_score = 0                                                          # score of scanned books from this library                                 
    #max_ship_scan = nbr_ship_bks * (D - (signup_days + prev_signup))
    
    for bk in lib_bks_ids: 
      if bk not in scanned_bks: 
        this_lib_score += int(Sc_scores[int(bk)])
        this_lib_scan.append(bk)

    total_score += this_lib_score
    scanned_bks.extend(this_lib_scan)

    prev_signup += signup_days
    scan_lib_info.append({'lib_id':l_ix ,'scanned books':this_lib_scan  })
    total_libs_done +=1
    l_ix +=1

  return total_libs_done, scan_lib_info, total_score, scanned_bks

#================================================================================================================================
def extract_results(tot_lib_done, signup_order, scanned_libs, tot_sc, all_scnd_bks):
  res_file = open("submission.txt", "w")
  line1 = str(tot_lib_done) + '\n'
  res_file.write(line1)
  for counter, lib in enumerate(scanned_libs):
    line2 = '' 
    line2 = str(counter) + ' ' + str(len(scanned_libs[counter]['scanned books'])) +  '\n'
    res_file.write(line2)

    line3 = ''
    bk_list = ''
    bk_list = ' '.join([j for j in scanned_libs[counter]['scanned books']]) 

    line3 = str(counter) + ' '+ bk_list+ '\n'
    res_file.write(line3)
  res_file.write(str(tot_sc))

def main(path): 
  B,L,D, scores, libraries = get_input(path)
  rang, signing_order = rank(B, L, D, scores, libraries)
  total_libraries_done, scanned_lib_info, total_score, all_scanned_bks = optimize(signing_order,L, D, scores, libraries)
  extract_results(total_libraries_done, signing_order, scanned_lib_info, total_score, all_scanned_bks)

if __name__ == "__main__":
  main(PATH)


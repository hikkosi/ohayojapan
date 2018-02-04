###########################
# ohayo_script
# keikoto
# r0 18.02.04 : make
###########################


import tweepy
import time
import math

#Twitter Access Token###
access_token = "949637157425111042-SmdJObQsgSHAyWLmPuFDKuzKg5aRQPF"
access_token_secret = "6jfJOv1f3JVEny5YEtur3vZkWBvImF9oQI2uuF2L9rNGP"
consumer_key = "6QTEFUxVMfYyjq766NIRvo0cr"
consumer_secret = "ug4oFG1n2CC76bmu2LXqMtlvtD6r3dXOTJFj4DX2LfWwgrjvOp"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api=tweepy.API(auth)

#Data Buffer###
id_buff=[]
id_list=[]
id_list_nrt=[]
id_list_nsm=[]
id_list_ex=[]

#Search Span###
timespan=5	#[sec]
loop_cnt_day  = math.ceil(24*3600/timespan)	#[loop/Day]
loop_cnt_hour = math.ceil(3600/timespan)		#[loop/Hour]
loop_cnt_min  = math.ceil(60/timespan)		#[loop/Min]
loop_cnt = 0	 #search loop cont
loop_cnt_over= 0 #search loop count over
twe_cnt_list = ['', 0]*loop_cnt_day			#define array size
twe_cnt_all = 0	#all tweet cnt
twe_cnt_new = 0 #init	
twe_cnt_min = 0
twe_cnt_min2 = 0
twe_cnt_hour = 0
twe_cnt_day = 0

#Searrch Tweet(query)###
while True:
	#Get tweet###
	results = api.search(q='おはよう', count=100)
	for tweet in results:
		date = tweet.created_at
		user = tweet.user
		id_last = tweet.id_str
		name = user.name
		text = tweet.text
		location = user.location

		#RT check###
		if 'RT' in text:
			RT_flg = True
		else:
			RT_flg = False

		#Make List###
		id_buff=[str(date), id_last, name, text, RT_flg, False]
		id_list.append(id_buff)
	

	#Filter Del RT###
	twe_cnt = 0
	dy_line = 0 #date
	id_line = 1 #id
	nm_line = 2 #user name
	txt_line= 3 #tweet text
	RT_line = 4 #RT or not
	sm_line = 5 #same tweet or not
	id_list_nrt=[]
	for twe_tmp in id_list:
		if twe_tmp[RT_line]==False:
			id_list_nrt.append(twe_tmp)	
	
	#Filter SameTweet###
	if loop_cnt >= 1:
		for twe_tmp_ex in id_list_ex:	
			twe_cnt = 0
			for twe_tmp_new in id_list_nrt:
				if twe_tmp_ex[id_line] == twe_tmp_new[id_line]:
					id_list_nrt[twe_cnt][sm_line] = True	#same tweet detected
				twe_cnt+=1
		
		id_list_nsm=[]	#Clear Same Tweet Checked list
		for twe_tmp in id_list_nrt:
			if twe_tmp[sm_line]==False:
				id_list_nsm.append(twe_tmp)

	#for debug
	#f_ex=open('f_ex.txt','w')
	#for ii in id_list_ex:
	#	f_ex.write(str(ii) + "\n")
	#f_ex.close
	#f_nrt=open('f_nrt.txt','w')
	#for ii in id_list_nrt:
	#	f_nrt.write(str(ii) + "\n")
	#f_nrt.close
	#f_nsm=open('f_nsm.txt','w')
	#for ii in id_list_nsm:
	#	f_nsm.write(str(ii) + "\n")
	#f_nsm.close


	#Calc Tweet Cnt###
	if loop_cnt >=1:
		date_line = 0
		cnt_line = 1
		twe_cnt_date = id_list_nsm[0][dy_line]
		twe_cnt_new = len(id_list_nsm)
		twe_cnt_list[loop_cnt] = [str(twe_cnt_date), twe_cnt_new]	#Add new tweet cnt to list
		#twe_cnt_list[loop_cnt][cnt_line] = twe_cnt_new			#Add new tweet cnt to list
		twe_cnt_beforem = twe_cnt_list[loop_cnt - loop_cnt_min]
		twe_cnt_all = twe_cnt_all + twe_cnt_new

		if loop_cnt <= loop_cnt_min:
			twe_cnt_min = twe_cnt_min + twe_cnt_new
		else:
			twe_cnt_exmin = twe_cnt_list[loop_cnt - loop_cnt_min]
			twe_cnt_min = twe_cnt_min + twe_cnt_new - twe_cnt_exmin	#add new and substract old one

		if loop_cnt <= loop_cnt_hour:
			twe_cnt_hour = twe_cnt_hour + twe_cnt_new
		else:
			twe_cnt_exhour = twe_cnt_list[loop_cnt - loop_cnt_hour]
			twe_cnt_hour = twe_cnt_hour + twe_cnt_new - twe_cnt_exhour #add new and substract old one
			twe_cnt_min2 = twe_cnt_hour/60 #moving average from hour tweet cnt

		twe_cnt_day=0	
		if loop_cnt_over >= 1:
			for cnt_tmp in range( loop_cnt_day - 1):
				twe_cnt_day = twe_cnt_day + twe_cnt_list[cnt_tmp][cnt_line]
	
	
	#Out Result###
	print("Search Loop [cnt/" + str(timespan) + "sec] :" + str(loop_cnt))
	print("Get Tweet [cnt/" + str(timespan) + "sec] :" + str(len(id_list)))
	print("RT Filtered [cnt/" + str(timespan) + "sec] :" + str(len(id_list_nrt)))
	print("New Tweet [cnt/" + str(timespan) + "sec] :" + str(twe_cnt_new))
	print("All Tweet [cnt] :" + str(twe_cnt_all))
	print("Tweet Minute [cnt/Min]" + str(twe_cnt_min))
	print("Tweet Minute2[cnt/Min]" + str(twe_cnt_min2))
	print("Tweet Hour [cnt/Hour]" + str(twe_cnt_hour))
	print("Tweet Day [cnt/Day]" + str(twe_cnt_day))
	print("--------------------------------------")
	#ii=0
	#for twe_tmp in id_list_nsm:
	#	ii = ii +1
	#	print(str(ii) + ":" + twe_tmp[nm_line] + ", " + twe_tmp[txt_line])	


	#List Renwe###
	id_list_ex = id_list_nrt #update old list
	id_list = []			 #clear list to get new search result
	time.sleep(timespan)
	loop_cnt+=1
	if loop_cnt > loop_cnt_day:
		loop_cnt = 0
		loop_cnt_over+=1
		
		f_ex=open('ohayo_day' + str(loop_cnt_over) + '.txt','w')
		for ii in twe_cnt_list:
			f_ex.write(str(ii) + "\n")
		f_ex.close



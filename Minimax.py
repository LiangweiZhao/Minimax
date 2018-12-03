import time
#HW2 of LiangweiZhao
BELONG_SPLA = 1    #An applicant is already in SPLA
BELONG_LAHSA = -1  #An applicant is already in LAHSA
ONLY_SPLA = 1      #An applicant only can go to SPLA
ONLY_LAHSA = -1    #An applicant only can go to LAHSA
BOTH = 2           #An applicant can go both of them
#P is related to the meaning of applicant or homeless people
def checkApplicants(P_Arr_Belong,P_Info):
	#P_Info is a string which contains 20 chars
	P_ID = int(P_Info[:5])
	gender = P_Info[5]
	age = int(P_Info[6:9])
	pet = P_Info[9]
	medical = P_Info[10]
	car = P_Info[11]
	dL = P_Info[12]
	if gender == 'F' and age > 17 and pet == 'N':
		if car == 'Y' and dL == 'Y' and medical == 'N': #Both
			P_Arr_Belong[P_ID] = BOTH
		else: #Only LAHSA 
			P_Arr_Belong[P_ID] = ONLY_LAHSA
	else: 
		if car == 'Y' and dL == 'Y' and medical == 'N': #Only SPLA
			P_Arr_Belong[P_ID] = ONLY_SPLA
		#Neither doesn't change the value
#Update the Week_States by add or delete applicant
def update_Wk_States(Week_States,id,oper):
	Week_Info = P_Arr_Week[id]
	for i in range(1,len(Week_States)):
			Week_States[i] += int(Week_Info[i]) * oper
#To get current used space each day(Just for initializing)
def P_EachDay_Start(Week_States,P_Arr_SL,P_Info):
	P_ID = int(P_Info[:5])
	if P_ID in P_Arr_SL:
		update_Wk_States(Week_States,P_ID,1)

#Check applicant P_Info is fine to add(*It will change Week_States)
def check_Valid(Week_States,id,SPACE):
	week_Info = P_Arr_Week[id]
	for i in range(1,len(Week_States)):
		if Week_States[i] + int(week_Info[i])> SPACE:
			return False
	return True
#Add new applicant if it is valid
def add_New_P(Week_States,id,X_Arr):
	update_Wk_States(Week_States,id,1)
	X_Arr.append(id)
#Scores
def score(days_Arr):
	sum = 0
	for i in days_Arr:
		sum += int(i)
	return sum
#Get max scores of valid apps based on current week states
def validPs(Week_States,validList,sco,SPACE):
	lenList = len(validList)
	maxSum = 0
	if lenList == 0:
		return sco
	elif lenList == 1:
		if check_Valid(Week_States,validList[0],SPACE):
			return sco + validList[0]
		return sco
	for i in range(lenList):
		Week_Tmp = list(Week_States)
		if check_Valid(Week_Tmp,validList[i],SPACE):
			curSum = score_Arr[validList[i]]
			update_Wk_States(Week_Tmp,validList[i],1)
		else:
			continue
		for j in range(lenList):
			if j == i: continue
			if check_Valid(Week_Tmp,validList[j],SPACE):
				update_Wk_States(Week_Tmp,validList[j],1)
				curSum += score_Arr[validList[j]]
		if curSum > maxSum:
			maxSum = curSum
	return maxSum+sco

#dfs for S_Max
def S_Max(id,S_Arr,L_Arr):
	print S_Arr
	print L_Arr
	print optScore_SL
	print "S"
	list_L = []
	if id != 0:
		add_New_P(Week_States_S,id,S_Arr)
		P_Arr_States[id] = ONLY_SPLA
		optScore_SL[0] += score_Arr[id]
	sco = optScore_SL[1]
	for i in range(lenL):
		cur_ID = P_LRmID_Sorted[i]
		if P_Arr_States[cur_ID] == 0:
			if check_Valid(Week_States_L,cur_ID,LAHSA_b):
				list_L.append(cur_ID)
				sco += score_Arr[cur_ID]
	#sco = validPs(Week_States_L,list_L,sco,LAHSA_b)
	if len(list_L) != 0:
		score = [0,0]
		for i in list_L:
			tmpSL = L_Max(i,S_Arr,L_Arr)
			if(tmpSL[1] > score[1]):
				score = list(tmpSL)
			tmpPop = L_Arr.pop(-1)
			P_Arr_States[tmpPop] = 0
			optScore_SL[1] -= score_Arr[tmpPop]
			update_Wk_States(Week_States_L,tmpPop,-1)
			if sco <= tmpSL[1]: return score
		return score
	else:
		if id != 0:
			return L_Max(0,S_Arr,L_Arr)
		else:
			return optScore_SL
#dfs for L_Max
def L_Max(id,S_Arr,L_Arr):
	print S_Arr
	print L_Arr
	print optScore_SL
	print "L"
	list_S = []
	if id != 0:
		add_New_P(Week_States_L,id,L_Arr)
		P_Arr_States[id] = ONLY_LAHSA
		optScore_SL[1] += score_Arr[id]
	sco = optScore_SL[0]
	for i in range(lenS):
		cur_ID = P_SRmID_Sorted[i]
		if P_Arr_States[cur_ID] == 0:
			if check_Valid(Week_States_S,cur_ID, SPLA_pk):
				list_S.append(cur_ID)
				sco += score_Arr[cur_ID]
	#sco = validPs(Week_States_S,list_S,sco,SPLA_pk)
	if len(list_S) != 0:
		score = [0,0]
		for i in list_S:
			tmpSL = S_Max(i,S_Arr,L_Arr)
			if(tmpSL[0] > score[0]):
				score = list(tmpSL)
			tmpPop = S_Arr.pop(-1)
			P_Arr_States[tmpPop] = 0
			optScore_SL[0] -= score_Arr[tmpPop]
			update_Wk_States(Week_States_S,tmpPop,-1)
			if sco <= tmpSL[0]: return score
		return score
	else:
		if id != 0:
			return S_Max(0,S_Arr,L_Arr)
		else:
			return optScore_SL

start = time.clock()
input_file = open("input2.txt","r")
output_file = open("output.txt","w")
#Get Input Data
LAHSA_b = int(input_file.readline())
SPLA_pk = int(input_file.readline())
#People in LAHSA
P_LAHSA = int(input_file.readline())
P_Arr_LAHSA = []
for i in range(P_LAHSA):
	P_Arr_LAHSA.append(int(input_file.readline()))
#People in SPLA
P_SPLA = int(input_file.readline())
P_Arr_SPLA = []
for i in range(P_SPLA):
	P_Arr_SPLA.append(int(input_file.readline()))
#People total
P = int(input_file.readline())
P_Arr = [] #start by index 0
P_Arr_States = [0 for i in range(P+1)] # (0:free,-1:LAHSA,1:SPLA)
P_Arr_Belong = [0 for i in range(P+1)] # (0:Neither,-1:LAHSA,1:SPLA,2:Both)
P_Arr_Week = ["" for i in range(P+1)] # (WeekState info)
Week_States_S = [0 for i in range(8)] # To store current states of parking lots each day
Week_States_L = [0 for i in range(8)] # To store current states of beds each day
for i in range(P):
	#Add all applicants' info
	tmp = input_file.readline()
	tmp1 = tmp.strip()
	P_Arr.append(tmp1)
	P_Arr_Week[i+1] = "-" + tmp1[13:20]
	checkApplicants(P_Arr_Belong,tmp1) #check which service applicants can go
	P_EachDay_Start(Week_States_S,P_Arr_SPLA,tmp1) #update current parking lot occupied
	P_EachDay_Start(Week_States_L,P_Arr_LAHSA,tmp1) #update current beds occupied
	#Update current states of applicants
	if i < P_LAHSA:
		P_Arr_States[P_Arr_LAHSA[i]] = ONLY_LAHSA
	if i < P_SPLA:
		P_Arr_States[P_Arr_SPLA[i]] = ONLY_SPLA

optScore_SL = [0,0]
#Count the score of each App
score_Arr = [0 for i in range(P+1)]
for i in range(1,P+1):
	score_Arr[i] = score(P_Arr[i-1][13:20])
#Remain applicants
P_SPLA_RmID = []
P_LAHSA_RmID = []
S_maxScore = 0
for i in range(1,len(P_Arr_States)):
	if(P_Arr_States[i] == 0):
		if P_Arr_Belong[i] == BOTH:
			P_SPLA_RmID.append(i)
			P_LAHSA_RmID.append(i)
			S_maxScore += score_Arr[i]
		elif P_Arr_Belong[i] == ONLY_SPLA:
			P_SPLA_RmID.append(i)
			S_maxScore += score_Arr[i]
		elif P_Arr_Belong[i] == ONLY_LAHSA:
			P_LAHSA_RmID.append(i)
#Sort Remain Array by the 7 days occupied
P_SRmID_Sorted = list(P_SPLA_RmID)
P_LRmID_Sorted = list(P_LAHSA_RmID)
P_SRmID_Sorted = sorted(P_SRmID_Sorted,reverse=True,key=lambda x:score_Arr[x])
P_SRmID_Sorted = sorted(P_SRmID_Sorted,reverse=True,key=lambda x:P_Arr_Belong[x])
P_LRmID_Sorted = sorted(P_LRmID_Sorted,reverse=True,key=lambda x:score_Arr[x])
P_LRmID_Sorted = sorted(P_LRmID_Sorted,reverse=True,key=lambda x:P_Arr_Belong[x])
print P_SRmID_Sorted
print Week_States_S
print P_LRmID_Sorted
print Week_States_L
#Count initial Score
for i in P_Arr_SPLA:
	optScore_SL[0] += score_Arr[i]
	S_maxScore += score_Arr[i]
for i in P_Arr_LAHSA:
	optScore_SL[1] += score_Arr[i]

lenS = len(P_SPLA_RmID)
lenL = len(P_LAHSA_RmID)
canUse = [0 for i in range(P+1)]
optID = ""
optScore = [0,0]
for i in P_SPLA_RmID:
	if not check_Valid(Week_States_S,i,SPLA_pk): continue
	val = S_Max(i,[],[])
	update_Wk_States(Week_States_S,i,-1)
	P_Arr_States[i] = 0
	optScore_SL[0] -= score_Arr[i]
	if val[0] > optScore[0]:
		optID = P_Arr[i-1][:5]
		optScore = list(val)
	if S_maxScore <= optScore[0]: break
	if time.clock() > start+156: break
print optScore
print optID
print time.clock() - start
output_file.write(optID)

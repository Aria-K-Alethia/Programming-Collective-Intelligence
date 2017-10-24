#Author:Aria-K-Alethia
#PCI-chapter2-Making Recommendations
from math import sqrt
from collections import defaultdict

critics = {
    'Lisa Rose': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'Superman Returns': 3.5,
        'You, Me and Dupree': 2.5,
        'The Night Listener': 3.0,
    },
    'Gene Seymour': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 1.5,
        'Superman Returns': 5.0,
        'The Night Listener': 3.0,
        'You, Me and Dupree': 3.5,
    },
    'Michael Phillips': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.0,
        'Superman Returns': 3.5,
        'The Night Listener': 4.0,
    },
    'Claudia Puig': {
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'The Night Listener': 4.5,
        'Superman Returns': 4.0,
        'You, Me and Dupree': 2.5,
    },
    'Mick LaSalle': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'Just My Luck': 2.0,
        'Superman Returns': 3.0,
        'The Night Listener': 3.0,
        'You, Me and Dupree': 2.0,
    },
    'Jack Matthews': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'The Night Listener': 3.0,
        'Superman Returns': 5.0,
        'You, Me and Dupree': 3.5,
    },
    'Toby': {'Snakes on a Plane': 4.5, 'You, Me and Dupree': 1.0,
             'Superman Returns': 4.0},
}

#A similarity metric using a changed Euclidean distance
def sim_distance(prefs,person1,person2):
    sim_list = [item for item in prefs[person1] if item in prefs[person2]]
    if(len(sim_list) == 0):return 0
    sum_of_square = sum([(prefs[person1][item] - prefs[person2][item])**2 for item in sim_list])
    return 1/(1+sqrt(sum_of_square))

#A similarity metric using pearson correlation score
def sim_pearson(prefs,person1,person2):
    #to get pearson score,we just need to get three kinds of sum
    #1.sum of item
    #2.sum of item**2
    #3.sum of item1*item2
    sim_list = [item for item in prefs[person1] if item in prefs[person2]]
    n = len(sim_list)
    if(n == 0): return 1
    sum1,sum2,sum1_sq,sum2_sq,p_sum = 0,0,0,0,0
    for item in sim_list:
        sum1 += prefs[person1][item]
        sum2 += prefs[person2][item]
        sum1_sq += prefs[person1][item]**2
        sum2_sq += prefs[person2][item]**2
        p_sum += prefs[person1][item] * prefs[person2][item]
    cov = p_sum - (sum1*sum2/n)
    p_svar = sqrt((sum1_sq - (sum1**2)/n) * (sum2_sq - (sum2**2)/n))
    if(p_svar == 0):return 0
    return cov/p_svar

#ranking the critics
def top_matches(prefs,person,n=5,similarity=sim_pearson):
    scores = [(similarity(prefs,person,other),other) for other in prefs if other != person]
    scores.sort(key = lambda x:-x[0])
    return scores[:n]

#Recommending Items
def get_recommendations(prefs,person,similarity=sim_pearson):

    sim_total = defaultdict(int)
    score_total = defaultdict(int)
    for other in prefs:
        if(other == person):continue
        sim = similarity(prefs,person,other)
        if(sim <= 0):continue
        for item in prefs[other]:
            if(item not in prefs[person] or prefs[person][item] == 0):
                score_total[item] += prefs[other][item]*sim
                sim_total[item] += sim
    rankings = [(total/sim_total[item],item) for item,total in score_total.items()]
    rankings.sort(key = lambda x:-x[0])
    return rankings

#if we want to get the recommendation of different movie,we just transform the dict's key and value
def transform_prefs(prefs):
    result = defaultdict(dict)
    for person in prefs:
        for item in prefs[person]:
            result[item][person] = prefs[person][item]
    return result


#item-based collaborative filtering
def calculate_similar_items(prefs,n=10):
    result={}
    item_prefs = transform_prefs(prefs)
    for item in item_prefs:
        top_match_list = top_matches(item_prefs,item,n,sim_distance)
        result[item] = top_match_list
    return result

#similar function if we want to recommend
def get_recommended_items(prefs,item_match,user):
    user_rating = prefs[user]
    item_scores = defaultdict(int)
    total_sim = defaultdict(int)
    for (item,rating) in user_rating.items():
        for (similarity,item2) in item_match[item]:
            if(item2 in user_rating):continue
            item_scores[item2] += rating*similarity
            total_sim[item2] += similarity
    rankings = [(total/total_sim[item],item) for (item,total) in item_scores.items()]
    rankings.sort(key = lambda x:-x[0])
    return rankings

#Exercise 1:Tanimoto coefficient(Jaccard coefficient)
#Tanimoto is suitable for the data where the data is 0(don't have) or 1(have)
#this metric only tell you the similarity between two set.
#does't suit for the movie rating data
def sim_tanimoto(prefs,person1,person2):
    #get the union set of person1 and person2
    union_set = set([item for item in prefs[person1] if prefs[person1][item]!=0]\
                    + [item for item in prefs[person2] if prefs[person2][item]!=0])
    #get the intersection of person1 and person2
    intersection = set([item for item in prefs[person1] if item in prefs[person2]])
    return len(intersection)/len(union_set)












#Author:Aria-K-Alethia
#PCI-chapter2-Making Recommendations
from math import sqrt

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




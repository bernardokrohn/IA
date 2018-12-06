import copy
import numpy as np

class Node():
    def __init__(self, prob, parents = [] ):
        self.prob = prob
        self.parents = parents
        
    
    def computeProb(self, evid):

        p = copy.deepcopy(self.prob)
        s = self.prob[0]
        for e in self.parents:
            p = p[evid[e]]
            s = p

        return np.array([1 - s , s ])


    
class BN():
    def __init__(self, gra, prob):
        self.gra = gra
        self.prob = prob

    def computePostProb(self, evid):
        evid1 = list(evid)
        evid2 = list(evid)

        enum1 = []
        enum2 = []
        for i in range(len(evid)):
            if evid[i] == -1:
                evid1[i] = 1
                evid2[i] = []
    
        self.evid_possabilities(evid1,enum1)
        self.evid_possabilities(evid2,enum2)

        p1 = 0
        for e in enum1:
            p1 = p1 + self.computeJointProb(e)

        p2 = 0
        for e in enum2:
            p2 = p2 + self.computeJointProb(e)

        return p1/p2
        

        
    def computeJointProb(self, evid):
        
        joint_prob = 1
        e = 0

        for p in self.prob:
            joint_prob = joint_prob * p.computeProb(evid)[evid[e]]
            e = e + 1
        
        return joint_prob


    def evid_possabilities(self, evid, poss):
            
        done = True
        for i in range(len(evid)):
            if evid[i] == []:
                done = False
                t = evid[:]
                f = evid[:]
                t[i] = 1
                f[i] = 0
                self.evid_possabilities(t,poss)
                self.evid_possabilities(f,poss)
                break
        if done:
            poss.append(tuple(evid))



gra = [[],[],[0,1],[2],[2]]
p1 = Node( np.array([.001]), gra[0] ) # burglary
p2 = Node( np.array([.002]), gra[1] ) # earthquake
p3 = Node( np.array([[.001,.29],[.94,.95]]), gra[2] ) # alarm
p4 = Node( np.array([.05,.9]), gra[3] ) # johncalls
p5 = Node( np.array([.01,.7]), gra[4] ) # marycalls
prob = [p1,p2,p3,p4,p5]
gra = [[],[],[0,1],[2],[2]]
bn = BN(gra, prob)

ev = (0,0,1,0,0)
print(bn.computeJointProb(ev))

jp = []
for e1 in [0,1]:
    for e2 in [0,1]:
        for e3 in [0,1]:
            for e4 in [0,1]:
                for e5 in [0,1]:
                    jp.append(bn.computeJointProb((e1, e2, e3, e4, e5)))
print("sum joint %.3f (1)" % sum(jp))



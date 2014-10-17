#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
#---------------------------------------------------------------------------
class Apriori(object):

    def __init__(self, filename):
        self.min_support = 14
        self.min_confidence = 20
        self.item_num = 11 # 项目数

        self.location = [[i] for i in range(self.item_num)]
        self.support = [0] * len(self.location)
        self.num = [i for i in range(self.item_num)] # 记录item

        self.pre_support = self.sut(self.location)
        self.pre_location = self.location
        self.pre_num = list(sorted(set([j for i in self.pre_location for j in i])))

        self.item_name = [] # 项目名
        self.find_item_name(filename)

    def deal_line(self, line):
        "提取出需要的项"
        return [i.strip() for i in line.split(' ') if i][2:]

    def find_item_name(self, filename):
        "根据第一行抽取item_name"
        with open(filename, 'r') as F:
            for index,line in enumerate(F.readlines()):
                if index == 0:
                    self.item_name = self.deal_line(line)
                    break

    def sut(self, location):
        """
        输入[[1,2,3],[2,3,4],[1,3,5]...]
        输出每个位置集的support [123,435,234...]
        """
        with open('basket.txt', 'r') as F:
            support = [0] * len(location)
            for index,line in enumerate(F.readlines()):
                if index == 0: continue
                # 提取每信息
                item_line = self.deal_line(line)
                for index_num,i in enumerate(location):
                    flag = 0
                    for j in i:
                        if item_line[j] != 'T':
                            flag = 1
                            break
                    if not flag:
                        support[index_num] += 1
        return support

    def select(self,  c):
        "返回位置"
        stack = []
        for i in self.pre_location:
            for j in self.num:
                if j in i:
                    if len(i) == c:
                        stack.append(i)
                else:
                    stack.append([j] + i)
        # 多重列表去重
        import itertools
        s = sorted([sorted(i) for i in stack])
        self.location = list(s for s,_ in itertools.groupby(s))

    def del_location(self):
        "清除不满足条件的候选集"
        # 小于最小支持度的剔除
        for index,i in enumerate(self.support):
            if i < 1000 * self.min_support / 100:
                self.support[index] = 0
        # apriori第二条规则,剔除
        for index,j in enumerate(self.location):
            sub_location = [j[:index_loc] + j[index_loc+1:]for index_loc in range(len(j))]
            flag = 0
            for k in sub_location:
                if k not in self.pre_location:
                    flag = 1
                    break
            if flag:
                self.support[index] = 0
        # 删除没用的位置
        self.location = [i for i,j in zip(self.location,self.support) if j != 0]
        self.support = [i for i in self.support if i != 0]

    def loop(self):
        s = 2
        while self.num and self.location:
            print '-'*80
            print 'The' ,s - 1,'loop'
            print 'location' , self.pre_location
            print 'support' , self.pre_support
            print 'num' , self.pre_num
            print '-'*80

            # 生成下一级候选集
            self.select(s)
            self.support = self.sut(self.location)
            self.del_location()
            s += 1
            if not self.location:
                break

            self.pre_num = list(sorted(set([j for i in self.location for j in i])))
            self.pre_location = self.location
            self.pre_support = self.support

    def confidenc_sup(self):
        "计算confidence"
        if sum(self.pre_support) == 0:
            print 'min_support error'
        else:
            for index_location,each_location in enumerate(self.pre_location):
                del_num = [each_location[:index] + each_location[index+1:] for index in range(len(each_location))]
                xy = self.sut(del_num)
                print del_num
                print self.pre_support[index_location]
                print xy
                if not del_num[0]:
                    print 'min_support error'
                    break
                for index,i in enumerate(del_num):
                    index_support = 0
                    if len(self.pre_support) != 1:
                        index_support = index
                    support =  float(self.pre_support[index_location])/10
                    s = [j for index_item,j in enumerate(self.item_name) if index_item in i]
                    if xy[index]:
                        print ','.join(s) , '->>' , self.item_name[self.pre_num[index]] , ' min_support: ' , str(support) + '%' , ' min_confidence:' , self.pre_support[index_location]/float(xy[index])

def main():
    c = Apriori('basket.txt')
    c.loop()
    c.confidenc_sup()

if __name__ == '__main__':
    main()

############################################################################

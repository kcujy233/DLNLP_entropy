import os
import re
import math
import time
import jieba

def stopwordslst(addr):#获得停词表
    stop_sum = 0  # 总的中文字符数
    stop_num_dic = {}  # 存储中文字符和出现次数的字典
    with open(addr, "r", encoding='utf-8', errors='ignore') as file1:
        fop = file1.readlines()
        for line in fop:
            wd = line.strip()#清除掉空格之类的乱七八糟的东西
            stop_sum += 1  # 总的中文字符数+1
            stop_num_dic[wd] = stop_num_dic.get(wd, 0) + 1
        del fop, line
    print('一共有：', stop_sum, ' 个停词')
    dic_lst = list(stop_num_dic.keys())
    return '|'.join(dic_lst)

def get_dic(dic, words):#一元模型
    for i in range(len(words)-1):
        dic[words[i]] = dic.get(words[i], 0) + 1
def get_dou_dic(dic, words):#二元模型
    for i in range(len(words)-1):
        dic[(words[i], words[i+1])] = dic.get((words[i], words[i+1]), 0) + 1
def get_tri_dic(dic, words):#三元模型
    for i in range(len(words)-2):
        dic[((words[i], words[i+1]), words[i+2])] = dic.get(((words[i], words[i+1]), words[i+2]), 0) + 1

def cal_uni(lst, words_sum):
    before = time.time()
    words_dic = {}
    get_dic(words_dic, lst)
    words_num = len(words_dic)
    print('\n')
    print("一元模型长度：", words_sum)
    print("出现的一元种类为：", words_num)
    print("平均词长:", round(words_sum / words_num, 5))
    entropy = []
    for uni_word in words_dic.items():
        entropy.append(-(uni_word[1] / words_sum) * math.log(uni_word[1] / words_sum, 2))
    print("基于词的一元模型的中文信息熵为:", round(sum(entropy), 5), "比特/词")
    after = time.time()
    print("一元运行时间：", round(after - before, 5), "s")

def cal_dou(lst):
    before = time.time()
    words_dic = {}
    douwords_dic = {}

    get_dic(words_dic, lst)
    get_dou_dic(douwords_dic, lst)
    douwords_num = len(douwords_dic)
    print('\n')
    douwords_len = sum([dic[1] for dic in douwords_dic.items()])
    print("二元模型长度：", douwords_len)
    print('出现的二元词组种类为：', douwords_num)
    print("平均词长:", round(douwords_len / douwords_num, 5))

    entropy = []
    for bi_word in douwords_dic.items():
        jp_xy = bi_word[1] / douwords_len  # 计算联合概率p(x,y)
        cp_xy = bi_word[1] / words_dic[bi_word[0][0]]  # 计算条件概率p(x|y)
        entropy.append(-jp_xy * math.log(cp_xy, 2))  # 计算二元模型的信息熵
    print("基于词的二元模型的中文信息熵为:", round(sum(entropy), 5), "比特/词")
    after = time.time()
    print("运行时间:", round(after - before, 5), "s")

def cal_tri(lst):
    before = time.time()
    words_dic = {}
    triwords_dic = {}

    get_dou_dic(words_dic, lst)
    get_tri_dic(triwords_dic, lst)
    triwords_num = len(triwords_dic)
    print('\n')
    triwords_len = sum([dic[1] for dic in triwords_dic.items()])
    print("三元模型长度:", triwords_len)
    print('出现的三元词组种类为：', triwords_num)
    print("平均词长:", round(triwords_len / triwords_num, 5))

    entropy = []
    for tri_word in triwords_dic.items():
        jp_xy = tri_word[1] / triwords_len  # 计算联合概率p(x,y)
        cp_xy = tri_word[1] / words_dic[tri_word[0][0]]  # 计算条件概率p(x|y)
        entropy.append(-jp_xy * math.log(cp_xy, 2))  # 计算三元模型的信息熵
    print("基于词的三元模型的中文信息熵为:", round(sum(entropy), 5), "比特/词")

    after = time.time()
    print("运行时间：", round(after - before, 5), "s")

start_time = time.time()
'''得到停词表'''
stopstr = stopwordslst("cn_stopwords.txt")
print('停词表为：', stopstr)
'''不分词，将每个字独立看待进行运算'''
filepath = 'D:/PythonProject/About_NLP/ch/'#需要遍历的文件夹
word_num = 0
wordlst = ''#最终将所有中文放到一个str里
char_sum = 0#记录总字符数，包括停词以及非中文字符
words_sum = 0#记录除了停词表中意外的字符出现个数
spe = '白马啸西风.txt'#需要单独遍历的文件
for root, path, fil in os.walk(filepath):
    for txt_file in fil:
        if txt_file != spe:#用来进行特定文章查找，全部遍历请删除这个条件判断
            continue
        with open(root+txt_file, "r", encoding='ANSI', errors='ignore') as file:
            fp = file.readlines()
            for line in fp:
                line = line.replace('\n', '')
                line = line.replace(' ', '')
                line = line.replace('　　', '')
                line = line.replace('\t', '')
                char_sum += len(line)
                wordstr = re.sub(stopstr, '', line)
                words_sum += len(wordstr)
                wordlst = wordlst + wordstr
            del file, fp
print('文章总字符数(包括停词)为： ', char_sum)
print('文章除去停词总字符数为： ', words_sum)
cal_uni(wordlst, words_sum)
'''应用分词后的结果'''
words_lst = []
words_sum = 0#记录除了停词表中意外的字符出现个数
for root, path, fil in os.walk(filepath):
    for txt_file in fil:
        if txt_file != spe:#用来进行特定文章查找，全部遍历请删除这个条件判断
            continue
        with open(root+txt_file, "r", encoding='ANSI', errors='ignore') as file:
            fp = file.readlines()
            for line in fp:
                line = line.replace('\n', '')
                line = line.replace(' ', '')
                line = line.replace('　　', '')
                line = line.replace('\t', '')
                wordstr = re.sub(stopstr, '', line)
                for x in jieba.cut(wordstr):
                    words_lst.append(x)
                    words_sum += 1
print('分词后的词组总数为： ', words_sum)
cal_uni(words_lst, words_sum)
cal_dou(words_lst)
cal_tri(words_lst)
end_time = time.time()
print('总共运行时间为: ', round(end_time - start_time, 5), "s")
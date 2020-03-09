import math
# Longest Common Prefix Array, 高度数组







#   作为基础我们先实现suffix array 后缀数组.
"""


2>后缀Suffix(i): 对于字符串中的任意一个索引i开始到字符串结束的子串称之为该字符串S的一个后缀。比如suffix(i) = S[i...len(s)].

3>后缀数组SA(i)：将一个字符串S的所有后缀串，按照字典顺序依次放入到一个数组中，这个数组表明了S的所有后缀串的字典顺序，这样一个有序的后缀串数组就是后缀数组。

后缀数组SA(i)表示排名第i的字符串是谁？当然要注意的是这里的SA(i)的值是一个索引，是第i名的后缀串在原有串的起始索引值。


————————————————
版权声明：本文为CSDN博主「dreamhougf」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/dreamhougf/article/details/43735687








    Suffix Array
    
    给一个字符串,计算他的后缀数组并且排序.
    ------------------
    In computer science, a suffix array is a sorted array of all suffixes
    of a string. It is a data structure used, among others, in full text
    indices, data compression algorithms and  within the field
    of bioinformatics.

    for more info : http://algs4.cs.princeton.edu/63suffix/
    Complexity :
        worst case : O(n log(n))
"""


def suffix_array(t):
    """
    Suffix array of a string t
    :param t: the string to extract suffix array from
    :return (s_array, rank): return a tuple that contain the  suffix array
    and the rank array which is the reversed version of the suffix array
    """
    length = len(t)
    rank = [0] * length
    s_array = [0] * length
    tuple_array = [0] * length
    iterations = int(math.log(length, 2)) + 1
    size = 1

    for i, t in enumerate(t):
        s_array[i] = ord(t)

    for _ in range(iterations):
        for i, ele in enumerate(tuple_array):
            if i + size < length: # 在迭代步奏里面也修改这个数组的内容.
                tuple_array[i] = ((s_array[i], s_array[i + size]), i)
            else: # 数组的最后一个元素的处理. 因为最后一个元素,没有后面的了,所以只存自己.
                tuple_array[i] = ((s_array[i], -1), i)  # 写-1表示优先级最高.



# 下面处理tuple_array
        tuple_array.sort()   # 按照tuple 的第一个位置排,重了再看后面的位置.
        s_array[tuple_array[0][1]] = 0
        for i in range(1, len(tuple_array)): # 处理tupple_aray
            cls, idx = tuple_array[i]
            if cls == tuple_array[i - 1][0]: # 如果当前跟上一个一样.就跟上一个值一样
                s_array[idx] = s_array[tuple_array[i - 1][1]]
            else:#否则就+1
                s_array[idx] = s_array[tuple_array[i - 1][1]] + 1
        size *= 2

    for i, p in enumerate(s_array):
        rank[p] = i

    return s_array, rank


tmp=suffix_array("abcdeda")
print(tmp)



#[1, 2, 3, 5, 6, 4, 0],[6, 0, 1, 2, 5, 3, 4] 返回结果s_array是这个表示.
#  后缀树的升序排列的首index.  abcdeda
#  的后缀数组为:直接看后面这个数组即可
# 6表示 abcdeda[6:]   为a   0表示abcdeda  1表示bcdeda  .....这就是后缀树的升幂排列.
# 都写下来就是:   a,  abcdeda, bcdeda, cdeda,da,deda,eda,
#
#
"""


假设字符串S, 后缀数组sa, LCP数组lcp, 那么有后缀S[sa[i]...]与S[sa[i + 1]...]的最长公共前缀的长度为lcp[i]。

    LCP Array
    ------------------
    the longest common prefix array (LCP array) is an auxiliary data
    structure to the suffix array. It stores the lengths of the longest
    common prefixes (LCPs) between all pairs of consecutive suffixes
    in a sorted suffix array.

    I use Kasai's algorithm in implementation :
    Pseudo Code: http://algs4.cs.princeton.edu/32bst

    Complexity :
     worst case :O(n)

"""


def lcp_array(t_str, s_array, rank):
    """

    :param t_str: the string to calculate the lcp array for
    :param s_array: the suffix array of the string
    :param rank: the suffix array reversed
    :return: the lcp array
    """
    t_length = len(t_str)
    lcp = [0] * t_length
    last_lcp = 1

    for i, ele in enumerate(s_array):
        last_lcp = last_lcp - 1 if last_lcp > 1 else 0
        if ele == t_length - 1:
            last_lcp = 0
            lcp[ele] = last_lcp
            continue
        n_suffix = rank[ele + 1]

        while i + last_lcp < t_length \
                and n_suffix + last_lcp < t_length \
                and t_str[i + last_lcp] == t_str[n_suffix + last_lcp]:
            last_lcp += 1
        lcp[ele] = last_lcp

    return lcp
print(lcp_array("abcdeda",suffix_array("abcdeda")[0],suffix_array("abcdeda")[1]))
# 后缀数组是:都写下来就是:   a,  abcdeda, bcdeda, cdeda,da,deda,eda,
#  lcp是:[1, 0, 0, 0, 1, 0, 0]


# 第一个1是以为内  a,  abcdeda 公共前缀是1个
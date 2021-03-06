# encoding=utf-8

"""
@desc:
设置问题模板，为每个模板设置对应的SPARQL语句。demo提供如下模板：

"""
from refo import finditer, Predicate, Star, Any, Disjunction
import re

# TODO SPARQL前缀和模板
SPARQL_PREXIX = u"""
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX : <http://www.semanticweb.org/kizzy/ontologies/2020/2/untitled-ontology-11#>
"""

SPARQL_SELECT_TEM = u"{prefix}\n" + \
             u"SELECT {select} WHERE {{\n" + \
             u"{expression}\n" + \
             u"}}\n"



class W(Predicate):
    def __init__(self, token=".*", pos=".*"):
        self.token = re.compile(token + "$")
        self.pos = re.compile(pos + "$")
        super(W, self).__init__(self.match)

    def match(self, word):
        m1 = self.token.match(word.token.decode("utf-8"))
        m2 = self.pos.match(word.pos)
        return m1 and m2


class Rule(object):
    def __init__(self, condition_num, condition=None, action=None):
        assert condition and action
        self.condition = condition
        self.action = action
        self.condition_num = condition_num

    def apply(self, sentence):
        matches = []
        for m in finditer(self.condition, sentence):
            i, j = m.span()
            matches.extend(sentence[i:j])

        return self.action(matches), self.condition_num




class QuestionSet:
    def __init__(self):
        pass

    @staticmethod
    def to_zhiyu(word_object):
        #桂枝汤方课用于治疗
        select = u"?x"
        sparql = None

        for w in word_object:
            if w.pos == tang_ji:
                e = u" :{tangji} :治疗_to ?o."\
                    u" ?o :症状名称 ?x.".format(tangji=w.token.decode('utf-8'))
            sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                              select=select,
                                              expression=e)
            break
        return sparql
    
    @staticmethod
    def to_xuewei(word_object):
        #中风需要搭配的穴位
        select = u"?x"
        sparql = None

        for w in word_object:
            if w.pos == zheng_zhuang:
                e = u" :{bingzheng} :配穴_by ?o."\
                    u" ?o :详细配穴 ?x.".format(bingzheng=w.token.decode('utf-8'))
            sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                              select=select,
                                              expression=e)
            break
        return sparql

    @staticmethod
    def to_tangji(word_object):
        #治疗中风的汤剂
        select = u"?x"
        sparql = None

        for w in word_object:
            if w.pos == zheng_zhuang:
                e = u" :{bingzheng} :治疗_by ?o."\
                    u" ?o :汤方名称 ?x.".format(bingzheng=w.token.decode('utf-8'))
            sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                              select=select,
                                              expression=e)
            break
        return sparql

    @staticmethod
    def to_zhize(word_object):
        #桂枝汤方的治则效果
        select = u"?x"
        sparql = None

        for w in word_object:
            if w.pos == tang_ji :
                e = u" :{tangji} :汤方治则 ?x.".format(tangji=w.token.decode('utf-8'))
            sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                              select=select,
                                              expression=e)
            break
        return sparql






# TODO 定义关键词
zheng_zhuang = "nz"
tang_ji = "nz"
pei_xue = "nz"


zheng_zhuang_entity = (W(pos=zheng_zhuang))
tang_ji_entity = (W(pos=tang_ji))
pei_xue_entity = (W(pos=pei_xue))

tangji = (W("汤方"))
bingzheng = (W("病症"))
xuewei =(W("穴位"))
zhiliao = (W("治疗"))
zhize = (W("治则"))

# TODO 问题模板/匹配规则
"""
#桂枝汤方用于治疗病症
#中风需要搭配的穴位
#治疗中风的汤方
#桂枝汤方的治则效果
"""
rules = [
    Rule(condition_num=2, condition=tang_ji_entity + Star(Any(), greedy=False) + bingzheng + Star(Any(), greedy=False), action=QuestionSet.to_zhiyu) ,
    Rule(condition_num=2, condition=zheng_zhuang_entity + Star(Any(), greedy=False) + xuewei + Star(Any(), greedy=False), action=QuestionSet.to_xuewei), 
    Rule(condition_num=2, condition=zheng_zhuang_entity + Star(Any(), greedy=False) + tangji + Star(Any(), greedy=False), action=QuestionSet.to_tangji) ,
    Rule(condition_num=2, condition=tang_ji_entity + Star(Any(), greedy=False) + zhize + Star(Any(), greedy=False), action=QuestionSet.to_zhize)
]






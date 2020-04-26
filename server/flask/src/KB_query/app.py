
from flask import Flask,request
from flask_cors import CORS
import jena_sparql_endpoint,question2sparql,question_temp

app = Flask(__name__)
 
@app.route('/test',  methods=['post'])
def hello_world():
    data = request.get_json(silent=True)
    question = data['question']
    my_query = q2s.get_sparql(question.encode("utf-8").decode('utf-8'))
    if my_query is not None:
        result = fuseki.get_sparql_result(my_query)
        value = fuseki.get_sparql_result_value(result)

            # TODO 查询结果为空，根据OWA，回答“不知道”
        if len(value) == 0:
            return "I don\'t know. :("
        elif len(value) == 1:
            return ''.join(value)
        else:
            output = ''
            for v in value:
                output += v + u'、'
                return ''.join(output[0:-1])

    else:
        return  "'I can\'t understand. :('"
            # TODO 自然语言问题无法匹配到已有的正则模板上，回答“无法理解”
        #print ('I can\'t understand. :(')
 
if __name__ == '__main__':
    # TODO 连接Fuseki服务器。
    fuseki = jena_sparql_endpoint.JenaFuseki()
    # TODO 初始化自然语言到SPARQL查询的模块，参数是外部词典列表。
    q2s = question2sparql.Question2Sparql(['./external_dict/word.txt'])
    app.run(port=5000)
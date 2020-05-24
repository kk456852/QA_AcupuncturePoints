
import React from 'react';
import ReactDOM from 'react-dom';
import 'antd/dist/antd.css';
import { Layout, Menu, Breadcrumb } from 'antd';
import { Input, Button,Collapse} from 'antd';
import { Tooltip } from 'antd';
import axios from 'axios';
import { Component } from 'react';

const { Header, Content, Footer } = Layout;
const { Panel } = Collapse;

function callback(key) {
  console.log(key);
}
  
function query_knowledge(question) {
   var x=  document.getElementById("input")
   // x.value
   axios.post('/test', {
    question: x.value
  })
  .then(function (response) {
   // console.log(response);
   
   var answer = response.data
   var  y=  document.getElementById("answer")
   y.innerHTML = answer
   
  })
  .catch(function (error) {
    console.log(error);
  });
}
class main extends Component{
    render(){
        return(
            <Layout className="layout">
    <Header>
      <div className="logo" />
      <Menu
        theme="dark"
        mode="horizontal"
        defaultSelectedKeys={['2']}
      >
        <Menu.Item key="1">主页</Menu.Item>
      </Menu>
    </Header>
    <Content style={{ padding: '0 50px' , margin : "10px 0px 15px 5px"}}>
      <Breadcrumb style={{ margin: '16px 0' }}>
        <Breadcrumb.Item>主页</Breadcrumb.Item>
      </Breadcrumb>
      
      <div className="site-layout-content">
      <div style={{ width: '500px ',float:'left' }}>
      <Input id = "input" placeholder ="输入你要查询的知识   例如：什么是太阳病？"  maxLength={100}/>
      </div>
      <div style={{ float:'left', padding:"0 0 0 20px"}}  >
      <Button type="primary" id="查询" onClick={query_knowledge} >查询</Button>
      </div>
      <br />
      <br />
      <Tooltip title="prompt text">
      <span id = "answer"></span>
      </Tooltip>
      </div>
      
    </Content>
    <div style={{ padding: '0 50px'}}>
    <Collapse defaultActiveKey={['1']} onChange={callback}>
          <Panel header="什么是太阳病？" key="2">
            <p>太阳病为《伤寒论》六经病之一，是太阳所主肤表与经络感受外邪，正邪交争于体表，营卫功能失调而发生的疾病，分太阳伤寒，太阳中风，太阳温病三大类。太阳病变证最多，是太阳病篇的特点之一，也最能体现辨证论治精髓的内容，包括太阳病本证、兼证、变证、类似证等四大病证</p>
          </Panel>
    </Collapse>
      </div>
    <Footer style={{ textAlign: 'center' }}>Kizzy ©2020 Created by Tkk</Footer>
  </Layout>
        )
    }
}

export default main;
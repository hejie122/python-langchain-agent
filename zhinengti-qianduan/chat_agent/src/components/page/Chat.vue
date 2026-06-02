<script>
import {marked} from 'marked'
import DOMPurify from 'dompurify'
import * as echarts from 'echarts';

export default {
  name: "Chat",
  data() {
    return {
      thinking:false,
      userID:"",
      isChat: false,
      inputMessage: "请查询2023年1月销售数据，请用柱状图图表分析一下",
      userAvatar: require('@/assets/image/user.jpeg'),
      botAvatar: require('@/assets/image/bot.jpeg'),
      activeChatId: "1",
      chatList: [],
      isShow:false,
    }
  },
  computed: {
    currentChat() {
      return this.chatList.find(x => x.id === this.activeChatId) || {"messages": []};
    }
  },
  mounted() {
      this.userID = localStorage.getItem("userID")
  },
  methods: {
    uploadSuccess(response) {
      if (response.code === 200) {
        this.inputMessage = "上传文件成功:"+response.filename;
        this.sendMessage();
      } else {
        this.$message.error("上传失败");
      }
    },
    selectChat(id) {
      this.activeChatId = id;
    },
    newChat() {
      const id = new Date().getTime().toString();
      const chat = {"id": id, "title": "新对话", "messages": []};
      this.chatList.push(chat);
      this.activeChatId = id;
      this.isChat = true;
    },

    formatMessage(content) {
      return DOMPurify.sanitize(marked.parse(content || ''))
    },
    showEcharts(data) {
      const id = new Date().getTime().toString();
      const reply = {"id": id, role: "assistant", content: "", type: "chart"};
      this.currentChat.messages.push(reply);
      this.$forceUpdate();
      
      this.$nextTick(() => {
        const dom = document.getElementById('chart-' + id);
        if (!dom) return;
        var myChart = echarts.init(dom);
        const json = JSON.parse(data);
        myChart.setOption(json);
      });
    },
    showAnlyze(data) {
      const id = new Date().getTime().toString();
      const reply = {"id": id, role: "assistant", content: data, type: "anlyze"};
      this.currentChat.messages.push(reply);
      this.$forceUpdate();
      
      this.$nextTick(() => {
        const dom = document.getElementById('chart-' + id);
        if (!dom) return;
        var myChart = echarts.init(dom);
        const json = JSON.parse(data.json);
        myChart.setOption(json);
      });
    },

    sendMessage() {
      
      if (this.inputMessage.includes("图表")){
        this.thinking = true
        const id = new Date().getTime().toString();
        const roleMessage ={"id": id, "role": "user", "content": this.inputMessage, "type": "text"};
        this.currentChat.messages.push(roleMessage);
        this.$forceUpdate();
        
        const p = {"question": this.inputMessage, "user_id": this.userID};
        this.$http.get("http://localhost:8000/chat",{params:p})
          .then(rs=>{
            this.thinking = false
            if (rs.data.code === 200){
              this.showEcharts(rs.data.json)
            }else{
              this.$message.error(rs.data.msg)
            }
          })
      }else if (this.inputMessage.includes("数据分析")){
        this.thinking = true
        const id = new Date().getTime().toString();
        const roleMessage ={"id": id, "role": "user", "content": this.inputMessage, "type": "text"};
        this.currentChat.messages.push(roleMessage);
        this.$forceUpdate();
        
        const p = {"question": this.inputMessage, "user_id": this.userID};
        this.$http.get("http://localhost:8000/chat",{params:p})
          .then(rs=>{
            this.thinking = false
            this.isShow = true
            if (rs.data.code === 200){
              this.showAnlyze(rs.data.data)
            }else{
              this.$message.error(rs.data.msg)
            }
          })
      } else {
        const id = new Date().getTime().toString();
        const roleMessage ={"id": id, "role": "user", "content": this.inputMessage, "type": "text"};
        this.currentChat.messages.push(roleMessage);
        
        const assistantMessage ={"id": id+1, "role": "assistant", "content": "", "type": "text"};
        this.currentChat.messages.push(assistantMessage);
        
        const p = `question=${encodeURIComponent(this.inputMessage)}&user_id=${this.userID}`;
        const s = new EventSource("http://localhost:8000/chat?"+p);
        s.onmessage = (e) => {
          const data = JSON.parse(e.data);
          if(data.done){
            s.close();
            return;
          }
          assistantMessage.content += data.content;
          this.$forceUpdate();
        }
      }
    }
  }
}
</script>

<template>
  <el-container>
    <el-header>
      <el-row>
        <el-col :span="8"><h1>AI智能数据分析助手</h1></el-col>
        <el-col :span="8">&nbsp;</el-col>
        <el-col :span="8" align="right" style="padding-top: 10px">
          <el-button type="success">退出登录</el-button>
          <el-button type="success">用户:{{ userID }}</el-button>
        </el-col>
      </el-row>
    </el-header>
    <el-container>
      <el-aside width="260px">
        <div align="center">
          <br>
          <el-button type="primary" icon="el-icon-plus" @click="newChat">新对话</el-button>
        </div>
        <hr>
        <el-menu :default-active="activeChatId" @select="selectChat" background-color="wheat">
          <el-menu-item
            v-for="chat in chatList"
            :key="chat.id"
            :index="chat.id"
          >
            <i class="el-icon-message"></i>
            <span slot="title">
              {{ chat.title.substring(0, 5) }}
              <el-button type="text" size="small" icon="el-icon-delete"></el-button>
            </span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <el-main>
          <div v-for="x in currentChat.messages" :key="x.id" class="chat-message" :class="x.role">
            <div>
              <el-avatar :src="x.role === 'user' ? userAvatar : botAvatar"></el-avatar>
            </div>
            <div>
              <div 
                v-if="x.type === 'text'" 
                v-html="formatMessage(x.content)" 
                class="bubble">
              </div>

              <div 
                v-if="x.type === 'chart' && x.role === 'assistant'" 
                :id="`chart-${x.id}`"
                style="width: 800px;height: 300px" 
                class="bubble">
              </div>

              <div v-if="x.type === 'anlyze' && x.content">
                <div v-if="x.content.table" id="first">
                  <el-table :data="x.content.table.data || []" style="width: 100%">
                    <el-table-column 
                      v-for="(j, j_idx) in x.content.table.column_name || []"
                      :key="j_idx"
                      :label="j"
                      :prop="j">
                    </el-table-column>
                  </el-table>
                </div>
                
                <div 
                  id="second" 
                  v-if="x.content.result" 
                  v-html="formatMessage(x.content.result)">
                </div>
                
                <div 
                  v-if="x.content.json" 
                  :id="`chart-${x.id}`" 
                  style="width: 800px;height: 300px" 
                  class="bubble">
                </div>
              </div>
            </div>
          </div>

          <div v-if="thinking" class="chat-message assistant">
            <div>
              <el-avatar :src="botAvatar"></el-avatar>
            </div>
            <div class="bubble typing-indicator">正在思考...</div>
          </div>

        </el-main>
        <el-footer>
          <el-form :inline="true">
            <el-form-item>
              <el-input type="textarea" v-model="inputMessage" style="width: 1100px"></el-input>
            </el-form-item>

            <el-form-item>
              <el-upload
                action="http://localhost:8000/upload"
                :show-file-list="false"
                :on-success="uploadSuccess"
              >
                <el-button icon="el-icon-upload2">上传文件</el-button>
              </el-upload>
            </el-form-item>

            <el-form-item>
              <el-button type="success" icon="el-icon-message" @click="sendMessage">发送</el-button>
            </el-form-item>
          </el-form>
        </el-footer>
      </el-container>
    </el-container>
  </el-container>
</template>

<style scoped>
.el-header {
  background-image: url(../../assets/image/login.jpeg);
  background-size: cover;
  background-repeat: no-repeat;
  overflow: hidden;
  height: 100%;
}

.el-footer {
  background-color: white;
  color: #333;
}

.el-aside {
  background-color: wheat;	
  color: #333;
  text-align: center;
}

.el-main {
  overflow: auto;
  height: 700px;
}

.chat-message {
  display: flex;
  gap: 12px;
  margin: 10px 0;
}

.chat-message.user {
  flex-direction: row-reverse;
}

.user .bubble {
  background: #409eff;
  color: #fff;
  padding: 12px 16px;
  border: 1px solid #eee;
  border-radius: 12px;
}

.assistant .bubble {
  background: white;
  color: #333;
  padding: 12px 16px;
  border: 1px solid #eee;
  border-radius: 12px;
}
</style>
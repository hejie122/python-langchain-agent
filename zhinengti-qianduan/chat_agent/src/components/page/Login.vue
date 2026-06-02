<script>
export default {
  name: "Login",
  data(){ //数据
    return{
         name:"", //姓名
         email:"", //邮箱
         code:"" //验证码
    }
  },
  methods:{ //方法
       sendCode(){ //发送验证码
            const p = {"email":this.email}
            this.$http.post("http://localhost:8000/send_code",p)
            .then(rs => {
              if(rs.data.code === 200){
                this.$message.success(rs.data.msg)
              }else{
                this.$message.warning(rs.data.msg)
              }
            })
       },
       login(){ //登录
            const p = {"email":this.email,"code":this.code}
            this.$http.post("http://localhost:8000/login",p)
            .then(rs => {
              if(rs.data.code === 200){
                this.$message.success(rs.data.msg)
                localStorage.setItem("userID",this.email)
                this.$router.push("/chat")
              }else{
                this.$message.warning(rs.data.msg)
              }
            })
       },
      signSend(){ //发送验证码
            const p = {"email":this.email}
            this.$http.post("http://localhost:8000/signup_sendemail",p)
            .then(rs => {
              if(rs.data.code === 200){
                this.$message.success(rs.data.msg)
              }else{
                this.$message.warning(rs.data.msg)
              }
            })
       },
       signup(){ //注册
            const p = {"name":this.name,"email":this.email,"code":this.code}
            this.$http.post("http://localhost:8000/signup",p)
            .then(rs => {
              if(rs.data.code === 200){
                this.$message.success(rs.data.msg)
                this.$router.push("/chat")
              }else{
                this.$message.warning(rs.data.msg)
              }
            })
       },
  }
}
</script>

<template>
  <div class="login-one">
    <el-row>
      <el-col :span="8">
        &nbsp;
      </el-col>
      <el-col :span="8">
        <br><br><br><br><br><br><br><br><br>
		<h1 align="center">AI智能数据分析助手</h1>
        <el-tabs type="border-card">
          <el-tab-pane label="用户登录">
             
            <el-form   label-width="80px">

              <el-form-item label="邮箱">
                <el-input v-model="email" ></el-input>
              </el-form-item>

              <el-form-item label="验证码">
				 <el-col :span="12">
					 <el-input v-model="code" ></el-input>
				 </el-col>
				 <el-col :span="1">
					 &nbsp;
				 </el-col>
                 <el-col :span="11">
					  <el-button type="success" icon="el-icon-message"  @click="sendCode">发送验证码</el-button>
				 </el-col>
              </el-form-item>

              <el-form-item >
                    <el-button type="success" icon="el-icon-user-solid" @click="login" >登录</el-button>
                   
              </el-form-item>

            </el-form>

          </el-tab-pane>
          <el-tab-pane label="用户注册">
					
					<el-form   label-width="80px">

            <el-form-item label="姓名">
                <el-input v-model="name" ></el-input>
              </el-form-item>
					
					  <el-form-item label="邮箱">
					    <el-input v-model="email" ></el-input>
					  </el-form-item>
					
					  <el-form-item label="验证码">
					   		<el-col :span="12">
					   					 <el-input v-model="code" ></el-input>
					   				 </el-col>
					   				 <el-col :span="1">
					   					 &nbsp;
					   				 </el-col>
					                    <el-col :span="11">
					   					  <el-button type="success" icon="el-icon-message"  @click="signSend">发送验证码</el-button>
					   				 </el-col>
					  </el-form-item>
					
					  <el-form-item >
					        <el-button type="success" icon="el-icon-user-solid" @click="signup" >注册</el-button>
					      
					  </el-form-item>
					
					</el-form>
		  </el-tab-pane>

        </el-tabs>

      </el-col>
      <el-col :span="8">
        &nbsp;
      </el-col>
    </el-row>

  </div>
</template>

<style scoped>
@import url('../../assets/css/login.css');
</style>

<template>
  <div class="login">
    <img src="../assets/opcito.png">
    <h1>Log In</h1>
    <form>

    <div class="form-group">
      <label>Email id<span class="text-danger">*</span></label> 
      <input type="email" v-model.trim="$v.email_id.$model" placeholder="Enter email address" :class="{'is-invalid': validationStatus($v.email_id)}" class="form-control" />
      <div style="margin-left: -70px;margin-top: -25px;margin-bottom: 10px;}" v-if="!$v.email_id.required" class="invalid-feedback">Email_id feild is required.</div>
      <div style="margin-left: -83px;margin-top: -25px;margin-bottom: 10px;}" v-if="!$v.email_id.email" class="invalid-feedback">Email_id is not valid.</div>
    </div>

    <div class="form-group">
      <label>Password<span class="text-danger">*</span></label>
      <input type="password" v-model.trim="$v.password.$model" placeholder="Enter password" :class="{'is-invalid': validationStatus($v.password)}" class="form-control"/>
      <div style="margin-left: -65px;margin-top: -25px;margin-bottom: 10px;}" v-if="!$v.password.required" class="invalid-feedback">Password feild is required.</div>
    </div>
    
    <div class="form-group">
      <button type="submit" :disabled="!$v.email_id.required || !$v.password.required" class="btn btn-success" v-on:click="login()" >Login</button>
      <button type="button" class="btn btn-link"><router-link to='/signup'>Signup</router-link></button>
    </div>

    </form>
  </div>
</template>

<script>
import axios from 'axios'
import {required, email} from 'vuelidate/lib/validators'

export default {
  name: "login",
  data() {
    return {
      email_id: "",
      password: "",
    };
  },
  validations(){
    return {
      email_id: {required, email},
      password: {required},
    };
  },
  methods:{
    validationStatus(validation){
      return typeof validation != "undefined" ? validation.$error : false;
    },
    login(){
      const options = {
        headers: { "Access-Control-Allow-Origin": "*" },
      };
      axios.post('http://0.0.0.0:5000/login', {
        email_id: this.email_id,
        password: this.password,
      },
      options
      )
      .then((result) => {
        this.$v.$touch();
        if (this.$v.$pendding || this.$v.$error) return;

        console.log("result:", result);
        let data = result.data.data;
        localStorage.setItem("id", data.id)
        localStorage.setItem("name", data.first_name)
        localStorage.setItem("access_token",'Bearer '+data.access_token);
        this.$toaster.success('Successfully Log in.')
        this.$router.push({name:"home"});
      })
      .catch((e) => {
        this.$toaster.error('Invalid input data.')
        console.log('error:', e);
      });
    }
  },
  mounted(){
    let user = localStorage.getItem("id");
    if (user) {
      this.$router.push({name:'home'})
    }
  }
};
</script>

<style>
.login .form-group label{
  padding-right: 218px;
}
.h1, h1 {
    font-size: 2.5rem;
    margin-top: 23px;
    margin-bottom: 20px;
}
</style>
<template>
<div id="app">
  <router-view/>
  <vue-confirm-dialog/>
</div>
</template>

<script>
export default {
  name: 'App',
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 10px;
}
.body{
  padding: 0px;
  margin: 0px;
}
.login input, .signup input , .profile input{
    width: 300px;
    height: 40px;
    padding-left: 20px;
    display: block;
    margin-bottom: 30px;
    margin-left: auto;
    margin-right: auto;
    margin-top: 8px;
    border: 2px solid skyblue;
}
.login button, .registration button{
  margin-right:16px;
}
</style>

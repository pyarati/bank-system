import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import login from './components/login.vue';
import signup from './components/signup.vue';
import home from './components/home.vue';
import profile from './components/profile.vue';
import Vuelidate from 'vuelidate'
import VueSimpleAlert from "vue-simple-alert";
import VueConfirmDialog from 'vue-confirm-dialog'
import Toaster from 'v-toaster'
import 'v-toaster/dist/v-toaster.css'
import axios from 'axios'

 
Vue.use(VueRouter);
Vue.use(Vuelidate);
Vue.use(VueSimpleAlert);
Vue.use(VueConfirmDialog);
Vue.use(Toaster, {timeout: 5000})

const routes=[
    {
        name:'home',
        component: home,
        path:'/home'
    },
    {
        name:'signup',
        component: signup,
        path:'/signup'
    },
    {
        name:'login',
        component: login,
        path:'/'
    },
    {
      name:'profile',
      component: profile,
      path:'/profile'
  },
]

axios.interceptors.request.use(
    function (config) {
      var access_token = localStorage.getItem('access_token')
      if(access_token != null){
        config.headers.Authorization=access_token
      }
      return config;
    },
    function (error) {
      return Promise.reject(error);
    }
  );

  // Add a response interceptor
    axios.interceptors.response.use(
    function (response) {
      return response;
    },
    (error) => {
      console.log(error.response)
      if (error.response && error.response.status === 401){
        router.push({name:'login'})
        localStorage.clear()
      }
      return Promise.reject(error);
    }
  );

const router = new VueRouter({
    routes
})

Vue.config.productionTip  = false
Vue.config.devtools = false
new Vue({
    router : router,
    render : h => h(App),
}).$mount('#app')

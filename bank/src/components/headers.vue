<template>
<div class="nav">
    <div class="logo">
        <a href="#"><img src="../assets/opcito.png" alt=""></a>
    </div>
    <div class="profile" v-on:click="menutoggle()">
        <img src="../assets/person-circle.svg">
    </div>
    <div class="menu">
        <ul>
            <li><img src="../assets/person-circle.svg"><a href="#"><router-link :to="'/profile'">My profile</router-link></a></li>
            <li><img src="../assets/box-arrow-left.svg" style="margin-left: -19px;"><a href="#" v-on:click="logout()">Logout</a></li>
        </ul>
    </div>
</div>
</template>

<script>
import axios from 'axios';
export default {
    name:'headers',
    methods:{
        menutoggle(){
            const togglemenu = document.querySelector('.menu');
            togglemenu.classList.toggle('active')
        },

        logout(){
            var access_token = localStorage.getItem('access_token')
            console.log(access_token)
            const options = {
                headers:{
                    "Access-Control-Allow-Origin":"*",
                    Authorization: access_token,
                }
            };
            this.$confirm({
                title: 'Confirm',
                message: 'Are you sure you want to logout?',
                button: {
                yes: 'confirm',
                no: 'cancel'
                },
                callback: confirm => {
                    if(confirm)
                    {
                        axios.delete("http://0.0.0.0:5000/logout", options)
                        .then(() => {
                            localStorage.clear();
                            this.$router.push({name:'login'})
                        })
                        .catch((e) => {
                            console.log(e);
                        });
                    }    
                }
            })
        },
    },
};
</script>

<style>
.nav{
    background-color:#3333;
    overflow: hidden;
}
.nav .logo {
    position: relative;
    float: left;
    margin-left: 18px;
    margin-top: 13px;
    height: 24px;
    overflow: hidden;
    cursor: pointer;
}
.nav .profile {
    position: relative;
    overflow: hidden;
    cursor: pointer;
    margin-top: -50px;
    margin-left: 215px;
    padding-bottom: 10px;
}
.nav .profile img {
    float: right;
    margin-top: 24px;
    margin-left: 1321px;
}
.nav .menu {
    box-sizing: 0 5px 25px rgba(0,0,0,0.1);
    background: bisque;
    right: 8px;
    position: absolute;
    top: 89px;
    padding: 10px 20px;
    width: 160px;
    height: 100px;
    border-radius: 7px;
    visibility: hidden;
    opacity: 0;
}
.nav .menu.active{
    visibility: visible;
    opacity: 1;
}
.nav .menu ul li {
    list-style: none;
    border-top: 1px solid rgba(0,0,0,0.5);
    display: flex;
    padding: 10px 0;
    align-items: center;
    justify-content: center;
    margin-left: -25px;
    margin-right: 10px;
}
.nav .menu ul li img {
    max-width: 20px;
    margin-right: 10px;
    opacity: 0.5;
    transition: 0.5s;
}
.nav .menu ul li:hover img{
    opacity: 1;
}
.nav .menu ul li a {
    color: black;
    display: inline-block;
    font-weight: 500;
    text-decoration: none;
    transition: 0.5s;
}
.nav .menu ul li:hover a {
    color:red;
}
</style>
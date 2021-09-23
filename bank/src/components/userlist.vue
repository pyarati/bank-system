<template>
  <div>
    <!-- <table border="1">
      <tr v-for="item in userlist" v-bind:key="item.id">
        <td>{{ item.id }}</td>
        <td>{{ item.first_name }}</td>
        <td>{{ item.last_name }}</td>
        <td>{{ item.address }}</td>
        <td>{{ item.mobile_number }}</td>
        <td>{{ item.email_id }}</td>
        <td>{{ item.password }}</td>
        <td>{{ item.user_type_id }}</td>
      </tr>
    </table> -->
      <table border="1">
        <tr v-if="item">
          <td>{{ item.id }}</td>
          <td>{{ item.first_name }}</td>
          <td>{{ item.last_name }}</td>
          <td>{{ item.address }}</td>
          <td>{{ item.mobile_number }}</td>
          <td>{{ item.email_id }}</td>
          <td>{{ item.created_at }}</td>
        </tr> 
      <button type='button' v-on:click="getuser()">user</button>
    </table>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "userlist",
  data() {
    return {
      item: undefined,
    };
  },
  methods: {
    getuser() {
        // let x=localStorage.getItem("login-info")
        // console.log(x.constructor.name)
        // let y=x["access_token"];
        // console.log('value for y', y);
       
        axios.defaults.headers.common["Authorization"] =
        "Bearer " + localStorage.getItem("access_value");
        let email_id= localStorage.getItem('email_id')

        let url="http://0.0.0.0:5000/user?email_id="+email_id

        axios.get(url)
        .then((result) => {
          this.item = result.data.data[0]
          console.log(this.item);
        })
        .catch((err) => {
          console.log("AXIOS ERROR: ", err);
        });
    },
  },
};
</script>

<style>
</style>

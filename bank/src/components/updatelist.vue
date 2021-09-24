<template>
<div>
  <headers/>
    <div class="update">
    <h1>Update</h1>
    <input type="text" v-model="userlist.first_name" placeholder="Enter first name" />
    <input type="text" v-model="userlist.last_name" placeholder="Enter last name" />
    <input type="text" v-model="userlist.address" placeholder="Enter address" />
    <input
      type="text"
      v-model="userlist.mobile_number"
      placeholder="Enter mobile number"
    />
    <input type="email" v-model="userlist.email_id" placeholder="Enter email address" />
    <button type="button" v-on:click="update()">Update user</button>
  </div>
</div>
</template>


<script>
import axios from 'axios';
import headers from './headers.vue'

export default {
  name: "updatelist",
  components:{
    headers
  },
  data: function () {
    return {
      userlist:{
      first_name: "",
      last_name: "",
      address: "",
      mobile_number: "",
      email_id: "",
      }
    };
  },
  methods:{
    async update(){
      console.log(this.userlist)
      axios.put("http://0.0.0.0:5000/user/"+this.$route.params.id,
          {
            first_name: this.userlist.first_name,
            last_name: this.userlist.last_name,
            address: this.userlist.address,
            mobile_number: this.userlist.mobile_number,
            email_id: this.userlist.email_id,
          },
        )
        .then((result) => {
          console.log("result:", result);
          //let data = result.data.data;
          this.$router.push();
        })
        .catch((e) => {
          console.log('error:', e);
        });
    }
  },
  async mounted() { 
    let user = localStorage.getItem("email_id");
    if (!user) {
        this.$router.push({name:'signup'})
    }
    let url="http://0.0.0.0:5000/user/"+this.$route.params.id

    axios.get(url)
    .then((result) => {
      this.userlist=result.data.data
    })
    .catch((err) => {
      console.log("AXIOS ERROR: ", err);
    });
  },
};
</script>
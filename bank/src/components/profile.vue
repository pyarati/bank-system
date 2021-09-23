<template>
  <div>
    <headers />
    <div class="profile" v-if="item">
      <h1>Profile</h1>

      <form>
        <div class="form-group">
          <label>First name<span class="text-danger">*</span></label> 
          <input type="text" v-model.trim="$v.item.first_name.$model" placeholder="Enter first name" :class="{'is-invalid': validationStatus($v.item.first_name)}" class="form-control" />
          <div style="margin-left: -60px;margin-top: -25px;margin-bottom: 10px;}" v-if="!$v.item.first_name.required" class="invalid-feedback">First name feild is required.</div>
          <div style="margin-left: -69px;margin-top: -25px;margin-bottom: 10px;}" v-if="!$v.item.first_name.minLength" class="invalid-feedback">You must have at least {{$v.item.first_name.$params.minLength.min}}.</div>
        </div>

        <div class="form-group">
          <label>Last name<span class="text-danger">*</span></label> 
          <input type="text" v-model.trim="$v.item.last_name.$model" placeholder="Enter last name" :class="{'is-invalid': validationStatus($v.item.last_name)}" class="form-control"/>
          <div style="margin-left: -60px;margin-top: -25px;margin-bottom: 10px;}" v-if="!$v.item.last_name.required" class="invalid-feedback">Last name feild is required.</div>
        <div style="margin-left: -69px;margin-top: -25px;margin-bottom: 10px;}" v-if="!$v.item.last_name.minLength" class="invalid-feedback">You must have at least {{$v.item.last_name.$params.minLength.min}}.</div>
        </div>
        
        <div class="form-group">
          <label style="margin-left: -11px;">Address<span class="text-danger">*</span></label> 
          <input type="text" v-model.trim="$v.item.address.$model" placeholder="Enter address" :class="{'is-invalid': validationStatus($v.item.address)}" class="form-control"/>
          <div style="margin-left: -67px;margin-top: -25px;margin-bottom: 10px;}" v-if="!$v.item.address.required" class="invalid-feedback">Address feild is required.</div>
        <div style="margin-left: -69px;margin-top: -25px;margin-bottom: 10px;}" v-if="!$v.item.address.minLength" class="invalid-feedback">You must have at least {{$v.item.address.$params.minLength.min}}.</div>
        </div>
        
        <div class="form-group">
          <label style="margin-left: 36px;">Mobile number<span class="text-danger">*</span></label> 
          <input type="text" v-model.trim="$v.item.mobile_number.$model" placeholder="Enter mobile number"  :class="{'is-invalid': validationStatus($v.item.mobile_number)}" class="form-control"/>
          <div style="margin-left: -50px;margin-top: -25px;margin-bottom: 10px;}" v-if="!$v.item.mobile_number.required" class="invalid-feedback">Mobile number feild is required.</div>
          <div style="margin-left: -32px;margin-top: -25px;margin-bottom: 10px;}" v-if="!$v.item.mobile_number.numeric" class="invalid-feedback">Mobile number feild must be numeric.</div>
          <div style="margin-left: -66px;margin-top: -25px;margin-bottom: 10px;}" v-if="!$v.item.mobile_number.minLength" class="invalid-feedback">You must have at least {{$v.item.mobile_number.$params.minLength.min}}.</div>
          <div style="margin-left: -39px;margin-top: -25px;margin-bottom: 10px;}" v-if="!$v.item.mobile_number.maxLength" class="invalid-feedback">You must have not greater than {{$v.item.mobile_number.$params.maxLength.max}}.</div>
        </div>
        
        <div class="form-group">
          <label style="margin-left: -12px;">Email id<span class="text-danger">*</span></label> 
          <input type="email" v-model.trim="$v.item.email_id.$model" placeholder="Enter email address" :class="{'is-invalid': validationStatus($v.item.email_id)}" class="form-control"/>
          <div style="margin-left: -68px;margin-top: -25px;margin-bottom: 10px;}" v-if="!$v.item.email_id.required" class="invalid-feedback">Email_id feild is required.</div>
          <div style="margin-left: -90px;margin-top: -25px;margin-bottom: 10px;}" v-if="!$v.item.email_id.email" class="invalid-feedback">Email is not valid.</div>
        </div>

        <!-- <router-link :to="'/updatelist/'+item.id"><button type="submit">Editprofile</button></router-link> -->
        <div class="form-group">
          <button type="button" class="btn btn-primary" v-on:click="back()">Back</button>
          <button type="button" class="btn btn-success" v-on:click="updateuser()">Update user</button>
          <button type="button" class="btn btn-danger"  v-on:click="deleteuser()">Delete user</button>
        </div>
      </form>

    </div>
  </div>
</template>

<script>
import axios from "axios";
import { required, email, minLength, maxLength, numeric } from 'vuelidate/lib/validators'
import _ from "lodash";
import headers from "./headers.vue";

export default {
  name: "home",
  components: {
    headers,
  },
  data() {
    return {
      name: "",
      item: {},
    };
  },
  validations(){
    return {
      item: {
        first_name: {required, minLength: minLength(4)},
        last_name: {required, minLength: minLength(4)},
        address: {required, minLength: minLength(3)},
        mobile_number: {required, numeric, minLength: minLength(10), maxLength: maxLength(10)},
        email_id: {required, email},
      }
    }
  },
  methods: {
    validationStatus(validation){
      return typeof validation != "undefined" ? validation.$error : false;
    },
    back() {
      this.$router.push({ name: "home" });
    },
    updateuser() {
      var access_token = localStorage.getItem("access_token");
      //console.log(access_token);
      const options = {
        headers: {
          "Access-Control-Allow-Origin": "*",
          Authorization: access_token,
        },
      };
      var data = {};
      if (this.item.first_name != this.itemCopy.first_name) {
        data["first_name"] = this.item.first_name;
      }
      if (this.item.last_name != this.itemCopy.last_name) {
        data["last_name"] = this.item.last_name;
      }
      if (this.item.address != this.itemCopy.address) {
        data["address"] = this.item.address;
      }
      if (this.item.email_id != this.itemCopy.email_id) {
        data["email_id"] = this.item.email_id;
      }
      if (this.item.mobile_number != this.itemCopy.mobile_number) {
        data["mobile_number"] = this.item.mobile_number;
      }
      if (Object.keys(data).length) {
        axios
          .put("http://0.0.0.0:5000/user/" + this.item.id, data, options)
          .then((result) => {
            this.$v.$touch();
            if (this.$v.$pendding || this.$v.$error) return;

            this.$toaster.success('Successfully Updated data.')
            console.log("result:", result);
            //let data = result.data.data;
            this.back();
          })
          .catch((e) => {
            this.$toaster.error('Invalid input data.')
            console.log("error:", e);
          });
      }
      else{
        this.$toaster.warning('Nothing to update.')
      }
    },
    deleteuser() {
      var access_token = localStorage.getItem("access_token");
      //console.log(access_token);
      const options = {
        headers: {
          "Access-Control-Allow-Origin": "*",
          Authorization: access_token,
        },
      };
      this.$confirm({
        title: 'Confirm',
        message: 'Are you sure you want to delete user?',
        button: {
          yes: 'confirm',
          no: 'cancel'
        },
        callback: confirm => 
        {
          if(confirm)
          {
            axios.delete("http://0.0.0.0:5000/user/" + this.item.id, options)
            .then((result) => {
              console.log("result:", result);
              localStorage.clear();
              this.$router.push({ name: "signup" });
            })
            .catch((e) => {
              console.log(e);
            });
          }    
        }
      })
    },
  },
  async mounted() {
    let user = localStorage.getItem("id");
    if (!user) {
      this.$router.push({ name: "signup" });
    }
    var access_token = localStorage.getItem("access_token");
    //console.log(access_token);
    const options = {
      headers: {
        "Access-Control-Allow-Origin": "*",
        Authorization: access_token,
      },
    };
    let url = "http://0.0.0.0:5000/user/" + user;

    axios
      .get(url, options)
      .then((result) => {
        this.item = result.data.data;
        this.itemCopy = _.cloneDeep(this.item);
      })
      .catch((err) => {
        console.log("AXIOS ERROR: ", err);
      });
  },
};
</script>

<style>
.profile button{
  margin-right: 5px;
}
.profile .form-group label{
  padding-right: 218px;
}
</style>
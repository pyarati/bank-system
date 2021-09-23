<template>
  <div class="signup">
    <img src="../assets/opcito.png">
    <h1>Sign Up</h1>
    <form>

      <div class="form-group">
        <label style="padding-right: 218px;">First name<span class="text-danger">*</span></label>
        <input type="text" v-model.trim="$v.first_name.$model" placeholder="Enter first name" :class="{'is-invalid': validationStatus($v.first_name)}" class="form-control" />
        <div style="margin-left: -60px;margin-top: -25px;margin-bottom: 10px;}" v-if="!$v.first_name.required" class="invalid-feedback">First name feild is required.</div>
        <div style="margin-left: -69px;margin-top: -25px;margin-bottom: 10px;}" v-if="!$v.first_name.minLength" class="invalid-feedback">You must have at least {{$v.first_name.$params.minLength.min}}.</div>
      </div>

      <div class="form-group">
        <label style="padding-right: 218px;">Last name<span class="text-danger">*</span></label>
        <input type="text" v-model.trim="$v.last_name.$model" placeholder="Enter last name" :class="{'is-invalid': validationStatus($v.last_name)}" class="form-control"/>
        <div style="margin-left: -60px;margin-top: -25px;margin-bottom: 10px;}" v-if="!$v.last_name.required" class="invalid-feedback">Last name feild is required.</div>
        <div style="margin-left: -69px;margin-top: -25px;margin-bottom: 10px;}" v-if="!$v.last_name.minLength" class="invalid-feedback">You must have at least {{$v.last_name.$params.minLength.min}}.</div>
      </div>

      <div class="form-group">
        <label style="padding-right: 228px;">Address<span class="text-danger">*</span></label>
        <input type="text" v-model.trim="$v.address.$model" placeholder="Enter address" :class="{'is-invalid': validationStatus($v.address)}" class="form-control"/>
        <div style="margin-left: -67px;margin-top: -25px;margin-bottom: 10px;}" v-if="!$v.address.required" class="invalid-feedback">Address feild is required.</div>
        <div style="margin-left: -69px;margin-top: -25px;margin-bottom: 10px;}" v-if="!$v.address.minLength" class="invalid-feedback">You must have at least {{$v.address.$params.minLength.min}}.</div>
      </div>

      <div class="form-group">
        <label style="padding-right: 183px;">Mobile number<span class="text-danger">*</span></label>
        <input type="text" v-model.trim="$v.mobile_number.$model" placeholder="Enter mobile number" :class="{'is-invalid': validationStatus($v.mobile_number)}" class="form-control" />
        <div style="margin-left: -50px;margin-top: -25px;margin-bottom: 10px;}" v-if="!$v.mobile_number.required" class="invalid-feedback">Mobile number feild is required.</div>
        <div style="margin-left: -32px;margin-top: -25px;margin-bottom: 20px;}" v-if="!$v.mobile_number.numeric" class="invalid-feedback">Mobile number feild must be numeric.</div>
        <div style="margin-left: -66px;margin-top: -25px;margin-bottom: 10px;}" v-if="!$v.mobile_number.minLength" class="invalid-feedback">You must have at least {{$v.mobile_number.$params.minLength.min}}.</div>
        <div style="margin-left: -83px;margin-top: -25px;margin-bottom: 10px;}" v-if="!$v.mobile_number.maxLength" class="invalid-feedback">You must have not greater than {{$v.mobile_number.$params.maxLength.max}}.</div>
      </div>

      <div class="form-group">
        <label style="padding-right: 230px;">Email id<span class="text-danger">*</span></label>
        <input type="email" v-model.trim="$v.email_id.$model" placeholder="Enter email address" :class="{'is-invalid': validationStatus($v.email_id)}" class="form-control"/>
        <div style="margin-left: -68px;margin-top: -25px;margin-bottom: 10px;}" v-if="!$v.email_id.required" class="invalid-feedback">Email_id feild is required.</div>
        <div style="margin-left: -90px;margin-top: -25px;margin-bottom: 10px;}" v-if="!$v.email_id.email" class="invalid-feedback">Email is not valid.</div>
      </div>

      <div class="form-group">
        <label style="padding-right: 218px;">Password<span class="text-danger">*</span></label>
        <input type="password" v-model.trim="$v.password.$model" placeholder="Enter password" autocomplete="on" :class="{'is-invalid': validationStatus($v.password)}" class="form-control"/>
        <div style="margin-left: -64px;margin-top: -25px;margin-bottom: 10px;}" v-if="!$v.password.required" class="invalid-feedback">Password feild is required.</div>
      </div>

      <div class="form-group">
        <div style="margin-top: 12px; margin-bottom: 12px; margin-left: -44px;">
          <label>User type:  </label>
            <input
              style="height: 14px; width: 30px; display: inline"
              type="radio"
              v-model="selectedValue"
              name="usertype"
              value="1"
            />
            <label><span> Admin</span></label>
      
          <input
            style="height: 14px; width: 30px; display: inline"
            type="radio"
            v-model="selectedValue"
            name="usertype"
            value="2"
          />
          <label>Customer</label>
        </div>
      </div>

      <div class="form-group">
        <button type="button" :disabled="!$v.first_name.required || !$v.last_name.required || !$v.address.required || !$v.mobile_number.required || !$v.email_id.required || !$v.password.required" class="btn btn-success" v-on:click="signup()">Sign Up</button>
        <button type="button" class="btn btn-link"><router-link to="/">Login</router-link></button>
      </div>

    </form>
  </div>
</template>

<script>
import axios from "axios";
import {required, email, minLength, maxLength, numeric} from 'vuelidate/lib/validators'

export default {
  name: "signup",
  data: function () {
    return {
      first_name: "",
      last_name: "",
      address: "",
      mobile_number: "",
      email_id: "",
      password: "",
      selectedValue: "2",
    };
  },
  validations(){
    return {
      first_name: {required, minLength: minLength(4)},
      last_name: {required, minLength: minLength(4)},
      address: {required, minLength: minLength(3)},
      mobile_number: {required, numeric, minLength: minLength(10), maxLength: maxLength(10)},
      email_id: {required, email},
      password: {required},
    };
  },
  methods: {
    validationStatus(validation){
      return typeof validation != "undefined" ? validation.$error : false;
    },
    signup() {
      const options = {
        headers: { "Access-Control-Allow-Origin": "*" },
      };
      axios.post(
          "http://0.0.0.0:5000/user",
          {
            first_name: this.first_name,
            last_name: this.last_name,
            address: this.address,
            mobile_number: this.mobile_number,
            email_id: this.email_id,
            password: this.password,
            user_type_id: Number(this.selectedValue),
          },
          options
        )
        .then((result) => {
          this.$v.$touch();
          if (this.$v.$pendding || this.$v.$error) return;

          console.log("result:", result);
          this.$toaster.success('Successfully Registered.')
          this.$router.push({name: "login"});
          
        })
        .catch((e) => {
          this.$toaster.error('Invalid input data.')
          console.log('error:', e);
        });
    },
  },
  mounted() { 
    let user = localStorage.getItem("id");
    if (user) {
        this.$router.push({name:'home'})
    }
  },
};
</script>

<style>
</style>

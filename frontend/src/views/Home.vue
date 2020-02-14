<template>
  <div class="home">
      <form class="mb-5" role="form" method="post">
        <div class="row">
          <div class="col-12">
            <h3 class="title"><small>輸入查詢地址</small></h3>
            <div class="row">
              <div class="col-4"></div>
              <div class="col-4">
                <div class="form-group">
                  <label for="address" class="control-label">查詢地址欄：</label
                  ><label for="address" class="error"></label>
                  <input
                    v-model="form_model.raw_address"
                    type="text"
                    class="form-control"
                    placeholder="範例：台北市中正區南海路13號"
                  />
                </div>
              </div>
              <div class="col-4"></div>
            </div>
          </div>

        </div>
        <button
          type="button"
          class="btn btn-primary require_btn"
          v-on:click="get_google_location"
        >
          確認送出
        </button>
      </form>

      <div class='container'>
        <button
          type="button"
          class="btn btn-primary require_btn mb-3"
          v-on:click="getLocation"
        >
          使用定位尋找
        </button>
        <P>{{ location_message }}</P>
      </div>

      <div v-if="inner_error" class="alert alert-warning" role="alert">
        <h4 class="alert-heading">地址無法定位</h4>
        <p>
          地址無法找到經緯度，請更換輸入地址。
        </p>
        <hr />
        <button
          type="button"
          class="btn btn-info"
          v-on:click="inner_error = false"
        >
          關閉
        </button>
      </div>
      <b><h5 class="mb-2">{{ message }}</h5></b>
      <b v-if="results.length !== 0"><h5 class="mb-2">1公里內醫療院所及健保特約藥局:</h5></b>
      <div class="container">
        <div class="table-responsive">
          <table class="table table-striped">
            <thead
              class="thead-dark"
              v-for="(result, index) in results"
              :key="result.pk"
            >
              <tr v-if="index === 0">
                <th scope="col">#</th>
                <th
                  scope="col"
                  v-for="column_name in column_names"
                  :key="column_name.pk"
                >
                  {{ column_name }}
                </th>
              </tr>
            </thead>
            <tbody v-for="(result, index) in results" :key="result.pk">
              <tr>
                <th scope="row">{{ index + 1 }}</th>
                <td>{{ result.name }}</td>
                <td>{{ result.phone }}</td>
                <td>{{ result.adult }}</td>
                <td>{{ result.child }}</td>
                <td><a :href="'https://www.google.com.tw/maps/place/'+results[index].address">{{ result.address }}</a></td>
                <td>{{ result.update_time }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";

export default {
  name: "home",
  data() {
    return {
      form_model: {
        raw_address: null,
      },
      message:null,
      location_message: null,
      results: [],
      inner_error: false,
      X: null,
      Y: null,
      column_names:[
        '名稱',
        '電話',
        '成人口罩數量',
        '兒童口罩數量',
        '地址',
        '最後更新時間'
      ]
    };
  },
  methods: {
    get_google_location(){
      let endpoint = "get_google_location/";
      this.X = null;
      this.Y = null;
      apiService(endpoint, "POST", this.form_model).then(data => {
        this.X = data["X"];
        this.Y = data["Y"];
        this.inner_error =  data["inner_error"];
        if (!this.inner_error){
          this.getPharmacy();
        };
      })
    },
    getPharmacy() {
      let endpoint = "pharmacy/";
      this.results = [];
      apiService(endpoint, "POST",{"X": this.X, "Y": this.Y}).then(data => {
        this.results = data["pharmacys"];
        this.inner_error =  data["inner_error"];
        this.message = data['message'];
      });
    },
    getLocation(){
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(this.setPosition, this.showError);
      } else {
        this.location_message = "瀏覽器不支援定位，請換個瀏覽器嘗試";
      }
    },
    setPosition(position) {
      this.Y = position.coords.latitude;
      this.X = position.coords.longitude;
      if (this.X !== null | this.Y !== null) {
        this.getPharmacy();
      };
    },
    showError(error) {
      switch(error.code) {
        case error.PERMISSION_DENIED:
          this.location_message = "User denied the request for Geolocation."
          break;
        case error.POSITION_UNAVAILABLE:
          this.location_message = "Location information is unavailable."
          break;
        case error.TIMEOUT:
          this.location_message = "The request to get user location timed out."
          break;
        case error.UNKNOWN_ERROR:
          this.location_message = "An unknown error occurred."
          break;
      }
    }
  }
};
</script>
<style scoped>
.home {
  font-size: 1em;
}
</style>
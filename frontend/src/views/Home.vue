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
          v-on:click="getPharmacy"
        >
          確認送出
        </button>
      </form>

      <div v-if="inner_error" class="alert alert-warning" role="alert">
        <h4 class="alert-heading">Oops Failed!</h4>
        <p>
          伺服器內部查詢錯誤，請檢查輸入地址或稍後再試，感謝！
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

      <b v-if="results.length !== 0"><h5 class="mb-2">500公尺內醫療院所及健保特約藥局:</h5></b>
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
      results: [],
      inner_error: false,
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
    getPharmacy() {
      let endpoint = "pharmacy/";
      this.results = [];
      apiService(endpoint, "POST", this.form_model).then(data => {
        this.results = data["pharmacys"];
        this.inner_error =  data["inner_error"];
      });
    }
  }
};
</script>

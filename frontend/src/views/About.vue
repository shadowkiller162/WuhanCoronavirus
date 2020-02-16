<template>
  <div class="about">
    <h4>使用說明</h4>
    <b><p>1. 以地址方式查詢，輸入查詢地址後，會將1公里內有提供口罩購買的醫療院所及特約藥局列出。</p></b>
    <b><p>2. 點擊定位查詢，會以當前定位將1公里內有提供口罩購買的醫療院所及特約藥局列出。</p></b>
    <b><p> 提供口罩購買的醫療院所及特約藥局（以10個為上限），顯示口罩剩餘相關資訊，並可點擊地址欄，會導航至Google地圖。</p></b>
    <img id="information" :src="inforImgUrl"/>
    <br>
    <h4>資料來源</h4>
    <ul class="list-inline">
      <li class="list-inline-item"><a href="https://g0v.hackmd.io/@kiang/mask-info">口罩供需資訊平台</a></li>
      <li class="list-inline-item"><a href="https://data.nhi.gov.tw/Datasets/DatasetResource.aspx?rId=A21030000I-D50001-001">健保特約機構口罩剩餘數量明細清單</a></li>
    </ul>
    <h4>開發者資訊</h4>
    <b><p>Hughe Chen</p></b>
  </div>
</template>
<script>
export default {
  name: "about",
  data() {
    return {
      inforImgUrl: require( "@/assets/information.jpeg" )
    }
  }
};
</script>
<style  scoped>
#information {
  width: 20rem;
  height: 30rem;
}
</style>
<template>
  <div id="second">
    <ul>
      <li v-for="project in projects">
        {{ project.name }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      author: "微信公众号 benson.zhi",
      projects: [],
    }
  },
  // mounted: function() {
  //     this.$http.jsonp('http://127.0.0.1:8000/api/getproject/', {}, {
  //         headers: {
  //         },
  //         emulateJSON: true
  //       }).then(function(response) {
  //         // 这里是处理正确的回调
  //
  //         this.projects = response.data;
  //         // this.articles = response.data["subjects"] 也可以
  //
  //       }, function(response) {
  //       // 这里是处理错误的回调
  //         console.log(response)
  //       });
  //   }
  created() {
    this.$http.get('http://127.0.0.1:8000/api/getproject/').then((response) => {
      emulateJSON: true;
      this.projects = response.body;
    }).then(function(response) {
      console.log(response)
    });
  }
}

</script>

<style>
</style>

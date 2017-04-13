<template>
  <div id="app">
    <img src="./assets/logo.png">
    <p>{{ message }}</p>
    <!-- <first></first> -->
    <!-- <second></second> -->
    <third></third>
    <!-- <four></four> -->
    <!-- <ul>
      <li><route-link to="/first">第一页</route-link></li>
      <li><route-link to="/second">第二页</route-link></li>
    </ul> -->
    <route-view class="view"></route-view>
  </div>
</template>

<script>
  // import first from './components/first.vue'
  // import second from './components/second.vue'
  import third from './components/third.vue'
  import four from './components/four.vue'
  export default {
    el: '#app',
    data() {
      return {
        message: 'Select your project & tags that you want to release'
      }
    },
    // methods: {
    //   reverseMessage: function () {
    //     this.message = this.message.split('').reverse().join('')
    //   }
    // },
    // components: { first, second }
    components: { third, four }
  }
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>

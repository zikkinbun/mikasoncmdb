// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import VueRouter from "vue-router";
// import VueResource from 'vue-resource'
import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.config.productionTip = false

// Vue.use(VueRouter);
/* eslint-disable no-new */
//开启debug模式
Vue.config.debug = true;

Vue.use(VueRouter);
// Vue.use(VueResource);
Vue.use(VueAxios, axios);

// 定义组件, 也可以像教程之前教的方法从别的文件引入
const First = { template: '<div><h2>我是第 1 个子页面</h2></div>' }
import second from './components/second.vue'
import third from './components/third.vue'
import four from './components/four.vue'

// 创建一个路由器实例
// 并且配置路由规则
const router = new VueRouter({
  mode: 'history',
  base: __dirname,
  routes: [
    {
      path: '/first',
      component: First
    },
    {
      path: '/second',
      component: second
    },
    {
      path: '/third',
      component: third
    },
    {
      path: '/four',
      component: four
    },
  ]
})

// 现在我们可以启动应用了！
// 路由器会创建一个 App 实例，并且挂载到选择符 #app 匹配的元素上。
const app = new Vue({
  router: router,
  render: h => h(App)
}).$mount('#app')

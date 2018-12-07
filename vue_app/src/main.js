import Vue from 'vue'
import router from './router.js'
import App from './App.vue'
import store from './store.js'


Vue.config.productionTip = false

window.vue = new Vue({
  router,
  store,
  ...App
}).$mount('#app')

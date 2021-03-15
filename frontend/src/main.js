import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from './views/Home.vue'
import About from './views/About.vue'
import App from './App.vue'
import { store } from './store.js';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

// Install BootstrapVue
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)
Vue.use(VueRouter)


const router = new VueRouter({
  mode: 'history',
  routes: [
    { path: '/predictor/', name:'references', component: Home },
    { path: '/predictor/about/',name:'toPredict', component: About },
  ]
})


Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

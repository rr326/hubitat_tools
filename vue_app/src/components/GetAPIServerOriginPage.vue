<template>
  <div>
    <div v-if="!triedDefaults">
      <h4>Looking for API Server...</h4>
      <img :src="require('../assets/img/loading.svg')" alt="">
    </div>
    <div v-if="triedDefaults && !storeServerAPIOrigin">
      <h1>Get Origin</h1>
      <input v-model="APIServerIP" placeholder="eg: 127.0.0.1:8027" @keyup.enter="checkIP()">
      <button type="button" class="mdl-button mdl-button--accent mdl-button--raised" v-on:click="checkIP()">Enter</button>
      <div>Local API Server Origin: {{APIServerOrigin}}</div>
      <div>STORE APIServerOrigin: {{storeServerAPIOrigin}}</div>
    </div>
    <div v-if="triedDefaults && storeServerAPIOrigin">
      <h1>Server API Found: {{storeServerAPIOrigin}}</h1>
    </div>
  </div>
</template>

<script>
import {
  testIPP, getOriginP
} from '../assets/js/getIP.js'

export default {
  name: 'GetAPIServerOrigin',
  data() {
    return {
      APIServerIP: null,
      APIServerOrigin: null,
      triedDefaults: false
    }
  },
  methods:  {
    checkIP() {
      let vueInst = this
      testIPP(this.APIServerIP)
        .then(res => {
          vueInst.APIServerOrigin = res
          console.log('Received origin from testIPP', res)
          vueInst.$store.commit('setAPIServerOrigin', res)
          this.$router.push({name:'homePage'})
        })
        .catch(() => {
          console.log(`CheckIP - improper API Server IP: ${this.APIServerIP}`)
        })

    }
  },
  computed: {
    storeServerAPIOrigin() {
      return this.$store.state.APIServerOrigin
    },
  },
  created() {
      let vueInst = this
      getOriginP(vueInst)
      .then(res => {
        vueInst.APIServerOrigin = res
        console.log('Received origin from getOringP', res)
        vueInst.$store.commit('setAPIServerOrigin', res)
        vueInst.triedDefaults = true
        this.$router.push({name:'homePage'})
      })
      .catch(() => {
        console.log('No valid IP found from defaults')
        vueInst.triedDefaults = true
      })
  }, 
  mounted() {
  }, 
}

</script>

<style lang="css" scoped>
</style>

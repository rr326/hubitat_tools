<template>
  <div id="app">
    <div class="navbar">
      <span class="left">
        <span class="item"><router-link to="/logs">Logs</router-link> </span>
        <span class="item"><router-link to="/log/entry">Log Entry</router-link></span>
        <span class="item"><router-link to="/getorigin">Get Origin</router-link></span>
        <span class="item"><span class="bold">HTools Server:</span> {{APIServerOrigin}}</span>
        <span class="item"><span class="bold">Hubitat Portal:</span> {{HubitatServerOrigin}}</span>
      </span>
      <span class=right>
        <span class="item" v-if="this.$store.state.hubitatServerOrigin"><a :href="this.$store.state.hubitatServerOrigin" target="_blank">Portal</a></span>
        <span class="item"><a href="https://docs.hubitat.com/index.php?title=Hubitat_Elevation_Documentation" target="_blank">Docs</a></span>        
      </span>
    </div>
    <router-view></router-view>
  </div>
</template>


<script>
import "./assets/vendor/css/google_material_icons.css"
import "./assets/vendor/css/material.indigo-red.min.css"
import "./assets/vendor/js/material.min.js"
import './assets/css/style.scss'

export default {
  name: 'app',
  components: {},
  data() {
    return {}
  },
  computed: {
    APIServerOrigin() {
      return this.$store.state.APIServerOrigin
    },
    HubitatServerOrigin() {
      return this.$store.state.hubitatServerOrigin
    }
  }, 
  mounted() {
    /**
     * Read Query Params and store globally
     * maxPastLogLines
     */
    let passedMaxPastLogLines = this.$route.query.maxPastLogLines || null
    if (passedMaxPastLogLines !== null) {
      this.$store.commit('setMaxPastLogLines', parseInt(passedMaxPastLogLines))
    }
  }
}

</script>

<style lang="scss" scoped>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin: 20px 10px 0px 10px;
}

.navbar {
  background-color: black;
  color: white;
  padding: 7px 10px;
  display: flex;
  justify-content: space-between;

  .left .item{
    margin-right: 12px;
  }

  .right .item{
    margin-left: 12px;
  }


  a {
    color: white;
    font-weight: 900;
  }

  .bold {
    font-weight: 900;
  }
}
</style>

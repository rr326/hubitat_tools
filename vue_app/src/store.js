import Vue from 'vue'
import Vuex from 'vuex'


Vue.use(Vuex)


export default new Vuex.Store({
  state: {
    APIServerOrigin: null,
    hubitatServerOrigin: null,
    maxPastLogLines: null
  },
  mutations: {
    setAPIServerOrigin(state, origin) {
      state.APIServerOrigin = origin
    },
    setHubitatServerOrigin(state, origin) {
      state.hubitatServerOrigin = origin
    },
    setMaxPastLogLines(state, maxPastLogLines) {
      state.maxPastLogLines = maxPastLogLines
    }
  }
})

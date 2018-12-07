<template>
  <div>
    <h4>Enter text to be inserted into your Hubitat logs</h4>
    <p>Note - Only viewable within Hubitat Tools Log Page</p>

    <div>
      <input type="text" v-model="manualMsg" @keyup.enter="manualMsgClicked()" style="width: 100%">
    </div>
    <div>
      <button type="button" class="mdl-button mdl-button--accent mdl-button--raised" v-on:click="manualMsgClicked()">Enter
      </button>
      <div class="response-message" :class="{'rsp-success': responseSuccess, 'rsp-error': !responseSuccess}" v-if="responseMsg">{{responseMsg}}</div>
    </div>
  </div>
</template>

<script>
const request = require("request")
const moment = require("moment")

export default {
  name: "ManualEntryPage",

  data() {
    return {
      manualMsg: "",
      responseMsg: "",
      responseSuccess: true
    }
  },
  methods: {
    manualMsgClicked() {
      let vueInst = this

      let data = {
        time: moment().format("YYYY-MM-DD hh:mm:ss.SSS a"),
        level: "info",
        type: "***",
        id: "***",
        name: "Manual Log Entry",
        msg: this.manualMsg
      }

      let url = `${this.$store.state.APIServerOrigin}/api/logs/add_manual_entry`
      request({
        method: "POST",
        uri: url,
        json: data
      }, function(error, response) {
        if (error) {
          console.error(`Error posting to ${url}.`)
          vueInst.setResponseMsg(`Error: ${error}`, false, 15000)
        } else {
          if (response.statusCode !== 200) {
            console.error(`Received error response for (${url}): ${response.statusCode}`)
            vueInst.setResponseMsg(`Received error response for (${url}): ${response.statusCode}`, false, 15000)
          } else {
            vueInst.setResponseMsg('Success', true, 5000)
          }
        }
      })
      this.manualMsg = ""
    },
    setResponseMsg(msg, success, timeout = 5000) {
      const vueInst = this
      vueInst.responseMsg = msg
      vueInst.responseSuccess = success
      setTimeout(() => {
        vueInst.responseMsg = ''
      }, timeout)
    }
  }
}

</script>


<style lang="scss" scoped>
.response-message {
  padding: 10px 5px;
}

.rsp-success {
  background-color: #d4edda;
}

.rsp-error {
  background-color: #f5c6cb;
}

input {
  font-size: large;
}
</style>

<template>
  <div>
    <h2>Hubitat Logs</h2>
    <div v-if="!gotLogs">
      <b>Hubitat IP Address: </b>
      <input v-model="hubitatIPAddress" placeholder="192.168.ddd.ddd:dddd" @keyup.enter="hubitatIPEntered">
      <button
        type="button"
        class="mdl-button mdl-button--accent mdl-button--raised"
        v-on:click="getPastLogs()"
        >Go</button>
      <br>
      <hr>
    </div>

    <div>
      <b>Log Level: </b>
      <input type="radio" v-model="levelRadio" id="radioError" value="error">
      <label for="radioError">Manual Log</label>
      <input type="radio" v-model="levelRadio" id="radioWarn" value="warn">
      <label for="radioWarn">Warn</label>
      <input type="radio" v-model="levelRadio" id="radioInfo" value="info">
      <label for="radioInfo">Info</label>
      <input type="radio" v-model="levelRadio" id="radioDebug" value="debug">
      <label for="radioDebug">Debug</label>
    </div>

    <device-picker :devices="devices" v-on:update:selectedDevices="selectedDevices = $event" :devicesOrdered="deviceList"></device-picker>

    <div class="mdl-grid">
      <button
        type="button"
        class="mdl-button mdl-button--accent mdl-button--raised mdl-cell mdl-cell--2-col"
        v-on:click="manualMsgClicked()"
        >Add Log >></button>
      <input type="text" v-model="manualMsg" @keyup.enter="manualMsgClicked()" class="mdl-cell mdl-cell--10-col-desktop mdl-cell--6-col-tablet mdl-cell--12-col-phone">
    </div>

    <table class="mdl-data-table mdl-js-data-table mdl-shadow--2dp logtable">
      <thead>
        <tr>
          <th class="mdl-data-table__cell--non-numeric">Time</th>
          <th class="mdl-data-table__cell--non-numeric">Level</th>
          <th class="mdl-data-table__cell--non-numeric">Type</th>
          <th class="mdl-data-table__cell--non-numeric">ID</th>
          <th class="mdl-data-table__cell--non-numeric" >Name</th>
          <th class="mdl-data-table__cell--non-numeric">Message</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="line in filteredLogs" :key="line.lineno">
          <td class="mdl-data-table__cell--non-numeric">{{line.time}}</td>
          <td class="mdl-data-table__cell--non-numeric">{{line.level}}</td>
          <td class="mdl-data-table__cell--non-numeric">{{line.type}}</td>
          <td>{{line.id}}</td>
          <td class="mdl-data-table__cell--non-numeric" :style="{'background-color': devices[line.name].color, color:'white'}">{{line.name}}</td>
          <td class="mdl-data-table__cell--non-numeric cell-wrap" :style="{'background-color': devices[line.name].color, color:'white'}">{{line.msg}}</td>
        </tr>
      </tbody>
    </table>

  </div>
</template>

<script>
const request = require('request')
const moment = require('moment')
const url = require('url')
import devicePicker from './DevicePicker.vue'

const levels = {
  error: 10,
  warn: 20,
  info: 30,
  debug: 40,
}

export default {
  name: 'LogPage',
  components: {
    devicePicker
  },
  data() {
    return {
      hubitatIPAddress: null,
      logs: [],
      devices: {
        'All': {
          isActive: true
        }
      },
      levels: ['error', 'warn', 'info', 'debug', 'default'],
      levelRadio: 'debug',
      deviceFilter: [],
      selectedDevices: [],
      mockData: false,
      colorize: true,
      loglines: 0,
      manualMsg: '',
      ws: null,
      wsKeepalive: null,
      gotLogs: false
    }
  },
  methods: {
    hubitatIPEntered() {
      if (!this.validIP(this.hubitatIPAddress)) {
        return
      }
      this.$store.commit('setHubitatServerOrigin', `http://${this.hubitatIPAddress}`)
      this.getPastLogs()
    },
    validIP(ip) {
      return (/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(:[0-9]+)?$/.test(ip) ||
        /^localhost(:[0-9]+)?$/.test(ip)
      )
    },
    showWarning(levelText) {
      return levels[levelText] <= levels[this.levelRadio]
    },
    getPastLogs() {
      if (!this.APIServerOrigin || !this.hubitatServerOrigin) {
        console.log(`getPastLogs. Do not yet have origin and hubitatip: ${this.APIServerOrigin} -- ${this.hubitatServerOrigin}`)
        return
      }

      let self = this
      request(`${self.hubitatPastLogUrl}`, function(error, response) {
        if (error) {
          console.error(`Error getting page ${self.hubitatPastLogUrl}.`)
          console.error(error)
        } else {
          if (response.statusCode !== 200) {
            console.error(`Received error response: ${response.statusCode}`)
          } else {
            let logs = JSON.parse(response.body)
            self.addLogs(logs)

            // Now start websocket
            self.insertLogData({
              time: moment().format('YYYY-MM-DD hh:mm:ss.SSS a'),
              level: 'info',
              type: '***',
              id: '***',
              name: 'Manual Log Entry',
              msg: 'vvv Past Logs. ^^^ New logs'
            })
            self.webSocketConnect()
            self.gotLogs = true
          }
        }
      })
    },
    addDevice(device) {
      let match = device.match(/^\s*([^<]*)(<span.*>.*<\/span>\s*)?$/)
      if (!match) {
        throw new Error(`addDevice: got unexpected device: (${device})`)
      }
      let deviceName = match[1]
      if (!(deviceName in this.devices)) {        
        this.$set(this.devices, deviceName, {})
      }
    },
    addLogs(logList) {
      logList.forEach((data) => {
        data.time = new moment(data.time, 'YYYY-MM-DD hh:mm:ss.SSS').format('YYYY-MM-DD hh:mm:ss.SSS a')
        data.lineno = this.loglines
        this.logs.push(data)
        this.loglines += 1
        this.addDevice(data.name)
      })
      if (this.logs.length > 2 && this.logs[1].time > this.logs[0].time) {
        throw new Error('Server is not returning past logs in chronilogical order as expected')
      }

    },
    insertLogData(data) {
      data.lineno = this.loglines
      this.logs.unshift(data)
      this.loglines += 1
      this.addDevice(data.name)
      this.colorizeLogs()
    },
    colorizeLogs() {
      // Slightly modified version of Tableau's new colors
      const colors = ["DeepPink", "#3399ff", "rgb(228,147,67)", "rgb(209,97,93)", "rgb(133,181,178)", "rgb(106,159,88)", "rgb(231,202,95)", "rgb(168,125,159)", "rgb(241,162,169)", "rgb(150,118,98)", "gray"]
      const defaultColor = "silver"

      colors.get = function(index, defaultVal = null) {
        if (index >= this.length) {
          return defaultVal
        } else {
          return this[index]
        }
      }
      this.selectedDevices.forEach((device, idx) => {
        if (this.colorize) {
          this.$set(this.devices[device], 'color', colors.get(idx, defaultColor))
        } else {
          this.$set(this.devices[device], 'color', defaultColor)
        }
      })
    },
    manualMsgClicked() {
      let data = {
        time: moment().format('YYYY-MM-DD hh:mm:ss.SSS a'),
        level: 'info',
        type: '***',
        id: '***',
        name: 'Manual Log Entry',
        msg: this.manualMsg
      }
      this.insertLogData(data)

      let url = `${this.APIServerOrigin}/api/logs/add_manual_entry`
      request({
        method: 'POST',
        uri: url,
        json: data
      }, function(error, response) {
        if (error) {
          console.error(`Error posting to ${url}.`)
        } else {
          if (response.statusCode !== 200) {
            console.error(`Received error response for (${url}): ${response.statusCode}`)
          }
        }
      })
      this.manualMsg = ''
    },
    webSocketConnect() {
      // Hubitat Code, modified
      // var port = location.port ? location.port : "80";
      // var ws = new WebSocket("ws://" + location.hostname + ":" + port + "/logsocket");
      let self = this
      self.ws = new WebSocket(this.hubitatLogsWSUrl)

      self.ws.onmessage = function(msg) {
        let data = JSON.parse(msg.data)
        self.insertLogData(data)
      };

      self.ws.onclose = function(e) {
        console.log(`${moment().format('hh:mm:ss a')}: Socket is closed. Reconnect will be attempted in 5 seconds.`, e.reason);
        setTimeout(function() {
          self.webSocketConnect();
        }, 5000)
      };

      self.ws.onerror = function(err) {
        console.error('Socket encountered error: ', err.message, 'Closing socket')
        self.ws.close()
      }

      // Keepalive - 5 min
      this.wsKeepalive = setInterval(() => {
        if (this.ws) {
          this.ws.send('')
        }
      }, 5 * 60 * 1000)
    }
  },
  computed: {
    APIServerOrigin() {
      return this.$store.state.APIServerOrigin
    },
    hubitatServerOrigin() {
      return this.$store.state.hubitatServerOrigin
    },
    hubitatPastLogUrl() {
      if (!this.$store.state.hubitatServerOrigin) {
        return null
      }
      let hubitat_ip = url.parse(this.$store.state.hubitatServerOrigin).host
      return `${this.$store.state.APIServerOrigin}/api/logs/past?hubitat_ip=${hubitat_ip}&mockData=${this.mockData}&max_log_lines=${this.maxPastLogLines}`
    },
    hubitatLogsWSUrl() {
      if (!this.$store.state.hubitatServerOrigin) {
        return null
      }
      const u = url.parse(this.$store.state.hubitatServerOrigin)
      return `ws://${u.host}:80/logsocket`
    },
    filteredLogs() {
      return this.logs.filter((log) => {
        return (
          (levels[log.level] <= levels[this.levelRadio]) &&
          (this.selectedDevices.includes(log.name))
        )
      })
    },
    deviceList() {
      const specialOrder = ['All', 'Manual Log Entry']

      let sorted = Object.keys(this.devices).sort(function(a, b) {
        let aIdx = specialOrder.indexOf(a),
          bIdx = specialOrder.indexOf(b)
        if (aIdx >= 0 && bIdx >= 0) {
          return aIdx - bIdx
        } else if (aIdx >= 0) {
          return -1
        } else if (bIdx >= 0) {
          return +1
        } else {
          return a.localeCompare(b)
        }
      })
      return sorted
    },
    maxPastLogLines() {
      return this.$store.state.maxPastLogLines || 1000
    }
  },
  mounted() {
    /**
     * Read Query Params
     * hubitatIP
     * mockData
     * nocolor 
     *
     * Note - maxPastLogLines is handled globally by App & Vuex
     * They probably all should be, but I don't feel like fixing them all.
     * Why global? So you can pass them once and they stick.
     */
      

    let passedIP = this.$route.query.hubitatIP || null
    if (this.validIP(passedIP)) {
      this.hubitatIPAddress = passedIP
      this.$store.commit('setHubitatServerOrigin', `http://${this.hubitatIPAddress}`)
    } else if (passedIP !== null) {
      console.error('Looks like you tried to pass in an ip address but it is not of the proper format. Got: ', passedIP)
    }

    let passed_nocolor = this.$route.query.noColor || null
    if (passed_nocolor !== null) {
      this.colorize = false
    }

    this.mockData = this.$route.query.mockData || false

    this.getPastLogs()

  },
  beforeDestroy() {
    if (this.ws) {
      this.ws.close()
    }
    if (this.wsKeepalive) {
      clearTimeout()
    }
  },
  watch: {
    selectedDevices() {
      this.colorizeLogs()
    },

  }

}

</script>

<style lang="scss" scoped>
.logtable {
  font-family: Monaco, monospace;

  .cell-wrap {
    white-space: normal;
  }

  tbody tr, tbody td {
    height: 15px;
    line-height: 15px;
  }

  tbody td {
    vertical-align: top;
    padding: 5px 5px;
  }

  thead {
    th {
      font-size: large;
      font-style: bold;
    }
    tr {
      border-bottom: solid rgba(0, 0, 0, 0.54);
      margin-bottom: 10px;  // This is not working. No idea why not.
    }
  }
}
</style>

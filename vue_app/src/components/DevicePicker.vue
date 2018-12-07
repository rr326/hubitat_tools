<template>
  <div>
    <div class="device-buttons">
      <button 
        v-for="device in devicesOrdered" 
        :key="device" 
        v-on:click="deviceButton(device)"
        class="mdl-button"
        :class="{active: deviceStates[device].isActive}"
        :style="{'background-color': deviceColor(device, deviceStates[device].isActive)}"  
        >
        {{device}}        
      </button>

    </div>
  </div>
</template>

<script>
export default {
  name: 'device-picker',
  props: ['devices', 'devicesOrdered'],
  data() {
    return {
      deviceStates: {
        All: {
          isActive: true
        },
      },
      selectedDevices: []
    }
  },
  mounted() {
    this.updateAllDevices()
  },
  methods: {
    updateSelectedDevices() {
      this.selectedDevices = Object.keys(this.deviceStates).filter((key) => { return (key !== 'All' && this.deviceStates[key].isActive)})      
      this.$emit('update:selectedDevices', this.selectedDevices )
    },
    deviceButton(value) {
      console.log('Button pressed: ', value)      
      let oldval = this.deviceStates[value].isActive
      this.deviceStates[value].isActive = ! oldval
      if (value === 'All') {
        Object.keys(this.deviceStates).forEach((deviceName) => {
          this.deviceStates[deviceName].isActive = this.deviceStates['All'].isActive
        })
      }
      this.updateSelectedDevices()
    },
    updateAllDevices() {
      this.devicesOrdered.forEach((device) => {
        if (!(device in this.deviceStates)) {
          this.$set(this.deviceStates, device, {isActive: true})
        }
      })
      this.updateSelectedDevices()
    },
    deviceColor(deviceName, isActive) {
      if (!isActive) {
        return "#f5f5f5"
      } else if (deviceName === 'All') {
        return "#337ab7"
      } else {
        return this.devices[deviceName].color
      }
    }
  },
  computed: {
  },
  watch: {
    devicesOrdered() {
      this.updateAllDevices()
    }
  }
}

</script>

<style lang="scss" scoped>
.device-buttons {
  margin: 10px 0px;

}
</style>

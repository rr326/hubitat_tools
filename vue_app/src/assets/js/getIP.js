/*
 This is complicated because:
 1. It's REALLY nice to use vue's hot-reloader in development. When you do that, the web page's location.origin != the server's origin
 2. So, you need to specify the server's origin
 3. But that's annoying, so all this is to try to guess, and work both for development and production
 */

const rp = require('request-promise')

export function testIPP(ip) {
  let l = window.location

  return testOriginP(`${l.protocol}//${ip}`)
}

export function testOriginP(origin) {
  let uri = `${origin}/api/ping`

  return rp({
      uri: uri,
      json: true
    })
    .then((data) => {
      if (data && data.ping && data.ping === 'success') {
        return Promise.resolve(origin)
      } else {
        console.log('Error getting ${uri}. Received response, but not of proper format. Received: ${data}')
        return Promise.reject(null)
      }
    })
    .catch((err) => {
      return Promise.reject(err)
    })
}

function testOriginArrayP(origins) {
  return testOriginP(origins.shift())
  .then((origin) => {
    return origin
  })
  .catch(() => {
    if (origins.length > 0) {
      return testOriginArrayP(origins) // shifted
    } else {
      return Promise.reject(`No valid server origins in ${origins}`)
    }
  })
}

export function getOriginP(vueInst) {
  let l = window.location,
    originsToTry = []

  // Passed origin
  if (vueInst && vueInst.$route && vueInst.$route.query && vueInst.$route.query.serverIP) {
    originsToTry.push(`${l.protocol}//${vueInst.$route.query.serverIP}`)
  }
  originsToTry.push(`${l.origin}`)  // window.location.origin
  originsToTry.push(`${l.protocol}//${l.hostname}:8027`) // default Origin



  return testOriginArrayP(originsToTry)
}

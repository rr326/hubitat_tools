import Vue from 'vue'
import VueRouter from 'vue-router'

const store = require('./store.js').default

const LogPage = require('./components/LogPage.vue').default
const ManualEntryPage = require('./components/ManualEntryPage.vue').default

Vue.use(VueRouter)

const routes = [
{
  path: '/',
  name: 'homePage',
  component: LogPage
},
{
  path: '/logs',
  component: LogPage
},
{
  path: '/log/entry',
  component: ManualEntryPage
},
{
  path: '/getorigin',
  name: 'getOrigin',
  component: require('./components/GetAPIServerOriginPage.vue').default
},
{
  path: '*',
  component: require('./components/404Page.vue').default
}]

const router = new VueRouter({
  mode: 'history',
  routes
})
export default router

/*
 * Get Server IP First
 */
let origPath = null,
  final = false
let ensureAPIServerOriginUnregister = null

  // Make sure the app is initialized
function ensureAPIServerOrigin(to, from, next) {
  // If no origin, goto getOrigin
  if (!store.state.APIServerOrigin) {
    if (to.name === 'getOrigin') {
      next()
    } else {
      origPath = {...to} // Vue bug. Need to copy the object.
      next({
        name: 'getOrigin',
        query: origPath.query
      })
    }
    return
  }

  if (store.state.APIServerOrigin) {
    // Remove the hook
    if (store.state.APIServerOrigin) {
      if (ensureAPIServerOriginUnregister) {
        ensureAPIServerOriginUnregister()
      } else {
        console.error('ensureAPIServerOrigin - unregister hook does not exist!')
      }
    }

    // If you've already set the origPath, move on
    if (final) {
      next()
      return
    }

    // If origPath, go there
    if (origPath) {
      final = true
      next(origPath)
      return
    }

    // Else, goto homePage
    if (to.name != 'homePage') { // Avoid circular loop
      next({
        name: 'homePage'
      })
    } else {
      next()
    }
    return
  }
}

// Register the hook
ensureAPIServerOriginUnregister = router.beforeEach(ensureAPIServerOrigin)

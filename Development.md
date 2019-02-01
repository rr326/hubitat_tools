# Development Page

## TODO
* Export button
* Bug
    * When you enter data on the phone, it should show up on the desktop
    * Would need my own web socket - maybe too hard
* UI - date limit?
* Command line
    * Parameter to limit by date


* Bundle size
    * My app seems way bigger than it shoudl be. 1.3mb of vendor code? Why>?
    * See vue-cli build --report
    * Is it moment? request? or does it just require some manual cleanup? 
    * Not worth fixing now.
    * Uncomment code in vue.config.js

* Lots of this is way too convoluted and confusing. Needs refactoring
    * Setting IPs
    * Navigation guards
 

## Github release process
A simplified version of [this](https://www.braintreepayments.com/blog/our-git-workflow/)  


Note - this is a little confusing because I used "github" both as a release and as a branch.  

Also, they have an extra branch in the middle (release) that I don't have.
```
git checkout github
git merge --squash master
git commit -m 'Info about release'
git tag -a 1.0.0 -m '1.0.0'
git push github HEAD:master
git checkout master
git merge github
git push origin master
```
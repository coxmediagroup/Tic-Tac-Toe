//---------Used for giving app access to native phone features
function onDeviceReady(){ 
	$.ui.launch();
	intel.xdk.device.hideSplashScreen();
}
document.addEventListener("intel.xdk.device.ready", onDeviceReady, false);
//---------Used for giving app access to native phone features

$.ui.autoLaunch = false; 
$.ui.animateHeaders = false;

$(document).ready(function(){
$.ui.launch();
});
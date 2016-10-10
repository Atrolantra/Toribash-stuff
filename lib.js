//Grab variables to see if this script (lib.js) has already been run.
//This avoids duplicate triggering of payload code.
var list = document.getElementsByTagName('script');
var i = list.length, flag = false;

//Function to load a script into the page.
function loadScript(url, callback)
{
    var head = document.getElementsByTagName('head')[0];
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = url;

    script.onreadystatechange = callback;
    script.onload = callback;

    head.appendChild(script);
}

//Code to run that uses the library being loaded in.
//Payload
var code = function() {
   cheet('U U D D L R L R b a',function(){alert('You found my secret');});
};

//Use variables and if this is the first time running this script
//load in the library and execute payload.
while (i--) {
    if (list[i].src == 'https://cdn.rawgit.com/namuol/cheet.js/master/cheet.min.js') {
        flag = true;
    }
}

if (!flag) {
    loadScript("https://cdn.rawgit.com/namuol/cheet.js/master/cheet.min.js", code); 
}

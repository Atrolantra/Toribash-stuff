var list = document.getElementsByTagName('script');
var i = list.length, flag = false;

function loadScript(url, callback)
{
    // Adding the script tag to the head as suggested before
    var head = document.getElementsByTagName('head')[0];
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = url;

    // Then bind the event to the callback function.
    // There are several events for cross browser compatibility.
    script.onreadystatechange = callback;
    script.onload = callback;

    // Fire the loading
    head.appendChild(script);
}

var code = function() {
   cheet('U U D D L R L R b a',function(){alert('You found my secret');});
};

while (i--) {
    if (list[i].src == 'https://cdn.rawgit.com/namuol/cheet.js/master/cheet.min.js') {
        flag = true;
    }
}

if (!flag) {
    loadScript("https://cdn.rawgit.com/namuol/cheet.js/master/cheet.min.js", code); 
}

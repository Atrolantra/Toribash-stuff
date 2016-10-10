var list = document.getElementsByTagName('script');
var i = list.length, flag = false;
while (i--) {
    if (list[i].src == '//cdn.rawgit.com/namuol/cheet.js/master/cheet.min.js') {
        flag = true;
    }
}
if (!flag) {
    var tag = document.createElement('script');
    tag.src = '//cdn.rawgit.com/namuol/cheet.js/master/cheet.min.js';
    document.getElementsByTagName('body')[0].appendChild(tag);
    cheet('U U D D L R L R b a',function(){alert('You found my secret');});
}

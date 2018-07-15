// $(document).ready(function(){
//     document.documentElement.style.fontSize = innerWidth / 10 + "px";
// })
$(document).ready(function () {
    //设置根元素的字体大小比例(基准单位)，可以使用em,rem获取相对值
    //em,rem就是这里的innerwidth,只要设置它就可以了
    document.documentElement.style.fontSize =innerWidth / 10+ "px";
});
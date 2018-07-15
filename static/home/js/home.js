$(document).ready(function () {
    setTimeout(function () {
      topSwiper();
      swiperMenu()
    },100)
});

function topSwiper() {
    var swiper1 = new Swiper("#topSwiper",{
        direction:'horizontal',
        loop:true,  //让slide看起来是循环的
        // 如果需要分页器
        pagination: '.swiper-pagination',
        paginationClickable:true,
        // effect:'cube', //播放效果
        autoplay:2000,  //自动播放
        autoplayDisableOnInteraction:false  //用户触动以后可以继续使用autoplay

        // 如果需要前进后退按钮
        // nextButton: '.swiper-button-next',
        // prevButton: '.swiper-button-prev',

        // 如果需要滚动条
        // scrollbar: '.swiper-scrollbar',
    })
}
function swiperMenu() {
    var swiper2 = new Swiper("#swiperMenu",{
        direction:"horizontal",
        slidesPerView:3,  //设置slide容器能够同时显示的slides数量
        paginationClickable:true,  //此参数设置为true时，点击分页器的指示点分页器会控制Swiper切换
        spaceBetween:2,  //slide之间的间距
        loop:false
    })
}
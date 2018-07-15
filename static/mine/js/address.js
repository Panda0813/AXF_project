//编辑信息和添加信息的函数
function uploadmsg(path) {
    name = $('#recipient-name').val();  //拿到表单中要提交的信息
    phone = $('#recipient-phone').val();
    address = $('#recipient-address').val();
    if(name != '' && phone != '' && address != '') {
        var xhr = new XMLHttpRequest();
        xhr.open('post', path, true);
        xhr.onload = function () {
            if (xhr.status == 200 && xhr.readyState == 4) {
                data = JSON.parse(xhr.responseText);
                console.log(data);
                if (data.status == 'ok') {
                    // 弹出模态框，但不能点击内容以外关闭
                    $('#saveModal').modal({backdrop: 'static', show: true});
                    setTimeout(function () {
                        $('#saveModal').modal('hide');
                        $('#myModal').modal('hide');
                        window.open('/address/0/0', target = '_self')
                    }, 2000)
                }
            }
        };
        var formdata = new FormData;
        formdata.append('name', name);
        formdata.append('phone', phone);
        formdata.append('address', address);
        xhr.send(formdata);
    }else {
        $('#recipient-name').attr('placeholder','信息不能为空');  //添加属性值
        $('#recipient-phone').attr('placeholder','信息不能为空');
        $('#recipient-address').attr('placeholder','信息不能为空');
    }
}

$(function () {
    $('#add > div > a').click(function () {
        $('#myModal').modal({backdrop:'static', show:true});
        $('#recipient-name').val('');
        $('#recipient-phone').val('');
        $('#recipient-address').val('');
        $('#exampleModalLabel').text('添加新地址');
        $('#save').click(function () {
            uploadmsg('/address/1/0');
        })
    });

    $('.change').click(function () {
        //编辑的时候讲原信息显示在表单中
        id = $(this).attr('title');
        name = document.getElementById('name'+id).title;
        phone = document.getElementById('phone'+id).title;
        address = document.getElementById('address'+id).title;
        $('#recipient-name').val(name);
        $('#recipient-phone').val(phone);
        $('#recipient-address').val(address);
        $('#exampleModalLabel').text('修改收货信息');
        $('#myModal').modal({backdrop:'static', show:true});
        $('#save').click(function () {
            uploadmsg("/address/2/"+id);
            console.log("/address/2/"+id)
        })
    });

    $('.delete').click(function () {
        id = $(this).attr('title');
        name = document.getElementById('name'+id).title;
        $('#close').css('display','inline-block');
        $('#close').next().css('display','inline-block');
        $('#payMsg').text('您确定要删除 '+name+' 的收货地址信息吗?');
        $('#saveModal').modal({backdrop:'static', show:true});
        $('#delete').click(function () {
            $('#close').css('display','none');
            $('#close').next().css('display','none');
            $('#payMsg').text('正在删除...请稍后');
            setTimeout(function () {
                $.getJSON('/address/3/'+id,function (data) {
                    if(data.status == 'ok'){
                        $('#payMsg').text(data.msg);
                        setTimeout(function () {
                            $('#saveModal').modal('hide');
                            window.open('/address/0/0', target = '_self')
                        },1000)
                    }
                })
            },2000)
        })
    });

    $('.isChose').click(function () {
        var child = $(this).children().first();
        id = $(child).attr('title');
        console.log(id);
        if(child.text().trim() == ''){  //设置默认
            $.getJSON('/address/4/'+id,function (data) {
                if(data.status == 'ok'){
                    console.log(data);
                    var last = document.getElementById('select'+data.lastid);
                    $(last).text('');  //先将上一个置空
                }
            });
            child.text('√');  //再将当前默认
        }else {
            child.text('');  //取消默认
        }
    });

    $('#back').click(function () {
        window.history.back();
    })
});
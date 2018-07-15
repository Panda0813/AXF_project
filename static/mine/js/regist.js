function showError(msg,fOrT) {
    var errorP = this.parentElement.nextElementSibling;
    errorP.innerText = fOrT?this.title + msg:msg;
    $(errorP).fadeIn();
    $(this.parentElement).addClass('has-error');

    $(this).focus(function () {
        $(errorP).fadeOut();
        $(this.parentElement).removeClass('has-error');
    });
}

$(function () {
    $('input').blur(function () {
        // if(this.value.trim().length == 0){
        //     showError.call(this,'信息不能为空');
        //     return
        // }
        if(this.name == 'username' &&
            (this.value.trim().length < 6 || this.value.trim().length>12) ){
            showError.call(this,this.placeholder,true);
            console.log(this.placeholder);
            return
        }

        if(this.name == 'passwd' &&
            (this.value.trim().length < 6 || this.value.trim().length>12)){
            showError.call(this,this.placeholder,true);
            // return
        }

        if(this.name == 'pass' ){
            var passwd1 = $('input[name=passwd]').val();  //获取到值
            if(this.value.trim() != passwd1.trim()){
                showError.call(this,'两次密码不同',false);
            }
            return
        }

        if(this.name == 'phone'){
            phone = this.value.trim();
            if(phone.length != 11 && phone.length != ''){
                showError.call(this, '请输入11位的手机号', false);
                return;
            }
            if(!/1[3-9]\d{9}/.test(phone)){
                showError.call(this, '输入手机号无效', false);
                return;
            }
        }
        var isT = True;
    })
});

function submitMsg() {
    var inputs = $('input');
    //验证提交信息是否为空
    for(var i=1;i<inputs.length;i++){
        var input = inputs[i];
        if($(input).val().trim() == ''){
            showError.call(input,'信息不能为空',false);
            return
        }
    }

    document.forms[0].submit();


}
function flushcode(icode) {
    icode.src = '/vcode?tm='+Math.random();
}
function showError() {
    var errorP = $(this).parent().next()[0];
    $(errorP).fadeIn();
    $(errorP).addClass('has-error');

    $(this).focus(function () {
        $(errorP).fadeOut();
        $(errorP).removeClass('has-error');
    });
}
function submitMsg() {
    var inputs = $('input');
    for(var i=1;i<inputs.length;i++){
        var input = inputs[i];
        if($(input).val().trim() == ''){
            showError.call(input);
            return
        }
    }
    document.forms[0].submit();
}
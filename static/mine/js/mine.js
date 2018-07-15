function uploadImg(file) {
    var xhr = new XMLHttpRequest();
    xhr.open('post','/upload',true);
    xhr.onload = function () {
        if(xhr.status == 200 && xhr.readyState == 4){
            data = JSON.parse(xhr.responseText);
            if(data.state == 'ok'){
                console.log(data.path);
                $('#img').attr('src','/static/'+data.path)
            }
        }
    };
    var formdata = new FormData;
    formdata.append('img',file);
    xhr.send(formdata);
}

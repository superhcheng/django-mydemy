function sendCodeChangeEmail($btn){
    var verify = verifyDialogSubmit(
        [
          {id: '#jsChangeEmail', tips: Dml.Msg.epMail, errorTips: Dml.Msg.erMail, regName: 'email', require: true}
        ]
    );
    if(!verify){
       return;
    }
    $.ajax({
        cache: false,
        type: "POST",
        dataType:'json',
        url:"/user/update_email_vc/",
        data:$('#jsChangeEmailForm').serialize(),
        async: true,
        beforeSend:function(XMLHttpRequest){
            $btn.val("Send...");
            $btn.attr('disabled',true);
        },
        success: function(data){
            if(data.email){
                Dml.fun.showValidateError($('#jsChangeEmail'), data.email);
            }else if(data.status == 'success'){
                Dml.fun.showErrorTips($('#jsChangeEmailTips'), "Verification code sent");
            }else if(data.status == 'fail'){
                 Dml.fun.showValidateError($('#jsChangeEmail'), data.err_msg);
            }
        },
        complete: function(XMLHttpRequest){
            $btn.val("Get Verification Code");
            $btn.removeAttr("disabled");
        }
    });

}

function changeEmailSubmit($btn){
var verify = verifyDialogSubmit(
        [
          {id: '#jsChangeEmail', tips: Dml.Msg.epMail, errorTips: Dml.Msg.erMail, regName: 'email', require: true},
        ]
    );
    if(!verify){
       return;
    }
    $.ajax({
        cache: false,
        type: 'POST',
        dataType:'json',
        url:"/user/update_email/ ",
        data:$('#jsChangeEmailForm').serialize(),
        async: true,
        beforeSend:function(XMLHttpRequest){
            $btn.val("Sending...");
            $btn.attr('disabled',true);
            $("#jsChangeEmailTips").html("Checking").show(500);
        },
        success: function(data) {
            if(data.email){
                Dml.fun.showValidateError($('#jsChangeEmail'), data.email);
            }else if(data.status == "success"){
                Dml.fun.showErrorTips($('#jsChangePhoneTips'), "E-mail updated.");
                setTimeout(function(){location.reload();},1000);
            }else{
                 Dml.fun.showValidateError($('#jsChangeEmail'), data.err_msg);
            }
        },
        complete: function(XMLHttpRequest){
            $btn.val("Done");
            $btn.removeAttr("disabled");
        }
    });
}

$(function(){
    $('#jsUserResetPwd').on('click', function(){
        Dml.fun.showDialog('#jsResetDialog', '#jsResetPwdTips');
    });

    $('#jsResetPwdBtn').click(function(){
        $.ajax({
            cache: false,
            type: "POST",
            dataType:'json',
            url:"/user/update_pwd/",
            data:$('#jsResetPwdForm').serialize(),
            async: true,
            success: function(data) {

                if(data.password1){
                    Dml.fun.showValidateError($("#pwd"), data.password1);
                }else if(data.password2){
                    Dml.fun.showValidateError($("#repwd"), data.password2);
                }else if(data.status == "success"){
                    Dml.fun.showTipsDialog({
                        title:'Submission Success',
                        h2:'Passowrd updated, please login',
                    });
                    Dml.fun.winReload();
                }else if(data.err_msg){
                    Dml.fun.showValidateError($("#pwd"), data.err_msg);
                    Dml.fun.showValidateError($("#repwd"), data.err_msg);
                }
            }
        });
    });

    //个人资料头像
    $('.js-img-up').uploadPreview({ Img: ".js-img-show", Width: 94, Height: 94 ,Callback:function(){
        $('#jsAvatarForm').submit();
    }});


    $('.changeemai_btn').click(function(){
        Dml.fun.showDialog('#jsChangeEmailDialog', '#jsChangePhoneTips' ,'jsChangeEmailTips');
    });
    $('#jsChangeEmailCodeBtn').on('click', function(){
        sendCodeChangeEmail($(this));
    });
    $('#jsChangeEmailBtn').on('click', function(){
        changeEmailSubmit($(this));
    });


    //input获得焦点样式
    $('.perinform input[type=text]').focus(function(){
        $(this).parent('li').addClass('focus');
    });
    $('.perinform input[type=text]').blur(function(){
        $(this).parent('li').removeClass('focus');
    });

    laydate({
        elem: '#birth_day',
        format: 'YYYY-MM-DD',
        max: laydate.now()
    });

    verify(
        [
            {id: '#nick_name', tips: Dml.Msg.epNickName, require: true}
        ]
    );
    //保存个人资料
    $('#jsEditUserBtn').on('click', function(){
        var _self = $(this),
            $jsEditUserForm = $('#jsEditUserForm')
            verify = verifySubmit(
            [
                {id: '#nick_name', tips: Dml.Msg.epNickName, require: true}
            ]
        );
        if(!verify){
           return;
        }
        $.ajax({
            cache: false,
            type: 'POST',
            dataType:'json',
            url:"/user/update_user/",
            data:$jsEditUserForm.serialize(),
            async: true,
            beforeSend:function(XMLHttpRequest){
                _self.val("Saving...");
                _self.attr('disabled',true);
            },
            success: function(data) {
                if(data.nickname){
                    _showValidateError($('#nick_name'), data.nick_name);
                }else if(data.birthday){
                   _showValidateError($('#birth_day'), data.birday);
                }else if(data.address){
                   _showValidateError($('#address'), data.address);
                }else if(data.status == "failure"){
                     Dml.fun.showTipsDialog({
                        title: 'Save failed',
                        h2: data.msg
                    });
                }else if(data.status == "success"){
                    Dml.fun.showTipsDialog({
                        title: 'Saved',
                        h2: 'User profile updated'
                    });
                    setTimeout(function(){
                            window.location.href = window.location.href;
                        },1500);
                }
            },
            complete: function(XMLHttpRequest){
                _self.val("Save");
                _self.removeAttr("disabled");
            }
        });
    });
});
function ajaxForm() {
    var csrftoken = $("meta[name=csrf-token]").attr("content");
    var username = $("input.login_name").val();
    var pwd = $("input.login_pwd").val()
    $.ajax({
        url: "/login",
        type: "POST",
        data: { "name": username, "pwd": pwd, },
        headers: { "X-CSRFToken": csrftoken },
        dataType: "html",
        success: function(data) {
            $('li.login_user').html(data);
            $.pjax({
                url: window.location.pathname,
                container: '#main-content'
            });
        },
        error: function(e) {
            alert("输入有误");
        }
    })
}

function ajaxForm1() {
    var csrftoken = $("meta[name=csrf-token]").attr("content");
    $.ajax({
        url: "/logout",
        type: "GET",
        data: {},
        headers: { "X-CSRFToken": csrftoken },
        dataType: "html",
        success: function(data) {
            $('li.login_user').html(data);
            $.pjax({ url: window.location.pathname, container: '#main-content' });
        },
        error: function(e) {
            alert("输入有误");
        }
    })
}

function login() {
    $('body,html').animate({ scrollTop: 0 }, 500);
    $.getScript("https://github.com/FezVrasta/dropdown.js/blob/master/jquery.dropdown.js", function() {
        $("a.login").dropdown('toggle');
    });


};
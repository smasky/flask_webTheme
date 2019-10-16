$(function() {

    // Set up PJAX.
    $('a[data-pjax]').pjax();
})

function reloadLatex() {
    window.renderMathInElement(document.getElementById("blog-post"), {
        delimiters: [{
            left: "$$",
            right: "$$",
            display: true
        }, {
            left: "\\[",
            right: "\\]",
            display: true
        }, {
            left: "$",
            right: "$",
            display: false
        }, {
            left: "\\(",
            right: "\\)",
            display: false
        }]
    });
}

function playPostMusic(id) {
    const subap = new APlayer({
        container: document.getElementById('sub-aplayer'),
        autoplay: false,
        audio: []
    });
    //var url = 'https://api.itooi.cn/music/netease/song?key=579621905&id=' + id
    //$.post(url, function(data1) {
    //   console.log(data1.data);
    //  subap.list.add([{
    //       name: '过客',
    //      artist: '周思涵',
    //      url: 'https://127.0.0.1:5000/music/music/guoke',
    //      cover: './static/img/guoke.jpg',
    //  }]);
    // }, 'json');
    var name = $("#sub-aplayer").attr("musicName")
    var artist = $("#sub-aplayer").attr("musicName")
    var url = 'http://127.0.0.1:5000/music/' + id
    var url1 = '../static/img/' + id + '.jpg'
    subap.list.add([{
        name: name,
        artist: artist,
        url: url,
        cover: url1,
    }]);
    subap.play();
}

function find_music(id, name, work, cover) {
    var baseUrl = 'http://120.79.36.48/';
    //id = '28815250';
    var url1 = baseUrl + 'music/url?id=' + id;
    console.log(url1);
    //var url3 = baseUrl + 'lyric?id=' + id;
    $.getJSON(url1, function(data1) {
        var url_m = data1.url;
        console.log('歌拉取成功！');
        ap.list.add([{
            name: String(name),
            artist: String(work),
            url: url_m,
            cover: String(cover),
        }]);
    });
};


function find_playlist(id) {
    var baseUrl = 'http://120.79.36.48/';
    url1 = baseUrl + 'playlist/detail?id=' + id;
    $.ajax({
        url: baseUrl + 'playlist/detail?id=' + id,
        beforeSend: () => {
            console.log('SKPlayer正在努力的拉取歌单 ...');
        },
        success: (data) => {
            console.log('歌单拉取成功！');
            var music = data;
            for (var i = 0; i < music.length; i++) {
                find_music(music[i].song_id, music[i].name, music[i].author, music[i].cover)
            }
        },
        fail: (status) => {
            console.error('歌单拉取失败！ 错误码：' + status);
        }
    });

}

function isMobile() {
    var userAgentInfo = navigator.userAgent;

    var mobileAgents = ["Android", "iPhone", "SymbianOS", "Windows Phone", "iPod"];

    var mobile_flag = false;

    //根据userAgent判断是否是手机
    for (var v = 0; v < mobileAgents.length; v++) {
        if (userAgentInfo.indexOf(mobileAgents[v]) > 0) {
            mobile_flag = true;
            break;
        }
    }

    var screen_width = window.screen.width;
    var screen_height = window.screen.height;

    //根据屏幕分辨率判断是否是手机
    if (screen_width < 500 && screen_height < 800) {
        mobile_flag = true;
    }

    return mobile_flag;
}
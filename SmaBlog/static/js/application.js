$(function() {

    // Set up PJAX.
    $('a[data-pjax]').pjax();
})

function playPostMusic(id) {
    const subap = new APlayer({
        container: document.getElementById('sub-aplayer'),
        autoplay: false,
        audio: []
    });
    var url = 'https://api.itooi.cn/music/netease/song?key=579621905&id=' + id
    $.post(url, function(data1) {
        console.log(data1.data);
        subap.list.add([{
            name: data1.data.name,
            artist: data1.data.singer,
            url: data1.data.url,
            cover: data1.data.pic,
        }]);
    }, 'json');
    subap.play();
}

function find_music(id, name, work, cover) {
    var baseUrl = 'http://120.79.36.48/';
    //id = '28815250';
    var url1 = baseUrl + 'music/url?id=' + id;
    var url3 = baseUrl + 'lyric?id=' + id;
    $.getJSON(url1, function(data1) {
        var url_m = data1.url;
        $.getJSON(url3, function(data) {
            var lrc1 = data.lrc.lyric;
            ap.list.add([{
                name: String(name),
                artist: String(work),
                url: url_m,
                cover: String(cover),
                lrc: lrc1,
            }]);

        });
    });
}

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

function GenerateContentList() {
    var mainContent = $('#mulu');
    var h1_list = $('#blog-post h1');　　 //如果你的章节标题不是h1,只需要将这里的h1换掉即可
    var h2_list = $('#blog-post h2');
    if (mainContent.length < 1)
        return;
    if (h1_list.length > 0) {
        var content = '';
        content += '';
        content += ' <h4 class="title_menue right-h4">文章目录</h4>';
        content += '<ul class="toc list-group">';
        for (var i = 0; i < h1_list.length; i++) {
            var go_to_top = '<a name="_label' + i + '"></a>';
            $(h1_list[i]).before(go_to_top);

            var h2_list = $(h1_list[i]).nextAll("h2");
            var li2_content = '';
            for (var j = 0; j < h2_list.length; j++) {
                var tmp = $(h2_list[j]).prevAll('h1').first();
                if (!tmp.is(h1_list[i]))
                    break;
                var li2_anchor = '<a pjax="no" name="_label' + i + '_' + j + '"></a>';
                $(h2_list[j]).before(li2_anchor);
                li2_content += '<li class="list-group-item toc-level-' + i + '_' + j + '"><a pjax="no" class="toc-link" href="#_label' + i + '_' + j + '"><span class="toc-text">' + $(h2_list[j]).text() + '</span></a></li>';
            }

            var li1_content = '';
            if (li2_content.length > 0)
                li1_content = '<li class="list-group-item toc-level-' + i + '"><a pjax="no" class="toc-link" href="#_label' + i + '"><span class="toc-text">' + $(h1_list[i]).text() + '</span></a></li><li class="toc-child">' + li2_content + '</li></ul>';
            else
                li1_content = '<li class="list-group-item toc-level-' + i + '"><a  pjax="no" class="toc-link" href="#_label' + i + '"><span class="toc-text">' + $(h1_list[i]).text() + '</span></a></li>';
            content += li1_content;
        }
        if ($('#mulu').length != 0) {
            $($('#mulu')[0]).html(content);
        }
    } else {
        if (h1_list.length == 0 && h2_list.length > 0) {
            var content = '';
            content += '';
            content += '<h4 class="title_menue right-h4">文章目录</h4>';
            content += '<ul class="toc list-group">';
            for (var i = 0; i < h2_list.length; i++) {
                var go_to_top = '<a  pjax="no" name="_label' + i + '"></a>';
                $(h2_list[i]).before(go_to_top);
                var h3_list = $(h2_list[i]).nextAll("h3");
                var li3_content = '';
                for (var j = 0; j < h3_list.length; j++) {
                    var tmp = $(h3_list[j]).prevAll('h2').first();
                    if (!tmp.is(h2_list[i]))
                        break;
                    var li3_anchor = '<a  pjax="no" name="_label' + i + '_' + j + '"></a>';
                    $(h3_list[j]).before(li3_anchor);
                    li3_content += '<li class="list-group-item toc-level-' + i + '_' + j + '"><a pjax="no" class="toc-link" href="#_label' + i + '_' + j + '"><span class="toc-text">' + $(h3_list[j]).text() + '</span></a></li>';
                }
                var li2_content = '';
                if (li3_content.length > 0)
                    li2_content = '<li class="list-group-item toc-level-' + i + '"><a pjax="no" class="toc-link" href="#_label' + i + '"><span class="toc-text">' + $(h2_list[i]).text() + '</span></a></li><li class="toc-child">' + li3_content + '</li></ul>';
                else
                    li2_content = '<li class="list-group-item toc-level-' + i + '"><a pjax="no" class="toc-link" href="#_label' + i + '"><span class="toc-text">' + $(h2_list[i]).text() + '</span></a></li>';
                content += li2_content;
            }
            if ($('#mulu').length != 0) {
                $($('#mulu')[0]).html(content);
            }
        }
    }
}
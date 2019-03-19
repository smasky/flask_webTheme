import markdown

mark=''
with open('about.md','r',encoding='utf-8') as f:
    is_info=False

    is_zw=False
    Info={}
    content=[]
    n=0
    for line in f:
        n+=1
        if(is_zw):
            content.append(line)
        if('@-' in line):
            is_info=not is_info
            if(not is_info):
                is_zw=True

        if(is_info and n>1):
            info=line.strip('\n').split(':')
            Info[info[0]]=info[1]

    print(Info)
    html = '''
    <html lang="zh-cn">
    <head>
    <meta content="text/html; charset=utf-8" http-equiv="content-type" />
    <link href="/static/default.css" rel="stylesheet">
    <link href="/static/github.css" rel="stylesheet">
    </head>
    <body>
    %s
        <script type="text/x-mathjax-config">
        MathJax.Hub.Config({
            showProcessingMessages: false,
            messageStyle: "none",
            extensions: ["tex2jax.js"],
            jax: ["input/TeX", "output/HTML-CSS"],
            tex2jax: {
                inlineMath:  [ ["$", "$"] ],
                displayMath: [ ["$$","$$"] ],
                skipTags: ['script', 'noscript', 'style', 'textarea', 'pre','code','a'],
                ignoreClass:"comment-content"
            },
            "HTML-CSS": {
                availableFonts: ["STIX","TeX"],
                showMathMenu: false
            }
        });
        MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
        </script>
        <script src="//cdn.bootcss.com/mathjax/2.7.0/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
    </body>
    </html>
    '''
    ret = markdown.markdown(''.join(content))
    output= html % ret

with open('OUTPUT.html','w',encoding='utf-8') as f:
    f.write(output)

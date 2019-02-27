import markdown

mark=''
with open('123.md','r',encoding='utf-8') as f:
    mark=f.read()
    html = '''
    <html lang="zh-cn">
    <head>
    <meta content="text/html; charset=utf-8" http-equiv="content-type" />
    <link href="/static/default.css" rel="stylesheet">
    <link href="/static/github.css" rel="stylesheet">
    </head>
    <body>
    %s
    </body>
    </html>
    '''
    ret = markdown.markdown(mark)
    output= html % ret

with open('OUTPUT.html','w',encoding='utf-8') as f:
    f.write(output)


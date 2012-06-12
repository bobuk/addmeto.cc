$ ->
    converter = new Markdown.Converter();
    text = $('#article-body').html()
    $('#article-body').html(converter.makeHtml(text))
    # document.write(converter.makeHtml("**I am bold!**"));
    $('article a').attr('target', '_blank')

editMD = ->
    $.get './' + page + '.md', (data) ->
        $('#article-md').html(data)
        alert('Loaded')
    $('#article-body').hide()
    $('#article-md').show()
    $('#edit-btn').click ->
        $('#edit-btn').unbind();
        alert('Saved')
        $('#article-body').toggle()
        $('#article-md').toggle()
        $('#edit-btn').click(editMD)


$ ->
    md = $('#article-md').html()
    # converter = new Markdown.Converter();
    # $('#article-body').html(converter.makeHtml(text))
    $('article a').attr('target', '_blank')
    $('.nav-tabs').button()
    $('#edit-btn').click(editMD)

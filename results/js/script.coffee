fillEdit = (response) ->
  meta = response.meta
  data = response.data
  console.log(meta)
  console.log(data)

editMD = ->

    $.ajax({
        url: 'https://api.github.com/repos/bobuk/addmeto.cc/contents/source/posts/'+page+'.md?callback=?',
        dataType: 'jsonp',
        success: (resp) ->
            $('#article-md').html(Base64.decode(resp.data.content))
    });
    $('#edit-btn').html('Сохранить')
    #$.get '/post/' + page + '/' + page + '.md', (data) ->
    #    $('#article-md').html(data)
    $('#article-body').hide()
    $('#article-md').show()
    $('#edit-btn').click ->
        $('#edit-btn').unbind();
        $('#edit-btn').html('Редактировать')
        $('#article-body').toggle()
        $('#article-md').toggle()
        $('#edit-btn').click(editMD)


$ ->
    # md = $('#article-md').html()
    # converter = new Markdown.Converter();
    # $('#article-body').html(converter.makeHtml(text))
    $('article a').attr('target', '_blank')
    $('.nav-tabs').button()
    $('#edit-btn').click(editMD)

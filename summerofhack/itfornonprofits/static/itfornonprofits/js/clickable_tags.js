function onclick_on_tag(url, token, what, e) {
    var data = [];
    data[what] = $(e.target).text();
    do_post_request(url, token, data);
}

function do_post_request(url, token, data) {
    var form = $('<form>').attr('method', 'post').append(token).attr('action', url);
    form.action= url;
    for (var key in data) {
        var input = $('<input>').attr('name', key).attr('value', data[key]).attr('type', 'hidden');
        form.append(input);
    }
    $('body').append(form);
    $(form).submit();
}

function register_clickable_tags(endpoint, token) {
    $('.badge-info').on('click', $.proxy(onclick_on_tag, this, endpoint, token, 'skills'));
    $('.badge-warning').on('click', $.proxy(onclick_on_tag, this, endpoint, token, 'sectors'));
}



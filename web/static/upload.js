
$(function () {
    var dropbox = $('#dropbox');
    var placeholder = dropbox.find('.placeholder');

    dropbox.filedrop({
        paramname: 'image',
        maxfiles: 1,
        maxfilesize: 2,
        url: 'upload_image',
        upload
    })
});



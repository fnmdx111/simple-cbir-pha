// TODO make two versions of upload.js
// TODO one-file-only and multiple-file versions

$(function () {
    var dropbox = $('#dropbox');
    var placeholder = dropbox.find('.placeholder');

    var template = '<div class="preview">' +
        '<span class="imageHolder">' +
        '<img />' +
        '<span class="uploaded"></span>' +
        '</span>' +
        '<div class="progressHolder">' +
        '<div class="progress"></div>' +
        '</div>' +
        '</div>';

    var createImagePreview = function (file) {
        var preview = $(template);
        var image = preview.find('img');
        var reader = new FileReader();

        image.width = 100;
        image.height = 100;

        reader.onload = function (e) {
            image.attr('src', e.target.result);
        };
        reader.readAsDataURL(file);

        placeholder.hide(); // TODO remove previous preview
        dropbox.remove('.preview');
        preview.appendTo(dropbox);

        $.data(file, preview);
    };

    var showMessage = function (msg) {
        placeholder.html(msg);
    };

    dropbox.filedrop({
        paramname: 'image',
        maxfiles: 1,
        maxfilesize: 2,
        url: 'upload_image',
        uploadFinished: function (i, file) {
            $.data(file).addClass('done');
        },
        error: function (err) {
            switch (err) {
                case 'BrowserNotSupported':
                    showMessage('Please use html5-friendly browser.');
                    break;
                case 'TooManyFiles':
                    showMessage('Too many files, please only select one image.');
                    break;
                case 'FileTooLarge':
                    showMessage('File size exceeds 2m.');
                    break;
                default:
                    break;
            }
        },
        beforeEach: function (file) {
            if (!file.type.match(/^image\//)) {
                alert('Only images are allowed.');
                return false;
            }
            return true;
        },
        uploadStarted: function (i, file) {
            createImagePreview(file);
        },
        progressUpdated: function (i, file, progress) {
            $.data(file).find('.progress').width(progress);
        }
    });
});



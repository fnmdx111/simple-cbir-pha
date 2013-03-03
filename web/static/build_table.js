
var build_table = function (loader, rri_form, result_table) {
    return function (response) {
        if (loader) {
            loader.hide();
        }
        if (rri_form) {
            rri_form.show();
        }

        var table = '' +
            '<thead>' +
                '<tr>' +
                    '<th>#</th>' +
                    '<th>Hash值</th>' +
                    '<th>链接（文件名）</th>' +
                '</tr>' +
            '</thead><tbody>';
        $.each(response['result'], function (idx, content) {
            var hash = content[0],
                filename = content[1];
            table += '' +
                '<tr>' +
                    '<td>' + idx + '</td>' +
                    '<td>' +
                        '<code>' + hash + '</code>' +
                    '</td>' +
                    '<td>' +
                        '<a href="static/images/' + filename + '" target="_self">' + filename + '</a>' +
                    '</td>' +
                '</tr>';
        });
        table += '</tbody></table>';

        result_table.html(table);
        result_table.show();
    }
}
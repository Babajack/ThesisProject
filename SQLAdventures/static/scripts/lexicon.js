function loadLexiconExamples(data) {
    $(document).ready(function () {

        $.getScript('/static/scripts/load-custom-sql-keywords.js', function () {

            if (data.hasOwnProperty('Example1')) {
                let example1 = CodeMirror.fromTextArea(document.getElementById("example1"), {
                    lineNumbers: true,
                    mode: "text/x-sqlite",
                    matchBrackets: true,
                    readOnly: 'nocursor',
                    value: data['Example1']
                });
                $('#example1').css('visibility', 'visible')
            }

            if (data.hasOwnProperty('Example2')) {
                let example2 = CodeMirror.fromTextArea(document.getElementById("example2"), {
                    lineNumbers: true,
                    mode: "text/x-sqlite",
                    matchBrackets: true,
                    readOnly: 'nocursor',
                    value: data['Example2']
                });
                $('#example2').css('visibility', 'visible')
            }
        })
    })
}
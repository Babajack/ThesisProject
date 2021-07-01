$(document).ready(function () {

    // load codemirror sql editor
    let editor = CodeMirror.fromTextArea(document.getElementById("code"), {
        lineNumbers: true,
        mode: "text/x-sql",
        matchBrackets: true
    });


    // ------- handle user query -------

    $("#SQLSubmitButton").click(function () {

        if (editor.getValue()) {

            let keywords_raw = document.getElementsByClassName('cm-keyword')
            let keywords = []
            for (let i = 0; i < keywords_raw.length; i++) {
                keywords.push(keywords_raw[i].textContent)
            }

            // make request with user query
            $.ajax({
                type: 'POST',
                url: '/quests/query',
                data: JSON.stringify({query: editor.getValue(), keywords: keywords}),
                contentType: "application/json",
                dataType: 'json',
                success: function (resultData) {
                    $("#feedback").css('visibility', 'invisible')

                    // check if query returns error, if not show the result table
                    if ('Error' in resultData) {
                        // display error
                        $("#feedback").css('visibility', 'visible')
                            .css('background-color', 'red')
                            .html(resultData['Error'])
                    } else {

                        /* --- create the html table from sql data --- */
                        let tableHead = "";
                        let tableBody = ""

                        for (let key in resultData[0]) {
                            tableHead += "<th> " + key + " </th>"
                        }

                        // last entry in resultData shows if task is solved
                        for (let i = 0; i < resultData.length - 1; i++) {
                            tableBody.concat("<tr> ")
                            let row = resultData[i]
                            for (let key in row) {
                                if (row.hasOwnProperty(key))
                                    tableBody += "<td>" + row[key] + "</td>"
                            }
                            tableBody += " </tr>"
                        }
                        tableHead = "<thead> <tr> " + tableHead + " </tr> </thead>"
                        tableBody = "<tbody> " + tableBody + " </tbody>"

                        let table = "<table class='table table-striped'>" + tableHead + tableBody + "</table>"

                        // update the screen
                        $("#response").html(table)

                        // display if result is correct or not
                        if (resultData[resultData.length - 1].hasOwnProperty('result')) {
                            let result = resultData[resultData.length - 1]['result']
                            if (result) {

                                // task is solved -> update display
                                $("#feedback").css('visibility', 'visible')
                                    .css('background-color', 'green')
                                    .html('<span class="fa fa-star checked"></span> Aufgabe gelöst! <span class="fa fa-star checked"></span>');

                                $('#navbar-buttons').hide();

                                $('#SQLSubmitButton').off('click');

                                $('#SQLSubmitButton').css('background-color', 'green').text('Zum Questbuch').click(function () {
                                    $.ajax({
                                        url: '/quests/questbook',
                                        type: 'GET',
                                        success: function (data) {
                                            window.location.href = this.url
                                        }
                                    });
                                });

                                // unlocked new keyword -> show modal
                                if (resultData[resultData.length - 1].hasOwnProperty('unlocked')) {
                                    let unlocked = resultData[resultData.length - 1]['unlocked']
                                    $('#unlocked-keyword-text').html('Glückwunsch! Du hast <b style="color:#708">' + unlocked + '</b> freigeschaltet!' +
                                    '\n Schau im Wiki vorbei für mehr Infos.')
                                    $('#unlocked-keyword').modal();

                                }

                            } else {
                                // task is not solved TODO update counter or smth/ show hints
                                $("#feedback").css('visibility', 'visible')
                                    .css('background-color', 'orange')
                                    .html('Das Ergebnis ist nicht korrekt')
                            }
                        }

                    }


                },
                error: function (error) {
                    console.log(error)
                },
            })
        }
    })
})
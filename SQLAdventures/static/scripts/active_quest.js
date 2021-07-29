function loadQuestProcedure(data, username) {
    let skipped = false
    let taskFinished = false
    let introCounter = 0
    let outroCounter = 0
    let currentTalkerPos
    let hasUnlockedKeywords = false
    let failCounter = 0

    $(document).ready(function () {

        // load custom CodeMirror mode
        $.getScript('/static/scripts/load-custom-sql-keywords.js', function () {

            // codemirror sql editor
            let editor = CodeMirror.fromTextArea(document.getElementById("code"), {
                lineNumbers: true,
                mode: "text/x-sqlite",
                matchBrackets: true,
                readOnly: 'nocursor'
            });

            // load first sequence
            nextSequence('Intro')

            // on user click anywhere -> skip intro animation
            // if clicked on button and text animation finished -> show next text sequence
            $(document).click(function (event) {

                if (event.target.id === 'SQLSubmitButton' || event.target.id === 'image-' + currentTalkerPos) {
                    if (skipped) {
                        // load next sequence
                        if (taskFinished) {
                            nextSequence('Outro')
                        } else {
                            nextSequence('Intro')
                        }
                        return
                    }
                }
                skipped = true
            })

            // load the next text sequence (intro or outro)
            function nextSequence(type) {
                let counter
                if (type === 'Intro') {
                    counter = introCounter
                } else if (type === 'Outro') {
                    counter = outroCounter
                }
                if (counter < data[type].length) {
                    let sequenceElement = data[type][counter]

                    // set current talker position -> enable continue by clicking on image
                    currentTalkerPos = sequenceElement['Position']

                    // set picture
                    $('#image-' + sequenceElement['Position']).attr('src', '/static/images/' + sequenceElement['Picture']).show()

                    // enable animation
                    skipped = false

                    // animate text
                    // enable user input if intro is finished
                    if (counter === data[type].length - 1) {
                        animateText(sequenceElement['Text'], sequenceElement['HTML'], 'bubble-' + sequenceElement['Position'], true)
                        if (type === 'Intro') {
                            handleUserQuery()
                        }
                    } else {
                        animateText(sequenceElement['Text'], sequenceElement['HTML'], 'bubble-' + sequenceElement['Position'], false)
                    }

                    // increase counter
                    counter++
                    if (type === 'Intro') {
                        introCounter++
                    } else if (type === 'Outro') {
                        outroCounter++
                    }

                }

            }

            // ----------- handle user query ----------------

            function handleUserQuery() {

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

                                            taskFinished = true

                                            $("#feedback").css('visibility', 'visible')
                                                .css('background-color', 'green')
                                                .html('<span class="fa fa-star checked"></span> Aufgabe gelöst! <span class="fa fa-star checked"></span>');

                                            $('#navbar-buttons').hide();

                                            $('#SQLSubmitButton').off('click');

                                            $('#SQLSubmitButton').text('Weiter');

                                            nextSequence('Outro')

                                            // unlocked new keyword -> show modal
                                            if (resultData[resultData.length - 1].hasOwnProperty('unlocked')) {
                                                let unlockedKeywords = resultData[resultData.length - 1]['unlocked']
                                                let b_open = "<b style=\"color:#708\">"
                                                let b_close = "</b>"
                                                let keywords_string = b_open + unlockedKeywords[0] + b_close
                                                for (let i = 1; i < unlockedKeywords.length; i++) {
                                                    keywords_string = keywords_string + " und " + b_open + unlockedKeywords[i] + b_close
                                                }
                                                $('#unlocked-keywords-text').html('Du hast ' + keywords_string + ' freigeschaltet!' +
                                                    '\n Schau im Lexikon vorbei für mehr Infos.')
                                                // set flag to show modal at the end
                                                hasUnlockedKeywords = true
                                            }

                                        } else {
                                            // task is not solved TODO update counter or smth/ show hints
                                            $("#feedback").css('visibility', 'visible')
                                                .css('background-color', 'orange')
                                                .html('Das Ergebnis ist nicht korrekt')
                                        }
                                    }
                                }
                                // if task is not solved after 3 tries -> give hint
                                if (!taskFinished) {
                                    failCounter++
                                    if (failCounter > 2) {
                                        $("#Hint").css('display', 'block')
                                    }
                                }
                            },
                            error: function (error) {
                                console.log(error)
                            },
                        })
                    }
                })
            }


            // animate text writing effect with text on given element with elementId
            // if text is last one of intro and animation finished -> enable user input and show task
            // if text is last one of outro and animation finished -> enable go back button
            function animateText(text, html, elementId, isLastOne) {
                $('#' + elementId).text('').show()
                text = text.replace("username", username)
                if (html !== undefined)
                    html = html.replace("username", username)
                type(0, 35, text, elementId)

                function type(i, speed, text, elementId) {
                    if (skipped) {
                        document.getElementById(elementId).innerHTML = html === undefined ? text : html
                        $('#SQLSubmitButton').removeClass('disabled')
                        if (isLastOne && !taskFinished) {
                            // intro is finished -> enable user input
                            $('#Task').css('visibility', 'visible')
                            editor.setOption('placeholder', 'SQL Code hier eintippen...')
                            editor.setOption('readOnly', false)
                            $('#SQLSubmitButton').text('SQL abschicken!')
                            $('#TableInfo').show()
                        } else if (isLastOne && taskFinished) {
                            // outro is finished -> enable go back button
                            $('#SQLSubmitButton').css('background-color', 'green').text('Zum Questbuch').click(function () {
                                // if user has unlocked new keywords -> show modal first
                                // else go back to questbook
                                if (hasUnlockedKeywords) {
                                    $('#unlocked-keywords_modal').modal();
                                    $('#unlocked-keywords_modal').on('hidden.bs.modal', function () {
                                        $.ajax({
                                            url: '/quests/questbook',
                                            type: 'GET',
                                            success: function (data) {
                                                window.location.href = this.url
                                            }
                                        });
                                    })
                                } else {
                                    $.ajax({
                                        url: '/quests/questbook',
                                        type: 'GET',
                                        success: function (data) {
                                            window.location.href = this.url
                                        }
                                    });
                                }
                            });
                        }
                        return
                    }
                    $('#SQLSubmitButton').addClass('disabled')
                    document.getElementById(elementId).innerHTML += text.charAt(i);
                    setTimeout(function () {
                        ((i < text.length) ? type(i + 1, speed, text, elementId) : lastType(i + 1, speed, text, elementId));
                    }, speed);
                }

                function lastType(i, speed, text, elementId) {
                    skipped = true
                    type(i, speed, text, elementId)
                }
            }
        });
    });
}



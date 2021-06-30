$(document).ready(function () {
    let editor = CodeMirror.fromTextArea(document.getElementById("code"), {
        lineNumbers: true,
        mode: "text/x-sql",
        matchBrackets: true
    });


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

                    // check if query returns error, if not show the result table
                    if ('Error' in resultData) {
                        // display error
                        $("#response").html(resultData['Error'])
                    } else {

                        /* --- create the html table from sql data --- */
                        let tableHead = "";
                        let tableBody = ""


                        for (let key in resultData[0]) {
                            tableHead += "<th> " + key + " </th>"
                        }

                        /*Object.keys(resultData[0]).forEach(function (key) {
                            tableHead += "<th> " + key + " </th>"
                        })*/

                        for (let i = 0; i < resultData.length; i++) {
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
                    }


                },
                error: function (error) {
                    console.log(error)
                },
            })
        }
    })
})
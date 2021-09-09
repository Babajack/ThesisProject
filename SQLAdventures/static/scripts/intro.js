function loadIntro(username) {
    $(document).ready(function () {
        let introText = ['Hallo username! Klicke auf weiter oder auf mich, um fortzufahren.', 'Ich bin König Alfonso und ich brauche dringend deine Hilfe!', 'Meine geliebte Tochter, die Prinzessin, wurde entführt...',
            'Du musst sie bitte wiederfinden!', 'Sie wurde von einem bösen SQL-Mafioso entführt und ich kann sie nicht finden.',
            'Dieser Mafioso ist ein echter SQL-Rätselmeister und du musst gut vorbereitet sein.', 'Am besten gehst du zuerst zum Bauern Manfred. Du findest ihn oben im Menü unter "Quests".',
            'Wenn du Hilfe brauchst, schau erst einmal im "Lexikon" vorbei.', 'Ich wünsche dir viel Spaß!']

        let skipped = false
        let counter = 0

        nextSequence()

        $(document).click(function (event) {
            if (event.target.id === 'ContinueButton' || event.target.id === 'image') {
                if (skipped) {
                    // load next sequence
                    nextSequence()
                    return
                }
            }
            skipped = true
        })


        function nextSequence() {
            if (counter < introText.length) {
                let sequenceElement = introText[counter]

                // enable animation
                skipped = false

                // animate text
                // enable user input if intro is finished
                if (counter === introText.length - 1) {
                    animateText(sequenceElement, true)
                } else {
                    animateText(sequenceElement, false)
                }

                // increase counter
                counter++
            }
        }


        function animateText(text, isLastOne) {
            $('#bubble').text('')
            text = text.replace("username", username)
            type(0, 35, text)

            function type(i, speed, text) {
                if (skipped) {
                    document.getElementById('bubble').innerHTML = text
                    $('#ContinueButton').removeClass('disabled')
                    if (isLastOne) {
                        $('#ContinueButton').css('background-color', 'green').text('Zum Questbuch').click(function () {
                            $.ajax({
                                url: '/quests/questbook',
                                type: 'GET',
                                success: function (data) {
                                    window.location.href = this.url
                                }
                            });
                        })
                    }
                    return
                }
                $('#ContinueButton').addClass('disabled')
                document.getElementById('bubble').innerHTML += text.charAt(i);
                setTimeout(function () {
                    ((i < text.length) ? type(i + 1, speed, text) : lastType(i + 1, speed, text));
                }, speed);
            }

            function lastType(i, speed, text) {
                skipped = true
                type(i, speed, text)
            }
        }
    })
}
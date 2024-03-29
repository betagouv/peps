function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", window.CSRF_TOKEN);
            xhr.setRequestHeader("Content-Type", "application/json");
        }
    }
});

$(document).ready(function () {

    $.get('api/v1/formSchema', (schema) => {
        schema.postRender = (control) => {
            window.alpacaForm = control.form;
            control.children.forEach((field) => {
                field.on('change', window.pepsRenderer.onFormChange);
                field.on('add', window.pepsRenderer.onFormChange);
                field.on('remove', window.pepsRenderer.onFormChange);
                field.on('move', window.pepsRenderer.onFormChange);
            });
        }
        $("#form").alpaca(schema)
    }).fail(() => {
        alert('Error getting form information');
    });


    $("#airtable-refresh").click(() => {
        let modal = $('#airtableModal');
        let modalIsVisible = modal.hasClass('in');
        if (modalIsVisible) {
            return;
        }
        modal.html(`<div class="modal-dialog" role="document">
            <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Fetching Airtable practices</h5>
            </div>
            <div class="modal-body">
                <div class="spinner-border" role="status">
                    <span class="sr-only">Loading...</span>
                </div>
                <div class="progress">
                    <div class="progress-bar progress-bar-animated bg-success" role="progressbar" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100" style="transition-duration:300ms;"></div>
                </div>
            </div>
            </div>
        </div>`)
        modal.modal('show');
        let progress = 0;
        let width = 0
        let progressBarInterval = setInterval(() => {
            progress++;
            width += 15 / progress;
            $('.progress-bar').css('width', width + '%');
        }, 100);
        $.ajax({
            type: "POST",
            url: '/api/v1/refreshData',
            data: {},
            success: (response) => {
                clearInterval(progressBarInterval);
                $('.progress-bar').remove();
                if (response.success) {
                    window.pepsRenderer.onFormChange();
                }

                if (response.errors.length == 0) {
                    modal.modal('hide');
                }

                let message = response.success ? '✔ Données mises à jour' : '✖ La mise à jour des données a échoué';
                let messageClasslist = response.success ? 'title success' : 'title fail'
                $('.modal-title').text('');
                $('.modal-title').append(`<div class="${messageClasslist}">${message}</div>`);
                $('.modal-title').append(`<button onclick="$('#airtableModal').modal('hide')">Fermer</button>`);

                response.errors.sort((a, b) => {
                    if (a.fatal && !b.fatal)
                        return -1;
                    if (b.fatal && !a.fatal)
                        return 1;
                    return 0
                })

                for (let i = 0; i < response.errors.length; i++) {
                    let error = response.errors[i];
                    let classlist = error.fatal ? 'error fatal' : 'error warning'
                    $('.modal-body').append(`
                     <div class="${classlist}">
                        <div class="dot">⬤</div>
                        <div class="message">${error.message}</div>
                        <a class="url-error" href="${error.url}">Link Airtable</div>
                     <div>
                    `)
                }
            },
            error: () => {
                clearInterval(progressBarInterval);
                $('.progress-bar').remove();
                $('.modal-title').text('An error has occurred');
            }
        });
    });


    $("#airtable-xp-refresh").click(() => {
        let modal = $('#airtableModal');
        let modalIsVisible = modal.hasClass('in');
        if (modalIsVisible) {
            return;
        }
        modal.html(`<div class="modal-dialog" role="document">
            <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Fetching Airtable XPs</h5>
            </div>
            <div class="modal-body">
                <div class="spinner-border" role="status">
                    <span class="sr-only">Loading...</span>
                </div>
                <div class="progress">
                    <div class="progress-bar progress-bar-animated bg-success" role="progressbar" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100" style="transition-duration:300ms;"></div>
                </div>
            </div>
            </div>
        </div>`)
        modal.modal('show');
        let progress = 0;
        let width = 0
        let progressBarInterval = setInterval(() => {
            progress++;
            width += 15 / progress;
            $('.progress-bar').css('width', width + '%');
        }, 100);
        $.ajax({
            type: "POST",
            url: '/api/v1/refreshXPData',
            data: {},
            success: (response) => {
                clearInterval(progressBarInterval);
                $('.progress-bar').remove();

                if (response.errors.length == 0) {
                    modal.modal('hide');
                }

                let message = response.success ? '✔ Données XP mises à jour' : '✖ La mise à jour des données XP a échoué';
                let messageClasslist = response.success ? 'title success' : 'title fail'
                $('.modal-title').text('');
                $('.modal-title').append(`<div class="${messageClasslist}">${message}</div>`);
                $('.modal-title').append(`<button onclick="$('#airtableModal').modal('hide')">Fermer</button>`);

                response.errors.sort((a, b) => {
                    if (a.fatal && !b.fatal)
                        return -1;
                    if (b.fatal && !a.fatal)
                        return 1;
                    return 0
                })

                for (let i = 0; i < response.errors.length; i++) {
                    let error = response.errors[i];
                    let classlist = error.fatal ? 'error fatal' : 'error warning'
                    $('.modal-body').append(`
                     <div class="${classlist}">
                        <div class="dot">⬤</div>
                        <div class="message">${error.message}</div>
                        <a class="url-error" href="${error.url}">Link Airtable</div>
                     <div>
                    `)
                }
            },
            error: () => {
                clearInterval(progressBarInterval);
                $('.progress-bar').remove();
                $('.modal-title').text('An error has occurred');
            }
        });
    });

    $(document).on("click", ".list-toggle-button" , function(event) {
        practiceId = event.target.parentElement.parentElement.id;
        containerId = event.target.parentElement.parentElement.parentElement.id

        if (containerId === "blacklist") {
            $('#' + practiceId).remove();
        } else if (containerId === "suggestions") {
            $('#' + practiceId).detach().appendTo('#blacklist');
        } else {
            console.error('Cannot toggle practice');
        }
        window.pepsRenderer.onFormChange();
    });
});

window.pepsRenderer = {
    'onFormChange': function(e) {
        if (!e) {
            // Due to a regression on Alpaca library: https://github.com/gitana/alpaca/issues/723
            return
        }
        e.stopImmediatePropagation();
        let formAnswers = window.alpacaForm.getValue()
        let blacklistedPractices = $.makeArray($('#blacklist').children().map((x, y) => y.id))

        data = JSON.stringify({
            "answers": formAnswers,
            "practice_blacklist": blacklistedPractices 
        });

        var promise = $.ajax({headers: {}, dataType: "json", url: "/api/v1/calculateRankings", type: "post", data: data});
        promise.done(function(response) {
            window.pepsRenderer.render(response['practices'], response['suggestions']);
        });
        promise.fail(function() {
            alert("Error");
        });
    },
    'render': function(practices, suggestions) {
        if (!practices) {
            return;
        }
        let results_container = $('#results');
        let suggestions_container = $('#suggestions');
        results_container.empty();
        suggestions_container.empty();

        for (let i = 0; i < practices.length; i++) {
            let practice = practices[i].practice;
            let weight = practices[i].weight.toFixed(6);
            let airtableUrl = practice.airtable_url;
            let description = practice.description.substring(0, 120) + '...'
            let image = 'https://cdn.pixabay.com/photo/2017/05/19/15/16/countryside-2326787_960_720.jpg'
            if (practice.image) {
                image = practice.image;
            } else {
                image = 'https://cdn.pixabay.com/photo/2017/05/19/15/16/countryside-2326787_960_720.jpg'
            }
            let difficultyBadge = window.pepsRenderer.getDifficultyBadge(practice.difficulty)
            let body = `
                <div class="media practice" onclick="window.open('${airtableUrl}')" id="${practice.id}">
                    <div class="media">
                    <img width="40" height="40" src="${image}" class="mr-3 pull-left practice">
                    <div class="media-body">
                        <h4 class="mt-0 practice_name">${(i + 1)} - ${practice.title}</h4>
                        <h5 class="practice-badges">
                            <span class="label label-pill label-default">${weight}</span>&nbsp;
                            ${difficultyBadge}
                        </h5>
                        <p class="practice-description">${description}</p>
                    </div>
                </div>
            `
            results_container.append(body)
        }

        suggestionsExternalIds = suggestions.map(x => x.practice.external_id);
        $('#user-display').attr('href', '/userDisplay?practices=' + suggestionsExternalIds.join(','));

        for (let i = suggestions.length - 1; i >= 0; i--) {
            let practice = suggestions[i].practice;
            let weight = suggestions[i].weight.toFixed(6);
            let airtableUrl = practice.airtable_url;
            let image = 'https://cdn.pixabay.com/photo/2017/05/19/15/16/countryside-2326787_960_720.jpg'
            if (practice.image) {
                image = practice.image;
            } else {
                image = 'https://cdn.pixabay.com/photo/2017/05/19/15/16/countryside-2326787_960_720.jpg'
            }

            let difficultyBadge = window.pepsRenderer.getDifficultyBadge(practice.difficulty);
            let practiceIndex = practices.map((x) => x.practice.id).indexOf(suggestions[i].practice.id);
            let body = `
                <div class="media suggestion" id="${practice.id}">
                    <div class="media">
                    <img width="40" height="40" src="${image}" class="mr-3 pull-left practice">
                    <div class="media-body">
                        <p class="mt-0 practice_name"><span class="practice-number">${practiceIndex + 1} - </span>${practice.title}</p>
                        <h5 class="practice-badges">
                            <span class="label label-pill label-default">${weight}</span>&nbsp;
                            ${difficultyBadge}
                        </h5>
                    </div>
                    <div class="list-toggle-button"></div>
                </div>
            `
            suggestions_container.append(body)
        }
    },
    'getDifficultyBadge': function(difficulty) {
        if (!difficulty) {
            return '<span class="label label-pill label-secondary">?</span>'
        } else if (difficulty < 0.34) {
            return '<span class="label label-pill label-success"> Difficulté : ' + difficulty + '</span>'
        } else if (difficulty < 0.67) {
            return '<span class="label label-pill label-warning"> Difficulté : ' + difficulty + '</span>'
        } else {
            return '<span class="label label-pill label-danger"> Difficulté : ' + difficulty + '</span>'
        }
    }
}

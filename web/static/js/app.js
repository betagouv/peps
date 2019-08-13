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
            control.children.forEach((x) => x.on('change', window.pepsRenderer.onFormChange));
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
        modal.modal('show');
        $.ajax({
            type: "POST",
            url: '/api/v1/refreshData',
            data: {},
            success: () => {
                window.pepsRenderer.onFormChange();
                modal.modal('hide');
            }
          });
    })

    $("#user-display").click(() => {
        let formAnswers = window.alpacaForm.getValue()
        let blacklistedPractices = $.makeArray($('#blacklist').children().map((x, y) => y.id))
        data = JSON.stringify({
            "answers": formAnswers,
            "blacklist": blacklistedPractices 
        });

        $.ajax({
            type: "POST",
            url: '/productionSystemForm',
            data: data,
            success: (response) => {
                window.location = response.url;
            },
            error: () => {
                alert('Error from redirect')
            }
          });
    })

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
        e && e.stopImmediatePropagation();
        let formAnswers = window.alpacaForm.getValue()
        let blacklistedPractices = $.makeArray($('#blacklist').children().map((x, y) => y.id))

        data = JSON.stringify({
            "answers": formAnswers,
            "blacklist": blacklistedPractices 
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
            if (practice.image_url) {
                image = practice.image_url;
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

        for (let i = suggestions.length - 1; i >= 0; i--) {
            let practice = suggestions[i].practice;
            let weight = suggestions[i].weight.toFixed(6);
            let airtableUrl = practice.airtable_url;
            let image = 'https://cdn.pixabay.com/photo/2017/05/19/15/16/countryside-2326787_960_720.jpg'
            if (practice.image_url) {
                image = practice.image_url;
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

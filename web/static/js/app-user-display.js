$(document).ready(function () {
    window.suggestions = JSON.parse(document.getElementById('suggestions').textContent);
    renderSuggestions();

    $('#send-email').click(() => {
        $.ajax({
            type: "POST",
            url: '/api/v1/sendEmail',
            data: JSON.stringify({
                email: $('#email').val(),
                first_name: $('#first-name').val(),
                problem: $('#problem').val(),
                practices: suggestions.map(x => x.external_id),
            }),
            success: (response, textStatus, jqXHR) => {
                let messages = response.Messages || [];
                let emailAddress;
                if (messages.length > 0) {
                    emailAddress = messages[0].To[0].Email;
                }
                if (jqXHR.status == 200) {
                    $('#email').val('');
                    $('#first-name').val('');
                    $('#problem').val('');
                    alert('✔ SUCCESS. Email pour ' + emailAddress + ' sera traité par Mailjet');
                } else {
                    alert('✖ FAIL. Status code: ' + jqXHR.status + '. ' + JSON.stringify(response));
                }
            }
        });
    });

    $('#refresh-practices').click(() => {
        var practices = '';
        var inputValues = $('.practice-at-id').toArray().reverse()
        for (var i = 0; i < inputValues.length; i++) {
            var elem = $(inputValues[i]);
            if (!!elem.val())
                practices += (elem.val() + ',');
        }

        window.location = location.protocol + '//' + location.host + '/userDisplay?practices=' + practices;
    })

    $("#airtable-refresh").click(() => {
        let modal = $('#airtableModal');
        let modalIsVisible = modal.hasClass('in');
        if (modalIsVisible) {
            return;
        }
        modal.html(`<div class="modal-dialog" role="document">
            <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Fetching Airtable data</h5>
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
                    location.reload();
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
    })

});
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


function renderSuggestions() {

    for (let i = window.suggestions.length - 1; i >= 0; i--) {
        let practice = window.suggestions[i];
        let columns = getColumnsHtml(practice);
        let resources = getResourcesHtml(practice);
        let practiceHtml = `
            <div class="practice" id="${practice.id}">
                <div class="practice-header">
                    <div class="mechanism"><strong>${practice.mechanism ? practice.mechanism.name : ""}</strong></div>
                    <div class="title">${practice.title}</div>
                    <a href="${practice.airtable_url}" target="_blank" class="airtable-link"><button>Airtable ➚</button></a>
                </div>
                <div class="columns">${columns}</div>
                <div class="mechanism mechanism-description"><strong>
                    ${practice.mechanism && practice.mechanism.description ? practice.mechanism.description : ""}
                </strong></div>
                <div class="description">${practice.description}</div>
                <div class="resources">${resources}</div>
                <div class="cta">
                    <button onclick="location.href='${practice.main_resource ? practice.main_resource.url : ''}'">
                        ${practice.main_resource_label ? practice.main_resource_label : practice.main_resource.name}
                    </button>
                </div>
            </div>
        `
        $('#content').append(practiceHtml);
        $('#practice' + (window.suggestions.length - i)).val(practice.external_id)
    }
}

function getColumnsHtml(practice) {
    let leftColumn = [];
    let rightColumn = [];

    let columns = []

    function get_item_html(title, value) {
        return `<div class="column-item">
            <span class="column-item-title">${title} : </span>${value}
        </div>`
    }

    if (practice.equipment)
        leftColumn.push(get_item_html('Matériel', practice.equipment));

    if (practice.schedule)
        leftColumn.push(get_item_html('Période de travail', practice.schedule));

    if (practice.impact)
        rightColumn.push(get_item_html('Impact', practice.impact));

    if (practice.additional_benefits)
        rightColumn.push(get_item_html('Bénéfices supplémentaires', practice.additional_benefits));

    if (practice.success_factors)
        rightColumn.push(get_item_html('Facteur clé de succès', practice.success_factors));

    if (leftColumn.length > 0)
        columns.push(`<div class="column column-left">${leftColumn.join(' ')}</div>`);

    if (rightColumn.length > 0)
        columns.push(`<div class="column column-right">${rightColumn.join(' ')}</div>`);

    return columns.join(' ');
}

function getResourcesHtml(practice) {
    if (!practice.secondary_resources || practice.secondary_resources.length == 0)
        return ''

    let resourceLabels = []
    let text = ''
    let start = 'Pour plus d\'informations voici'
    for (let i = 0; i < practice.secondary_resources.length; i++) {
        let resource = practice.secondary_resources[i];
        let type = ''
        if (resource.resource_type === 'SITE_WEB')
            type = 'le site web';
        else if (resource.resource_type === 'VIDEO')
            type = 'la vidéo';
        else if (resource.resource_type === 'PDF')
            type = 'le document';
        else 
            type = 'la resource';

        resourceLabel = `<span class="resource-inline">${type} <a href="${resource.url}">"${resource.name}"</a></span>`;
        if (resource.description)
            resourceLabel += ` (${resource.description.firstLower()})`;
        resourceLabels.push(resourceLabel);
    }

    if (resourceLabels.length === 1)
        return `${start} ${resourceLabels.join(', ')}.`;

    return `${start} ${resourceLabels.slice(0, -1).join(', ')} et ${resourceLabels[resourceLabels.length - 1]}.`;
}
String.prototype.firstLower = function () {
    return this.charAt(0).toLowerCase() + this.slice(1)
}
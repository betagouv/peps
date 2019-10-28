// Once the document is ready and every time we pop a history event we will load the content
$(document).ready(loadContent);
window.onpopstate = (event) => loadContent();

// Include CSRF token on relevant AJAX methods
function csrfSafeMethod(method) {
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


function loadContent() {
    // The user wants to see the results
    if (window.location.toString().indexOf('page=results') != -1) {
        let suggestions = history.state && history.state.hasOwnProperty('suggestions') ? history.state.suggestions : null;
        let answers = history.state && history.state.hasOwnProperty('answers') ? history.state.answers : null;
        if (suggestions) {
            return window.peps.renderSuggestions(suggestions);
        } 
        if (answers) {
            return window.peps.fetchSuggestions();
        }
    }
    // The user wants to see the form
    return window.peps.renderForm();
}


window.peps = {
    'onFieldChange': function(e) {
        let hasIncompleteFields = window.alpacaControl.children.some((field) => {
            let isVisible = field.isHidden && !field.isHidden();
            let isEmpty = Array.isArray(field.getValue()) ? !!field.getValue().length : !!field.getValue();
            return isVisible && !isEmpty;
        });
        $('#submit').prop('disabled', hasIncompleteFields);
    },
    'submit': function(e) {
        if (peps.waitingModalIsVisible()) {
            return;
        }
        window.peps.showWaitingModal();
        let answers = window.alpacaControl.form.getValue();
        window.history.pushState({'answers': answers}, window.title, window.location);
        setTimeout(() => peps.fetchSuggestions(), 2000);
    },
    'renderSuggestions': function(suggestions) {
        $('#form').hide();
        $('#submit').hide();
        let results = $('#results');

        results.empty();

        for (let i = suggestions.length - 1; i >= 0; i--) {
            let practice = suggestions[i].practice;
            let columns = getColumnsHtml(practice);
            let resources = getResourcesHtml(practice);
    
            let practiceHtml = `
                <div class="practice" id="${practice.id}">
                    <div class="practice-header">
                        <div class="mechanism"><strong>${practice.mechanism ? practice.mechanism.name : ""}</strong></div>
                        <div class="title">${practice.title}</div>
                    </div>
                    <div class="columns well">${columns}</div>
                    <div class="description">${practice.description}</div>
                    <div class="subtitle">Resources</div>
                    <div class="resources">${resources}</div>
                    <div class="button-row">
                        <button class="blacklist" id="blacklist-${practice.id}"><span class="button-emoji">🚫</span> Recalculer sans cette pratique</button>
                        <button class="try" id="try-${practice.id}"><span class="button-emoji">👍</span> Essayer cette pratique</button>
                    </div>
                </div>
            `
            results.append(practiceHtml);
        }
        window.scrollTo(0, 0);
        results.show();
        $('#content').show();
    },
    'renderForm': function() {

        if (window.alpacaControl && window.alpacaControl.form) {
            $('#content').show();
            $('#form').show();
            $('#submit').show();
            $('#results').hide();
            window.scrollTo(0, 0);
            return;
        }

        let prefilledAnswers = history.state && history.state.hasOwnProperty('answers') ? history.state.answers : {};

        $('#submit').click(window.peps.submit);
        $.get('api/v1/formSchema', (schema) => {
            schema.postRender = (control) => {
                $('#content').show();
                $('#form').show();
                $('#submit').show();
                $('#results').hide();
                window.scrollTo(0, 0);
                window.alpacaControl = control;
                control.children.forEach((field) => {
                    ['change', 'add', 'remove', 'move'].forEach(x => field.on(x, window.peps.onFieldChange));
                });
                window.peps.onFieldChange();
            }
            schema.data = prefilledAnswers;
            $("#form").alpaca(schema);
        }).fail(() => {
            alert('Error getting form information');
        });
        window.scrollTo(0, 0);
    },
    'fetchSuggestions': function() {
        $('#content').show();
        answers = history.state.answers;
        data = JSON.stringify({
            "answers": answers,
            "practice_blacklist": []
        });

        var promise = $.ajax({headers: {}, dataType: "json", url: "/api/v1/calculateRankings", type: "post", data: data});

        promise.done(function(response) {
            window.peps.hideWaitingModal();
            $('.progress-bar').css('width', '100%');
            setTimeout(() => {
                window.history.pushState({
                    'answers': answers,
                    'suggestions': response['suggestions'],
                }, 'Results', '?page=results');
                window.peps.renderSuggestions(response['suggestions']);
            }, 600)
        });
        promise.fail(function() {
            window.peps.hideWaitingModal();
            alert("Error");
        });
    },
    'showWaitingModal': function() {
        if (peps.waitingModalIsVisible()) {
            return;
        }
        if (window.peps.progressBarInterval) {
            window.peps.hideWaitingModal();
        }
        $('#loadingModal').modal('show')
        let progress = 0;
        let width = 0
        window.peps.progressBarInterval = setInterval(() => {
            progress++;
            width += 15 / progress;
            $('.progress-bar').css('width', width + '%');
        }, 100);
    },
    'hideWaitingModal': function() {
        if (window.peps.progressBarInterval) {
            clearInterval(window.peps.progressBarInterval);
            window.peps.progressBarInterval = null;
        }
        $('#loadingModal').modal('hide');
    },
    'waitingModalIsVisible': function() {
        return $('#loadingModal').hasClass('in');
    },
}

function getColumnsHtml(practice) {
    let leftColumn = [];
    let rightColumn = [];

    let columns = []

    function get_item_html(title, value) {
        return `<table class="column-item">
            <tr>
                <td class="column-item-title">${title} : </td>
                <td class="column-item-value">${value}</td>
            </tr>
        </table>`
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

    let hasMainResource = !!practice.main_resource;
    let hasSecondaryResource = !!practice.secondary_resources && practice.secondary_resources.length == 0;
    if (!hasMainResource && !hasSecondaryResource)
        return ''

    let resources = [practice.main_resource].concat(practice.secondary_resources || []);
    let html = '';

    for (let i = 0; i < resources.length; i++) {
        let resource = resources[i];
        let glyphicons = {
            'SITE_WEB': 'glyphicon-globe',
            'PDF': 'glyphicon-file',
            'VIDEO': 'glyphicon-film',
        }
        let glyphicon = glyphicons.hasOwnProperty(resource.resource_type) ? glyphicons[resource.resource_type] : 'glyphicon-info-sign';
        html += `
            <a class="resource" id="resource-${resource.id}" target="_blank" href="${resource.url}">
                <div class="resource-icon">
                    <span class="glyphicon ${glyphicon}" aria-hidden="true"></span>
                </div>
                <div class="resource-title">${resource.name}</div>
                <div class="resource-description">${resource.description}</div>
            </a>
        `
    }
    return html;
}

String.prototype.firstLower = function () {
    return this.charAt(0).toLowerCase() + this.slice(1)
}

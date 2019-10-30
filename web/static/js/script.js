// Include CSRF token on relevant AJAX methods
function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", window.CSRF_TOKEN);
            xhr.setRequestHeader("Content-Type", "application/json");
        }
    }
});

String.prototype.firstLower = function () {
    return this.charAt(0).toLowerCase() + this.slice(1)
}
String.prototype.isEmail = function () {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(this.toLowerCase());
}

window.peps = {
    'loadContent': function () {
        // button bindings
        $('#try-modal-close').click(window.peps.hideTryModal);

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
    },
    'onFieldChange': function (e) {
        let hasIncompleteFields = window.alpacaControl.children.some((field) => {
            let isVisible = field.isHidden && !field.isHidden();
            let isEmpty = Array.isArray(field.getValue()) ? !!field.getValue().length : !!field.getValue();
            return isVisible && !isEmpty;
        });
        $('#submit').prop('disabled', hasIncompleteFields);
    },
    'submit': function (e) {
        if (peps.waitingModalIsVisible()) {
            return;
        }
        let answers = window.alpacaControl.form.getValue();
        window.history.pushState({ 'answers': answers }, window.title, window.location);
        window.peps.fetchSuggestions();
    },
    'toggleForm': function (visible) {
        [$('#form'), $('#submit'), $('#info-form')].forEach(x => x.toggle(visible));
    },
    'toggleResults': function (visible) {
        [$('#results'), $('#info-results')].forEach(x => x.toggle(visible));
    },
    'renderSuggestions': function (suggestions) {
        window.peps.toggleForm(false);
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
            $('#blacklist-' + practice.id).click(() => window.peps.blacklistPractice(practice.id));
            $('#try-' + practice.id).click(() => window.peps.showTryModal(practice.id));
        }
        window.scrollTo(0, 0);
        window.peps.toggleResults(true);
        $('#content').show();
    },
    'renderForm': function () {

        if (window.alpacaControl && window.alpacaControl.form) {
            $('#content').show();
            window.peps.toggleResults(false);
            window.peps.toggleForm(true);
            window.scrollTo(0, 0);
            return;
        }

        let prefilledAnswers = history.state && history.state.hasOwnProperty('answers') ? history.state.answers : {};

        $('#submit').click(window.peps.submit);
        $.get('api/v1/formSchema', (schema) => {
            schema.postRender = (control) => {
                window.peps.toggleResults(false);
                window.peps.toggleForm(true);
                $('#content').show();
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
            alert("🙁 Oops ! On n'a pas pu charger les données. Veuillez essayer plus tard.");
        });
        window.scrollTo(0, 0);
    },
    'fetchSuggestions': function (silent=false) {
        window.peps.showWaitingModal('⌛️ Nous cherchons des pratiques alternatives', 'Nous vous proposerons 3 pratiques alternatives de gestion des adventices, des maladies et des ravageurs qui sont adaptées à votre exploitation');
        setTimeout(() => {
            $('#content').show();
            answers = history.state.answers;
            let blacklist = history.state.hasOwnProperty('blacklist') ? history.state.blacklist : [];
            data = JSON.stringify({
                "answers": answers,
                "practice_blacklist": blacklist
            });

            var promise = $.ajax({ headers: {}, dataType: "json", url: "/api/v1/calculateRankings", type: "post", data: data });

            promise.done(function (response) {
                $('.progress-bar').css('width', '100%');
                setTimeout(() => {
                    historyFn = silent ? window.history.replaceState : window.history.pushState;
                    historyFn.call(history, {
                        'answers': answers,
                        'blacklist': blacklist,
                        'suggestions': response['suggestions'],
                    }, 'Results', '?page=results');
                    window.peps.hideWaitingModal();
                    window.peps.renderSuggestions(response['suggestions']);
                }, 600)
            });
            promise.fail(function () {
                window.peps.hideWaitingModal();
                alert("🙁 Oops ! On n'a pas pu trouver des suggestions. Veuillez essayer plus tard.");
            });
        }, 2000);
    },
    'showWaitingModal': function (title, body) {
        if (peps.waitingModalIsVisible()) {
            return;
        }
        if (window.peps.progressBarInterval) {
            window.peps.hideWaitingModal();
        }
        $('#modalTitle').text(title);
        $('#modalBody').text(body);
        $('#loadingModal').modal('show')
        let progress = 0;
        let width = 0
        window.peps.progressBarInterval = setInterval(() => {
            progress++;
            width += 15 / progress;
            $('.progress-bar').css('width', width + '%');
        }, 100);
    },
    'hideWaitingModal': function () {
        if (window.peps.progressBarInterval) {
            clearInterval(window.peps.progressBarInterval);
            window.peps.progressBarInterval = null;
        }
        $('#loadingModal').modal('hide');
        $('.progress-bar').css('width', '0%');
    },
    'waitingModalIsVisible': function () {
        return $('#loadingModal').hasClass('in');
    },
    'blacklistPractice': function (practiceId) {
        let answers = history.state && history.state.hasOwnProperty('answers') ? history.state.answers : null;
        let blacklist = history.state && history.state.hasOwnProperty('blacklist') ? history.state.blacklist : [];

        window.history.replaceState({
            'answers': answers,
            'blacklist': blacklist.concat(practiceId)
        }, window.title, window.location);
        window.peps.fetchSuggestions(true);
    },
    'showTryModal': function (practiceId) {
        $('#tryModal').modal('show');
        $('#try-modal-confirm').unbind().click(() => {
            let invalidFields = window.peps.getInvalidTryModalFields();
            if (invalidFields.length > 0) {
                invalidFields.forEach(x => x.toggleClass('invalid', true));
                return;
            }
            let nameField = $('#nameField');
            let emailField = $('#emailField');
            let phoneField = $('#phoneField');
            let dateField = $('#dateTimeField');
            [nameField, emailField, phoneField].forEach(x => x.toggleClass('invalid', false));

            let date = moment($('#dateTimeField').val(), 'dddd, MMMM Do YYYY, H:mm', 'FR').toISOString(true);
            let problem = $('#try-problem input[type="radio"]:checked').first().attr('value') || 'Problème pas connu';

            window.peps.createTryTask(nameField.val(), emailField.val(), phoneField.val(), date, problem, practiceId);
        });
    },
    'getInvalidTryModalFields': function () {
        let nameField = $('#nameField');
        let emailField = $('#emailField');
        let phoneField = $('#phoneField');
        let dateField = $('#dateTimeField');
        let invalidFields = [];

        if (!nameField.val()) {
            invalidFields.push(nameField);
        }
        if (!emailField.val() || !emailField.val().isEmail()) {
            invalidFields.push(emailField);
        }
        if (!phoneField.val()) {
            invalidFields.push(phoneField);
        }
        if (!dateField.val()) {
            invalidFields.push(dateField);
        }
        return invalidFields;
    },
    'hideTryModal': function () {
        $('#tryModal').modal('hide');
        [$('#nameField'), $('#emailField'), $('#phoneField')].forEach(x => x.val('').toggleClass('invalid', false));
        $('#try-problem input[type="radio"]').prop("checked", false);
    },
    'createTryTask': function (name, email, phone, date, problem, practiceId) {
        window.peps.hideTryModal();
        this.showWaitingModal('Juste un instant', 'Nous envoyons vos disponibilités à notre équipe...');
        let answers = history.state && history.state.hasOwnProperty('answers') ? history.state.answers : {};
        let readableAnswers = '';
        for (let key in answers) {
            readableAnswers += key + '\n' + answers[key].toString() + '\n\n';
        }
        setTimeout(function () {
            var promise = $.ajax({
                headers: {}, dataType: "json", url: "/api/v1/sendTask", type: "post", data: JSON.stringify({
                    'answers': readableAnswers,
                    'email': email,
                    'name': name,
                    'phone_number': phone,
                    'datetime': date,
                    'practice_id': practiceId,
                    'problem': problem,
                })
            });

            promise.done(function (response) {
                $('.progress-bar').css('width', '100%');
                setTimeout(() => {
                    window.peps.hideWaitingModal();
                    alert('👍 Vos disponibilités ont bien été envoyées. À bientôt !');
                }, 600)
            });
            promise.fail(function () {
                window.peps.hideWaitingModal();
                alert("🙁 Oops ! On n'a pas pu envoyer vos disponibilités. Veuillez essayer plus tard.");
            });
        }, 1500)
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

// Once the document is ready and every time we pop a history event we will load the content
$(document).ready(window.peps.loadContent);
window.onpopstate = (event) => window.peps.loadContent();

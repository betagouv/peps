$(document).ready(function () {
    window.suggestions = JSON.parse(document.getElementById('suggestions').textContent);
    window.answers = JSON.parse(document.getElementById('answers').textContent);
    window.blacklist = JSON.parse(document.getElementById('practice_blacklist').textContent);
    renderSuggestions();
})

function renderSuggestions() {

    for (let i = window.suggestions.length - 1; i >= 0; i--) {
        let practice = window.suggestions[i].practice;
        let columns = getColumnsHtml(practice);
        let resources = getResourcesHtml(practice);
        let practiceHtml = `
            <div class="practice" id="${practice.id}">
                <div class="practice-header">
                    <div class="mechanism"><strong>${practice.mechanism ? practice.mechanism.name : ""}</strong></div>
                    <div class="title">${practice.title}</div>
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
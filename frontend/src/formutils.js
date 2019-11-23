export default {
    formsAreComplete() {

    },
    miaFormIsComplete() {

    },
    statsFormIsComplete() {

    },
    contactFormIsComplete() {

    },
    getVisibleFields(schema, options, data) {
        let visibleFields = []
        for (const name in schema.properties) {
            if (this.dependenciesAreMet(name, schema, options, data)) {
                visibleFields.push(name)
            }
        }
        return visibleFields
    },
    dependenciesAreMet(fieldName, schema, options, data) {
        const dependencies = schema.dependencies
        const opts = options && options.fields && options.fields[fieldName] ? options.fields[fieldName] : undefined
        if (!dependencies || !dependencies[fieldName] || !opts || !opts.dependencies)
            return true

        for (let dependentFieldName in opts.dependencies) {
            if (!this.dependenciesAreMet(dependentFieldName, schema, options, data))
                return false
            const dependentValue = (data || {})[dependentFieldName]
            let dependency = opts.dependencies[dependentFieldName]

            if (!Array.isArray(dependency))
                dependency = [dependency]

            if (dependency.indexOf(dependentValue) === -1)
                return false
        }
        return true
    },
}

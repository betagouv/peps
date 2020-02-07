export default {
    formIsComplete(schema, options, data) {
        const visibleFields = this.getVisibleFields(schema, options, data)
        return visibleFields.every(fieldName => {
            const value = data[fieldName]
            return !!(value && value !== undefined && value !== null && value !== '' && (Array.isArray(value) ? value.length > 0 : true))
        })
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
    getHumanReadableAnswers(schema, options, data) {
        let readableAnswers = ''
        for (const fieldName in data) {
            if (!data[fieldName])
                continue

            readableAnswers += fieldName + '\n'
            let type = this.getFieldType(schema, options, fieldName)

            if (type === 'radio' || type === 'select') {
                const response = this.getDataSource(schema, options, fieldName).find(x => x.value === data[fieldName])
                readableAnswers += response ? response.text : ''
            }
            if (type === 'checkbox') {
                const responses = this.getDataSource(schema, options, fieldName).filter(x => data[fieldName].indexOf(x.value) > -1).map(x => x.text)
                readableAnswers += responses.join(', ')
            }
            if (type === 'string') {
                readableAnswers += data[fieldName]
            }
            if (type === 'array') {
                if (options && options.fields[fieldName] && options.fields[fieldName].items && options.fields[fieldName].items.dataSource) {
                    const responses = options.fields[fieldName].items.dataSource.filter(x => data[fieldName].indexOf(x.value) > -1).map(x => x.text)
                    readableAnswers += responses.join(', ')
                }
            }
            readableAnswers += '\n\n'
        }
        return readableAnswers
    },
    getFieldType(schema, options, fieldName) {
        const hasOwnProperty = Object.prototype.hasOwnProperty
        if (schema && hasOwnProperty.call(schema.properties, fieldName) && hasOwnProperty.call(schema.properties[fieldName], 'type')) {
            return schema.properties[fieldName].type
        }
        if (options && hasOwnProperty.call(options.fields, fieldName) && hasOwnProperty.call(options.fields[fieldName],'type')) {
            return options.fields[fieldName].type
        }
    },
    getDataSource(schema, options, fieldName) {
        if (options && options.fields[fieldName] && options.fields[fieldName].dataSource) {
            return options.fields[fieldName].dataSource
        }
        if (options && options.fields[fieldName] && options.fields[fieldName].enum) {
            return options.fields[fieldName].enum.map(x => {
                return { text: x, value: x };
            })
        }
        if (schema && schema.properties[fieldName] && schema.properties[fieldName].enum) {
            return schema.properties[fieldName].enum.map(x => {
                return { text: x, value: x };
            })
        }
        return []
    }
}

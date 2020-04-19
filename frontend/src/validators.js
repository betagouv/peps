export default {
  notEmpty(input) {
    const errorMessage = 'Ce champ ne peut pas être vide'
    if (typeof input === 'undefined')
      return errorMessage
    if (typeof input === 'object' && input === null)
      return errorMessage
    if (typeof input === 'boolean')
      return true
    if (typeof input === 'number')
      return true
    if (typeof input === 'string')
      return input.trim().length > 0 ? true : errorMessage
    if (!input)
      return errorMessage
    return input.length && input.length > 0 ? true : errorMessage
  },
}

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
  isUrl(input) {
    let url
    const errorMessage = 'Le lien doit être une URL valide (par ex. "https://exemple.com")'
    try {
      url = new URL(input)
    } catch (_) {
      return errorMessage
    }
    const isValid = url.protocol === "http:" || url.protocol === "https:"
    return isValid ? true : errorMessage
  },
  isEmail(input) {
    const errorMessage = 'Ce champ doit contenir un email valide'
    if (typeof input === 'string' && /\S+@\S+\.\S+/.test(input))
      return true
    return errorMessage
  }
}

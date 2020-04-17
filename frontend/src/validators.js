export default {
  textNotEmpty(input) {
      if (!!input && input.length > 0) {
        return true
      }
      return 'Ce champ ne peut pas être vide'
  },
}

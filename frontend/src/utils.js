export default {
  getObjectDiff(obj1, obj2) {
    if (!obj2 || Object.prototype.toString.call(obj2) !== '[object Object]') {
      return obj1
    }

    let diffs = {}
    let key
    let arraysMatch = this.arraysMatch
    let getObjectDiff = this.getObjectDiff

    let compare = function (item1, item2, key) {
      var type1 = Object.prototype.toString.call(item1)
      var type2 = Object.prototype.toString.call(item2)

      // If type2 is undefined it has been removed
      if (type2 === '[object Undefined]') {
        diffs[key] = null
        return
      }

      // If items are different types
      if (type1 !== type2) {
        diffs[key] = item2
        return
      }

      // If an object, compare recursively
      if (type1 === '[object Object]') {
        var objDiff = getObjectDiff(item1, item2)
        if (Object.keys(objDiff).length > 0) {
          diffs[key] = objDiff
        }
        return;
      }

      // If an array, compare
      if (type1 === '[object Array]') {
        if (!arraysMatch(item1, item2)) {
          diffs[key] = item2
        }
        return;
      }

      // If it's a function, convert to a string and compare
      if (type1 === '[object Function]') {
        if (item1.toString() !== item2.toString()) {
          diffs[key] = item2;
        }
      } else {
        if (item1 !== item2) {
          diffs[key] = item2;
        }
      }
    }

    for (key in obj1) {
      if (Object.prototype.hasOwnProperty.call(obj1, key)) {
        compare(obj1[key], obj2[key], key)
      }
    }

    for (key in obj2) {
      if (Object.prototype.hasOwnProperty.call(obj2, key)) {
        if (!obj1[key] && obj1[key] !== obj2[key]) {
          diffs[key] = obj2[key]
        }
      }
    }

    return diffs
  },
  arraysMatch(arr1, arr2) {
    if (arr1.length !== arr2.length) return false

    for (var i = 0; arr1.length < i; i++) {
      if (arr1[i] !== arr2[i]) return false;
    }

    return true
  }
}

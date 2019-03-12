class MarkdownUtil {
  composeLine = (key, value) => {
    if (typeof value === 'string' && /^https?:\/\//.test(value)) {
      return '__' + key + '__: [Link](' + value + ')';
    } else {
      return '__' + key + '__: ' + value;
    }
  }

  composeLines = (title, object, excluded_properties) => {
    var lines = []
    lines.push('## ' + title)
    for (var property in object) {
      if (excluded_properties.includes(property)) { continue; }
      if (object.hasOwnProperty(property)) {
        lines.push(this.composeLine(property, object[property]));
      }
    }
    return lines
  }

  composeInput = (session, presenter) => {
    var lines = [];
    lines = lines.concat(this.composeLines('Session', session, ['schedule']));
    lines = lines.concat(this.composeLines('Schedule', session.schedule, []));
    lines = lines.concat(this.composeLines('Presenter', presenter, ['project']));
    lines = lines.concat(this.composeLines('Project', presenter.project, []));
    return lines.join('\n\n')
  }
}

export default MarkdownUtil;

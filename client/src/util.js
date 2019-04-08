class MarkdownUtil {
  composeLine = (key, value) => {
    if (['photo', 'logo', 'github', 'linkedin', 'membership_card'].includes(key)) {
      if (!value.startsWith('https')) {
        value = 'https://' + value;
      }
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
    if (session.schedule) {
      lines = lines.concat(this.composeLines('Schedule', session.schedule, []));
    }
    lines = lines.concat(this.composeLines('Presenter', presenter, ['project']));
    if (presenter.project) {
      lines = lines.concat(this.composeLines('Project', presenter.project, []));
    }
    return lines.join('\n\n')
  }

  composeMember = (member) => {
    var lines = this.composeLines(member['name'], member, ['name', 'membership_card', 'member_card'])
    if (member.member_card) {
      lines.push(this.composeLine('member_card', member.member_card.link))
    }
    return lines.join('\n\n')
  }
}

export default MarkdownUtil;

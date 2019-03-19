import axios from 'axios';

const BASE_URI = 'https://blockchainabc.org:4433';

const client = axios.create({
   baseURL: BASE_URI,
   json: true
});

class APIClient {
  constructor(accessToken) {
    this.accessToken = accessToken;
  }

  getSessions() {
    return this.perform('get', '/sessions');
  }

  getSession(session_id) {
    return this.perform('get', '/session/' + session_id);
  }

  getPresenter(username) {
    return this.perform(
      'get', '/presenter/' + encodeURIComponent(username));
  }

  getPoster(session_id, credential_id) {
    var url = '/event_poster/' + session_id
    if (credential_id) {
      url += ('?credential_id=' + credential_id)
    }
    return this.perform('get', url);
  }

  refresh() {
    return this.perform('post', '/refresh');
  }

  async perform(method, resource, data) {
    return client({
      method,
      url: resource,
      data,
      headers: {Authorization: `Bearer ${this.accessToken}`}
    }).then(resp => {
      return resp.data ? resp.data : [];
    })
  }
}

export default APIClient;

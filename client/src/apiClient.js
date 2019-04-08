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

  getPoster(session_id) {
    return this.perform('get', '/event_poster/' + session_id);
  }

  reloadEvents() {
    return this.perform('get', '/refresh_events');
  }

  reloadMembers() {
    return this.perform('get', '/refresh_members');
  }

  getMembers() {
    return this.perform('get', '/members');
  }

  storeGoogleCreds(tokenObj) {
    return this.perform('post', '/store_google_creds', tokenObj);
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

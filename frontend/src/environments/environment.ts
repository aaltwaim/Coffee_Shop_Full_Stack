
export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'fsndaltwaim.auth0.com', // the auth0 domain prefix
    audience: 'shop', // the audience set for the auth0 app
    clientId: 'WyWis97TNbzec8R2o5rPk2npFg294j3i', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};

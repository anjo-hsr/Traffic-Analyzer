require([
    'splunkjs/mvc',
    'splunkjs/mvc/simplexml/ready!'
], function (mvc) {
    let defaultTokenModel = mvc.Components.get('default');

    const savedTokens = window.sessionStorage;
    Object.keys(savedTokens).forEach(tokenKey => {
        const currentToken = defaultTokenModel.get(tokenKey);
        if (Boolean(currentToken)) {
            const parsedToken = JSON.parse(savedTokens[tokenKey]);
            defaultTokenModel.set(tokenKey, parsedToken);
        }
    });

    defaultTokenModel.on('change', function () {
        const attributes = defaultTokenModel.attributes;
        Object.keys(attributes).forEach(tokenKey => {
            const stringifiedToken = JSON.stringify(attributes[tokenKey]);
            window.sessionStorage.setItem(tokenKey, stringifiedToken);
        });
    });
});

require([
    "splunkjs/mvc",
    "splunkjs/mvc/simplexml/ready!"
], function (mvc) {
    let defaultTokenModel = mvc.Components.get("default");

    let savedTokens = window.sessionStorage;
    Object.keys(savedTokens).forEach(tokenKey => {
        let currentToken = defaultTokenModel.get(tokenKey);
        if (Boolean(currentToken)) {
            let parsedToken = JSON.parse(savedTokens[tokenKey]);
            defaultTokenModel.set(tokenKey, parsedToken);
        }
    });

    defaultTokenModel.on("change", function () {
        let attributes = defaultTokenModel.attributes;
        Object.keys(attributes).forEach(tokenKey => {
            let stringifiedToken = JSON.stringify(attributes[tokenKey]);
            window.sessionStorage.setItem(tokenKey, stringifiedToken);
        });
    });
});

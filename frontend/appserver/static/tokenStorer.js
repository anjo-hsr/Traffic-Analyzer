require([
    "splunkjs/mvc",
    "splunkjs/mvc/simplexml/ready!"
], function (mvc) {
    let defaultTokenModel = mvc.Components.get("default");

    let savedTokens = window.sessionStorage;
    Object.keys(savedTokens).forEach(tokenKey => {
        let currentToken = defaultTokenModel.get(tokenKey);
        if (Boolean(currentToken)) {
            defaultTokenModel.set(tokenKey, savedTokens[tokenKey]);
        }
    });

    defaultTokenModel.on("change", function () {
        let attributes = defaultTokenModel.attributes;
        Object.keys(attributes).forEach(tokenKey =>
            window.sessionStorage.setItem(tokenKey, attributes[tokenKey])
        );
    });
});

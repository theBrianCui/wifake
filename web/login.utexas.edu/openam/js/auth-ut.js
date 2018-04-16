/**
 * This file contains Javascript functions to support Login.jsp such that
 * the auth.js file in this directory can be a stock version from ForgeRock.
 * It is notable that the markupButton method that is used in Login.jsp
 * requires some modification from the stock because of some differences
 * in Login.jsp to HTML id and class values.
 */

/**
 * After a pre-specified period of time, disable the login form.
 * @param timeToDisableInMs if > 0, after this many milliseconds the login form will be disabled.
 */
function disableLoginAfter(timeToDisableInMs) {
    if (timeToDisableInMs > 0) {
        setTimeout(function() {
            var oldBoxShadow = jQuery('#content').css("box-shadow");
            // For IE, disable the drop shadow before the #content resizes
            jQuery('#content').css("box-shadow", "none");
            jQuery("#loginForm").html(
                "<p aria-live='assertive'><br/><br/>This login page is active for a limited period "
                    + "of time for security purposes. Please refresh this page to login.<br/><br/><br/></p>");
            jQuery("#reloadAnchor").click(function() {
                window.location.href = removeURLParam(window.location.href, "error");
            });
            jQuery("#loginForm").addClass("error");
            jQuery('#content').css("box-shadow", oldBoxShadow);
        }, timeToDisableInMs);
    }
}

/**
 * Given a specific parameter, if it exists, remove it from the URL.
 * @param url the url in question
 * @param param the param to remove, if it exists
 */
function removeURLParam(url, param) {
    var urlparts = url.split('?');
    var result;
    if (urlparts.length >= 2) {
        var prefix = encodeURIComponent(param) + '=';
        var pars = urlparts[1].split(/[&;]/g);
        for (var i = pars.length; i-- > 0;) {
            if (pars[i].indexOf(prefix, 0)==0) {
                pars.splice(i, 1);
            }
        }
        if (pars.length > 0) {
            result = urlparts[0] + '?' + pars.join('&');
        } else {
            result = urlparts[0];
        }
    } else {
        result = url;
    }
    return result;
}

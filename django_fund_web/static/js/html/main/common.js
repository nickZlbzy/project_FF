// 正则匹配cookie中的csrftoken，传入cookie名字
function getCsrfFromCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

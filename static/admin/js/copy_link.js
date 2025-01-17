function copyToClipboard(url) {
    var dummy = document.createElement("input"),
        text = url;

    document.body.appendChild(dummy);
    dummy.setAttribute("value", text);
    dummy.select();
    document.execCommand("copy");

    document.body.removeChild(dummy);

    alert("Link copied to clipboard!");
}
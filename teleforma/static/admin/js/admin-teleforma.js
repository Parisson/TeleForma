$(document).ready(function() {
    // links should be opened in new tab to avoid a bug with the back button and multiselect field on FF : https://trackers.pilotsystems.net/prebarreau/0311
    $("a:contains('Voir sur le site')").attr("target", "_blank")
})
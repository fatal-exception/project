console.log("char-ner javascript loaded");
$( ".unrendered" ).click(function(event) {
    const $elem = $( this );
    const text = $elem.text();
    $elem.effect("bounce", "slow");
    $.post("http://localhost:5000/predict/", text, function(data) {
        $elem.text(data);
        $elem.removeClass("unrendered");
        $elem.addClass("rendered");
        $elem.unbind("click");
    })
});
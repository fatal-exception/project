console.log("char-ner javascript loaded");
$( "p" ).click(function(event) {
    console.log("Para clicked on");
    const $elem = $( this );
    const text = $elem.text();
    $.post("http://localhost:5000/predict/", text, function(data) {
        console.log(data);
        $elem.text(data);
    })
});
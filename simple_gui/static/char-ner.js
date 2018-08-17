console.log("char-ner javascript loaded");
$( "p" ).click(function(event) {
    const $elem = $( this );
    console.log("You clicked on a paragraph!");
    console.log($elem.text());
});
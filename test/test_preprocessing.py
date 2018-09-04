from hansard_gathering.preprocessing import unxml_hansard_document


def test_unxml_hansard_document():
    text = """
    <?xml version="1.0" encoding="ISO-8859-1"?>
    <publicwhip scrapeversion="a" latest="yes">
    <major-heading id="uk.org.publicwhip/debate/1940-03-20a.1953.0" colnum="1953">Preamble</major-heading>
    <speech id="uk.org.publicwhip/debate/1940-03-20a.1953.1" colnum="1953" time="">
    <p><i>The House met at a Quarter before Three of the Clock</i>, Mr. SPEAKER <i>in the Chair</i>.</p
    """

    result = unxml_hansard_document(text)
    expected = b'\n    Preamble\n    \n    The House met at a Quarter before Three of ' \
               b'the Clock, Mr. SPEAKER in the Chair.'
    assert result == expected

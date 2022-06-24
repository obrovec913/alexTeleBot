from natasha import (
    Segmenter,
    MorphVocab,
    
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    
    PER,
    NamesExtractor,

    Doc
)


segmenter = Segmenter()
morph_vocab = MorphVocab()

emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)

names_extractor = NamesExtractor(morph_vocab)

text = 'Классика белорусской драматургии и музыки демонстрируется на театральных подмостках и в концертных залах, экранизируется.'
def fasta(tex=""):
    doc = Doc(tex)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.parse_syntax(syntax_parser)
    doc.tag_ner(ner_tagger)
    for span in doc.spans:
        span.normalize(morph_vocab)
    po = {_.text: _.normal for _ in doc.spans if _.text != _.normal}
    opp={_.normal: _.fact.as_dict for _ in doc.spans if _.type == PER}
    return doc.tokens[2:], doc.sents[0].syntax.print(), doc.spans[2:],po, opp
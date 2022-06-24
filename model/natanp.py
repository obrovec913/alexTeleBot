


from natasha import (
	    Segmenter,
	    NewsEmbedding,
	    NewsMorphTagger,
	    NewsSyntaxParser,
	    Doc
	)

segmenter = Segmenter()
	
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
	
	#
text = 'Классификатор может расширяться и уточняться экспертами. '
	
def natanp(tex:str):
	doc = Doc(tex)
	
	doc.segment(segmenter)
	doc.tag_morph(morph_tagger)
	doc.parse_syntax(syntax_parser)
	
	npp =[]
	i = 0
	while i < len(doc.sents):
		sent = doc.sents[i]
		np = ""

		index = 0
		marked_index = []
		for token in sent.tokens:
			if(marked_index.__contains__(index)):
				index += 1
				continue
			if(("NOUN" == token.pos or "PROPN" == token.pos) and ("nmod" == token.rel or "nsubj" == token.rel or "obl" == token.rel or "obj" == token.rel)):
				np +=token.text
				marked_index.append(index)
				l_i = index - 1
				while l_i >= 0:
					if(marked_index.__contains__(l_i)):
						l_i -= 1
					else:
						if (sent.tokens[l_i].head_id == token.id and (sent.tokens[l_i].rel == "amod" or sent.tokens[l_i].rel == "nmod") and (sent.tokens[l_i].pos == "NOUN" or sent.tokens[l_i].pos == "ADJ")):
							np = sent.tokens[l_i].text + " " + np
							marked_index.append(l_i)
						l_i -= 1
					r_i = index + 1
				while r_i < len(sent.tokens):
					if(marked_index.__contains__(r_i)):
						r_i += 1
						continue
					if (sent.tokens[r_i].head_id == token.id and (
						sent.tokens[r_i].rel == "amod" or sent.tokens[r_i].rel == "nmod") and (
						sent.tokens[r_i].pos == "NOUN" or sent.tokens[r_i].pos == "ADJ")):
						np = np + " " + sent.tokens[r_i].text
						marked_index.append(r_i)
					r_i += 1
		
			if (np != ""):
				npp.append(np)				
				np = ""
			index += 1
		i += 1
	on={"Именные группы из текста ":npp}
	return on
# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2013 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""Template context function to get fulltext snippets via Solr."""

from invenio.config import CFG_WEBSEARCH_FULLTEXT_SNIPPETS, \
                            CFG_WEBSEARCH_FULLTEXT_SNIPPETS_CHARS
from invenio.errorlib import register_exception
from invenio.solrutils_bibindex_searcher import solr_get_snippet
#from invenio.bibformat_utils import get_pdf_snippets
from invenio.search_engine_utils import get_fulltext_terms_from_search_pattern
from invenio.websearch_cache import get_pattern_from_cache

def template_context_function(id_bibrec, pattern, qid):
    """
    @param id_bibrec ID of record
    @param pattern search pattern
    @param current_user user object
    @param qid query id
    @return HTML containing snippet
    """

    if not pattern: pattern = get_pattern_from_cache(qid)

    nb_chars = CFG_WEBSEARCH_FULLTEXT_SNIPPETS_CHARS.get('', 0)
    max_snippets = CFG_WEBSEARCH_FULLTEXT_SNIPPETS.get('', 0)

    if id_bibrec and pattern:
        if CFG_WEBSEARCH_FULLTEXT_SNIPPETS and 'fulltext:' in pattern:
            terms = get_fulltext_terms_from_search_pattern(pattern)
            if terms:
                snippets = ''
                try:
                    snippets = solr_get_snippet(terms, id_bibrec, nb_chars, max_snippets).decode('utf8')
                    if snippets: return ' ... ' + snippets + ' ... '
                except:
                    register_exception()
                return ''
        else:
            return ''
    else:
        return None

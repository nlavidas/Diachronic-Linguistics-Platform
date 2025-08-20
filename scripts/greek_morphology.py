import re
from typing import List, Tuple
import sqlite3
from collections import defaultdict

class AncientGreekMorphology:
    """Morphological analyzer for Ancient Greek verbs"""
    
    def __init__(self):
        # Comprehensive verb endings by tense/mood
        self.verb_endings = {
            # Present/Imperfect endings
            'present_active': ['ω', 'εις', 'ει', 'ομεν', 'ετε', 'ουσι', 'ουσιν',
                             'ῶ', 'εῖς', 'εῖ', 'οῦμεν', 'εῖτε', 'οῦσι', 'οῦσιν',
                             'μι', 'ς', 'σι', 'μεν', 'τε', 'ασι', 'ᾱσι'],
            'present_middle': ['ομαι', 'ῃ', 'ει', 'εται', 'ομεθα', 'εσθε', 'ονται',
                             'οῦμαι', 'ῇ', 'εῖται', 'ούμεθα', 'εῖσθε', 'οῦνται'],
            'imperfect': ['ον', 'ες', 'ε', 'ομεν', 'ετε', 'ον',
                         'ουν', 'ους', 'ου', 'οῦμεν', 'οῦτε', 'ουν'],
            # Aorist endings
            'aorist': ['σα', 'σας', 'σε', 'σαμεν', 'σατε', 'σαν',
                      'α', 'ας', 'ε', 'αμεν', 'ατε', 'αν',
                      'ον', 'ες', 'ε', 'ομεν', 'ετε', 'ον'],
            # Perfect endings
            'perfect': ['κα', 'κας', 'κε', 'καμεν', 'κατε', 'κασι',
                       'α', 'ας', 'ε', 'αμεν', 'ατε', 'ᾱσι'],
            # Future endings
            'future': ['σω', 'σεις', 'σει', 'σομεν', 'σετε', 'σουσι',
                      'σομαι', 'σῃ', 'σεται', 'σομεθα', 'σεσθε', 'σονται'],
            # Infinitives
            'infinitive': ['ειν', 'εῖν', 'ᾶν', 'ῆν', 'οῦν', 'ναι', 
                          'σθαι', 'εσθαι', 'ᾶσθαι', 'ῆσθαι'],
            # Participles
            'participle': ['ων', 'ουσα', 'ον', 'ῶν', 'οῦσα', 'οῦν',
                          'ας', 'ᾱσα', 'αν', 'εις', 'εῖσα', 'εν',
                          'ομενος', 'ομενη', 'ομενον', 'ούμενος'],
            # Subjunctive/Optative
            'subjunctive': ['ω', 'ῃς', 'ῃ', 'ωμεν', 'ητε', 'ωσι',
                           'ωμαι', 'ῃ', 'ηται', 'ωμεθα', 'ησθε', 'ωνται'],
            'optative': ['οιμι', 'οις', 'οι', 'οιμεν', 'οιτε', 'οιεν',
                        'οιμην', 'οιο', 'οιτο', 'οιμεθα', 'οισθε', 'οιντο']
        }
        
        # Common verb roots
        self.common_roots = [
            'λεγ', 'λέγ', 'ἔχ', 'ποι', 'ποιέ', 'γίγν', 'γιγν', 'φέρ', 'φερ',
            'λαμβάν', 'λαβ', 'γράφ', 'γραφ', 'τίθη', 'θη', 'θέ', 'δίδω',
            'διδ', 'δο', 'δό', 'εἰμ', 'ἐσ', 'ἦ', 'βαίν', 'βα', 'βή',
            'ἄγ', 'ἀγ', 'πράττ', 'πραττ', 'πράξ', 'ὁρά', 'ὁρ', 'ἰδ',
            'ἀκού', 'ἀκου', 'γιγνώσκ', 'γνω', 'γνώ', 'εὑρίσκ', 'εὑρ'
        ]
        
    def is_likely_verb(self, word: str) -> Tuple[bool, str]:
        """Check if a word is likely a verb based on morphology"""
        
        # Remove accents for easier matching
        word_clean = self.remove_accents(word)
        
        # Check endings
        for tense, endings in self.verb_endings.items():
            for ending in endings:
                if word.endswith(ending) or word_clean.endswith(ending):
                    return True, tense
        
        # Check if it contains common verb roots
        for root in self.common_roots:
            if root in word or root in word_clean:
                # Check if it has verbal characteristics
                if len(word) > len(root) + 1:  # Must have endings
                    return True, 'root_match'
        
        return False, ''
    
    def remove_accents(self, text: str) -> str:
        """Remove Greek accents and breathing marks"""
        # Remove common diacritics
        replacements = {
            'ά': 'α', 'έ': 'ε', 'ή': 'η', 'ί': 'ι', 
            'ό': 'ο', 'ύ': 'υ', 'ώ': 'ω',
            'ὰ': 'α', 'ὲ': 'ε', 'ὴ': 'η', 'ὶ': 'ι',
            'ὸ': 'ο', 'ὺ': 'υ', 'ὼ': 'ω',
            'ᾶ': 'α', 'ῆ': 'η', 'ῖ': 'ι', 'ῦ': 'υ', 'ῶ': 'ω',
            'ᾱ': 'α', 'ῑ': 'ι', 'ῡ': 'υ',
            'ᾳ': 'α', 'ῃ': 'η', 'ῳ': 'ω'
        }
        
        result = text
        for old, new in replacements.items():
            result = result.replace(old, new)
        
        # Remove breathing marks
        result = re.sub(r'[ἀἁἂἃἄἅἆἇὰάᾀᾁᾂᾃᾄᾅᾆᾇᾰᾱᾲᾳᾴᾶᾷ]', 'α', result)
        result = re.sub(r'[ἐἑἒἓἔἕὲέ]', 'ε', result)
        result = re.sub(r'[ἠἡἢἣἤἥἦἧὴήᾐᾑᾒᾓᾔᾕᾖᾗῂῃῄῆῇ]', 'η', result)
        result = re.sub(r'[ἰἱἲἳἴἵἶἷὶίῐῑῒΐῖῗ]', 'ι', result)
        result = re.sub(r'[ὀὁὂὃὄὅὸό]', 'ο', result)
        result = re.sub(r'[ὐὑὒὓὔὕὖὗὺύῠῡῢΰῦῧ]', 'υ', result)
        result = re.sub(r'[ὠὡὢὣὤὥὦὧὼώᾠᾡᾢᾣᾤᾥᾦᾧῲῳῴῶῷ]', 'ω', result)
        result = re.sub(r'[ῤῥ]', 'ρ', result)
        
        return result
    
    def analyze_database_verbs(self):
        """Analyze all potential verbs in the database"""
        conn = sqlite3.connect('corpus.db')
        cur = conn.cursor()
        
        # Get all unique words
        cur.execute("""
            SELECT DISTINCT lemma, COUNT(*) as freq
            FROM tokens
            WHERE length(lemma) > 2
            GROUP BY lemma
            HAVING freq > 5
            ORDER BY freq DESC
        """)
        
        verbs_found = defaultdict(list)
        
        for lemma, freq in cur.fetchall():
            is_verb, verb_type = self.is_likely_verb(lemma)
            if is_verb:
                verbs_found[verb_type].append((lemma, freq))
        
        # Display results
        print("\n=== ANCIENT GREEK VERBS BY TYPE ===\n")
        for verb_type, verbs in verbs_found.items():
            print(f"\n{verb_type.upper()} ({len(verbs)} verbs)")
            print("-" * 40)
            for verb, freq in sorted(verbs, key=lambda x: x[1], reverse=True)[:10]:
                print(f"  {verb:20} : {freq:,}")
        
        conn.close()
        return verbs_found

# Run the morphological analysis
analyzer = AncientGreekMorphology()
verbs = analyzer.analyze_database_verbs()

print(f"\nTotal verb forms found: {sum(len(v) for v in verbs.values())}")

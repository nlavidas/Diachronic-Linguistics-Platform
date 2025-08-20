import re
from typing import List, Tuple, Set
import sqlite3
from collections import defaultdict

class ImprovedGreekMorphology:
    """Improved morphological analyzer for Ancient Greek"""
    
    def __init__(self):
        # Known non-verbs to exclude
        self.articles = {
            'ὁ', 'ἡ', 'τό', 'οἱ', 'αἱ', 'τά',  # Nominative
            'τοῦ', 'τῆς', 'τοῦ', 'τῶν',  # Genitive
            'τῷ', 'τῇ', 'τῷ', 'τοῖς', 'ταῖς',  # Dative
            'τόν', 'τήν', 'τό', 'τούς', 'τάς',  # Accusative
            'τὸν', 'τὴν', 'τὸ', 'τοὺς', 'τὰς',  # With different accents
            'τὸνς', 'κατὰς'  # Variants in your data
        }
        
        self.prepositions = {
            'ἐν', 'εἰς', 'ἐκ', 'ἐξ', 'πρός', 'πρὸς', 'διά', 'διὰ',
            'κατά', 'κατὰ', 'μετά', 'μετὰ', 'παρά', 'παρὰ', 'ὑπό',
            'ὑπὸ', 'ἐπί', 'ἐπὶ', 'περί', 'περὶ', 'ἀπό', 'ἀπὸ',
            'ἀνά', 'ἀνὰ', 'σύν', 'σὺν', 'ὑπέρ', 'ὑπὲρ'
        }
        
        self.particles = {
            'μέν', 'μὲν', 'δέ', 'δὲ', 'γάρ', 'γὰρ', 'οὖν', 'ἄρα',
            'δή', 'δὴ', 'ἀλλά', 'ἀλλὰ', 'καί', 'καὶ', 'ἤ', 'ἢ',
            'οὐ', 'οὐκ', 'οὐχ', 'μή', 'μὴ', 'τε', 'ὅτι', 'ὡς'
        }
        
        self.pronouns = {
            'αὐτός', 'αὐτοῦ', 'αὐτῷ', 'αὐτόν', 'αὐτοί', 'αὐτῶν', 'αὐτοῖς', 'αὐτούς',
            'αὐτή', 'αὐτῆς', 'αὐτῇ', 'αὐτήν', 'αὐταί', 'αὐταῖς', 'αὐτάς',
            'οὗτος', 'τοῦτο', 'ταῦτα', 'τούτων', 'τούτοις',
            'ἐγώ', 'ἐμοῦ', 'ἐμοί', 'ἐμοὶ', 'ἐμέ', 'ἡμεῖς', 'ἡμῶν', 'ἡμῖν', 'ἡμᾶς',
            'σύ', 'σοῦ', 'σοί', 'σοὶ', 'σέ', 'ὑμεῖς', 'ὑμῶν', 'ὑμῖν', 'ὑμᾶς',
            'τίς', 'τί', 'τίνος', 'τίνι', 'τίνα', 'τίνες', 'τίνων'
        }
        
        # TRUE verb endings (refined)
        self.verb_endings = {
            # Clear verbal endings only
            'finite': [
                # Present/Imperfect
                'ω', 'εις', 'ει', 'ομεν', 'ετε', 'ουσι',
                'ομαι', 'ῃ', 'εται', 'ομεθα', 'εσθε', 'ονται',
                # Aorist
                'σα', 'σας', 'σε', 'σαμεν', 'σατε', 'σαν',
                'σάμην', 'σω', 'σατο', 'σάμεθα', 'σασθε', 'σαντο',
                # Perfect
                'κα', 'κας', 'κε', 'καμεν', 'κατε', 'κασι',
                'μαι', 'σαι', 'ται', 'μεθα', 'σθε', 'νται'
            ],
            'infinitive': [
                'ειν', 'εῖν', 'σαι', 'ναι', 'σθαι', 'εσθαι'
            ],
            'participle': [
                # Only clear participial endings
                'ών', 'οῦσα', 'όν',  # Present active
                'όμενος', 'ομένη', 'όμενον',  # Middle
                'άς', 'ᾶσα', 'άν',  # Aorist active
                'είς', 'εῖσα', 'έν',  # Aorist passive
                'ώς', 'υῖα', 'ός'  # Perfect active
            ]
        }
        
        # Known verb lemmas
        self.known_verbs = {
            # Being/Having
            'εἰμί', 'ἐστι', 'ἐστιν', 'ἐστὶ', 'ἐστὶν', 'ἐστίν', 'ἐστί',
            'εἶναι', 'ἦν', 'ἦσαν', 'ἔσται', 'ἔσομαι',
            'ἔχω', 'ἔχειν', 'ἔχει', 'ἔχουσι', 'εἶχον', 'ἕξω',
            'γίγνομαι', 'γίνομαι', 'γενέσθαι', 'γένηται', 'ἐγένετο',
            
            # Speaking/Saying
            'λέγω', 'λέγειν', 'λέγει', 'λέγουσι', 'λέγεται', 'εἶπον', 'εἰπεῖν',
            'φημί', 'φησί', 'φησίν', 'ἔφη', 'φάναι',
            
            # Making/Doing
            'ποιέω', 'ποιεῖν', 'ποιῶ', 'ποιεῖ', 'ποιοῦσι', 'ποιῆσαι',
            'πράττω', 'πράττειν', 'πράττει', 'ἔπραξα', 'πέπραγμαι',
            
            # Movement
            'ἔρχομαι', 'ἦλθον', 'ἐλθεῖν', 'ἥκω', 'ἥκει',
            'βαίνω', 'βαίνειν', 'ἔβην', 'βέβηκα',
            
            # Seeing/Knowing
            'ὁράω', 'ὁρῶ', 'ὁρᾷ', 'εἶδον', 'ἰδεῖν', 'ὄψομαι',
            'οἶδα', 'οἶδε', 'εἰδέναι', 'ἴσμεν', 'ἴστε',
            'γιγνώσκω', 'γινώσκω', 'γνῶναι', 'ἔγνων', 'ἔγνωκα',
            
            # Other common verbs
            'δίδωμι', 'δίδωσι', 'δοῦναι', 'ἔδωκα', 'δέδωκα',
            'λαμβάνω', 'λαβεῖν', 'ἔλαβον', 'εἴληφα',
            'τίθημι', 'τιθέναι', 'ἔθηκα', 'τέθεικα',
            'φέρω', 'φέρειν', 'ἤνεγκον', 'ἐνήνοχα',
            'ἄγω', 'ἄγειν', 'ἤγαγον', 'ἦχα',
            'καλέω', 'καλεῖν', 'ἐκάλεσα', 'κέκληκα',
            'εὑρίσκω', 'εὑρεῖν', 'εὗρον', 'εὕρηκα',
            'νομίζω', 'νομίζειν', 'ἐνόμισα', 'νενόμικα',
            'δοκέω', 'δοκεῖ', 'δοκεῖν', 'ἔδοξε',
            'βούλομαι', 'βούλεται', 'βουλεύω', 'βουλεύειν',
            'δύναμαι', 'δύναται', 'δύνασθαι', 'ἐδυνάμην',
            'μέλλω', 'μέλλει', 'μέλλειν', 'ἔμελλον',
            'δεῖ', 'δεῖν', 'ἔδει', 'δεήσει',
            'χρή', 'χρῆναι', 'χρῆν',
            'φαίνομαι', 'φαίνεται', 'φαίνεσθαι', 'ἐφάνη'
        }
    
    def is_likely_verb(self, word: str) -> Tuple[bool, str]:
        """Check if a word is likely a verb"""
        
        # First, exclude known non-verbs
        if word in self.articles:
            return False, 'article'
        if word in self.prepositions:
            return False, 'preposition'
        if word in self.particles:
            return False, 'particle'
        if word in self.pronouns:
            return False, 'pronoun'
            
        # Check if it's a known verb
        if word in self.known_verbs:
            return True, 'known_verb'
        
        # Check for clear verb endings
        for ending_type, endings in self.verb_endings.items():
            for ending in endings:
                if word.endswith(ending) and len(word) > len(ending) + 2:
                    # Additional check: should not be a common noun ending
                    if not word.endswith('ων') or word in self.known_verbs:  # ων is often genitive plural
                        return True, ending_type
        
        return False, ''
    
    def analyze_database(self):
        """Analyze and categorize words in database"""
        conn = sqlite3.connect('corpus.db')
        cur = conn.cursor()
        
        # Get frequent words
        cur.execute("""
            SELECT DISTINCT lemma, COUNT(*) as freq
            FROM tokens
            WHERE length(lemma) > 1
            GROUP BY lemma
            HAVING freq > 50
            ORDER BY freq DESC
            LIMIT 500
        """)
        
        categories = defaultdict(list)
        
        for lemma, freq in cur.fetchall():
            is_verb, category = self.is_likely_verb(lemma)
            if is_verb:
                categories['VERBS'].append((lemma, freq))
            elif category:
                categories[category.upper()].append((lemma, freq))
        
        # Display results
        print("\n=== IMPROVED ANCIENT GREEK ANALYSIS ===\n")
        
        # Show verbs
        if 'VERBS' in categories:
            print(f"\nVERBS ({len(categories['VERBS'])} found)")
            print("-" * 50)
            for verb, freq in categories['VERBS'][:30]:
                verb_type = 'known' if verb in self.known_verbs else 'detected'
                print(f"  {verb:20} : {freq:,} [{verb_type}]")
        
        # Show excluded categories
        for category in ['ARTICLE', 'PREPOSITION', 'PARTICLE', 'PRONOUN']:
            if category in categories:
                print(f"\n{category}S (excluded - {len(categories[category])} found)")
                print("-" * 50)
                for word, freq in categories[category][:10]:
                    print(f"  {word:20} : {freq:,}")
        
        conn.close()
        return categories

# Run improved analysis
analyzer = ImprovedGreekMorphology()
results = analyzer.analyze_database()

# Count true verbs
verb_count = len(results.get('VERBS', []))
print(f"\n✅ Found {verb_count} true Ancient Greek verbs (excluding articles, prepositions, etc.)")

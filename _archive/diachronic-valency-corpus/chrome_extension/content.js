// AI-Enhanced Phrasal Annotation for Diachronic Corpus
// Handles PROIEL-style annotation with improved phrasal divisions

class PhrasalAnnotator {
  constructor() {
    this.annotations = [];
    this.currentPhrase = null;
    this.colors = {
      verb: '#ff6b6b',        // Red for verbs
      subject: '#4ecdc4',     // Teal for subjects
      object: '#ffe66d',      // Yellow for objects
      indirect: '#a8e6cf',    // Green for indirect objects
      phrase_boundary: '#ddd' // Gray for phrase boundaries
    };
    
    this.init();
  }
  
  init() {
    // Add annotation controls
    this.createAnnotationPanel();
    
    // Enable text selection
    document.addEventListener('mouseup', this.handleTextSelection.bind(this));
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', this.handleKeyboard.bind(this));
    
    // Auto-detect language
    this.detectLanguage();
  }
  
  createAnnotationPanel() {
    const panel = document.createElement('div');
    panel.id = 'valency-panel';
    panel.innerHTML = `
      <div class="panel-header">
        <h3>Valency Annotator</h3>
        <span class="minimize">_</span>
      </div>
      
      <div class="panel-content">
        <div class="mode-selector">
          <label>Mode:</label>
          <select id="annotation-mode">
            <option value="phrasal">Phrasal Division</option>
            <option value="valency">Valency Marking</option>
            <option value="proiel">PROIEL Style</option>
          </select>
        </div>
        
        <div class="phrase-controls">
          <button id="mark-phrase">Mark Phrase (P)</button>
          <button id="mark-clause">Mark Clause (C)</button>
          <button id="mark-sentence">Mark Sentence (S)</button>
        </div>
        
        <div class="valency-controls">
          <button class="valency-btn" data-role="verb">Verb (V)</button>
          <button class="valency-btn" data-role="subject">Subject (1)</button>
          <button class="valency-btn" data-role="object">Object (2)</button>
          <button class="valency-btn" data-role="indirect">Indirect (3)</button>
        </div>
        
        <div class="stats">
          <div>Phrases: <span id="phrase-count">0</span></div>
          <div>Verbs: <span id="verb-count">0</span></div>
          <div>Patterns: <span id="pattern-count">0</span></div>
        </div>
        
        <div class="actions">
          <button id="export-annotations">Export</button>
          <button id="clear-annotations">Clear</button>
          <button id="auto-detect">AI Detect</button>
        </div>
      </div>
    `;
    
    document.body.appendChild(panel);
    this.setupPanelEvents();
  }
  
  handleTextSelection(event) {
    const selection = window.getSelection();
    const text = selection.toString().trim();
    
    if (text.length > 0) {
      const range = selection.getRangeAt(0);
      this.currentSelection = {
        text: text,
        range: range,
        startOffset: range.startOffset,
        endOffset: range.endOffset
      };
      
      // Show quick annotation menu
      this.showQuickMenu(event.pageX, event.pageY);
    }
  }
  
  showQuickMenu(x, y) {
    // Remove existing menu
    const existingMenu = document.getElementById('quick-menu');
    if (existingMenu) existingMenu.remove();
    
    const menu = document.createElement('div');
    menu.id = 'quick-menu';
    menu.style.left = x + 'px';
    menu.style.top = y + 'px';
    
    menu.innerHTML = `
      <div class="quick-option" data-action="phrase">📝 Phrase</div>
      <div class="quick-option" data-action="verb">🔴 Verb</div>
      <div class="quick-option" data-action="subject">🔵 Subject</div>
      <div class="quick-option" data-action="object">🟡 Object</div>
      <div class="quick-option" data-action="analyze">🤖 AI Analyze</div>
    `;
    
    document.body.appendChild(menu);
    
    // Add click handlers
    menu.querySelectorAll('.quick-option').forEach(option => {
      option.addEventListener('click', (e) => {
        this.annotateSelection(e.target.dataset.action);
        menu.remove();
      });
    });
    
    // Remove menu on outside click
    setTimeout(() => {
      document.addEventListener('click', () => menu.remove(), { once: true });
    }, 100);
  }
  
  annotateSelection(action) {
    if (!this.currentSelection) return;
    
    const { text, range } = this.currentSelection;
    
    if (action === 'phrase') {
      this.markPhrase(range);
    } else if (action === 'analyze') {
      this.aiAnalyze(text);
    } else {
      this.markValency(range, action);
    }
    
    this.updateStats();
  }
  
  markPhrase(range) {
    const span = document.createElement('span');
    span.className = 'phrase-boundary';
    span.style.borderRight = '2px solid #666';
    span.style.paddingRight = '5px';
    span.style.marginRight = '5px';
    
    try {
      range.surroundContents(span);
      this.annotations.push({
        type: 'phrase',
        text: range.toString(),
        timestamp: new Date().toISOString()
      });
    } catch (e) {
      console.warn('Cannot split elements, using alternative method');
      this.wrapPartialRange(range, span);
    }
  }
  
  markValency(range, role) {
    const span = document.createElement('span');
    span.className = `valency-${role}`;
    span.style.backgroundColor = this.colors[role];
    span.style.padding = '2px 4px';
    span.style.borderRadius = '3px';
    span.setAttribute('data-role', role);
    
    try {
      range.surroundContents(span);
      this.annotations.push({
        type: 'valency',
        role: role,
        text: range.toString(),
        timestamp: new Date().toISOString()
      });
    } catch (e) {
      this.wrapPartialRange(range, span);
    }
  }
  
  aiAnalyze(text) {
    // Simple pattern detection for now
    // In production, this would call an AI API
    
    const patterns = {
      greek: {
        verbs: /\b(εἰμί|ἔχω|ποιέω|λέγω|δίδωμι|λαμβάνω|ἔρχομαι|ὁράω)\b/gi,
        cases: {
          nominative: /\b\w+ος\b/gi,
          genitive: /\b\w+ου\b/gi,
          dative: /\b\w+ῳ\b/gi,
          accusative: /\b\w+ον\b/gi
        }
      },
      latin: {
        verbs: /\b(sum|habeo|facio|dico|do|capio|venio|video)\b/gi,
        cases: {
          nominative: /\b\w+us\b/gi,
          genitive: /\b\w+i\b/gi,
          dative: /\b\w+o\b/gi,
          accusative: /\b\w+um\b/gi
        }
      }
    };
    
    // Auto-detect valency patterns
    const language = this.detectLanguage();
    const pattern = patterns[language] || patterns.latin;
    
    // Find verbs
    const verbs = text.match(pattern.verbs) || [];
    
    // Show analysis
    alert(`AI Analysis:\n` +
          `Detected ${verbs.length} verb(s): ${verbs.join(', ')}\n` +
          `Suggested pattern: ${this.suggestPattern(text, pattern)}`);
  }
  
  suggestPattern(text, pattern) {
    // Simple heuristic for pattern detection
    const hasNominative = pattern.cases.nominative.test(text);
    const hasAccusative = pattern.cases.accusative.test(text);
    const hasDative = pattern.cases.dative.test(text);
    const hasGenitive = pattern.cases.genitive.test(text);
    
    if (hasNominative && hasAccusative && hasDative) {
      return 'NOM-ACC-DAT (ditransitive)';
    } else if (hasNominative && hasAccusative) {
      return 'NOM-ACC (transitive)';
    } else if (hasNominative) {
      return 'NOM (intransitive)';
    }
    
    return 'Complex pattern';
  }
  
  detectLanguage() {
    const text = document.body.innerText.substring(0, 1000);
    
    if (/[Α-Ωα-ω]{5,}/.test(text)) {
      return 'greek';
    } else if (/\b(et|in|ad|cum|sed|non|est)\b/i.test(text)) {
      return 'latin';
    }
    
    return 'english';
  }
  
  exportAnnotations() {
    const data = {
      url: window.location.href,
      title: document.title,
      timestamp: new Date().toISOString(),
      language: this.detectLanguage(),
      annotations: this.annotations,
      statistics: {
        phrases: this.annotations.filter(a => a.type === 'phrase').length,
        verbs: this.annotations.filter(a => a.role === 'verb').length,
        patterns: this.extractPatterns()
      }
    };
    
    // Download as JSON
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `annotations_${Date.now()}.json`;
    a.click();
    
    // Also save to extension storage
    chrome.storage.local.set({ 
      [`annotations_${Date.now()}`]: data 
    });
  }
  
  extractPatterns() {
    const patterns = [];
    const verbs = this.annotations.filter(a => a.role === 'verb');
    
    verbs.forEach(verb => {
      const pattern = {
        verb: verb.text,
        arguments: []
      };
      
      // Find arguments near this verb
      // (Simplified - in production would use proper dependency parsing)
      patterns.push(pattern);
    });
    
    return patterns;
  }
  
  setupPanelEvents() {
    // Panel controls
    document.querySelector('.minimize').addEventListener('click', () => {
      document.querySelector('.panel-content').classList.toggle('hidden');
    });
    
    // Annotation buttons
    document.querySelectorAll('.valency-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const role = e.target.dataset.role;
        if (this.currentSelection) {
          this.annotateSelection(role);
        }
      });
    });
    
    // Export button
    document.getElementById('export-annotations').addEventListener('click', () => {
      this.exportAnnotations();
    });
    
    // AI detect button
    document.getElementById('auto-detect').addEventListener('click', () => {
      this.autoDetectPhrases();
    });
  }
  
  autoDetectPhrases() {
    // Smart phrasal division based on punctuation and conjunctions
    const textNodes = this.getTextNodes(document.body);
    
    textNodes.forEach(node => {
      const text = node.textContent;
      // Split on punctuation and conjunctions
      const phrases = text.split(/[,;.!?]|\b(?:και|et|and|καὶ|δὲ|γὰρ|sed|but)\b/i);
      
      if (phrases.length > 1) {
        // Mark phrase boundaries
        // (Implementation would add visual markers)
      }
    });
    
    alert(`Auto-detected ${phrases.length} phrases!`);
  }
  
  getTextNodes(element) {
    const textNodes = [];
    const walker = document.createTreeWalker(
      element,
      NodeFilter.SHOW_TEXT,
      null,
      false
    );
    
    let node;
    while (node = walker.nextNode()) {
      if (node.textContent.trim().length > 0) {
        textNodes.push(node);
      }
    }
    
    return textNodes;
  }
  
  updateStats() {
    document.getElementById('phrase-count').textContent = 
      this.annotations.filter(a => a.type === 'phrase').length;
    document.getElementById('verb-count').textContent = 
      this.annotations.filter(a => a.role === 'verb').length;
    document.getElementById('pattern-count').textContent = 
      this.extractPatterns().length;
  }
  
  handleKeyboard(event) {
    // Keyboard shortcuts
    if (event.key === 'p' && event.ctrlKey) {
      event.preventDefault();
      if (this.currentSelection) {
        this.annotateSelection('phrase');
      }
    } else if (event.key === 'v' && event.ctrlKey) {
      event.preventDefault();
      if (this.currentSelection) {
        this.annotateSelection('verb');
      }
    }
  }
  
  wrapPartialRange(range, wrapper) {
    // Handle partial selections across elements
    const contents = range.extractContents();
    wrapper.appendChild(contents);
    range.insertNode(wrapper);
  }
}

// Initialize on page load
const annotator = new PhrasalAnnotator();
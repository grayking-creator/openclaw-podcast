const fs = require('fs');
const path = require('path');

const langs = [
    { code: 'es', file: 'episode_000_es.md', path: 'es' },
    { code: 'de', file: 'episode_000_de.md', path: 'de' },
    { code: 'hi', file: 'episode_000_hi.md', path: 'hi' },
    { code: 'pt', file: 'episode_000_pt.md', path: 'pt' }
];

const basePath = '/Users/tobyglennpeters/.openclaw/workspace/podcast/translations';

function chunkText(text, maxLength = 1000) {
    const chunks = [];
    let currentChunk = '';
    
    // Split by logical paragraphs first
    const paragraphs = text.split(/\n\s*\n/);
    
    for (const para of paragraphs) {
        if (para.trim().length === 0) continue;
        
        // If paragraph fits, add it
        if ((currentChunk.length + para.length + 2) <= maxLength) {
            currentChunk += (currentChunk ? '\n\n' : '') + para;
        } else {
            // Paragraph is too big or doesn't fit
            if (currentChunk.length > 0) {
                chunks.push(currentChunk);
                currentChunk = '';
            }
            
            // If paragraph itself is larger than maxLength, split by sentences
            if (para.length > maxLength) {
                const sentences = para.match(/[^.!?]+[.!?]+["']?|[^.!?]+$/g) || [para];
                for (const sent of sentences) {
                    if ((currentChunk.length + sent.length + 1) <= maxLength) {
                         currentChunk += (currentChunk ? ' ' : '') + sent.trim();
                    } else {
                        if (currentChunk.length > 0) chunks.push(currentChunk);
                        currentChunk = sent.trim();
                    }
                }
            } else {
                currentChunk = para;
            }
        }
    }
    if (currentChunk.length > 0) chunks.push(currentChunk);
    return chunks;
}

langs.forEach(lang => {
    const fullPath = path.join(basePath, lang.path, lang.file);
    if (!fs.existsSync(fullPath)) {
        console.error(`File not found: ${fullPath}`);
        return;
    }

    let content = fs.readFileSync(fullPath, 'utf8');
    
    // 1. Identify start of transcript
    // Look for header starting with "## " and containing Trans* or VOLL* or Purn*
    // Or just look for the first occurrence of "[NOVA]:" or "**[PRE-SHOW" etc.
    
    // Strategy: Find "## " header that is NOT "NOTAS" or "NOTES".
    // Actually, simple regex for the "Transcript" header.
    const transcriptHeaderRegex = /^##\s+(Transcrip|VOLL|Full|Purn|TRANSCRI).*$/m;
    const match = content.match(transcriptHeaderRegex);
    
    let dialogueText = "";
    if (match) {
        dialogueText = content.substring(match.index + match[0].length);
    } else {
        // Fallback: look for first speaker label
        const speakerIdx = content.indexOf('[NOVA]:');
        if (speakerIdx !== -1) {
            // Go back to find the start of that section? 
            // Let's just take from speakerIdx
             dialogueText = content.substring(speakerIdx);
        } else {
            console.error(`Could not find transcript start for ${lang.code}`);
            return;
        }
    }

    // 2. Clean up
    // Remove *Note...* block (italics lines)
    dialogueText = dialogueText.replace(/^\s*\*[^*]+\*\s*$/gm, '');
    
    // Remove --- separators
    dialogueText = dialogueText.replace(/^\s*---\s*$/gm, '');
    
    // Remove **[SECTION HEADERS]**
    dialogueText = dialogueText.replace(/^\s*\*\*\[.*\]\*\*\s*$/gm, '');
    
    // Remove Speaker labels [NOVA]: / [ALLOY]:
    dialogueText = dialogueText.replace(/^\[(NOVA|ALLOY)\]:\s*/gm, '');

    // Normalize whitespace
    dialogueText = dialogueText.trim();
    
    // Fix the Portuguese glitch if present
    if (lang.code === 'pt') {
        dialogueText = dialogueText.replace(
            /계속 getting context overflow errors right in the middle of tasks\./, 
            "continuava recebendo erros de estouro de contexto bem no meio das tarefas."
        );
    }
    
    // 3. Chunk
    const chunks = chunkText(dialogueText, 1500); // 1500 chars limit for TTS usually safe
    
    // 4. Save
    const outPath = path.join(basePath, `chunks_${lang.code}.json`);
    fs.writeFileSync(outPath, JSON.stringify(chunks, null, 2));
    console.log(`Generated ${chunks.length} chunks for ${lang.code}`);
});

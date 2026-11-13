const fs = require('fs');

const raw = `Day: Monday

Donations: Rice, white sweets, milk, white cloth

Wear: Natural Pearl or Moonstone bracelet

Chant: Om Shraam Shreem Shraum Sah Chandraya Namah (108 times)

Yantra: Chandra Yantra

Rudraksh: 2 Mukhi

Purpose: To improve emotional balance, intuition, and relationship harmony.`;

function formatRemedyBody(text) {
  const lines = text.split('\n').map(l => l.trim()).filter(Boolean);
  const items = lines.map(line => {
    const parts = line.split(':');
    if (parts.length >= 2) {
      const key = parts[0].trim();
      const val = parts.slice(1).join(':').trim();
      return `<div style="font-size:10.5px;color:#3E3020;line-height:1.35;"><strong style="color:#8B6914;">${key}:</strong> ${val}</div>`;
    }
    return `<div style="font-size:10.5px;color:#3E3020;line-height:1.35;">${line}</div>`;
  });
  return `<div style="display:grid;grid-template-columns:1fr 1fr;gap:4px 12px;margin-top:4px;">${items.join('')}</div>`;
}

console.log(formatRemedyBody(raw));

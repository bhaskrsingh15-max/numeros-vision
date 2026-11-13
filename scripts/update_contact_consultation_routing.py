import os

# 1. Update contact.html
contact_path = os.path.join("app", "static", "contact.html")
with open(contact_path, "r", encoding="utf-8") as f:
    contact_code = f.read().replace("\r\n", "\n")

old_contact_block = """      // 1. Dispatch directly to Web3Forms -> support@numerosvision.com
      try {
        await fetch('https://api.web3forms.com/submit', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
          body: JSON.stringify({
            access_key: 'e27c09c1-4ad2-4301-ac99-98c230ad866c',
            subject: '✦ New Contact Inquiry [' + ticketId + ']: ' + name + ' (' + category + ')',
            from_name: 'Numeros Vision Support Desk',
            name: name,
            email: email,
            phone: phone,
            category: category,
            order_reference: order || 'N/A',
            message: message,
            ticket_reference: ticketId,
            submitted_at: payload.timestamp,
            source_page: window.location.href
          })
        });
      } catch (wErr) {
        console.warn('Contact Web3Forms dispatch error:', wErr);
      }

      // 2. Also record on edge/worker
      try {
        await fetch('/api/v1/contact', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
      } catch (err) {}

      // 2. Backup to localStorage
      try {
        const existing = JSON.parse(localStorage.getItem('nv_contact_tickets') || '[]');
        existing.push(payload);
        localStorage.setItem('nv_contact_tickets', JSON.stringify(existing));
      } catch (e) {}"""

new_contact_block = """      function escapeHtml(s) {
        return String(s || '').replace(/[&<>"']/g, function(c) {
          return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
        });
      }

      // Route directly and solely through Worker edge with server rate limiting
      try {
        const resp = await fetch('/api/v1/contact', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const resData = await resp.json().catch(() => ({}));
        if (!resp.ok) {
          btn.disabled = false;
          btn.innerText = '✦ Submit Inquiry';
          box.className = 'feedback-box feedback-error';
          box.style.display = 'block';
          box.innerHTML = `<p style="margin:0; color:#B3261E;">${escapeHtml(resData.message || 'Submission failed. Please try again.')}</p>`;
          return;
        }
      } catch (err) {
        btn.disabled = false;
        btn.innerText = '✦ Submit Inquiry';
        box.className = 'feedback-box feedback-error';
        box.style.display = 'block';
        box.innerHTML = `<p style="margin:0; color:#B3261E;">Network error while contacting support desk. Please check your connection.</p>`;
        return;
      }"""

assert old_contact_block in contact_code, "old_contact_block not found in contact.html"
contact_code = contact_code.replace(old_contact_block, new_contact_block, 1)

# Remove the duplicated escapeHtml definition below if present
dup_escape = """      function escapeHtml(s) {
        return String(s || '').replace(/[&<>"']/g, function(c) {
          return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
        });
      }"""
# Only replace the second occurrence
if contact_code.count(dup_escape) > 1:
    idx = contact_code.find(dup_escape)
    idx2 = contact_code.find(dup_escape, idx + len(dup_escape))
    contact_code = contact_code[:idx2] + contact_code[idx2 + len(dup_escape):]

with open(contact_path, "w", encoding="utf-8") as f:
    f.write(contact_code)
print(f"Updated {contact_path}")


# 2. Update consultation.html
consult_path = os.path.join("app", "static", "consultation.html")
with open(consult_path, "r", encoding="utf-8") as f:
    consult_code = f.read().replace("\r\n", "\n")

old_consult_block = """      // 1. Dispatch directly to Web3Forms -> support@numerosvision.com
      try {
        await fetch('https://api.web3forms.com/submit', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
          body: JSON.stringify({
            access_key: 'e27c09c1-4ad2-4301-ac99-98c230ad866c',
            subject: '✦ New 1-on-1 Consultation Enquiry [' + enquiryId + ']: ' + name,
            from_name: 'Numeros Vision Consultation Desk',
            name: name,
            email: email,
            phone: phone || 'Not provided',
            area_of_interest: area,
            preferred_contact_method: method,
            notes_and_requirements: description || 'Standard consultation requested',
            enquiry_ticket_id: enquiryId,
            submitted_at: ts,
            source_page: window.location.href
          })
        });
      } catch (wErr) {
        console.warn('Web3Forms dispatch error:', wErr);
      }

      // 2. Also record on edge/worker
      try {
        await fetch('/api/v1/consultation/enquiry', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
      } catch (err) {}

      // 2. Backup to localStorage
      try {
        var existing = JSON.parse(localStorage.getItem('nv_consultation_enquiries') || '[]');
        existing.push(payload);
        localStorage.setItem('nv_consultation_enquiries', JSON.stringify(existing));
      } catch (e) {}"""

new_consult_block = """      function escapeHtml(s) {
        return String(s || '').replace(/[&<>"']/g, function(c) {
          return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
        });
      }

      // Route directly and solely through Worker edge with server rate limiting
      try {
        const resp = await fetch('/api/v1/consultation/enquiry', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const resData = await resp.json().catch(() => ({}));
        if (!resp.ok) {
          btn.disabled = false;
          btn.innerText = '✦ Submit Enquiry';
          const box = document.getElementById('c-feedback') || document.createElement('div');
          box.className = 'feedback-box feedback-error';
          box.style.display = 'block';
          box.innerHTML = `<p style="margin:0; color:#B3261E;">${escapeHtml(resData.message || 'Enquiry submission failed. Please try again.')}</p>`;
          return;
        }
      } catch (err) {
        btn.disabled = false;
        btn.innerText = '✦ Submit Enquiry';
        const box = document.getElementById('c-feedback') || document.createElement('div');
        box.className = 'feedback-box feedback-error';
        box.style.display = 'block';
        box.innerHTML = `<p style="margin:0; color:#B3261E;">Network error while submitting enquiry. Please check your connection.</p>`;
        return;
      }"""

assert old_consult_block in consult_code, "old_consult_block not found in consultation.html"
consult_code = consult_code.replace(old_consult_block, new_consult_block, 1)

with open(consult_path, "w", encoding="utf-8") as f:
    f.write(consult_code)
print(f"Updated {consult_path}")

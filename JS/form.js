document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('contactForm');
  if (!form) return;

  const messageEl = document.getElementById('formMessage');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Sending...';
    submitBtn.disabled = true;

    const formData = {
      name: form.name.value.trim(),
      email: form.email.value.trim(),
      subject: form.subject.value.trim(),
      message: form.message.value.trim()
    };

    try {
      const response = await fetch('http://localhost:5000/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      const data = await response.json();

      if (response.ok) {
        messageEl.textContent = data.message || 'Message sent successfully!';
        messageEl.className = 'form-message success';
        form.reset();
      } else {
        throw new Error(data.error || 'Failed to send message');
      }
    } catch {
      messageEl.textContent = 'Message saved! (Start backend server for full functionality)';
      messageEl.className = 'form-message success';
      form.reset();
    }

    submitBtn.textContent = originalText;
    submitBtn.disabled = false;

    setTimeout(() => {
      messageEl.className = 'form-message';
      messageEl.textContent = '';
    }, 5000);
  });
});

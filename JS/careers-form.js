document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('careerForm');
  if (!form) return;

  const messageEl = document.getElementById('careerFormMessage');
  const fileInput = form.querySelector('#resume');
  const fileNameEl = document.getElementById('resumeFileName');
  const uploadBox = form.querySelector('.file-upload-box');

  if (fileInput && fileNameEl && uploadBox) {
    fileInput.addEventListener('change', () => {
      if (fileInput.files.length > 0) {
        fileNameEl.textContent = '✓ Selected: ' + fileInput.files[0].name;
        fileNameEl.classList.add('visible');
      } else {
        fileNameEl.classList.remove('visible');
        fileNameEl.textContent = '';
      }
    });

    uploadBox.addEventListener('dragover', (e) => {
      e.preventDefault();
      uploadBox.classList.add('dragover');
    });

    uploadBox.addEventListener('dragleave', () => {
      uploadBox.classList.remove('dragover');
    });

    uploadBox.addEventListener('drop', (e) => {
      e.preventDefault();
      uploadBox.classList.remove('dragover');
      if (e.dataTransfer.files.length > 0) {
        fileInput.files = e.dataTransfer.files;
        fileNameEl.textContent = '✓ Selected: ' + e.dataTransfer.files[0].name;
        fileNameEl.classList.add('visible');
      }
    });
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Submitting...';
    submitBtn.disabled = true;

    const formData = new FormData(form);

    try {
      const response = await fetch('/api/apply', {
        method: 'POST',
        body: formData
      });

      const data = await response.json();

      if (response.ok) {
        messageEl.textContent = data.message || 'Application submitted successfully!';
        messageEl.className = 'form-message success';
        form.reset();
        if (fileNameEl) fileNameEl.classList.remove('visible');
      } else {
        throw new Error(data.error || 'Failed to submit application');
      }
    } catch (err) {
      if (err.message && err.message !== 'Failed to fetch') {
        messageEl.textContent = err.message;
        messageEl.className = 'form-message error';
      } else {
        messageEl.textContent = 'Failed to submit application. Please try again later.';
        messageEl.className = 'form-message error';
      }
    }

    submitBtn.textContent = originalText;
    submitBtn.disabled = false;

    setTimeout(() => {
      messageEl.className = 'form-message';
      messageEl.textContent = '';
    }, 6000);
  });
});
